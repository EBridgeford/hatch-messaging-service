import os
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, EmailStr, validator
from sqlalchemy import (
    ARRAY,
    CheckConstraint,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    create_engine,
    or_,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

from app.core.database import Base


# CREATE TABLE messages (
#    id SERIAL PRIMARY KEY,
#    conversation_id INTEGER REFERENCES conversations(id) ON DELETE CASCADE,
#    from_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
#    to_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
#    body TEXT NOT NULL,
#    attachments TEXT[],
#    messaging_provider_id TEXT,
#    xillio_id TEXT,
#    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
#
# );
class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"))
    from_id = Column(Integer, ForeignKey("users.id"))
    to_id = Column(Integer, ForeignKey("users.id"))
    body = Column(Text)
    attachments = Column(ARRAY(Text))
    messaging_provider_id = Column(Text)
    xillio_id = Column(Text)
    message_type = Column(Text, nullable=False)
    sent_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)


class MessageBase(BaseModel):
    conversation_id: int
    from_id: int
    to_id: int
    body: str
    attachments: Optional[List[str]] = None
    messaging_provider_id: Optional[str] = None
    xillio_id: Optional[str] = None


class MessageResponse(MessageBase):
    id: int
    sent_at: datetime

    class Config:
        from_attributes = True
