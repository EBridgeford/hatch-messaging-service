from sqlalchemy import func
from sqlalchemy.orm import Session

from app.schemas.conversation_participants import ConversationParticipant


def find_conversation_id_for_users(db: Session, user_ids: list[int]) -> int | None:
    conversation_id: int = (
        db.query(ConversationParticipant.conversation_id)
        .filter(ConversationParticipant.user_id.in_(user_ids))
        .group_by(ConversationParticipant.conversation_id)
        .having(func.count(ConversationParticipant.user_id) == len(user_ids))
        .scalar()
    )

    return conversation_id


def assign_users_for_new_convo(
    db: Session, conversation_id: int, user_ids: list[int]
) -> bool:
    try:
        participant_list = [
            {"conversation_id": conversation_id, "user_id": user_id}
            for user_id in user_ids
        ]
        db.bulk_insert_mappings(ConversationParticipant, participant_list)
        db.commit()
        return True
    except Exception as e:
        print(f"Encountered error while assigning users to a new conversation {e}")
        return False
