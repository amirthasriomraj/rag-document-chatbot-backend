from sqlalchemy.orm import Session

from app.models.chat import Chat


class ChatRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_chat(
        self,
        user_id,
        document_id,
        question: str,
        answer: str
    ):
        chat = Chat(
            user_id=user_id,
            document_id=document_id,
            question=question,
            answer=answer
        )

        self.db.add(chat)
        self.db.commit()
        self.db.refresh(chat)

        return chat

    def get_user_chats(
        self,
        user_id
    ):
        return (
            self.db.query(Chat)
            .filter(Chat.user_id == user_id)
            .order_by(Chat.created_at.desc())
            .all()
        )
    

    def get_chat_count(
        self,
        user_id
    ):
        return (
            self.db.query(Chat)
            .filter(Chat.user_id == user_id)
            .count()
        )