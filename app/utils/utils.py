import os
from uuid import UUID

from config import UPLOAD_DIR


def get_file_path(filename: str, unique_name: UUID) -> str:
    file_extension = (
        os.path.splitext(filename)[1]
        if os.path.splitext(filename)[1] else '.bin'
    )
    return os.path.join(UPLOAD_DIR, f'{str(unique_name)}{file_extension}')
