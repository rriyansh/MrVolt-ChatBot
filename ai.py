import httpx
from config import OPENROUTER_API_KEY, AI_MODEL

OPENROUTER_BASE = "https://openrouter.ai/api/v1"

SYSTEM_PROMPT = """you are mr volt, an advanced ai assistant bot on telegram.
you are helpful, intelligent, and friendly.
always respond in lowercase only.
keep responses concise and clear.
you can help with coding, writing, analysis, math, and general questions.
you were coded by @riyanshV."""

conversation_history: dict[int, list[dict]] = {}


async def chat(user_id: int, message: str) -> str:
    if user_id not in conversation_history:
        conversation_history[user_id] = []

    conversation_history[user_id].append({
        "role": "user",
        "content": message
    })

    # Keep last 20 messages for context
    history = conversation_history[user_id][-20:]

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://t.me/ProjectPythons",
        "X-Title": "Mr Volt ChatBot"
    }

    payload = {
        "model": AI_MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            *history
        ],
        "max_tokens": 1024,
        "temperature": 0.7
    }

    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.post(
            f"{OPENROUTER_BASE}/chat/completions",
            headers=headers,
            json=payload
        )
        response.raise_for_status()
        data = response.json()

    reply = data["choices"][0]["message"]["content"].lower()

    conversation_history[user_id].append({
        "role": "assistant",
        "content": reply
    })

    return reply


def clear_history(user_id: int):
    conversation_history.pop(user_id, None)
