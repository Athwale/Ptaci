import sys
from pathlib import Path

import yaml
from bs4 import BeautifulSoup


if __name__ == '__main__':
    data_directory = Path(Path.cwd() / Path('../www/images/ptaci'))
    if not data_directory.exists():
        print(f'Working directory not found: {data_directory}')
    else:
        for path in data_directory.iterdir():
            if path.is_dir():
                try:
                    metadata = list(path.glob('data.yml'))[0]
                    with open(metadata, 'r', encoding='utf-8') as file:
                        data = yaml.safe_load(file)
                        print(data)
                except Exception as e:
                    print(f'Error: {path}, {e}')
                    sys.exit(1)
