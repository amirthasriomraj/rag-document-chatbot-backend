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


    def get_documents_by_user(
        self,
        user_id,
        skip: int = 0,
        limit: int = 10
    ):
        return (
            self.db.query(Document)
            .filter(Document.user_id == user_id)
            .order_by(Document.upload_time.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    
    def get_by_id(self, document_id):
        return (
            self.db.query(Document)
            .filter(Document.id == document_id)
            .first()
        )


    def update_status(
        self,
        document_id,
        status: str
    ):
        document = self.get_by_id(document_id)

        if document:
            document.processing_status = status
            self.db.commit()
            self.db.refresh(document)

        return document
    

    def get_by_id_and_user(
        self,
        document_id,
        user_id
    ):
        return (
            self.db.query(Document)
            .filter(
                Document.id == document_id,
                Document.user_id == user_id
            )
            .first()
        )
    

    def delete_document(
        self,
        document
    ):
        self.db.delete(document)
        self.db.commit()


    def get_document_summary(
        self,
        user_id
    ):
        documents = (
            self.db.query(Document)
            .filter(Document.user_id == user_id)
            .all()
        )

        total_documents = len(documents)

        completed_documents = len([
            d for d in documents
            if d.processing_status == "COMPLETED"
        ])

        processing_documents = len([
            d for d in documents
            if d.processing_status == "PROCESSING"
        ])

        failed_documents = len([
            d for d in documents
            if d.processing_status == "FAILED"
        ])

        return {
            "total_documents": total_documents,
            "completed_documents": completed_documents,
            "processing_documents": processing_documents,
            "failed_documents": failed_documents
        }