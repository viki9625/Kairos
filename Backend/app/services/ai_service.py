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
        
        # Empathy prompt engineering for better responses
        self.system_prompt = """You are a compassionate mental wellness assistant for youth. Your role is to:

1. LISTEN with empathy and validate feelings
2. Respond in a warm, caring, and non-judgmental way
3. Use mix of English and Hindi naturally (code-switching like Indian youth)
4. Keep responses concise (2-3 sentences max)
5. Offer small, actionable steps when appropriate
6. Never give medical advice or diagnosis
7. If someone expresses self-harm intentions, acknowledge their pain and suggest professional help

Response style examples:
- "Main samajh raha hoon tum kya feel kar rahe ho. Kya tum aur share karna chahoge?"
- "That sounds really tough. You're brave for sharing this with me."
- "Kabhi kabhi aisa feel karna normal hai. Tumhari feelings valid hain."
- "It's okay to feel like this. Take a deep breath, you're not alone."

Be genuine, warm, and supportive. Avoid clinical language."""

        # Fallback responses for when API is unavailable
        self.fallback_responses = [
            "Main samajh raha hoon tum kya feel kar rahe ho. Kya tum aur share karna chahoge?",
            "That sounds tough. You're not alone in this journey.",
            "Kabhi kabhi aisa feel karna normal hai. Tumhari feelings valid hain.",
            "I hear you. Would you like to share more about what you're going through?",
            "It's okay to feel like this. Take a deep breath, you're not alone."
        ]

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
            
            # Try to parse JSON response
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
                # Fallback if JSON parsing fails
                return {"label": "neutral", "score": 0.5, "intensity": "moderate", "source": "fallback"}
                
        except Exception as e:
            print(f"⚠️ Emotion analysis error: {e}")
            return {"label": "neutral", "score": 0.5, "intensity": "moderate", "source": "error_fallback"}

    async def get_conversation_context(self, user_id: str, limit: int = 5) -> str:
        """Get recent conversation context for better responses"""
        try:
            from db.models import ChatMessage
            from utils.encryption import decrypt_text
            
            # Get recent messages
            docs = await (
                ChatMessage.find(ChatMessage.user_id == user_id)
                .sort(-ChatMessage.created_at)
                .limit(limit)
                .to_list()
            )
            
            if not docs:
                return ""
            
            context_parts = []
            for msg in reversed(docs[-3:]):  # Last 3 messages for context
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
            # Get conversation context
            context = ""
            if user_id:
                context = await self.get_conversation_context(user_id)
            
            # Build the prompt with context
            user_prompt = f"""Current user message: "{text}"

Recent conversation context:
{context if context else "No previous context"}

Please respond as a compassionate mental wellness assistant. Be empathetic, supportive, and offer hope. Mix English and Hindi naturally. Keep it conversational and warm (2-3 sentences max)."""

            # Call Groq API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=150,
                temperature=0.7,  # Balanced creativity
                top_p=0.9,
                frequency_penalty=0.1,
                presence_penalty=0.1
            )
            
            reply = response.choices[0].message.content.strip()
            
            # Basic validation and cleanup
            if not reply or len(reply.strip()) < 10:
                import random
                return random.choice(self.fallback_responses)
            
            # Remove any potential harmful content (basic filter)
            if any(word in reply.lower() for word in ['suicide', 'kill', 'die', 'hurt yourself']):
                return "I hear that you're going through a really tough time. Please consider reaching out to a counselor or trusted adult. You matter, and there are people who want to help."
            
            return reply
            
        except Exception as e:
            print(f"⚠️ Reply generation error: {e}")
            import random
            return random.choice(self.fallback_responses)

    async def get_wellness_suggestions(self, emotion: str, user_id: Optional[str] = None) -> List[str]:
        """Get personalized wellness suggestions based on emotion"""
        if not self.ready or not self.client:
            return [
                "Take a few deep breaths",
                "Write in a journal",
                "Talk to someone you trust",
                "Go for a short walk"
            ]

        try:
            suggestions_prompt = f"""Based on someone feeling {emotion}, suggest 3-4 simple, actionable wellness activities for a young person. Mix English and Hindi naturally.

Format as a simple list, one activity per line. Keep each suggestion short and practical.

Emotion: {emotion}"""

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": suggestions_prompt}],
                max_tokens=200,
                temperature=0.6
            )
            
            suggestions_text = response.choices[0].message.content.strip()
            suggestions = [s.strip() for s in suggestions_text.split('\n') if s.strip()]
            
            return suggestions[:4] if suggestions else [
                "Take deep breaths", 
                "Share with someone you trust",
                "Do something creative",
                "Step outside for fresh air"
            ]
            
        except Exception as e:
            print(f"⚠️ Suggestions generation error: {e}")
            return [
                "Take a few deep breaths",
                "Write in a journal", 
                "Talk to someone you trust",
                "Go for a short walk"
            ]


# Global instance
ai_service = AIService()
