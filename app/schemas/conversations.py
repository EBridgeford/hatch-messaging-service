from datetime import datetime

from sqlalchemy import (
    Column,
    DateTime,
    Integer,
)

from app.core.database import Base


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
