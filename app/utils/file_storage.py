import os
import uuid

from fastapi import UploadFile

UPLOAD_DIR = "uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)


def save_uploaded_file(file: UploadFile) -> tuple[str, str]:
    unique_filename = f"{uuid.uuid4()}_{file.filename}"
    file_path = os.path.join(
        UPLOAD_DIR,
        unique_filename
    )

    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())

    return unique_filename, file_path