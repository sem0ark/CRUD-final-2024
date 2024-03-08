import os
from functools import cache
from typing import IO

import boto3

from src.shared.config import TMP_FOLDER
from src.shared.logs import log


@cache
def get_s3():
    return boto3.resource("s3")


class AWSFileService:
    def __init__(self, folder, bucket):
        self.folder = folder
        self.bucket = bucket
        self.s3 = get_s3()

    def save_file(self, in_file: IO, id: str):
        log.debug(f"Saving file {id} into {self.get_file_path(id)}")
        self.s3.Object(Bucket=self.bucket, Key=self.get_file_path(id)).put(Body=in_file)

    def delete_file_by_id(self, id: str):
        log.debug(f"Deleting file {id} from {self.get_file_path(id)}")
        self.s3.Object(Bucket=self.bucket, Key=self.get_file_path(id)).delete()

    def download_file(self, id: str):
        # Use couple characters of the UUID to achieve tmp storage to send back the file
        # and avoid potential collisions
        download_path = os.path.join(TMP_FOLDER, id[:2])
        log.debug(f"Downloading file {id} to {download_path}")
        self.s3.Object(Bucket=self.bucket, Key=self.get_file_path(id)).download(
            download_path
        )
        return download_path

    def get_file_path(self, id: str) -> str:
        return f"{self.folder}/{id}"
