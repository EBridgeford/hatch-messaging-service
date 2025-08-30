from typing import List

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from tenacity import RetryError

import app.crud.conversation_participants as convo_participants_crud
import app.crud.conversations as convo_crud
import app.crud.messages as msg_crud
import app.crud.users as users_crud
from app.api import deps
from app.models import messages
from app.schemas import users
from app.schemas.messages import Message
from app.services.mock_twilio import send_sms

router = APIRouter()


@router.post("/sms")
def sms(
    *,
    db: Session = Depends(deps.get_database),
    sms: messages.SMS,
):
    try:
        nums_in_msg = [sms.from_num, sms.to_num]
        user_ids = users_crud.get_or_create_users_by_phones(db, nums_in_msg)
        print(f"Got these user_ids {user_ids}")
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

        print("Writing message to messages table")

        msg = Message()
        msg.from_id = user_ids[0]
        msg.to_id = user_ids[1]
        msg.message_type = sms.message_type
        msg.body = sms.body
        msg.attachments = sms.attachments
        msg.sent_at = sms.timestamp
        msg_crud.create(db, msg)
        return Response(status_code=status.HTTP_200_OK)
    except Exception as e:
        print(str(e))
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@router.post("/email")
def email(
    *,
    db: Session = Depends(deps.get_database),
    email: messages.EMAIL,
):
    try:
        nums_in_msg = [email.from_email, email.to_email]
        user_ids = users_crud.get_or_create_users_by_emails(db, nums_in_msg)
        print(f"Got these user_ids {user_ids}")
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

        print("Writing message to messages table")

        msg = Message()
        msg.from_id = user_ids[0]
        msg.to_id = user_ids[1]
        msg.message_type = "email"
        msg.body = email.body
        msg.attachments = email.attachments
        msg.sent_at = email.timestamp
        msg_crud.create(db, msg)

        return Response(status_code=status.HTTP_200_OK)
    except Exception as e:
        print(str(e))
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
