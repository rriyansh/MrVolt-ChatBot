import os

# Telegram
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "8581114695:AAF0znEGt6al2FGidAX03Y0V_84UxzUZPsM")

# OpenRouter (OpenAI-compatible API)
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "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")

# Model for chat
AI_MODEL = os.getenv("AI_MODEL", "openai/gpt-4o-mini")

# Channel
CHANNEL_LINK = "https://t.me/ProjectPythons"
CHANNEL_NAME = "ProjectPythons"
