from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.repositories.chat_repo import ChatRepository
from app.repositories.document_repo import DocumentRepository
from app.schemas.dashboard import DashboardSummaryResponse

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


@router.get("/summary")
def get_dashboard_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    document_repo = DocumentRepository(db)
    chat_repo = ChatRepository(db)

    doc_summary = document_repo.get_document_summary(
        current_user.id
    )

    total_chats = chat_repo.get_chat_count(
        current_user.id
    )

    return {
        "success": True,
        "data": DashboardSummaryResponse(
            total_documents=doc_summary["total_documents"],
            completed_documents=doc_summary["completed_documents"],
            processing_documents=doc_summary["processing_documents"],
            failed_documents=doc_summary["failed_documents"],
            total_chats=total_chats
        )
    }