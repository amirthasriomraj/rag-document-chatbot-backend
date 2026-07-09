from openai import OpenAI

from app.core.config import settings


class EmbeddingService:
    def __init__(self):
        self.client = OpenAI(
            api_key=settings.OPENAI_API_KEY
        )

    def generate_embeddings(
        self,
        texts: list[str]
    ):
        response = self.client.embeddings.create(
            model="text-embedding-3-small",
            input=texts
        )

        return [
            item.embedding
            for item in response.data
        ]