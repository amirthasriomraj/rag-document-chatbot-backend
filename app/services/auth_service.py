from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
)
from app.repositories.user_repo import UserRepository


class AuthService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def signup(
        self,
        name: str,
        email: str,
        password: str
    ):
        existing_user = self.user_repo.get_by_email(email)

        if existing_user:
            raise ValueError("Email already registered")

        hashed_password = hash_password(password)

        user = self.user_repo.create_user(
            name=name,
            email=email,
            password_hash=hashed_password
        )

        token = create_access_token(
            {"sub": str(user.email)}
        )

        return {
            "access_token": token,
            "token_type": "bearer"
        }

    def login(
        self,
        email: str,
        password: str
    ):
        user = self.user_repo.get_by_email(email)

        if not user:
            raise ValueError("Invalid credentials")

        if not verify_password(
            password,
            user.password_hash
        ):
            raise ValueError("Invalid credentials")

        token = create_access_token(
            {"sub": str(user.email)}
        )

        return {
            "access_token": token,
            "token_type": "bearer"
        }