from pydantic import BaseModel


class DashboardSummaryResponse(BaseModel):
    total_documents: int
    completed_documents: int
    processing_documents: int
    failed_documents: int
    total_chats: int