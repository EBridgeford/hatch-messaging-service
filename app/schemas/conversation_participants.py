from sqlalchemy import Column, ForeignKey, Integer

from app.core.database import Base


class ConversationParticipant(Base):
    __tablename__ = "conversation_participants"

    conversation_id = Column(Integer, ForeignKey("conversations.id"), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
