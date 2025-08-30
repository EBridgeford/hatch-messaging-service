from sqlalchemy.orm import Session

from app.schemas.messages import Message


def create(db: Session, new_message: Message) -> bool:
    db.add(new_message)
    db.flush()
    db.commit()
    return True


def get_all(db: Session) -> list[Message] | None:
    # All test messages are sent at the same moment, so I'm sorting by created_at to meaningfuly sort them
    return db.query(Message).order_by(Message.created_at).all()


def get_by_id(db: Session, conversation_id: int) -> list[Message] | None:
    # All test messages are sent at the same moment, so I'm sorting by created_at to meaningfuly sort them
    return (
        db.query(Message)
        .filter(Message.conversation_id == conversation_id)
        .order_by(Message.created_at)
        .all()
    )
