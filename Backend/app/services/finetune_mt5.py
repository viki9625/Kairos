# app/services/groq_empathy_service.py
"""
Enhanced Groq-based empathy service with advanced prompt engineering
This replaces the local MT5 training approach with cloud-based Groq API
"""

import asyncio
import json
import logging
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from groq import Groq
from core.config import settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GroqEmpathyService:
    """
    Advanced empathy service using Groq API with sophisticated prompt engineering
    Designed to provide contextually aware, culturally sensitive responses
    """
    
    def __init__(self):
        """Initialize Groq client and empathy framework"""
        try:
            self.client = Groq(api_key=settings.groq_api_key)
            self.model = settings.groq_model
            self.ready = True
            logger.info("✅ Groq Empathy Service initialized successfully")
        except Exception as e:
            logger.error(f"❌ Failed to initialize Groq service: {e}")
            self.client = None
            self.ready = False
        
        # Advanced empathy framework
        self.empathy_framework = {
            "core_principles": [
                "Listen with genuine care and presence",
                "Validate emotions without judgment", 
                "Offer hope and practical support",
                "Respect cultural and linguistic diversity",
                "Encourage connection with support systems"
            ],
            
            "response_styles": {
                "validation": [
                    "Tumhari feelings bilkul valid hain",
                    "I hear you, and what you're feeling makes complete sense",
                    "Main samajh raha hoon ye kitna mushkil hai",
                    "Your emotions are important and deserve attention"
                ],
                
                "empathy": [
                    "That sounds really challenging",
                    "Main feel kar sakta hoon ye tumhare liye kitna tough hai",
                    "I can imagine how overwhelming this must be",
                    "Ye sach mein difficult situation lag rahi hai"
                ],
                
                "support": [
                    "You don't have to go through this alone",
                    "Tum akele nahi ho, main yahaan hoon",
                    "There are people who care about you",
                    "Support lena strength ki nishani hai, weakness nahi"
                ],
                
                "encouragement": [
                    "You're stronger than you know",
                    "Tumne ye share kiya hai, that takes courage",
                    "Small steps can lead to big changes",
                    "Recovery aur healing possible hai, time lagta hai bas"
                ]
            }
        }

        # Cultural context for Indian youth
        self.cultural_context = """
        Indian youth context:
        - Academic and family pressure is common
        - Code-switching between English and Hindi is natural
        - Extended family and social expectations matter
        - Mental health stigma needs to be addressed gently
        - Practical, achievable suggestions work best
        - Respect for family while encouraging individual wellbeing
        """

    async def generate_contextual_empathy_response(
        self, 
        user_message: str, 
        conversation_history: Optional[List[Dict]] = None,
        user_profile: Optional[Dict] = None
    ) -> Dict:
        """
        Generate contextually aware empathic response using advanced prompt engineering
        """
        if not self.ready:
            return self._get_fallback_response(user_message)

        try:
            # Build sophisticated prompt
            prompt = self._build_empathy_prompt(
                user_message, 
                conversation_history, 
                user_profile
            )
            
            # Call Groq API with optimized parameters
            response = self.client.chat.completions.create(
                model=self.model,
                messages=prompt,
                max_tokens=200,
                temperature=0.7,
                top_p=0.9,
                frequency_penalty=0.1,
                presence_penalty=0.1,
                stop=None
            )
            
            reply = response.choices[0].message.content.strip()
            
            # Post-process and validate response
            processed_reply = self._post_process_response(reply, user_message)
            
            # Analyze response quality
            quality_metrics = self._analyze_response_quality(processed_reply, user_message)
            
            return {
                "response": processed_reply,
                "quality_score": quality_metrics["score"],
                "empathy_elements": quality_metrics["elements"],
                "cultural_sensitivity": quality_metrics["cultural_fit"],
                "model_used": self.model,
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Response generation error: {e}")
            return self._get_fallback_response(user_message)

    def _build_empathy_prompt(
        self, 
        user_message: str, 
        history: Optional[List[Dict]] = None,
        profile: Optional[Dict] = None
    ) -> List[Dict]:
        """Build sophisticated empathy prompt with context"""
        
        # System prompt with empathy framework
        system_prompt = f"""You are an advanced AI empathy assistant specialized in supporting Indian youth mental wellness.

CORE FRAMEWORK:
{json.dumps(self.empathy_framework, indent=2)}

CULTURAL CONTEXT:
{self.cultural_context}

RESPONSE GUIDELINES:
1. Use natural code-switching (English + Hindi) 
2. Keep responses warm, concise (2-3 sentences)
3. Validate feelings first, then offer gentle support
4. Suggest small, practical steps when appropriate
5. Never diagnose or give medical advice
6. If crisis indicators, guide to professional help gently

QUALITY MARKERS:
- Emotional validation present
- Culturally appropriate language
- Actionable but not overwhelming suggestions
- Hope and connection emphasized
- Natural, conversational tone"""

        # Context from conversation history
        context_prompt = ""
        if history:
            recent_messages = history[-3:]  # Last 3 exchanges
            context_prompt = "\nRECENT CONVERSATION:\n"
            for msg in recent_messages:
                role = msg.get('role', 'user')
                content = msg.get('content', '')
                context_prompt += f"{role.title()}: {content}\n"

        # User profile context
        profile_prompt = ""
        if profile:
            profile_prompt = f"\nUSER CONTEXT: {json.dumps(profile, indent=2)}"

        # Current message prompt
        user_prompt = f"""
{context_prompt}
{profile_prompt}

CURRENT USER MESSAGE: "{user_message}"

Respond with empathy, cultural sensitivity, and appropriate support. Focus on emotional validation and gentle encouragement."""

        return [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]

    def _post_process_response(self, reply: str, user_message: str) -> str:
        """Post-process and validate AI response"""
        
        # Basic cleanup
        reply = reply.strip()
        
        # Remove any unwanted patterns
        unwanted_patterns = [
            "As an AI", "I'm just an AI", "I cannot", "I'm not qualified"
        ]
        
        for pattern in unwanted_patterns:
            if pattern.lower() in reply.lower():
                # Replace with more natural language
                reply = reply.replace(pattern, "")
        
        # Ensure minimum length and quality
        if len(reply.strip()) < 20:
            return self._get_simple_fallback()
        
        # Check for crisis content and adjust if needed
        if any(word in reply.lower() for word in ['suicide', 'kill', 'die', 'hurt yourself']):
            return "I hear that you're going through something really difficult. Please consider reaching out to a counselor or trusted adult - you deserve support and care."
        
        return reply

    def _analyze_response_quality(self, response: str, user_message: str) -> Dict:
        """Analyze quality and empathy elements of response"""
        
        elements_found = []
        score = 0.5  # Base score
        
        # Check for validation language
        validation_indicators = [
            "samajh", "feel", "emotions", "valid", "understand", "hear you"
        ]
        if any(word in response.lower() for word in validation_indicators):
            elements_found.append("validation")
            score += 0.15
        
        # Check for empathy language
        empathy_indicators = [
            "tough", "difficult", "challenging", "mushkil", "hard"
        ]
        if any(word in response.lower() for word in empathy_indicators):
            elements_found.append("empathy")
            score += 0.15
        
        # Check for support language
        support_indicators = [
            "alone", "akele", "support", "help", "saath", "care"
        ]
        if any(word in response.lower() for word in support_indicators):
            elements_found.append("support")
            score += 0.1
        
        # Check for cultural sensitivity (code-switching)
        hindi_words = ["hai", "hoon", "kya", "tum", "main", "aur", "se"]
        if any(word in response.lower() for word in hindi_words):
            elements_found.append("cultural_sensitivity")
            score += 0.1
        
        # Check length appropriateness
        if 50 <= len(response) <= 300:
            score += 0.1
        
        cultural_fit = "high" if "cultural_sensitivity" in elements_found else "medium"
        
        return {
            "score": min(score, 1.0),  # Cap at 1.0
            "elements": elements_found,
            "cultural_fit": cultural_fit
        }

    def _get_fallback_response(self, user_message: str) -> Dict:
        """Generate fallback response when API fails"""
        fallbacks = [
            "Main samajh raha hoon tum kya feel kar rahe ho. Kya tum aur share karna chahoge?",
            "That sounds really tough. You're not alone in feeling this way.",
            "Tumhari feelings bilkul valid hain. Main sun raha hoon.",
            "I hear you. Would you like to share more about what you're going through?",
            "Ye difficult time hai, but tum strong ho. Kya koi aur baat share karni hai?"
        ]
        
        import random
        selected_response = random.choice(fallbacks)
        
        return {
            "response": selected_response,
            "quality_score": 0.6,
            "empathy_elements": ["validation", "support"],
            "cultural_sensitivity": "high",
            "model_used": "fallback",
            "timestamp": datetime.utcnow().isoformat()
        }

    def _get_simple_fallback(self) -> str:
        """Simple fallback for post-processing"""
        return "Main tumhari baat sun raha hoon. You're not alone in this."

    async def get_personalized_wellness_plan(
        self, 
        emotion_analysis: Dict, 
        user_context: Optional[Dict] = None
    ) -> Dict:
        """Generate personalized wellness suggestions"""
        
        if not self.ready:
            return self._get_default_wellness_plan()

        try:
            wellness_prompt = f"""
Based on the emotional analysis and user context, create a personalized wellness plan for an Indian youth.

EMOTIONAL ANALYSIS:
{json.dumps(emotion_analysis, indent=2)}

USER CONTEXT:
{json.dumps(user_context or {}, indent=2)}

Generate a JSON response with:
1. immediate_steps: 3-4 quick actions (5-15 minutes each)
2. daily_practices: 3-4 sustainable daily habits  
3. weekly_goals: 2-3 longer-term wellness goals
4. resources: helpful apps, websites, or activities

Focus on:
- Culturally appropriate suggestions for Indian context
- Mix of English and Hindi terms naturally
- Practical, achievable actions
- Building social connection and support

Format as valid JSON only."""

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": wellness_prompt}],
                max_tokens=400,
                temperature=0.6
            )
            
            plan_text = response.choices[0].message.content.strip()
            
            try:
                wellness_plan = json.loads(plan_text)
                return wellness_plan
            except json.JSONDecodeError:
                return self._get_default_wellness_plan()
                
        except Exception as e:
            logger.error(f"Wellness plan generation error: {e}")
            return self._get_default_wellness_plan()

    def _get_default_wellness_plan(self) -> Dict:
        """Default wellness plan fallback"""
        return {
            "immediate_steps": [
                "Take 5 deep breaths slowly",
                "Drink a glass of water mindfully", 
                "Step outside for fresh air",
                "Text a friend or family member"
            ],
            "daily_practices": [
                "Morning gratitude - think of 3 good things",
                "15-minute walk or movement",
                "Evening reflection or journaling",
                "Regular sleep schedule (10-11pm)"
            ],
            "weekly_goals": [
                "Connect with one supportive person",
                "Try one new relaxing activity",
                "Spend time in nature or green space"
            ],
            "resources": [
                "Headspace app for meditation",
                "iCall helpline: 9152987821",
                "Local counseling services",
                "Creative activities (art, music, writing)"
            ]
        }


# Global service instance  
groq_empathy_service = GroqEmpathyService()
