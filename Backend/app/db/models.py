from beanie import Document
from datetime import datetime
from typing import Optional, Dict

class User(Document):
    # --- Existing Fields ---
    username: Optional[str]
    is_anonymous: bool = True
    hashed_password: Optional[str] = None
    
    # --- New Fields for Google OAuth ---
    email: Optional[str] = None
    google_id: Optional[str] = None
    provider: str = "local"  # "local" or "google"
    
    # --- Timestamp ---
    created_at: datetime = datetime.utcnow()

    class Settings:
        name = "users"


class ChatMessage(Document):
    user_id: str
    role: str = "user"  # "user" | "bot" | "counselor"
    content: str
    metadata: Optional[Dict] = None
    created_at: datetime = datetime.utcnow()

    class Settings:
        name = "chat_messages"


class ConversationState(Document):
    """
    Tracks where the user is in the conversation so the bot remembers
    beyond just message history.
    """
    user_id: str
    last_intent: Optional[str] = None  # e.g., "asked_for_steps", "neutral", "crisis"
    step_stage: Optional[str] = None   # e.g., "offered", "confirmed", "completed"
    updated_at: datetime = datetime.utcnow()

    class Settings:
        name = "conversation_state"
