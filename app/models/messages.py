from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Union

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr, Field, validator


class SMS(BaseModel):
    from_num: str = Field(alias="from")
    to_num: str = Field(alias="to")
    message_type: str = Field(alias="type")
    body: str
    attachments: Optional[List[str]]
    timestamp: datetime


class EMAIL(BaseModel):
    from_email: str = Field(alias="from")
    to_email: str = Field(alias="to")
    body: str
    attachments: Optional[List[str]]
    timestamp: datetime
