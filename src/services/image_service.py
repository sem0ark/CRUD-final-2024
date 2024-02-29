from pathlib import Path
from typing import IO

from PIL import Image

from src.shared.config import LOGO_SIZE


def resize_image(file: IO, filename: Path):
    with Image.open(file) as im:
        im.thumbnail((LOGO_SIZE, LOGO_SIZE))
        im.save(filename, "JPEG")
