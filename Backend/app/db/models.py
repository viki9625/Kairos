from beanie import Document
from datetime import datetime
from typing import Optional, Dict

class User(Document):
    # This model remains the same, with all user fields
    username: Optional[str]
    is_anonymous: bool = True
    hashed_password: Optional[str] = None
    email: Optional[str] = None
    google_id: Optional[str] = None
    provider: str = "local"
    profile_picture_url: Optional[str] = None
    created_at: datetime = datetime.utcnow()

    class Settings:
        name = "users"

# --- REVERTED: ChatMessage Model ---
# We have removed the 'conversation_id' field.
# All messages are now only linked to a user.
class ChatMessage(Document):
    user_id: str
    role: str = "user"  # "user" or "bot"
    content: str # This content is encrypted
    metadata: Optional[Dict] = None
    created_at: datetime = datetime.utcnow()

    class Settings:
        name = "chat_messages"

# --- Unchanged: ConversationState Model ---
class ConversationState(Document):
    user_id: str
    last_intent: Optional[str] = None
    step_stage: Optional[str] = None
    updated_at: datetime = datetime.utcnow()

    class Settings:
        name = "conversation_state"

