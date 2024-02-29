import os
from pathlib import Path

from fastapi import UploadFile

from src.shared.config import FILE_FOLDER


def save_document(in_file: UploadFile, id: str):
    path_to_file = get_document_path(id)

    # TODO: change to aiofile for asynchronous download
    with open(path_to_file, "wb") as f:
        f.write(in_file.file.read())

    return path_to_file


def get_document_path(id: str):
    return Path(os.path.join(FILE_FOLDER, id))


def delete_document_by_id(id: str):
    os.remove(get_document(id))


def delete_file(destination: str):
    os.remove(destination)


def get_document(id: str):
    return os.path.join(FILE_FOLDER, id)
