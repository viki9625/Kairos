from db.models import ChatMessage
from .ai_service import ai_service # Your existing AI service
from core.websocket_manager import manager
from utils.encryption import encrypt_text, decrypt_text

async def get_user_chat_history(user_id: str):
    """Retrieves and decrypts all chat messages for a given user."""
    docs = await ChatMessage.find(ChatMessage.user_id == user_id).sort(+ChatMessage.created_at).to_list()
    
    decrypted_history = []
    for doc in docs:
        try:
            # We are assuming the 'content' field exists on the ChatMessage model
            # and is the field that needs decryption.
            decrypted_content = decrypt_text(doc.content)
            # Create a new object or modify a copy to avoid altering the original DB model instance directly
            # in a way that might be confusing. For Beanie, direct modification is often fine.
            doc.content = decrypted_content
            decrypted_history.append(doc)
        except Exception as e:
            # Handle cases where decryption might fail for a specific message
            print(f"Could not decrypt message {doc.id} for user {user_id}: {e}")
            doc.content = "[message content unreadable]"
            decrypted_history.append(doc)
            
    return decrypted_history

async def process_user_message(user_id: str, user_message: str):
    """
    Saves the user's message, gets an AI response, saves the AI response, 
    and then broadcasts the AI's reply back to the user via WebSocket.
    """
    # 1. Save the user's message to the database, encrypting the content
    user_msg_doc = ChatMessage(
        user_id=user_id, 
        role="user", 
        content=encrypt_text(user_message)
    )
    await user_msg_doc.insert()

    # 2. Get the AI's reply using your existing ai_service
    # The generate_empathic_reply method is well-suited for this.
    ai_reply_content = await ai_service.generate_empathic_reply(user_message, user_id=user_id)

    # 3. Save the AI's reply to the database, encrypting the content
    ai_msg_doc = ChatMessage(
        user_id=user_id, 
        role="bot", 
        content=encrypt_text(ai_reply_content)
    )
    await ai_msg_doc.insert()

    # 4. Send the AI's (unencrypted) reply back to the specific user via WebSocket.
    # The frontend expects a JSON object with 'role' and 'content' keys.
    await manager.send_personal_message(
        {"role": "bot", "content": ai_reply_content},
        user_id
    )

