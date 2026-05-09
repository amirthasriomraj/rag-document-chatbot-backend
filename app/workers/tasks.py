import time

from app.db.session import SessionLocal
from app.repositories.document_repo import DocumentRepository
from app.workers.celery_app import celery_app


@celery_app.task
def process_document_task(document_id: str):
    db = SessionLocal()

    try:
        document_repo = DocumentRepository(db)

        document_repo.update_status(
            document_id,
            "PROCESSING"
        )

        time.sleep(5)

        document_repo.update_status(
            document_id,
            "COMPLETED"
        )

        print(
            f"Document {document_id} processed successfully"
        )

    finally:
        db.close()