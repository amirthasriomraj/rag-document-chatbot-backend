from sqlalchemy.orm import Session

from app.models.document_embedding import DocumentEmbedding


class DocumentEmbeddingRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_embedding(
        self,
        document_id,
        chunk_text: str,
        embedding
    ):
        record = DocumentEmbedding(
            document_id=document_id,
            chunk_text=chunk_text,
            embedding=embedding
        )

        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)

        return record

    def similarity_search(
        self,
        query_embedding,
        document_id,
        limit: int = 5
    ):
        return (
            self.db.query(DocumentEmbedding)
            .filter(
                DocumentEmbedding.document_id == document_id
            )
            .order_by(
                DocumentEmbedding.embedding.cosine_distance(
                    query_embedding
                )
            )
            .limit(limit)
            .all()
        )