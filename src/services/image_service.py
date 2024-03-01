from pathlib import Path
from typing import IO

from PIL import Image

from src.shared.config import LOGO_SIZE


# https://note.nkmk.me/en/python-pillow-square-circle-thumbnail/
def crop_center(pil_img: Image.Image, crop_width, crop_height):
    img_width, img_height = pil_img.size

    return pil_img.crop(
        (
            (img_width - crop_width) // 2,
            (img_height - crop_height) // 2,
            (img_width + crop_width) // 2,
            (img_height + crop_height) // 2,
        )
    )


def crop_max_square(pil_img):
    return crop_center(pil_img, min(pil_img.size), min(pil_img.size))


def resize_image(file: IO, filename: Path):
    with Image.open(file) as im:
        im = crop_max_square(im)
        im.thumbnail((LOGO_SIZE, LOGO_SIZE))
        im.save(filename, "JPEG")
