from fastapi import UploadFile

from app.repositories.document_repo import DocumentRepository
from app.utils.file_storage import save_uploaded_file


ALLOWED_EXTENSIONS = {".pdf", ".docx"}


class DocumentService:
    def __init__(self, document_repo: DocumentRepository):
        self.document_repo = document_repo

    def upload_document(
        self,
        user_id,
        file: UploadFile
    ):
        filename = file.filename.lower()

        if not any(
            filename.endswith(ext)
            for ext in ALLOWED_EXTENSIONS
        ):
            raise ValueError(
                "Only PDF and DOCX files are allowed"
            )

        stored_filename, file_path = save_uploaded_file(file)

        document = self.document_repo.create_document(
            user_id=user_id,
            filename=stored_filename,
            file_path=file_path
        )

        return document