#!/bin/python3
import os
from pathlib import Path
from PIL import Image


def optimize_image(img_path: Path, thumbnail: int, work_dir: Path) -> None:
    """
    Optimize image convert, resize and optimize.
    :param img_path: Path to image.
    :param thumbnail: thumbnail size.
    :param work_dir: Main working directory.
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
    with open(work_dir / Path('./optimalizovano.txt'), 'a') as optimized_files:
        optimized_files.write(img_path.name + '\n')


if __name__ == '__main__':
    script_dir = Path.cwd()
    working_directory = Path(Path.cwd() / Path('../databaze'))
    if not working_directory.exists():
        print(f'Working directory not found: {working_directory}')
    else:
        with open('optimalizovano.txt', 'r') as already_optimized:
            optimized = [name.strip('\n') for name in already_optimized.readlines()]
        os.chdir(working_directory)
        for path in Path(Path.cwd()).iterdir():
            if path.is_dir():
                try:
                    os.chdir(path)
                    for img_p in list(Path.cwd().glob('*.jpg')):
                        if img_p.name not in optimized:
                            optimize_image(img_p, 500, script_dir)
                except Exception as e:
                    print(f'Error: {path}, {e}')
                finally:
                    os.chdir(working_directory)
    print("Remove exif after optimization.")
