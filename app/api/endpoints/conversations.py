from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api import deps

router = APIRouter()

# @router.post("/", response_model=schemas.User)
# def create_user(
#    *,
#    db: Session = Depends(deps.get_database),
#    user_in: schemas.UserCreate,
# ):
#    user = crud.user.get_by_email(db, email=user_in.email)
#    if user:
#        raise HTTPException(status_code=400, detail="Email already registered")
#    return crud.user.create(db, obj_in=user_in)
#
