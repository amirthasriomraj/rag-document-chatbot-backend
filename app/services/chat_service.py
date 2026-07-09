from app.repositories.chat_repo import ChatRepository
from app.repositories.document_embedding_repo import DocumentEmbeddingRepository
from app.services.embedding_service import EmbeddingService
from app.services.llm_service import LLMService
from app.repositories.document_repo import DocumentRepository

from fastapi import HTTPException


class ChatService:
    def __init__(
        self,
        chat_repo: ChatRepository,
        embedding_repo: DocumentEmbeddingRepository,
        document_repo: DocumentRepository
    ):
        self.chat_repo = chat_repo
        self.embedding_repo = embedding_repo
        self.document_repo = document_repo
        self.embedding_service = EmbeddingService()
        self.llm_service = LLMService()

    def ask_question(
        self,
        user_id,
        document_id,
        question: str
    ):
        document = self.document_repo.get_by_id_and_user(
            document_id=document_id,
            user_id=user_id
        )

        if not document:
            raise HTTPException(
                status_code=403,
                detail="You do not have access to this document."
            )
                
        query_vector = self.embedding_service.generate_embeddings(
            [question]
        )[0]

        results = self.embedding_repo.similarity_search(
            query_embedding=query_vector,
            document_id=document_id
        )

        context = "\n\n".join(
            [result.chunk_text for result in results]
        )

        answer = self.llm_service.generate_answer(
            question=question,
            context=context
        )

        self.chat_repo.create_chat(
            user_id=user_id,
            document_id=document_id,
            question=question,
            answer=answer
        )

        return answer