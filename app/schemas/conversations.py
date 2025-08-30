import os
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, EmailStr, validator
from sqlalchemy import (
    CheckConstraint,
    Column,
    DateTime,
    Integer,
    String,
    create_engine,
    or_,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, Session, mapped_column, sessionmaker

from app.core.database import Base


# CREATE TABLE conversations (
#    id SERIAL PRIMARY KEY,
#    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
# );
# SQLAlchemy Model
class Conversations(Base):
    __tablename__ = "conversations"

    id: int = Column(Integer, primary_key=True, index=True)
    created_at: datetime = Column(DateTime, default=datetime.utcnow)
    updated_at: datetime = Column(DateTime, default=datetime.utcnow)


class ConversationsBase(BaseModel):
    conversation_id: int
    created_at: datetime
    updated_at: datetime


class ConversationsResponse(ConversationsBase):
    id: int

    class Config:
        from_attributes = True
