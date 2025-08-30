from typing import Optional

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.schemas.conversation_participants import ConversationParticipants


def find_conversation_id_for_users(db: Session, user_ids: list[int]) -> int | None:
    conversation_id: int = (
        db.query(ConversationParticipants.conversation_id)
        .filter(ConversationParticipants.user_id.in_(user_ids))
        .group_by(ConversationParticipants.conversation_id)
        .having(func.count(ConversationParticipants.user_id) == len(user_ids))
        .scalar()
    )

    return conversation_id


def assign_users_for_new_convo(db: Session, conversation_id, user_ids: list[int]):
    try:
        participant_list = []

        for user_id in user_ids:
            participant_list.append(
                {"conversation_id": conversation_id, "user_id": user_id}
            )

        db.bulk_insert_mappings(ConversationParticipants, participant_list)
        db.commit()
        return True
    except Exception as e:
        print("Error!")
        print(str(e))
        return False
