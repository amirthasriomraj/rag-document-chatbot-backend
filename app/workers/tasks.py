from app.db.session import SessionLocal
from app.repositories.document_embedding_repo import DocumentEmbeddingRepository
from app.repositories.document_repo import DocumentRepository
from app.services.document_processing_service import DocumentProcessingService
from app.services.embedding_service import EmbeddingService
from app.workers.celery_app import celery_app
from app.core.logging import logger


@celery_app.task
def process_document_task(document_id: str):
    db = SessionLocal()

    try:
        document_repo = DocumentRepository(db)
        embedding_repo = DocumentEmbeddingRepository(db)

        processing_service = DocumentProcessingService()
        embedding_service = EmbeddingService()

        document_repo.update_status(
            document_id,
            "PROCESSING"
        )

        logger.info(
            f"Started processing document "
            f"{document_id}"
        )

        document = document_repo.get_by_id(document_id)

        if not document:
            return

        text = processing_service.extract_text_from_pdf(
            document.file_path
        )

        chunks = processing_service.chunk_text(text)

        vectors = embedding_service.generate_embeddings(
            chunks
        )

        for chunk, vector in zip(chunks, vectors):
            embedding_repo.create_embedding(
                document_id=document.id,
                chunk_text=chunk,
                embedding=vector
            )

        document_repo.update_status(
            document_id,
            "COMPLETED"
        )

        logger.info(
            f"Completed processing document "
            f"{document_id}"
        )

    except Exception as e:
        document_repo.update_status(
            document_id,
            "FAILED"
        )
        
        logger.error(
            f"Failed processing document "
            f"{document_id}: {str(e)}"
        )

    finally:
        db.close()