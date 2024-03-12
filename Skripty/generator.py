import os
from pathlib import Path

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
                    print(metadata)
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
