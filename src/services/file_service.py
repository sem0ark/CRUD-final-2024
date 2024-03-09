import src.services.aws.file_service as aws
import src.services.local.file_service as local
from src.shared.config import (
    DOCUMENT_FOLDER,
    FILE_FOLDER,
    LOGO_FOLDER,
    RUN_CLOUD,
    RUN_CONTAINER,
    RUN_LOCAL,
)
from src.shared.logs import log


def init_file_service(
    folder: str, used_processing: bool = False
) -> local.LocalFileService | aws.AWSFileService:
    log.warning(
        f"received RUN_LOCAL={RUN_LOCAL} \
RUN_CONTAINER={RUN_CONTAINER} RUN_CLOUD={RUN_CLOUD}"
    )

    if RUN_CLOUD:
        if used_processing:
            return aws.AWSFileService(folder, FILE_FOLDER, folder + "-processed")
        return aws.AWSFileService(folder, FILE_FOLDER)

    if RUN_LOCAL or RUN_CONTAINER:
        return local.LocalFileService(folder)

    raise ValueError(
        "Failed to define correct service for file handling,\
 please define RUN_LOCAL, RUN_CONTAINER or RUN_CLOUD."
    )


documents = init_file_service(DOCUMENT_FOLDER)
logos = init_file_service(LOGO_FOLDER, True)
