from fastapi import APIRouter, Depends, HTTPException
from api.deps import get_moderator
from db.models import ChatMessage


router = APIRouter(prefix="/api/admin", tags=["admin"])


@router.get("/flagged")
async def list_flagged(moderator = Depends(get_moderator)):
    docs = await ChatMessage.find(ChatMessage.flagged == True).sort(-ChatMessage.created_at).to_list()
    out = []
    for d in docs:
        out.append({"id": str(d.id), "user_id": d.user_id, "role": d.role, "flagged_reason": d.flagged_reason, "created_at": d.created_at})
    return out


@router.post("/flag/{message_id}")
async def flag_message(message_id: str, reason: str, moderator = Depends(get_moderator)):
    msg = await ChatMessage.get(message_id)
    if not msg:
        raise HTTPException(status_code=404, detail="Message not found")
    msg.flagged = True
    msg.flagged_reason = reason
    await msg.save()
    return {"ok": True}