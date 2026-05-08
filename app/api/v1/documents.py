from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    UploadFile,
    File,
)
from sqlalchemy.orm import Session

from app.core.dependencies import (
    get_db,
    get_current_user,
)
from app.repositories.document_repo import DocumentRepository
from app.schemas.document import DocumentResponse
from app.services.document_service import DocumentService

router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)


@router.post(
    "/upload",
    response_model=DocumentResponse
)
def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    try:
        document_repo = DocumentRepository(db)
        document_service = DocumentService(document_repo)

        return document_service.upload_document(
            user_id=current_user.id,
            file=file
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )