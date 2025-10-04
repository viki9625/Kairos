from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException
from typing import List

# Import the new manager and services
from core.websocket_manager import manager
from services import chat_service
from db.models import ChatMessage # Your existing model

router = APIRouter(prefix="/api/chat", tags=["Chat"])

class ChatMessageResponse(ChatMessage):
    """A Pydantic model to control the response, ensuring content is a string."""
    content: str

# --- CORRECTED HISTORY ENDPOINT ---
@router.get("/history/{user_id}", response_model=List[ChatMessageResponse])
async def get_chat_history(user_id: str):
    """Gets the decrypted chat history for a specific user."""
    try:
        # Call the service function to get the decrypted history
        history = await chat_service.get_user_chat_history(user_id)
        return history
    except Exception as e:
        # Handle potential errors during history retrieval
        print(f"Error fetching history for user {user_id}: {e}")
        raise HTTPException(status_code=500, detail="Could not retrieve chat history.")


# --- CORRECTED WEBSOCKET ENDPOINT ---
@router.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    """Handles the real-time WebSocket connection for an authenticated user."""
    await manager.connect(websocket, user_id)
    try:
        while True:
            # Wait for a message from the client (e.g., {'message': 'Hello'})
            data = await websocket.receive_json()
            user_message = data.get("message")

            if user_message:
                # Use the service to process the message (save, get AI reply, broadcast)
                await chat_service.process_user_message(user_id, user_message)

    except WebSocketDisconnect:
        # If the user disconnects, remove their connection from the manager
        manager.disconnect(user_id)
        print(f"User {user_id} disconnected.")
    except Exception as e:
        # Handle any other errors that might occur
        print(f"An error occurred in the websocket for user {user_id}: {e}")
        manager.disconnect(user_id)

