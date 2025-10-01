from fastapi import APIRouter, BackgroundTasks, Depends, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
from typing import List
from services.ai_service import ai_service
from services.escalation import check_crisis
from db.models import ChatMessage
from utils.encryption import encrypt_text, decrypt_text
from api.deps import get_current_user


router = APIRouter(prefix="/api/chat", tags=["chat"])


class ChatReq(BaseModel):
    message: str


class ChatResp(BaseModel):
    reply: str
    crisis: bool = False
    analysis: dict | None = None


@router.post("/message", response_model=ChatResp)
async def post_message(
    payload: ChatReq,
    background_tasks: BackgroundTasks,
    user=Depends(get_current_user)
):
    text = payload.message
    analysis = ai_service.analyze_emotion(text)
    crisis = await check_crisis(text)

    if crisis:
        background_tasks.add_task(lambda uid: print(f"Escalation for user {uid}"), str(user.id))
        reply = (
            "I'm really sorry you're feeling this way. "
            "If you're in immediate danger please contact local emergency services or a crisis hotline."
        )
        await ChatMessage(
            user_id=str(user.id),
            role="bot",
            content=encrypt_text(reply),
            metadata={"crisis": True}
        ).insert()
        return {"reply": reply, "crisis": True, "analysis": analysis}

    # ✅ save user message before reply generation
    await ChatMessage(
        user_id=str(user.id),
        role="user",
        content=encrypt_text(text)
    ).insert()

    # ✅ now generate reply with up-to-date history
    reply = await ai_service.generate_empathic_reply(text, user_id=str(user.id))

    await ChatMessage(
        user_id=str(user.id),
        role="bot",
        content=encrypt_text(reply)
    ).insert()

    return {"reply": reply, "crisis": False, "analysis": analysis}

# Fetch conversation (last N messages)
@router.get("/history", response_model=List[dict])
async def get_history(limit: int = 50, user=Depends(get_current_user)):
    docs = await (
        ChatMessage.find(ChatMessage.user_id == str(user.id))
        .sort(-ChatMessage.created_at)
        .limit(limit)
        .to_list()
    )
    out = []
    for d in reversed(docs):
        try:
            content = decrypt_text(d.content)
        except Exception:
            content = "[stored content encrypted or corrupted]"
        out.append({
            "id": str(d.id),
            "role": d.role,
            "content": content,
            "created_at": d.created_at
        })
    return out


# Minimal Websocket manager for real-time chat (echo + AI reply)
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)


manager = ConnectionManager()


@router.websocket('/ws')
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            crisis = await check_crisis(data)
            if crisis:
                await manager.send_personal_message(
                    "[CRISIS] Please contact local emergency services or a crisis hotline.",
                    websocket
                )
                continue
            # ✅ Await the coroutine here
            reply = await ai_service.generate_empathic_reply(data)
            await manager.send_personal_message(reply, websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
