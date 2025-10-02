from typing import Optional


CRISIS_KEYWORDS = ["kill myself", "suicide", "end my life", "hurt myself", "want to die", "die by suicide"]


async def check_crisis(text: str) -> Optional[str]:
    low = text.lower()
    for kw in CRISIS_KEYWORDS:
        if kw in low:
            return "CRISIS"
    return None