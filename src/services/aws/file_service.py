import os
from functools import cache
from typing import IO

import boto3

from src.shared.config import AWS_ID, AWS_REGION, AWS_SECRET, TMP_FOLDER
from src.shared.logs import log


# Used cache to make it function as a singleton
@cache
def get_s3():
    session = boto3.Session(
        aws_access_key_id=AWS_ID,
        aws_secret_access_key=AWS_SECRET,
        region_name=AWS_REGION,
    )
    return session.client("s3")


class AWSFileService:
    def __init__(self, folder, bucket, source_folder: str | None = None):
        self.folder = folder

        # bucket folder where the files will be actually stored after processing
        # e.g. where the updated file will be put by AWS Lambda
        if source_folder:
            self.source_folder = source_folder
        else:
            self.source_folder = folder

        self.bucket = bucket
        self.s3 = get_s3()

    def save_file(self, in_file: IO, id: str, content_type: str | None = None):
        log.debug(f"Saving file {id} into {self.get_file_path(id)}")

        args = (
            {"ContentType": content_type, "ContentDisposition": content_type}
            if content_type
            else {}
        )
        self.s3.upload_fileobj(
            in_file, self.bucket, self.get_file_path(id), ExtraArgs=args
        )

    def delete_file_by_id(self, id: str):
        log.debug(f"Deleting file {id} from {self.get_file_path(id)}")
        self.s3.delete_object(Bucket=self.bucket, Key=self.get_file_path(id))

    def download_file(self, id: str):
        # Use couple characters of the UUID to achieve tmp storage to send back the file
        # and avoid potential collisions
        download_path = os.path.join(TMP_FOLDER, id[:2])
        log.debug(f"Downloading file {id} to {download_path}")
        self.s3.download_file(
            self.bucket, self.get_file_path(id, self.source_folder), download_path
        )
        return download_path

    def get_file_path(self, id: str, folder=None) -> str:
        if folder is None:
            return f"{self.folder}/{id}"
        return f"{folder}/{id}"
