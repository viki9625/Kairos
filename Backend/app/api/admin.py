from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from api.deps import get_moderator
from db.models import ChatMessage, User
from utils.encryption import decrypt_text
from services.ai_service import ai_service
from datetime import datetime, timedelta


router = APIRouter(prefix="/api/admin", tags=["admin"])


@router.get("/dashboard")
async def admin_dashboard(moderator = Depends(get_moderator)):
    """Get admin dashboard overview"""
    try:
        # Count total messages in last 24 hours
        yesterday = datetime.utcnow() - timedelta(days=1)
        recent_messages = await ChatMessage.find(
            ChatMessage.created_at >= yesterday
        ).count()
        
        # Count total users
        total_users = await User.find().count()
        
        # Count flagged messages
        flagged_count = await ChatMessage.find(
            ChatMessage.metadata != None
        ).count()
        
        # Get emotional trends
        emotions_sample = await ChatMessage.find(
            ChatMessage.metadata != None,
            ChatMessage.created_at >= yesterday
        ).limit(100).to_list()
        
        emotion_counts = {}
        for msg in emotions_sample:
            if msg.metadata and 'analysis' in msg.metadata:
                emotion = msg.metadata['analysis'].get('label', 'neutral')
                emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
        
        return {
            "total_users": total_users,
            "messages_24h": recent_messages,
            "flagged_messages": flagged_count,
            "emotion_trends": emotion_counts,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Dashboard error: {str(e)}")


@router.get("/messages")
async def list_messages(
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    filter_emotion: Optional[str] = Query(None),
    filter_crisis: Optional[bool] = Query(None),
    moderator = Depends(get_moderator)
):
    """List messages with filtering options"""
    try:
        # Build query
        query_conditions = []
        
        if filter_crisis is not None:
            if filter_crisis:
                query_conditions.append({"metadata.crisis": True})
            else:
                query_conditions.append({"metadata.crisis": {"$ne": True}})
        
        if filter_emotion:
            query_conditions.append({"metadata.analysis.label": filter_emotion})
        
        # Get messages
        if query_conditions:
            docs = await ChatMessage.find(
                {"$and": query_conditions}
            ).sort(-ChatMessage.created_at).skip(offset).limit(limit).to_list()
        else:
            docs = await ChatMessage.find().sort(
                -ChatMessage.created_at
            ).skip(offset).limit(limit).to_list()
        
        messages = []
        for msg in docs:
            try:
                content = decrypt_text(msg.content)
            except Exception:
                content = "[encrypted content]"
            
            messages.append({
                "id": str(msg.id),
                "user_id": msg.user_id,
                "role": msg.role,
                "content": content,
                "metadata": msg.metadata or {},
                "created_at": msg.created_at
            })
        
        return {
            "messages": messages,
            "total_returned": len(messages),
            "offset": offset,
            "limit": limit
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Messages retrieval error: {str(e)}")


@router.get("/flagged")
async def list_flagged(moderator = Depends(get_moderator)):
    """List flagged or crisis messages"""
    try:
        docs = await ChatMessage.find(
            {"$or": [
                {"metadata.crisis": True},
                {"metadata.flagged": True}
            ]}
        ).sort(-ChatMessage.created_at).to_list()
        
        flagged_messages = []
        for msg in docs:
            try:
                content = decrypt_text(msg.content)
            except Exception:
                content = "[encrypted content]"
            
            flagged_messages.append({
                "id": str(msg.id),
                "user_id": msg.user_id,
                "role": msg.role,
                "content": content,
                "crisis": msg.metadata.get("crisis", False) if msg.metadata else False,
                "flagged_reason": msg.metadata.get("flagged_reason") if msg.metadata else None,
                "created_at": msg.created_at
            })
        
        return flagged_messages
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Flagged messages error: {str(e)}")


@router.post("/flag/{message_id}")
async def flag_message(
    message_id: str, 
    reason: str, 
    moderator = Depends(get_moderator)
):
    """Flag a message for review"""
    try:
        msg = await ChatMessage.get(message_id)
        if not msg:
            raise HTTPException(status_code=404, detail="Message not found")
        
        # Update metadata
        if not msg.metadata:
            msg.metadata = {}
        
        msg.metadata["flagged"] = True
        msg.metadata["flagged_reason"] = reason
        msg.metadata["flagged_by"] = str(moderator.id)
        msg.metadata["flagged_at"] = datetime.utcnow().isoformat()
        
        await msg.save()
        
        return {"success": True, "message": "Message flagged successfully"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Flag message error: {str(e)}")


@router.post("/analyze-conversation/{user_id}")
async def analyze_user_conversation(
    user_id: str,
    moderator = Depends(get_moderator)
):
    """Analyze a user's conversation for insights"""
    try:
        # Get user's messages
        messages = await ChatMessage.find(
            ChatMessage.user_id == user_id
        ).sort(ChatMessage.created_at).limit(50).to_list()
        
        if not messages:
            raise HTTPException(status_code=404, detail="No messages found for user")
        
        # Decrypt and analyze
        conversation_text = []
        emotions_found = []
        crisis_indicators = []
        
        for msg in messages:
            try:
                content = decrypt_text(msg.content)
                conversation_text.append(f"{msg.role}: {content}")
                
                if msg.metadata:
                    if msg.metadata.get("crisis"):
                        crisis_indicators.append({
                            "message": content,
                            "timestamp": msg.created_at.isoformat()
                        })
                    
                    if "analysis" in msg.metadata:
                        emotion = msg.metadata["analysis"].get("label")
                        if emotion:
                            emotions_found.append(emotion)
            except Exception:
                continue
        
        # Generate summary using AI service
        conversation_summary = "\n".join(conversation_text[-10:])  # Last 10 messages
        
        # Use Groq to analyze patterns
        analysis_result = ai_service.analyze_emotion(conversation_summary)
        
        # Count emotions
        emotion_counts = {}
        for emotion in emotions_found:
            emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
        
        return {
            "user_id": user_id,
            "total_messages": len(messages),
            "emotion_distribution": emotion_counts,
            "crisis_indicators": crisis_indicators,
            "overall_sentiment": analysis_result,
            "requires_attention": len(crisis_indicators) > 0 or analysis_result.get("label") in ["sadness", "fear", "anger"],
            "analysis_timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Conversation analysis error: {str(e)}")


@router.get("/emotions-report")
async def emotions_report(
    days: int = Query(7, ge=1, le=30),
    moderator = Depends(get_moderator)
):
    """Generate emotions report for specified period"""
    try:
        start_date = datetime.utcnow() - timedelta(days=days)
        
        # Get messages with emotion analysis
        messages = await ChatMessage.find(
            ChatMessage.created_at >= start_date,
            ChatMessage.metadata != None
        ).to_list()
        
        # Aggregate emotions by day
        daily_emotions = {}
        emotion_totals = {}
        
        for msg in messages:
            if not msg.metadata or "analysis" not in msg.metadata:
                continue
            
            emotion = msg.metadata["analysis"].get("label", "neutral")
            day_key = msg.created_at.date().isoformat()
            
            # Daily breakdown
            if day_key not in daily_emotions:
                daily_emotions[day_key] = {}
            daily_emotions[day_key][emotion] = daily_emotions[day_key].get(emotion, 0) + 1
            
            # Overall totals
            emotion_totals[emotion] = emotion_totals.get(emotion, 0) + 1
        
        return {
            "period_days": days,
            "start_date": start_date.isoformat(),
            "end_date": datetime.utcnow().isoformat(),
            "daily_breakdown": daily_emotions,
            "emotion_totals": emotion_totals,
            "total_analyzed_messages": len(messages)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Emotions report error: {str(e)}")


@router.post("/wellness-insights")
async def generate_wellness_insights(moderator = Depends(get_moderator)):
    """Generate wellness insights and recommendations"""
    try:
        # Get recent data for analysis
        recent_date = datetime.utcnow() - timedelta(days=7)
        
        messages = await ChatMessage.find(
            ChatMessage.created_at >= recent_date,
            ChatMessage.metadata != None
        ).limit(200).to_list()
        
        # Analyze patterns
        negative_emotions = ["sadness", "anger", "fear", "anxiety"]
        positive_emotions = ["joy", "excitement"]
        
        negative_count = 0
        positive_count = 0
        crisis_count = 0
        common_themes = {}
        
        for msg in messages:
            if not msg.metadata:
                continue
            
            # Count crisis indicators
            if msg.metadata.get("crisis"):
                crisis_count += 1
            
            # Count emotions
            if "analysis" in msg.metadata:
                emotion = msg.metadata["analysis"].get("label", "neutral")
                if emotion in negative_emotions:
                    negative_count += 1
                elif emotion in positive_emotions:
                    positive_count += 1
        
        # Generate recommendations based on patterns
        recommendations = []
        
        if crisis_count > 0:
            recommendations.append({
                "priority": "high",
                "type": "crisis_support",
                "message": f"{crisis_count} crisis indicators detected. Review crisis response protocols.",
                "action": "immediate_review"
            })
        
        if negative_count > positive_count * 2:
            recommendations.append({
                "priority": "medium",
                "type": "emotional_support",
                "message": "High proportion of negative emotions detected. Consider enhanced support resources.",
                "action": "resource_enhancement"
            })
        
        recommendations.append({
            "priority": "low",
            "type": "general",
            "message": "Continue monitoring emotional trends and user engagement patterns.",
            "action": "routine_monitoring"
        })
        
        return {
            "analysis_period": "7 days",
            "messages_analyzed": len(messages),
            "emotional_breakdown": {
                "negative_emotions": negative_count,
                "positive_emotions": positive_count,
                "crisis_indicators": crisis_count
            },
            "recommendations": recommendations,
            "generated_at": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Wellness insights error: {str(e)}")


@router.get("/users")
async def list_users(
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    moderator = Depends(get_moderator)
):
    """List users with basic stats"""
    try:
        users = await User.find().skip(offset).limit(limit).to_list()
        
        user_stats = []
        for user in users:
            # Get message count for each user
            message_count = await ChatMessage.find(
                ChatMessage.user_id == str(user.id)
            ).count()
            
            # Get last activity
            last_message = await ChatMessage.find(
                ChatMessage.user_id == str(user.id)
            ).sort(-ChatMessage.created_at).limit(1).to_list()
            
            last_activity = last_message[0].created_at if last_message else None
            
            user_stats.append({
                "id": str(user.id),
                "username": user.username,
                "is_anonymous": user.is_anonymous,
                "created_at": user.created_at,
                "message_count": message_count,
                "last_activity": last_activity
            })
        
        return {
            "users": user_stats,
            "total_returned": len(user_stats),
            "offset": offset,
            "limit": limit
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Users list error: {str(e)}")