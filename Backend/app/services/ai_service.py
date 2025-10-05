import asyncio
from typing import Optional, Dict, Any, List
from groq import Groq
from core.config import settings


class AIService:
    def __init__(self):
        """Initialize Groq client and empathy prompts"""
        try:
            self.client = Groq(api_key=settings.groq_api_key)
            self.model = settings.groq_model
            self.ready = True
            print("✅ Groq AI service initialized successfully")
        except Exception as e:
            print(f"❌ Failed to initialize Groq AI service: {e}")
            self.client = None
            self.ready = False
        
        # System prompt for empathic replies
        self.system_prompt = """You are a compassionate mental wellness assistant for youth. Your role is to:
1. LISTEN with empathy and validate feelings
2. Respond in a warm, caring, and non-judgmental way
3. Use mix of English and Hindi naturally (code-switching like Indian youth)
4. Keep responses concise (2-3 sentences max)
5. Offer small, actionable steps when appropriate
6. Never give medical advice or diagnosis
7. If someone expresses self-harm intentions, acknowledge their pain and suggest professional help
Be genuine, warm, and supportive. Avoid clinical language."""

        # Fallback responses for when the API is unavailable
        self.fallback_responses = [
            "Main samajh raha hoon tum kya feel kar rahe ho. Kya tum aur share karna chahoge?",
            "That sounds tough. You're not alone in this journey.",
            "I hear you. Would you like to share more about what you're going through?",
        ]

    # --- THIS IS THE NEW FUNCTION ---
    async def generate_title_for_text(self, text: str) -> str:
        """Generates a short, concise title (3-5 words) for a given text."""
        if not self.ready or not self.client:
            return "New Conversation"

        try:
            # A specific prompt to ask the AI for a short title
            prompt = f'Generate a very short, concise title (3-5 words max) for the following conversation starter. Respond with only the title and nothing else.\n\nMessage: "{text}"'
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=20,
                temperature=0.3
            )
            
            # Clean up the response to get just the title
            title = response.choices[0].message.content.strip().replace('"', '')
            return title if title else "New Conversation"
        except Exception as e:
            print(f"⚠️ Title generation error: {e}")
            return "New Conversation" # Return a default title on error
    
    def analyze_emotion(self, text: str) -> Dict[str, Any]:
        """Analyze emotion using Groq API with prompt engineering"""
        if not self.ready or not self.client:
            return {"label": "neutral", "score": 0.5, "source": "fallback"}
        
        try:
            emotion_prompt = f"""Analyze the emotional tone of this message and respond with ONLY a JSON object in this exact format:
{{"label": "emotion_name", "score": 0.8, "intensity": "mild/moderate/high"}}

Valid emotions: joy, sadness, anger, fear, surprise, disgust, anxiety, excitement, neutral

Message to analyze: "{text}"

Respond with only the JSON object, no other text."""

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": emotion_prompt}],
                max_tokens=100,
                temperature=0.1
            )
            
            result_text = response.choices[0].message.content.strip()
            
            import json
            try:
                emotion_data = json.loads(result_text)
                return {
                    "label": emotion_data.get("label", "neutral"),
                    "score": float(emotion_data.get("score", 0.5)),
                    "intensity": emotion_data.get("intensity", "moderate"),
                    "source": "groq"
                }
            except json.JSONDecodeError:
                return {"label": "neutral", "score": 0.5, "intensity": "moderate", "source": "fallback"}
                
        except Exception as e:
            print(f"⚠️ Emotion analysis error: {e}")
            return {"label": "neutral", "score": 0.5, "intensity": "moderate", "source": "error_fallback"}

    async def get_conversation_context(self, user_id: str, limit: int = 5) -> str:
        """Get recent conversation context for better responses"""
        try:
            from db.models import ChatMessage
            from utils.encryption import decrypt_text
            
            docs = await (
                ChatMessage.find({"user_id": user_id})
                .sort(-ChatMessage.created_at)
                .limit(limit)
                .to_list()
            )
            
            if not docs:
                return ""
            
            context_parts = []
            for msg in reversed(docs[-3:]):
                try:
                    content = decrypt_text(msg.content)
                    role = "User" if msg.role == "user" else "Assistant"
                    context_parts.append(f"{role}: {content}")
                except Exception:
                    continue
            
            return "\n".join(context_parts) if context_parts else ""
            
        except Exception as e:
            print(f"⚠️ Context retrieval error: {e}")
            return ""

    async def generate_empathic_reply(self, text: str, user_id: Optional[str] = None) -> str:
        """Generate empathic reply using Groq API with conversation context"""
        if not self.ready or not self.client:
            import random
            return random.choice(self.fallback_responses)

        try:
            context = ""
            if user_id:
                context = await self.get_conversation_context(user_id)
            
            user_prompt = f"""Current user message: "{text}"

Recent conversation context:
{context if context else "No previous context"}

Please respond as a compassionate mental wellness assistant. Be empathetic, supportive, and offer hope. Mix English and Hindi naturally. Keep it conversational and warm (2-3 sentences max)."""

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=150,
                temperature=0.7,
            )
            
            reply = response.choices[0].message.content.strip()
            
            if not reply or len(reply.strip()) < 5:
                import random
                return random.choice(self.fallback_responses)
            
            return reply
            
        except Exception as e:
            print(f"⚠️ Reply generation error: {e}")
            import random
            return random.choice(self.fallback_responses)

    async def get_wellness_suggestions(self, emotion: str, user_id: Optional[str] = None) -> List[str]:
        """Get personalized wellness suggestions based on emotion"""
        # (This function remains the same, no changes needed)
        if not self.ready or not self.client:
            return [
                "Take a few deep breaths",
                "Write in a journal",
                "Talk to someone you trust",
            ]

        try:
            suggestions_prompt = f"""Based on someone feeling {emotion}, suggest 3 simple, actionable wellness activities for a young person. Mix English and Hindi naturally.

Format as a simple list, one activity per line. Keep each suggestion short and practical.

Emotion: {emotion}"""

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": suggestions_prompt}],
                max_tokens=200,
                temperature=0.6
            )
            
            suggestions_text = response.choices[0].message.content.strip()
            suggestions = [s.strip().lstrip('- ') for s in suggestions_text.split('\n') if s.strip()]
            
            return suggestions[:4] if suggestions else ["Take deep breaths", "Share with someone you trust"]
            
        except Exception as e:
            print(f"⚠️ Suggestions generation error: {e}")
            return ["Take a few deep breaths", "Write in a journal"]

# Global instance
ai_service = AIService()

