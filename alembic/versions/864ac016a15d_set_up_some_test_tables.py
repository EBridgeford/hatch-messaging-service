"""Set up some test tables

Revision ID: 864ac016a15d
Revises:
Create Date: 2025-08-26 19:34:16.544628

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "864ac016a15d"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

#    "from": "+18045551234",
#    "to": "+12016661234",
#    "type": "sms",
#    "messaging_provider_id": "message-1",
#    "body": "This is an incoming SMS message",
#    "attachments": null,
#    "timestamp": "2024-11-01T14:00:00Z"


#    "from": "contact@gmail.com",
#    "to": "user@usehatchapp.com",
#    "xillio_id": "message-3",
#    "body": "<html><body>This is an incoming email with <b>HTML</b> content</body></html>",
#    "attachments": ["https://example.com/received-document.pdf"],
#    "timestamp": "2024-11-01T14:00:00Z"
def upgrade() -> None:
    """Upgrade schema."""
    op.execute(
        """
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    phone VARCHAR(20) UNIQUE,
    email VARCHAR(255) UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    CONSTRAINT contact_required CHECK (email IS NOT NULL OR phone IS NOT NULL)
);

CREATE TABLE conversations (
    id SERIAL PRIMARY KEY,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE conversation_participants (
    conversation_id INTEGER REFERENCES conversations(id) ON DELETE CASCADE,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    PRIMARY KEY (conversation_id, user_id)
);

CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    conversation_id INTEGER REFERENCES conversations(id) ON DELETE CASCADE,
    from_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    to_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    body TEXT NOT NULL,
    attachments TEXT[],
    messaging_provider_id TEXT,
    xillio_id TEXT,
    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);
        """
    )


def downgrade() -> None:
    op.execute(
        """
            DROP TABLE users CASCADE;
            DROP TABLE conversations CASCADE;
            DROP TABLE conversation_participants CASCADE;
            DROP TABLE messages CASCADE;
            """
    )
