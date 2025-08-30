from datetime import datetime

from pydantic import BaseModel
from sqlalchemy import (
    Column,
    DateTime,
    Integer,
)

from app.core.database import Base
from app.schemas.messages import MessageBase


# CREATE TABLE conversations (
#    id SERIAL PRIMARY KEY,
#    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
# );
# SQLAlchemy Model
class Conversation(Base):
    __tablename__ = "conversations"

    id: int = Column(Integer, primary_key=True, index=True)
    created_at: datetime = Column(DateTime, default=datetime.utcnow)
    updated_at: datetime = Column(DateTime, default=datetime.utcnow)


class ConversationBase(BaseModel):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ConversationWithMessages(ConversationBase):
    messages: list[MessageBase] | None = None
