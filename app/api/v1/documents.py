from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    UploadFile,
    File,
    Query,
)
from sqlalchemy.orm import Session
from typing import List
import os

from app.core.dependencies import (
    get_db,
    get_current_user,
)
from app.repositories.document_repo import DocumentRepository
from app.schemas.document import DocumentResponse
from app.services.document_service import DocumentService
from app.schemas.document import DocumentListItem
from app.models.user import User
from app.core.logging import logger

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
    
        document = document_service.upload_document(
            user_id=current_user.id,
            file=file
        )

        logger.info(
            f"Document uploaded: {document.id}"
        )

        return document

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    

@router.get("")
def list_documents(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    repo = DocumentRepository(db)

    skip = (page - 1) * page_size

    documents = repo.get_documents_by_user(
        user_id=current_user.id,
        skip=skip,
        limit=page_size
    )

    response = [
        DocumentListItem.model_validate(doc)
        for doc in documents
    ]

    return {
        "success": True,
        "data": response
    }


@router.delete("/{document_id}")
def delete_document(
    document_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    repo = DocumentRepository(db)

    document = repo.get_by_id_and_user(
        document_id=document_id,
        user_id=current_user.id
    )

    if not document:
        raise HTTPException(
            status_code=403,
            detail="You do not have access to this document."
        )

    if os.path.exists(document.file_path):
        os.remove(document.file_path)

    repo.delete_document(document)

    return {
        "success": True,
        "data": {
            "message": "Document deleted successfully."
        }
    }