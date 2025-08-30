from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

import app.crud.conversation_participants as convo_participants_crud
import app.crud.conversations as convo_crud
import app.crud.messages as msg_crud
import app.crud.users as users_crud
from app.api import deps
from app.models import messages
from app.schemas.messages import Message

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

            if success is False:
                    raise HTTPException(status_code=500, detail="Error creating new conversation")

        print("Writing message to messages table")

        msg = Message.from_sms_model(
            sms=sms,
            from_id=user_ids[0],
            to_id=user_ids[1],
            conversation_id=conversation_id,
        )
        msg_crud.create(db, msg)
        return Response(status_code=status.HTTP_200_OK)
    except Exception as e:
        print(f"Exception {e}")
        raise HTTPException(status_code=500, detail=f"Error handling sms webhook")


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
            if success is False:
                    raise HTTPException(status_code=500, detail="Error creating new conversation")

        print("Writing message to messages table")

        msg = Message.from_email_model(
            email=email,
            from_id=user_ids[0],
            to_id=user_ids[1],
            conversation_id=conversation_id,
        )
        msg_crud.create(db, msg)

        return Response(status_code=status.HTTP_200_OK)
    except Exception as e:
        print(f"Exception {e}")
        raise HTTPException(status_code=500, detail=f"Error handling email webhook")
