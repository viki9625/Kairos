from db.models import ChatMessage
from .ai_service import ai_service
from core.websocket_manager import manager
from utils.encryption import encrypt_text, decrypt_text
from typing import List

async def get_user_chat_history(user_id: str) -> List[ChatMessage]:
    """
    Retrieves and decrypts all chat messages for a given user,
    sorted by creation time.
    """
    try:
        docs = await ChatMessage.find(
            {"user_id": user_id}
        ).sort(+ChatMessage.created_at).to_list()
        
        for doc in docs:
            try:
                doc.content = decrypt_text(doc.content)
            except Exception:
                doc.content = "[message unreadable]"
        return docs
    except Exception as e:
        print(f"--- DATABASE ERROR in get_user_chat_history: {e} ---")
        return []

async def process_user_message(user_id: str, user_message: str):
    """
    Saves the user's message, gets an AI response, saves the AI response,
    and then broadcasts the AI's reply back to the user via WebSocket.
    """
    try:
        # 1. Save the user's message to the database
        user_msg_doc = ChatMessage(
            user_id=user_id,
            role="user",
            content=encrypt_text(user_message)
        )
        await user_msg_doc.insert()

        # 2. Get the AI's reply
        ai_reply_content = await ai_service.generate_empathic_reply(user_message, user_id=user_id)

        # 3. Save the AI's reply to the database
        ai_msg_doc = ChatMessage(
            user_id=user_id,
            role="bot",
            content=encrypt_text(ai_reply_content)
        )
        await ai_msg_doc.insert()

        # 4. Send the AI's reply back to the user via WebSocket
        await manager.send_personal_message(
            {
                "role": "bot",
                "content": ai_reply_content,
            },
            user_id
        )
    except Exception as e:
        print(f"--- ERROR in process_user_message: {e} ---")
        # Send an error message back to the user if something goes wrong
        await manager.send_personal_message(
            {"role": "bot", "content": "I'm sorry, an error occurred while processing your message."},
            user_id
        )

