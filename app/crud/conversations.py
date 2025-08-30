from sqlalchemy.orm import Session

from app.schemas.conversations import Conversation


def create(db: Session) -> int:
    new_convo = Conversation()
    db.add(new_convo)
    db.flush()
    db.commit()
    return new_convo.id
