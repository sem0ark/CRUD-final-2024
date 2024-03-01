import os
from pathlib import Path
from typing import IO

from src.services import image_service
from src.shared.config import FILE_FOLDER


def save_document(in_file: IO, id: str):
    path_to_file = get_document_path(id)

    # TODO: change to aiofile for asynchronous download
    with open(path_to_file, "wb") as f:
        f.write(in_file.read())

    return path_to_file


def save_image(in_file: IO, id: str):
    path_to_file = get_document_path(id)

    image_service.resize_image(in_file, path_to_file)

    return path_to_file


def get_document_path(id: str):
    return Path(os.path.join(FILE_FOLDER, id))


def delete_document_by_id(id: str):
    os.remove(get_document(id))


def delete_file(destination: str):
    os.remove(destination)


def get_document(id: str):
    return os.path.join(FILE_FOLDER, id)
