import os

# Telegram
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# OpenRouter (OpenAI-compatible API)
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# Model for chat
AI_MODEL = os.getenv("AI_MODEL", "openai/gpt-4o-mini")

# Channel
CHANNEL_LINK = "https://t.me/ProjectPythons"
CHANNEL_NAME = "ProjectPythons"
