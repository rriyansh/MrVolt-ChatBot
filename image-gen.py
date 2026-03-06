import httpx
from config import OPENROUTER_API_KEY

OPENROUTER_BASE = "https://openrouter.ai/api/v1"


async def generate_image(prompt: str) -> bytes | None:
    """Generate image using OpenRouter image generation API."""
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://t.me/ProjectPythons",
        "X-Title": "Mr Volt ChatBot"
    }

    payload = {
        "model": "black-forest-labs/flux-schnell",
        "prompt": prompt,
        "n": 1,
        "size": "1024x1024"
    }

    async with httpx.AsyncClient(timeout=60) as client:
        response = await client.post(
            f"{OPENROUTER_BASE}/images/generations",
            headers=headers,
            json=payload
        )
        response.raise_for_status()
        data = response.json()

    image_url = data["data"][0]["url"]

    # Download the image
    async with httpx.AsyncClient(timeout=30) as client:
        img_response = await client.get(image_url)
        img_response.raise_for_status()
        return img_response.content
