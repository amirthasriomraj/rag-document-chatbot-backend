from fastapi import FastAPI

from app.api.v1.auth import router as auth_router
from app.api.v1.documents import router as document_router
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0"
)

app.include_router(auth_router)
app.include_router(document_router)


@app.get("/")
def root():
    return {
        "message": "RAG Backend Running"
    }