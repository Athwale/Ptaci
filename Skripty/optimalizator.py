#!/bin/python3
import os
from pathlib import Path
from PIL import Image


def optimize_image(img_path: Path, thumbnail: int) -> None:
    """
    Optimize image convert, resize and optimize.
    :param img_path: Path to image.
    :param thumbnail: thumbnail size.
    :return: None
    """
    print(f'Optimizing: {img_path}')
    # Convert.
    if img_path.suffix.lower() == '.png':
        png = Image.open(img_path)
        rgb_img = png.convert('RGB')
        img_path = img_path.rename(img_path.with_suffix('.jpg'))
        rgb_img.save(img_path)
    # Optimize.
    img = Image.open(img_path)
    img.save(img_path, optimize=True, quality=95)
    # Resize.
    img = Image.open(img_path)
    img.thumbnail((thumbnail, thumbnail), Image.LANCZOS)
    img.save(img_path, "JPEG")


if __name__ == '__main__':
    working_directory = Path(Path.home() / 'Downloads/birds')
    if not working_directory.exists():
        print(f'Working directory not found: {working_directory}')
    else:
        os.chdir(working_directory)
        for path in Path(Path.cwd()).iterdir():
            if path.is_dir():
                try:
                    os.chdir(path)
                    for img_p in list(Path.cwd().glob('*.jpg')):
                        optimize_image(img_p, 500)
                except:
                    print(f'Error: {path}')
                finally:
                    os.chdir(working_directory)
