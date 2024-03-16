import os
from pathlib import Path
from typing import Dict

import htmlmin
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
        for option in sorted(filter_data[translator[part]]):
            option: str
            part_id = f'{part}_{option}'
            input_item = index.new_tag('input', attrs={'type': 'checkbox', 'id': part_id, 'name': part_id,
                                                       'value': option, 'onchange': 'onFilter()'})
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

                authors = {}
                card_title = index.new_tag('h5')
                if not female:
                    # Both genders the same.
                    card_title.insert(0, NavigableString('Samec/Samice'))
                elif female:
                    # First we do the male.
                    card_title.insert(0, NavigableString('Samec'))

                # The whole block under is for the male part only, female is below that.
                gender_div = index.new_tag('div', attrs={'class': 'birdGender'})
                bird_card_div.append(gender_div)
                gender_div.append(card_title)

                img_id = 0
                for img in m_photos:
                    image_link = index.new_tag('a', attrs={'href': img['url'],
                                                           'title': f'ID: {img_id}, {name}, Zdroj: {img["zdroj"]}',
                                                           'target': '_blank'})
                    photo = index.new_tag('img', attrs={'height': '200px',
                                                        'alt': f'{name}, Zdroj: {img["zdroj"]}',
                                                        'src': f"images/ptaci/{path.cwd().name}/{img['file']}"})
                    image_link.append(photo)
                    gender_div.append(image_link)
                    authors[img_id] = img['zdroj']
                    img_id = img_id + 1

                # Description and authors.
                data_container = index.new_tag('div')
                m_details = index.new_tag('details')
                summary = index.new_tag('summary')
                summary.insert(0, NavigableString('Popis'))
                m_details.append(summary)

                # Description.
                spotted = 'Ano' if m_spotted else 'Ne'
                for part, content in {'Hlava': m_head, 'Křídla': m_wings, 'Hruď': m_chest, 'Ocas': m_tail,
                                      'Nohy': m_legs, 'Záda': m_back, 'Zobák': m_beak, 'Kropenatost': [spotted],
                                      'Typ': [kind], 'Velikost': [size]}.items():
                    body_part_p = index.new_tag('p',  attrs={'class': 'description'})
                    body_part_b = index.new_tag('b')
                    body_part_b.insert(0, NavigableString(f'{part}: '))
                    body_part_p.append(body_part_b)
                    body_part_p.insert(1, NavigableString(f'{(", ".join(content))}'))
                    m_details.append(body_part_p)

                # Authors.
                for i_id, source in authors.items():
                    author_p = index.new_tag('p')
                    author_p.insert(0, NavigableString(f'Zdroj obrázku: [{i_id}] - {source}'))
                    m_details.append(author_p)
                if not female:
                    data_container.append(m_details)

                    # Links.
                    # We only want to add this once at the bottom of the whole card.
                    avibase_link = index.new_tag('a', attrs={'class': 'birdLink',
                                                             'href': avibase,
                                                             'title': 'Avibase',
                                                             'target': '_blank'})
                    avibase_link.insert(0, NavigableString('Avibase'))
                    photos_link = index.new_tag('a', attrs={'class': 'birdLink',
                                                            'href': photos_url,
                                                            'title': 'Více fotografií',
                                                            'target': '_blank'})
                    photos_link.insert(0, NavigableString('Fotky'))
                    wiki_link = index.new_tag('a', attrs={'class': 'birdLink',
                                                          'href': wiki_url,
                                                          'title': 'Wikipedie',
                                                          'target': '_blank'})
                    wiki_link.insert(0, NavigableString('Wiki'))

                    data_container.append(wiki_link)
                    data_container.append(photos_link)
                    data_container.append(avibase_link)

                    # Dodatek
                    note_p = index.new_tag('p', attrs={'class': 'birdNote'})
                    if note:
                        note_b = index.new_tag('b')
                        note_b.insert(0, NavigableString('Poznámka: '))
                        note_p.append(note_b)
                        note_p.insert(1, NavigableString(f'{note}'))
                    m_details.append(note_p)
                    bird_card_div.append(data_container)

                # Female: #############################################################################################
                if female:
                    card_title = index.new_tag('h5')
                    card_title.insert(0, NavigableString('Samice'))
                    gender_div = index.new_tag('div', attrs={'class': 'birdGender female'})
                    bird_card_div.append(gender_div)
                    gender_div.append(card_title)

                    img_id = 0
                    authors = {}
                    if f_photos:
                        for img in f_photos:
                            image_link = index.new_tag('a', attrs={'href': img['url'],
                                                                   'title': f'ID: {img_id}, {name}, Zdroj: {img["zdroj"]}',
                                                                   'target': '_blank'})
                            photo = index.new_tag('img', attrs={'height': '200px',
                                                                'alt': f'{name}, Zdroj: {img["zdroj"]}',
                                                                'src': f"images/ptaci/{path.cwd().name}/{img['file']}"})
                            image_link.append(photo)
                            gender_div.append(image_link)
                            authors[img_id] = img['zdroj']
                            img_id = img_id + 1
                    else:
                        image_link = index.new_tag('a', attrs={'href': 'images/neznámý_pták/nemame.png',
                                                               'title': f'ID: {img_id}, Obrázek není, Zdroj: whitebear',
                                                               'target': '_blank'})
                        photo = index.new_tag('img', attrs={'height': '200px',
                                                            'alt': 'Neznámý pták',
                                                            'src': 'images/neznámý_pták/nemame.png'})
                        image_link.append(photo)
                        gender_div.append(image_link)
                        authors[img_id] = 'Fotku nemáme'

                    # Description and authors.
                    data_container = index.new_tag('div')
                    details_container = index.new_tag('div', attrs={'class': 'singleBlock'})
                    details = index.new_tag('details')
                    summary = index.new_tag('summary')
                    summary.insert(0, NavigableString('Popis'))
                    details.append(summary)
                    details.append(details_container)

                    f_div = index.new_tag('div', attrs={'class': 'femaleDetails'})
                    gender_p = index.new_tag('p', attrs={'class': 'bold'})
                    gender_p.insert(0, NavigableString('Samice:'))
                    f_div.append(gender_p)

                    m_div = index.new_tag('div')
                    gender_p = index.new_tag('p', attrs={'class': 'bold'})
                    gender_p.insert(0, NavigableString('Samec:'))
                    m_div.append(gender_p)
                    m_content = m_details.findAll('p')
                    for p in m_content:
                        m_div.append(p)
                    details_container.append(m_div)

                    # Description.
                    spotted = 'Ano' if f_spotted else 'Ne'
                    for part, content in {'Hlava': f_head, 'Křídla': f_wings, 'Hruď': f_chest, 'Ocas': f_tail,
                                          'Nohy': f_legs, 'Záda': f_back, 'Zobák': f_beak, 'Kropenatost': [spotted],
                                          'Typ': [kind], 'Velikost': [size]}.items():
                        body_part_p = index.new_tag('p', attrs={'class': 'description'})
                        body_part_b = index.new_tag('b')
                        body_part_b.insert(0, NavigableString(f'{part}: '))
                        body_part_p.append(body_part_b)
                        body_part_p.insert(1, NavigableString(f'{(", ".join(content))}'))
                        f_div.append(body_part_p)

                    # Authors.
                    for i_id, source in authors.items():
                        author_p = index.new_tag('p')
                        author_p.insert(0, NavigableString(f'Zdroj obrázku: [{i_id}] - {source}'))
                        f_div.append(author_p)
                    details_container.append(f_div)
                    data_container.append(details)

                    # Links.
                    avibase_link = index.new_tag('a', attrs={'class': 'birdLink',
                                                             'href': avibase,
                                                             'title': 'Avibase',
                                                             'target': '_blank'})
                    avibase_link.insert(0, NavigableString('Avibase'))
                    photos_link = index.new_tag('a', attrs={'class': 'birdLink',
                                                            'href': photos_url,
                                                            'title': 'Více fotografií',
                                                            'target': '_blank'})
                    photos_link.insert(0, NavigableString('Fotky'))
                    wiki_link = index.new_tag('a', attrs={'class': 'birdLink',
                                                          'href': wiki_url,
                                                          'title': 'Wikipedie',
                                                          'target': '_blank'})
                    wiki_link.insert(0, NavigableString('Wiki'))

                    data_container.append(wiki_link)
                    data_container.append(photos_link)
                    data_container.append(avibase_link)

                    # Dodatek
                    note_p = index.new_tag('p', attrs={'class': 'birdNote'})
                    if note:
                        note_b = index.new_tag('b')
                        note_b.insert(0, NavigableString('Poznámka: '))
                        note_p.append(note_b)
                        note_p.insert(1, NavigableString(f'{note}'))
                    details_container.append(note_p)
                    bird_card_div.append(data_container)

            except Exception as ex:
                print(f'Error: {path}, {ex}')
            finally:
                os.chdir(database_dir.resolve())


if __name__ == '__main__':
    print('Start')
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
            html = template.prettify("utf-8").decode("utf-8")
            minimized = htmlmin.minify(html, remove_empty_space=True, remove_comments=True)
            with open("index.html", "w") as file:
                file.write(minimized)

    print('Done', www_dir / Path('index.html'))
