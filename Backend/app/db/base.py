import motor.motor_asyncio
from beanie import init_beanie
from db.models import User, ChatMessage, ConversationState   # ✅ include ConversationState
from core.config import settings


client = motor.motor_asyncio.AsyncIOMotorClient(settings.mongodb_url)
database = client[settings.mongodb_db]


async def init_db():
    await init_beanie(
        database=database,
        document_models=[User, ChatMessage, ConversationState]  # ✅ register all models
    )
