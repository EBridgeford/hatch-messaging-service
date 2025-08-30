from typing import Optional

from sqlalchemy import func, insert
from sqlalchemy.orm import Session

from app.schemas.messages import Message


def create(db: Session, new_message: Message) -> bool:
    db.add(new_message)
    db.flush()
    db.commit()
    return True
