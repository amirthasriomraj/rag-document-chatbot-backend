from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.repositories.user_repo import UserRepository
from app.schemas.auth import (
    UserSignup,
    UserLogin,
    TokenResponse,
)
from app.services.auth_service import AuthService

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post(
    "/signup",
    response_model=TokenResponse
)
def signup(
    payload: UserSignup,
    db: Session = Depends(get_db)
):
    try:
        user_repo = UserRepository(db)
        auth_service = AuthService(user_repo)

        return auth_service.signup(
            name=payload.name,
            email=payload.email,
            password=payload.password
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@router.post(
    "/login",
    response_model=TokenResponse
)
def login(
    payload: UserLogin,
    db: Session = Depends(get_db)
):
    try:
        user_repo = UserRepository(db)
        auth_service = AuthService(user_repo)

        return auth_service.login(
            email=payload.email,
            password=payload.password
        )

    except ValueError as e:
        raise HTTPException(
            status_code=401,
            detail=str(e)
        )