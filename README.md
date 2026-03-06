# 🤖 Mr Volt ChatBot

Advanced AI Telegram bot with intent detection, image generation, voice messages, PDF creation, and code formatting.

**Coded by @riyanshV | Channel: [ProjectPythons](https://t.me/ProjectPythons)**

---

## ✨ Features

| Feature | Trigger Examples |
|---|---|
| 🤖 AI Chat | Any general question |
| 🖼 Image Generation | "create an image of a cat", "generate picture of mountains" |
| 🎤 Voice Messages | "convert to voice", "send voice", "make audio" |
| 📄 PDF Generator | "create a pdf", "make document" |
| 💻 Code Formatting | "format this code", send a code block |
| 🛡 Anti-Spam | Auto rate limiting & temp bans |

---

## 🚀 Setup & Run

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure credentials
Edit `config.py` or set environment variables:
```bash
export TELEGRAM_TOKEN="your_bot_token"
export OPENROUTER_API_KEY="your_openrouter_key"
```

### 3. Run the bot
```bash
python bot.py
```

---

## 🌐 Deploy to Railway / Render / Heroku

1. Push this folder to a GitHub repo
2. Connect to Railway / Render / Heroku
3. Set environment variables:
   - `TELEGRAM_TOKEN`
   - `OPENROUTER_API_KEY`
4. Deploy — the `Procfile` handles the rest

---

## 📁 Project Structure

```
telegram_bot/
├── bot.py            # Main bot + message router
├── ai.py             # GPT chat via OpenRouter
├── image_gen.py      # AI image generation
├── voice.py          # Text-to-speech
├── pdf.py            # PDF generator
├── intent_detector.py # NLP intent classification
├── anti_spam.py      # Rate limiting & ban system
├── config.py         # API keys & settings
├── requirements.txt
├── Procfile
└── .env.example
```

---

## ⚡ Rate Limits (Anti-Spam)

- Max **10 messages/minute** per user
- Max **50 messages/hour** per user  
- **100 msg/hour** → 10-minute temp ban
- **5 second cooldown** between messages

---

## 🔧 Commands

| Command | Action |
|---|---|
| `/start` | Welcome message |
| `/clear` | Clear conversation history |
