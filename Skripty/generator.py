import os
from pathlib import Path
from typing import Dict

import yaml
from bs4 import BeautifulSoup, NavigableString
from vyplnovac import scan_options


def fill_filter(index, filter_data) -> None:
    """
    Create the filter section in the template index.html
    :param index: Parsed bs4 template html file.
    :param filter_data: Data to create the filter elements from.
    :return: None
    """
    translator = {'beak': 'zobák',
                  'head': 'hlava',
                  'chest': 'hruď',
                  'wings': 'křídla',
                  'back': 'záda',
                  'tail': 'ocas',
                  'legs': 'nohy',
                  'size': 'velikost',
                  'type': 'typ'}

    for part in ('beak', 'head', 'chest', 'wings', 'back', 'tail', 'legs', 'size', 'type'):
        html_part = index.find("div", {"id": part}).find('form')
        for option in filter_data[translator[part]]:
            option: str
            part_id = f'{part}{option.capitalize()}'
            input_item = index.new_tag('input', attrs={'type': 'checkbox', 'id': part_id, 'name': part_id,
                                                       'value': option})
            input_label = index.new_tag('label', attrs={'for': part_id})
            input_item.append(input_label)
            br = index.new_tag('br')
            input_item.append(br)
            input_label.insert(0, NavigableString(option))
            html_part.append(input_item)


def fill_cards(index, database_dir) -> None:
    """
    Create the bird cards in the template index.html
    :param index: Parsed bs4 template html file.
    :param database_dir: Directory with bird data.
    :return: None
    """
    html_output = index.find("output")
    for path in database_dir.iterdir():
        if path.is_dir():
            try:
                os.chdir(path.resolve())
                with open('data.yml', 'r') as metadata_file:
                    metadata = yaml.safe_load(metadata_file)
                    note = metadata['dodatek']
                    name = metadata['jméno']
                    latin = metadata['latinsky']
                    avibase = metadata['odkazy']['celosvětová databáze']
                    photos_url = metadata['odkazy']['více fotek']
                    wiki_url = metadata['odkazy']['wiki']
                    kind = metadata['typ']
                    size = metadata['velikost']

                    description = metadata['popis']
                    male = description['samec']
                    female = description['samice']

                    m_colors = male['barvy']
                    for part in m_colors:
                        part: Dict
                        if list(part.keys())[0] == 'hlava':
                            m_head = part['hlava']
                        elif list(part.keys())[0] == 'křídla':
                            m_wings = part['křídla']
                        elif list(part.keys())[0] == 'hruď':
                            m_chest = part['hruď']
                        elif list(part.keys())[0] == 'ocas':
                            m_tail = part['ocas']
                        elif list(part.keys())[0] == 'nohy':
                            m_legs = part['nohy']
                        elif list(part.keys())[0] == 'záda':
                            m_back = part['záda']
                        elif list(part.keys())[0] == 'zobák':
                            m_beak = part['zobák']
                    m_photos = male['fotky']
                    m_spotted = male['kropenatost']

                    if female:
                        f_colors = female['barvy']
                        for part in f_colors:
                            part: Dict
                            if list(part.keys())[0] == 'hlava':
                                f_head = part['hlava']
                            elif list(part.keys())[0] == 'křídla':
                                f_wings = part['křídla']
                            elif list(part.keys())[0] == 'hruď':
                                f_chest = part['hruď']
                            elif list(part.keys())[0] == 'ocas':
                                f_tail = part['ocas']
                            elif list(part.keys())[0] == 'nohy':
                                f_legs = part['nohy']
                            elif list(part.keys())[0] == 'záda':
                                f_back = part['záda']
                            elif list(part.keys())[0] == 'zobák':
                                f_beak = part['zobák']
                        f_photos = female['fotky']
                        f_spotted = female['kropenatost']

                # Create a bird card.
                bird_card_div = index.new_tag('div', attrs={'class': 'birdCard'})
                html_output.append(bird_card_div)

                # Card title.
                bird_name = index.new_tag('h4')
                bird_name.insert(0, NavigableString(f'{name}'))
                latin_name = index.new_tag('p', attrs={'class': 'birdLatin'})
                latin_name.insert(0, NavigableString(f'{latin}'))
                bird_card_div.append(bird_name)
                bird_card_div.append(latin_name)

                # Both genders the same.
                if not female:
                    gender_div = index.new_tag('div', attrs={'class': 'birdGender'})
                    card_title = index.new_tag('h5')
                    card_title.insert(0, NavigableString('Samec/Samice'))
                    bird_card_div.append(gender_div)
                    gender_div.append(card_title)

                    for img in m_photos:
                        # TODO popis pro obe pohlavi do jednoho details dole
                        image_link = index.new_tag('a', attrs={'href': img['url'],
                                                               'title': f'{name}, Zdroj: {img["zdroj"]}',
                                                               'target': '_blank'})
                        photo = index.new_tag('img', attrs={'height': '200px',
                                                            'alt': f'{name}, Zdroj: {img["zdroj"]}',
                                                            'src': f"images/ptaci/{path.cwd().name}/{img['file']}"})
                        image_link.append(photo)
                        gender_div.append(image_link)

                    # Description and authors.
                    details = index.new_tag('details')
                    summary = index.new_tag('summary')
                    summary.insert(0, NavigableString('Popis'))
                    details.append(summary)

                    # Description.
                    for part, content in {'Hlava': m_head, 'Křídla': m_wings, 'Hruď': m_chest, 'Ocas': m_tail,
                                          'Nohy': m_legs, 'Záda': m_back, 'Zobák': m_beak}.items():
                        body_part_p = index.new_tag('p')
                        body_part_p.insert(0, NavigableString(f'{part}: {(", ".join(content))}'))
                        details.append(body_part_p)


                    bird_card_div.append(details)




            except Exception as ex:
                print(f'Error: {path}, {ex}')
            finally:
                os.chdir(database_dir.resolve())


if __name__ == '__main__':
    www_dir = Path.cwd() / Path('../www').resolve()
    data_directory = Path(Path.cwd() / Path('../www/images/ptaci')).resolve()
    with open(Path('./template.html'), 'r') as html:
        template = BeautifulSoup(html, 'html.parser')
        if not data_directory.exists():
            print(f'Working directory not found: {data_directory}')
        else:
            fill_filter(template, scan_options(data_directory))
            fill_cards(template, data_directory)

            os.chdir(www_dir)
            html = template.prettify("utf-8")
            with open("index.html", "wb") as file:
                file.write(html)
    print('Done', www_dir / Path('index.html'))
