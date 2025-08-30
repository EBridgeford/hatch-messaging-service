from datetime import datetime

from pydantic import BaseModel, Field


class SMS(BaseModel):
    from_num: str = Field(alias="from")
    to_num: str = Field(alias="to")
    message_type: str = Field(alias="type")
    body: str
    attachments: list[str] | None = None
    timestamp: datetime
    message_provider_id: str | None = None


class EMAIL(BaseModel):
    from_email: str = Field(alias="from")
    to_email: str = Field(alias="to")
    body: str
    attachments: list[str] | None = None
    timestamp: datetime
    xillio_id: str | None = None
