from typing import IO

# @cache
# def get_s3():
#     return boto3.resource('s3')


class AWSFileService:
    def __init__(self, folder):
        self.folder = folder
        raise ValueError("Called not created S3 Service!")
        # self.s3 = get_s3()

    def save_file(self, in_file: IO, id: str):
        return "not implemented"

    def delete_file_by_id(self, id: str):
        pass

    def get_file_path(self, id: str) -> str:
        return f"{self.folder}/{id}"
