from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import app.crud.conversations as convo_crud
from app.api import deps

router = APIRouter()


@router.get("")
def get_conversations_all(
    *,
    db: Session = Depends(deps.get_database),
):
    return convo_crud.get_all(db)


@router.get("/{conversation_id}/messages")
def get_conversations_by_id(
    conversation_id: int,
    *,
    db: Session = Depends(deps.get_database),
):
    return convo_crud.get_conversation_by_id(db, conversation_id)
