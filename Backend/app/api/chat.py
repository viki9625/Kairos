from fastapi import APIRouter, BackgroundTasks, Depends, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
from typing import List, Optional
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
    suggestions: List[str] = []


@router.post("/message", response_model=ChatResp)
async def post_message(
    payload: ChatReq,
    background_tasks: BackgroundTasks,
    user=Depends(get_current_user)
):
    text = payload.message
    
    # Analyze emotion using Groq
    analysis = ai_service.analyze_emotion(text)
    
    # Check for crisis keywords
    crisis = await check_crisis(text)

    if crisis:
        background_tasks.add_task(
            lambda uid: print(f"🚨 CRISIS ESCALATION for user {uid}"), 
            str(user.id)
        )
        reply = (
            "I'm really sorry you're feeling this way. "
            "Your feelings matter, and you don't have to go through this alone. "
            "Please consider reaching out to a crisis helpline or a trusted adult immediately. "
            "You are valuable and there are people who want to help."
        )
        await ChatMessage(
            user_id=str(user.id),
            role="bot",
            content=encrypt_text(reply),
            metadata={"crisis": True, "analysis": analysis}
        ).insert()
        return {
            "reply": reply, 
            "crisis": True, 
            "analysis": analysis,
            "suggestions": [
                "Call a crisis helpline immediately",
                "Reach out to a trusted adult",
                "Go to your nearest emergency room",
                "Text a crisis support number"
            ]
        }

    # Save user message before generating reply
    await ChatMessage(
        user_id=str(user.id),
        role="user",
        content=encrypt_text(text),
        metadata={"analysis": analysis}
    ).insert()

    # Generate empathic reply using Groq
    reply = await ai_service.generate_empathic_reply(text, user_id=str(user.id))

    # Get wellness suggestions based on detected emotion
    suggestions = await ai_service.get_wellness_suggestions(
        analysis.get("label", "neutral"), 
        user_id=str(user.id)
    )

    # Save bot reply
    await ChatMessage(
        user_id=str(user.id),
        role="bot",
        content=encrypt_text(reply),
        metadata={"analysis": analysis, "suggestions": suggestions}
    ).insert()

    return {
        "reply": reply, 
        "crisis": False, 
        "analysis": analysis,
        "suggestions": suggestions
    }


@router.get("/history", response_model=List[dict])
async def get_history(limit: int = 50, user=Depends(get_current_user)):
    """Fetch conversation history with enhanced metadata"""
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
        
        message_data = {
            "id": str(d.id),
            "role": d.role,
            "content": content,
            "created_at": d.created_at,
            "metadata": d.metadata or {}
        }
        out.append(message_data)
    return out


@router.get("/wellness-suggestions")
async def get_wellness_suggestions(
    emotion: str = "neutral",
    user=Depends(get_current_user)
):
    """Get personalized wellness suggestions"""
    suggestions = await ai_service.get_wellness_suggestions(emotion, str(user.id))
    return {"emotion": emotion, "suggestions": suggestions}


@router.get("/emotion-analysis")
async def analyze_text_emotion(
    text: str,
    user=Depends(get_current_user)
):
    """Analyze emotion of any text"""
    analysis = ai_service.analyze_emotion(text)
    return {"text": text, "analysis": analysis}


# Enhanced WebSocket manager for real-time chat
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

    async def send_json_message(self, data: dict, websocket: WebSocket):
        await websocket.send_json(data)


manager = ConnectionManager()


@router.websocket('/ws')
async def websocket_endpoint(websocket: WebSocket):
    """Enhanced WebSocket with emotion analysis and suggestions"""
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            
            # Analyze emotion
            analysis = ai_service.analyze_emotion(data)
            
            # Check for crisis
            crisis = await check_crisis(data)
            if crisis:
                await manager.send_json_message({
                    "type": "crisis_alert",
                    "message": "I'm concerned about you. Please reach out to a crisis helpline or trusted adult immediately.",
                    "crisis": True,
                    "analysis": analysis
                }, websocket)
                continue
            
            # Generate empathic reply
            reply = await ai_service.generate_empathic_reply(data)
            
            # Get suggestions
            suggestions = await ai_service.get_wellness_suggestions(analysis.get("label", "neutral"))
            
            # Send comprehensive response
            await manager.send_json_message({
                "type": "bot_reply",
                "message": reply,
                "crisis": False,
                "analysis": analysis,
                "suggestions": suggestions
            }, websocket)
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)
