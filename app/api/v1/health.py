from fastapi import APIRouter
from sqlalchemy import text
from app.db.session import get_db
from fastapi import Depends
from sqlalchemy.orm import Session
from redis import Redis
from app.core.config import settings


router = APIRouter(
    prefix="/health",
    tags=["Health"]
)

@router.get("")
def health_check():
    return {
        "success": True,
        "data": {
            "status": "healthy"
        }
    }

@router.get("/db")
def database_health(
    db: Session = Depends(get_db)
):
    db.execute(
        text("SELECT 1")
    )

    return {
        "success": True,
        "data": {
            "database": "healthy"
        }
    }

@router.get("/redis")
def redis_health():
    redis_client = Redis.from_url(
        settings.REDIS_URL
    )

    redis_client.ping()

    return {
        "success": True,
        "data": {
            "redis": "healthy"
        }
    }