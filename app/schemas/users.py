from datetime import datetime

from pydantic import BaseModel, validator
from sqlalchemy import (
    CheckConstraint,
    Column,
    DateTime,
    Integer,
    String,
    or_,
)

from app.core.database import Base


# SQLAlchemy Model
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    phone = Column(String(20), unique=True, nullable=True)
    email = Column(String(255), unique=True, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        CheckConstraint(
            or_(email.isnot(None), phone.isnot(None)), name="contact_required"
        ),
    )


class UserBase(BaseModel):
    user_id: int
    phone: str | None = None
    email: str | None = None

    @validator("email", "phone")
    def contact_required(cls, v, values):
        if not v and not any(values.values()):
            raise ValueError("Either phone or email must be provided")
        return v


class UserResponse(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
