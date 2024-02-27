import os
from pathlib import Path

from fastapi import UploadFile

from src.config import DOCUMENT_FOLDER


def save_document(in_file: UploadFile, id: str):
    path_to_file = Path(os.path.join(DOCUMENT_FOLDER, id))

    # TODO: change to aiofile for asynchronous download
    with open(path_to_file, "wb") as f:
        f.write(in_file.file.read())


def delete_document_by_id(id: str):
    os.remove(get_document(id))


def delete_file(destination: str):
    os.remove(destination)


def get_document(id: str):
    return os.path.join(DOCUMENT_FOLDER, id)
