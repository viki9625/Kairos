import motor.motor_asyncio
from beanie import init_beanie
from core.config import settings
from db.models import User, ChatMessage, ConversationState # Import all your models

async def init_db():
    """
    Initializes the Beanie ODM with the MongoDB client and registers all Document models.
    This function should be called on application startup.
    """
    print("Attempting to connect to the database...")
    
    # Create the MongoDB client
    client = motor.motor_asyncio.AsyncIOMotorClient(settings.mongodb_url)
    
    # Get the database object
    database = client[settings.mongodb_db]

    # Initialize beanie with the database and all your models
    await init_beanie(
        database=database,
        document_models=[
            User,
            ChatMessage,
            ConversationState
        ]
    )
    print("✅ Database initialized successfully.")
