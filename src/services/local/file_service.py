import os
from pathlib import Path
from typing import IO

# from PIL import Image
# https://note.nkmk.me/en/python-pillow-square-circle-thumbnail/
# def crop_center(pil_img: Image.Image, crop_width, crop_height):
#     img_width, img_height = pil_img.size

#     return pil_img.crop(
#         (
#             (img_width - crop_width) // 2,
#             (img_height - crop_height) // 2,
#             (img_width + crop_width) // 2,
#             (img_height + crop_height) // 2,
#         )
#     )


# def crop_max_square(pil_img):
#     return crop_center(pil_img, min(pil_img.size), min(pil_img.size))


# def resize_image(file: IO, filename: Path):
#     with Image.open(file) as im:
#         im = crop_max_square(im)
#         im.thumbnail((LOGO_SIZE, LOGO_SIZE))
#         im.save(filename, "JPEG")


class LocalFileService:
    def __init__(self, folder):
        self.folder = folder

    def save_file(self, in_file: IO, id: str, content_type: str | None = None):
        path_to_file = Path(self.get_file_path(id))

        # TODO: change to aiofile for asynchronous download
        with open(path_to_file, "wb") as f:
            f.write(in_file.read())

        return path_to_file

    def download_file(self, id: str):
        return self.get_file_path(id)

    def delete_file_by_id(self, id: str):
        os.remove(self.get_file_path(id))

    def get_file_path(self, id: str):
        return os.path.join(self.folder, id)
