# todo prepsat img url na https://commons.wikimedia.org/wiki/File:Tystie1.jpg kde je autor a licence.

import os
import yaml
from pathlib import Path


if __name__ == '__main__':
    script_dir = Path.cwd()
    for state in ['finished', 'unfinished']:
        working_directory = Path(Path.cwd() / Path(f'../databaze/{state}'))
        if not working_directory.exists():
            print(f'Working directory not found: {working_directory}')
        else:
            os.chdir(working_directory)
            for path in Path(Path.cwd()).iterdir():
                if path.is_dir():
                    try:
                        os.chdir(path)
                        # TODO open yaml and change links
                        with open('data.yml', 'r') as file:
                            metadata = yaml.safe_load(file)
                            available_genders = ['samec']
                            if metadata['popis']['samice']:
                                available_genders.append('samice')
                            for gender in available_genders:
                                for p in metadata['popis'][gender]['fotky']:
                                    filename = (p['url'].split('/')[-1])
                                    new_url = f'https://commons.wikimedia.org/wiki/File:{filename}'
                                    print(new_url)
                    except Exception as e:
                        print(f'Error: {path}, {e}')
                    finally:
                        os.chdir(working_directory)
            os.chdir(script_dir)
