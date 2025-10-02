import os
from typing import Optional, Dict, Any
from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM


class AIService:
    def __init__(self):
        # ✅ Dynamically build local path (cross-platform safe)
        BASE_DIR = os.path.dirname(os.path.dirname(__file__))  # goes up to app/
        MODEL_PATH = os.path.join(BASE_DIR, "output", "mt5-empathy").replace("\\", "/")

        print(f"⚡ Loading empathy model from {MODEL_PATH}...")
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
            self.model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_PATH)

            self.generator = pipeline(
                "text2text-generation",
                model=self.model,
                tokenizer=self.tokenizer,
                max_new_tokens=120
            )
            self.ready = True
            print("✅ Empathy model loaded successfully.")
        except Exception as e:
            print("❌ Failed to load empathy model:", e)
            self.generator = None
            self.ready = False

        # ✅ Load emotion classifier
        try:
            print("⚡ Loading emotion classifier...")
            self.emotion = pipeline(
                "text-classification",
                model="j-hartmann/emotion-english-distilroberta-base"
            )
        except Exception:
            self.emotion = None

    def analyze_emotion(self, text: str) -> Dict[str, Any]:
        if not self.emotion:
            return {"label": "neutral", "score": 0.5}
        res = self.emotion(text)
        if isinstance(res, list) and len(res) > 0:
            return {"label": res[0]["label"], "score": float(res[0]["score"])}
        return {"label": "neutral", "score": 0.5}

    async def generate_empathic_reply(self, text: str, user_id: Optional[str] = None) -> str:
        if not self.ready or not self.generator:
            return "Main samajh raha hoon tum kya feel kar rahe ho. Kya tum aur share karna chahoge?"

        try:
            outputs = self.generator(
                text,
                max_new_tokens=80,
                num_return_sequences=1
            )
            reply = outputs[0].get("generated_text", "").strip()

            if not reply or len(reply) < 5:
                reply = "Tumhare jazbaat samajhne ki koshish kar raha hoon. Kya tum aur batana chahoge?"
            return reply
        except Exception as e:
            print("⚠️ Generation error:", e)
            return "Main samajh raha hoon tum kya feel kar rahe ho. Kya tum thoda aur share karna chahoge?"


# Global instance
ai_service = AIService()
