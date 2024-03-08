import src.services.aws.file_service as aws
import src.services.local.file_service as local
from src.shared.config import (
    DOCUMENT_FOLDER,
    LOGO_FOLDER,
    RUN_CLOUD,
    RUN_CONTAINER,
    RUN_LOCAL,
)


def init_file_service(folder: str) -> local.LocalFileService | aws.AWSFileService:
    if RUN_LOCAL or RUN_CONTAINER:
        return local.LocalFileService(folder)
    if RUN_CLOUD:
        return aws.AWSFileService(folder)

    raise ValueError(
        "Failed to define correct service for file handling,\
 please define RUN_LOCAL, RUN_CONTAINER or RUN_CLOUD."
    )


documents = init_file_service(DOCUMENT_FOLDER)
logos = init_file_service(LOGO_FOLDER)
