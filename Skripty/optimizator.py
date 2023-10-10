#!/bin/python3
from pathlib import Path
from PIL import Image


def optimize_image(img_path: Path, thumbnail: int) -> None:
    """
    Optimize image convert, resize and optimize.
    :param img_path: Path to image.
    :param thumbnail: thumbnail size.
    :return: None
    """
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
