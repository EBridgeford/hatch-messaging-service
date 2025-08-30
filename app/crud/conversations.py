from typing import Optional

from sqlalchemy import func, insert
from sqlalchemy.orm import Session

from app.schemas.conversations import Conversations


def create(db: Session) -> int:
    new_convo = Conversations()
    db.add(new_convo)
    db.flush()
    db.commit()
    return new_convo.id
