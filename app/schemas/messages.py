from datetime import datetime

from pydantic import BaseModel, Field
from sqlalchemy import (
    ARRAY,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    Text,
)

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
    conversation_id = Column(Integer, ForeignKey("conversations.id"), nullable=False)
    from_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    to_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    body = Column(Text)
    attachments = Column(ARRAY(Text))
    messaging_provider_id = Column(Text)
    xillio_id = Column(Text)
    message_type = Column(Text, nullable=False)
    sent_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)


class MessageBase(BaseModel):
    from_field: str = Field(alias="from")
    to_field: str = Field(alias="to")
    from_id: int | None = None
    to_id: int | None = None
    message_type: str = Field(alias="type", default="email")
    conversation_id: int | None = None
    body: str
    attachments: list[str] | None = None
    sent_at: datetime = Field(alias="timestamp")
    messaging_provider_id: str | None = None
    xillio_id: str | None = None

    class Config:
        from_attributes = True  # For Pydantic v2
