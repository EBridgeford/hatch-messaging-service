from sqlalchemy.orm import Session

from app.schemas.conversations import Conversation, ConversationWithMessages
from app.schemas.messages import MessageBase
import app.crud.messages as crud_messages


def create(db: Session) -> int:
    new_convo = Conversation()
    db.add(new_convo)
    db.flush()
    db.commit()
    return new_convo.id


def get_conversation_by_id(
    db: Session, conversation_id: int
) -> ConversationWithMessages | None:
    conversation = (
        db.query(Conversation).filter(Conversation.id == conversation_id).first()
    )

    if not conversation:
        return None

    messages = crud_messages.get_by_id(db, conversation_id)

    ret = ConversationWithMessages.model_validate(conversation)

    if messages:
        ret.messages = [MessageBase.model_validate(message) for message in messages]

    return ret


def get_all(db: Session) -> list[ConversationWithMessages] | None:
    conversations = db.query(Conversation).all()

    if not conversations:
        return None

    ret = []
    for conversation in conversations:
        messages = crud_messages.get_by_id(db, conversation.id)

        inner_ret = ConversationWithMessages.model_validate(conversation)

        if messages:
            inner_ret.messages = [
                MessageBase.model_validate(message) for message in messages
            ]

        ret.append(inner_ret)

    return ret
