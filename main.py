import uvicorn

from app.core.database import create_tables, drop_tables

# These imports are not directly used, but automagically used by sqlalchemy to power drop_tables and create_tables
from app.schemas.users import User  # noqa: F401
from app.schemas.conversations import Conversation  # noqa: F401
from app.schemas.conversation_participants import ConversationParticipant  # noqa: F401
from app.schemas.messages import Message  # noqa: F401

if __name__ == "__main__":
    drop_tables()
    create_tables()
    uvicorn.run("app.app:app", host="localhost", port=8080, reload=True)
