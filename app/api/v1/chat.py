from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List

from app.core.dependencies import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.repositories.chat_repo import ChatRepository
from app.repositories.document_embedding_repo import DocumentEmbeddingRepository
from app.schemas.chat import ChatAskRequest, ChatAskResponse
from app.services.chat_service import ChatService
from app.repositories.document_repo import DocumentRepository
from app.schemas.chat import ChatHistoryItem
from app.core.logging import logger

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post("/ask")
def ask_question(
    payload: ChatAskRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    chat_repo = ChatRepository(db)
    embedding_repo = DocumentEmbeddingRepository(db)
    document_repo = DocumentRepository(db)

    chat_service = ChatService(
        chat_repo=chat_repo,
        embedding_repo=embedding_repo,
        document_repo=document_repo
    )

    logger.info(
        f"Question received for document "
        f"{payload.document_id}"
    )

    answer = chat_service.ask_question(
        user_id=current_user.id,
        document_id=payload.document_id,
        question=payload.question
    )

    logger.info(
        f"Answer generated for document "
        f"{payload.document_id}"
    )

    return {
        "success": True,
        "data": {
            "answer": answer
        }
    }


@router.get("/history")
def get_chat_history(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    chat_repo = ChatRepository(db)

    skip = (page - 1) * page_size

    chats = chat_repo.get_user_chats(
        user_id=current_user.id,
        skip=skip,
        limit=page_size
    )

    response = [
        ChatHistoryItem.model_validate(chat)
        for chat in chats
    ]

    return {
        "success": True,
        "data": response
    }