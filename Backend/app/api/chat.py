from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException
from typing import List
from pydantic import BaseModel

from core.websocket_manager import manager
from services import chat_service
from db.models import ChatMessage

router = APIRouter(prefix="/api/chat", tags=["Chat"])

class ChatMessageResponse(BaseModel):
    """A Pydantic model to define the shape of a chat message response."""
    role: str
    content: str

# --- REVERTED: A single endpoint to get all messages for a user ---
@router.get("/history/{user_id}", response_model=List[ChatMessageResponse])
async def get_chat_history(user_id: str):
    """Gets the decrypted chat history for a specific user."""
    try:
        # Call the simplified service function
        messages = await chat_service.get_user_chat_history(user_id)
        # Convert the database objects to the response model format
        return [{"role": msg.role, "content": msg.content} for msg in messages]
    except Exception as e:
        print(f"Error fetching history for user {user_id}: {e}")
        raise HTTPException(status_code=500, detail="Could not retrieve chat history.")


# --- REVERTED: A simplified WebSocket endpoint ---
@router.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    """Handles the real-time WebSocket connection for a user."""
    await manager.connect(websocket, user_id)
    try:
        while True:
            # It now only expects a simple message, not a conversation_id
            data = await websocket.receive_json()
            user_message = data.get("message")

            if user_message:
                # Call the simplified service function
                await chat_service.process_user_message(user_id, user_message)

    except WebSocketDisconnect:
        manager.disconnect(user_id)
    except Exception as e:
        print(f"Error in websocket for user {user_id}: {e}")
        manager.disconnect(user_id)

