from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from tenacity import RetryError

import app.crud.conversation_participants as convo_participants_crud
import app.crud.conversations as convo_crud
import app.crud.messages as msg_crud
import app.crud.users as users_crud
from app.api import deps
from app.core.config import Settings
from app.models.sms_email import EMAIL, SMS
from app.schemas.messages import Message
from app.services.mock_sendgrid import send_email
from app.services.mock_twilio import send_sms

router = APIRouter()


@router.post("/sms")
def sms(
    *,
    db: Session = Depends(deps.get_database),
    config: Settings = Depends(deps.get_settings),
    sms: SMS,
):
    nums_in_msg = [sms.from_num, sms.to_num]
    user_ids = users_crud.get_or_create_users_by_phones(db, nums_in_msg)
    conversation_id = convo_participants_crud.find_conversation_id_for_users(
        db, user_ids
    )
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
    else:
        print(f"These users are part of conversation_id {conversation_id}")

    msg = Message.from_sms_model(
        sms=sms, from_id=user_ids[0], to_id=user_ids[1], conversation_id=conversation_id
    )

    try:
        response = send_sms(msg, config.twilio_api_key)
        print("Send text via service, now writing message to messages table")
        msg_crud.create(db, msg)
    except RetryError:
        raise HTTPException(status_code=500, detail="Error calling SMS/MMS service")

    return Response(status_code=status.HTTP_200_OK)


@router.post("/email")
def email(
    *,
    db: Session = Depends(deps.get_database),
    config: Settings = Depends(deps.get_settings),
    email: EMAIL,
):
    emails_in_msg = [email.from_email, email.to_email]
    user_ids = users_crud.get_or_create_users_by_emails(db, emails_in_msg)
    conversation_id = convo_participants_crud.find_conversation_id_for_users(
        db, user_ids
    )
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
    else:
        print(f"These users are part of conversation_id {conversation_id}")

    msg = Message.from_email_model(
        email=email,
        from_id=user_ids[0],
        to_id=user_ids[1],
        conversation_id=conversation_id,
    )

    try:
        response = send_email(msg, config.sendgrid_api_key)
        print("Sent email via service, now writing  message to messages table")
        msg_crud.create(db, msg)
    except RetryError:
        raise HTTPException(status_code=500, detail="Error calling email service")

    return Response(status_code=status.HTTP_200_OK)
