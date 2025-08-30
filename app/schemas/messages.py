from datetime import datetime

from pydantic import BaseModel
from sqlalchemy import (
    ARRAY,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    Text,
)

from app.core.database import Base
from app.models.messages import EMAIL, SMS


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

    @classmethod
    def from_sms_model(
        cls, sms: SMS, from_id: int, to_id: int, conversation_id: int
    ) -> "Message":
        msg = Message()
        msg.from_id = from_id
        msg.to_id = to_id
        msg.conversation_id = conversation_id
        msg.message_type = sms.message_type
        msg.body = sms.body
        msg.attachments = sms.attachments
        msg.sent_at = sms.timestamp
        msg.messaging_provider_id = sms.message_provider_id
        return msg

    @classmethod
    def from_email_model(
        cls, email: EMAIL, from_id: int, to_id: int, conversation_id: int
    ) -> "Message":
        msg = Message()
        msg.from_id = from_id
        msg.to_id = to_id
        msg.conversation_id = conversation_id
        msg.message_type = "email"
        msg.body = email.body
        msg.attachments = email.attachments
        msg.sent_at = email.timestamp
        msg.xillio_id = email.xillio_id
        return msg


class MessageBase(BaseModel):
    conversation_id: int
    from_id: int
    to_id: int
    body: str
    attachments: list[str] | None = None
    messaging_provider_id: str | None = None
    xillio_id: str | None = None


class MessageResponse(MessageBase):
    id: int
    sent_at: datetime

    class Config:
        from_attributes = True
