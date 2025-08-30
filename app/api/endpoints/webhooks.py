from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

import app.crud.conversation_participants as convo_participants_crud
import app.crud.conversations as convo_crud
import app.crud.messages as msg_crud
import app.crud.users as users_crud
from app.api import deps
from app.schemas.messages import Message, MessageBase

router = APIRouter()


@router.post("/sms")
def sms(
    *,
    db: Session = Depends(deps.get_database),
    message: MessageBase,
):
    try:
        nums_in_msg = [message.from_field, message.to_field]
        user_ids = users_crud.get_or_create_users_by_phones(db, nums_in_msg)
        conversation_id = convo_participants_crud.find_conversation_id_for_users(
            db, user_ids
        )
        print(f"These users are part of conversation_id {conversation_id}")
        if conversation_id is None:
            conversation_id = convo_crud.create(db)
            print(f"No conversation in progress, created id {conversation_id}")
            success = convo_participants_crud.assign_users_for_new_convo(
                db, conversation_id, user_ids
            )

            if success is False:
                raise HTTPException(
                    status_code=500, detail="Error creating new conversation"
                )

        message.conversation_id = conversation_id
        message.from_id = user_ids[0]
        message.to_id = user_ids[1]
        print("Writing message to messages table")
        message_db = Message(**message.model_dump(exclude={"from_field", "to_field"}))
        msg_crud.create(db, message_db)
        return Response(status_code=status.HTTP_200_OK)
    except Exception as e:
        print(f"Exception {e}")
        raise HTTPException(status_code=500, detail="Error handling sms webhook")


@router.post("/email")
def email(
    *,
    db: Session = Depends(deps.get_database),
    message: MessageBase,
):
    try:
        emails_in_msg = [message.from_field, message.to_field]
        user_ids = users_crud.get_or_create_users_by_emails(db, emails_in_msg)
        conversation_id = convo_participants_crud.find_conversation_id_for_users(
            db, user_ids
        )
        print(f"These users are part of conversation_id {conversation_id}")
        if conversation_id is None:
            conversation_id = convo_crud.create(db)
            print(f"No conversation in progress, created id {conversation_id}")
            success = convo_participants_crud.assign_users_for_new_convo(
                db, conversation_id, user_ids
            )
            if success is False:
                raise HTTPException(
                    status_code=500, detail="Error creating new conversation"
                )

        message.conversation_id = conversation_id
        message.from_id = user_ids[0]
        message.to_id = user_ids[1]
        message_db = Message(**message.model_dump(exclude={"from_field", "to_field"}))
        print("Writing message to messages table")
        msg_crud.create(db, message_db)

        return Response(status_code=status.HTTP_200_OK)
    except Exception as e:
        print(f"Exception {e}")
        raise HTTPException(status_code=500, detail="Error handling email webhook")
