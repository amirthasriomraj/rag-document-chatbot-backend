from openai import OpenAI

from app.core.config import settings


class LLMService:
    def __init__(self):
        self.client = OpenAI(
            api_key=settings.OPENAI_API_KEY
        )

    def generate_answer(
        self,
        question: str,
        context: str
    ):
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a document assistant. "
                        "Answer ONLY using the provided context. "
                        "If the answer is not in context, say "
                        "'I could not find that information in the document.'"
                    )
                },
                {
                    "role": "user",
                    "content": (
                        f"Context:\n{context}\n\n"
                        f"Question:\n{question}"
                    )
                }
            ]
        )

        return response.choices[0].message.content