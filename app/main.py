from fastapi import FastAPI
from fastapi import HTTPException

from app.core.exceptions import (
    http_exception_handler,
    generic_exception_handler
)

from app.api.v1.auth import router as auth_router
from app.api.v1.documents import router as document_router
from app.api.v1.chat import router as chat_router
from app.api.v1.dashboard import router as dashboard_router
from app.api.v1.health import router as health_router
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0"
)

app.add_exception_handler(
    HTTPException,
    http_exception_handler
)

app.add_exception_handler(
    Exception,
    generic_exception_handler
)

app.include_router(auth_router)
app.include_router(document_router)
app.include_router(chat_router)
app.include_router(dashboard_router)
app.include_router(health_router)

@app.get("/")
def root():
    return {
        "message": "RAG Backend Running"
    }

