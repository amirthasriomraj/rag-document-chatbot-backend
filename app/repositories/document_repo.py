from sqlalchemy.orm import Session

from app.models.document import Document


class DocumentRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_document(
        self,
        user_id,
        filename: str,
        file_path: str
    ):
        document = Document(
            user_id=user_id,
            filename=filename,
            file_path=file_path
        )

        self.db.add(document)
        self.db.commit()
        self.db.refresh(document)

        return document

    def get_documents_by_user(self, user_id):
        return (
            self.db.query(Document)
            .filter(Document.user_id == user_id)
            .order_by(Document.upload_time.desc())
            .all()
        )