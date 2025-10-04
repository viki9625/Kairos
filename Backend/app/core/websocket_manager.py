from fastapi import WebSocket
from typing import Dict

class ConnectionManager:
    def __init__(self):
        # A dictionary to store active connections, mapping user_id to WebSocket
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, user_id: str):
        """Accepts a new WebSocket connection and associates it with a user_id."""
        await websocket.accept()
        self.active_connections[user_id] = websocket

    def disconnect(self, user_id: str):
        """Closes and removes a WebSocket connection for a given user_id."""
        if user_id in self.active_connections:
            # Although the connection might be closed already, we remove it from our dict
            del self.active_connections[user_id]

    async def send_personal_message(self, message: dict, user_id: str):
        """Sends a JSON message to a specific user's WebSocket."""
        if user_id in self.active_connections:
            websocket = self.active_connections[user_id]
            await websocket.send_json(message)

# Create a single global instance of the manager
manager = ConnectionManager()

