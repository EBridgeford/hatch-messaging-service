import uvicorn
from app.core.database import create_tables, drop_tables
from app.schemas.users import User
from app.schemas.conversation_participants import ConversationParticipants
from app.schemas.conversations import Conversations
from app.schemas.messages import Message

if __name__ == "__main__":
    drop_tables()
    create_tables()
    uvicorn.run("app.main:app", host="localhost", port=8080, reload=True)
