import httpx
import io
from config import OPENROUTER_API_KEY

OPENROUTER_BASE = "https://openrouter.ai/api/v1"


async def text_to_voice(text: str) -> bytes | None:
    """Convert text to voice using OpenAI TTS via OpenRouter."""
    # Clean text
    text = text.strip()
    if not text:
        return None

    # Cap at 4000 chars
    if len(text) > 4000:
        text = text[:4000]

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://t.me/ProjectPythons",
        "X-Title": "Mr Volt ChatBot"
    }

    payload = {
        "model": "openai/tts-1",
        "input": text,
        "voice": "alloy",
        "response_format": "ogg"
    }

    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.post(
            f"{OPENROUTER_BASE}/audio/speech",
            headers=headers,
            json=payload
        )
        response.raise_for_status()
        return response.content
