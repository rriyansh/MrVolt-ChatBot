import asyncio
import io
import logging
import re
import sys
from telebot.async_telebot import AsyncTeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, Message

import ai
import image_gen
import voice
import pdf as pdf_module
from intent_detector import detect_intent, extract_prompt
from anti_spam import AntiSpam
from config import TELEGRAM_TOKEN, CHANNEL_LINK, CHANNEL_NAME

# Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

bot = AsyncTeleBot(TELEGRAM_TOKEN, parse_mode="Markdown")
spam_guard = AntiSpam()

WELCOME_MESSAGE = """*welcome to mr volt chatbot.*

*this bot can do it all.*

🖼 *image generation.*
📄 *file making.*
💻 *write codes.*
🎤 *send voice messages.*

*and many more.*

_coded by @riyanshV_"""


def channel_keyboard() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(
        f"📢 {CHANNEL_NAME}",
        url=CHANNEL_LINK
    ))
    return markup


def loading_text(intent: str) -> str:
    messages = {
        "image": "🎨 *generating your image... please wait.*",
        "voice": "🎤 *converting to voice... please wait.*",
        "pdf": "📄 *creating your pdf... please wait.*",
        "code": "💻 *formatting your code...*",
        "chat": "🤖 *thinking...*"
    }
    return messages.get(intent, "⏳ *processing...*")


def detect_language(code: str) -> str:
    patterns = {
        "python": [r"def\s+\w+", r"import\s+\w+", r"print\s*\(", r":\s*$", r"elif\s+"],
        "javascript": [r"function\s+\w+", r"const\s+\w+", r"let\s+\w+", r"console\.log", r"=>\s*{"],
        "java": [r"public\s+class", r"public\s+static\s+void", r"System\.out\.print"],
        "cpp": [r"#include\s*<", r"using\s+namespace", r"cout\s*<<", r"cin\s*>>"],
        "html": [r"<html", r"<div", r"<p>", r"<!DOCTYPE"],
        "css": [r"\{[\s\S]*?\}", r":\s*[\w#]", r"px|em|rem|%"],
        "sql": [r"SELECT\s+", r"FROM\s+\w+", r"WHERE\s+", r"INSERT\s+INTO"],
        "bash": [r"#!/bin/bash", r"\$\w+", r"echo\s+", r"fi$"],
        "rust": [r"fn\s+\w+", r"let\s+mut", r"println!", r"use\s+std"],
        "go": [r"func\s+\w+", r"package\s+main", r"fmt\.Print"],
    }

    for lang, pats in patterns.items():
        matches = sum(1 for p in pats if re.search(p, code, re.MULTILINE))
        if matches >= 2:
            return lang

    return ""


async def handle_chat(message: Message, text: str):
    try:
        response = await ai.chat(message.from_user.id, text)
        await bot.send_message(
            message.chat.id,
            f"*{response}*",
            reply_markup=channel_keyboard()
        )
    except Exception as e:
        logger.error(f"Chat error: {e}")
        await bot.send_message(
            message.chat.id,
            "*❌ sorry, i couldn't process that. please try again.*",
            reply_markup=channel_keyboard()
        )


async def handle_image(message: Message, prompt: str):
    try:
        image_bytes = await image_gen.generate_image(prompt)
        if image_bytes:
            await bot.send_photo(
                message.chat.id,
                photo=io.BytesIO(image_bytes),
                caption=f"*🖼 here's your image for: {prompt[:50]}*",
                reply_markup=channel_keyboard()
            )
        else:
            await bot.send_message(
                message.chat.id,
                "*❌ image generation failed. try a different prompt.*",
                reply_markup=channel_keyboard()
            )
    except Exception as e:
        logger.error(f"Image error: {e}")
        await bot.send_message(
            message.chat.id,
            "*❌ couldn't generate the image. please try again.*",
            reply_markup=channel_keyboard()
        )


async def handle_voice(message: Message, text: str):
    try:
        # If text is too short or empty, ask for content
        if len(text.strip()) < 5:
            await bot.send_message(
                message.chat.id,
                "*📝 please tell me what text you'd like me to convert to voice.*",
                reply_markup=channel_keyboard()
            )
            return

        audio_bytes = await voice.text_to_voice(text)
        if audio_bytes:
            await bot.send_voice(
                message.chat.id,
                voice=io.BytesIO(audio_bytes),
                caption="*🎤 here's your voice message.*",
                reply_markup=channel_keyboard()
            )
        else:
            await bot.send_message(
                message.chat.id,
                "*❌ voice generation failed. please try again.*",
                reply_markup=channel_keyboard()
            )
    except Exception as e:
        logger.error(f"Voice error: {e}")
        await bot.send_message(
            message.chat.id,
            "*❌ couldn't generate voice. please try again.*",
            reply_markup=channel_keyboard()
        )


async def handle_pdf(message: Message, content: str):
    try:
        if len(content.strip()) < 5:
            await bot.send_message(
                message.chat.id,
                "*📝 please tell me what content you'd like in the pdf.*",
                reply_markup=channel_keyboard()
            )
            return

        lines = content.strip().split("\n")
        title = lines[0][:60] if lines else "document"
        body = content

        pdf_bytes = pdf_module.generate_pdf(title, body)

        await bot.send_document(
            message.chat.id,
            document=io.BytesIO(pdf_bytes),
            visible_file_name=f"{title[:30].replace(' ', '_')}.pdf",
            caption="*📄 here's your pdf document.*",
            reply_markup=channel_keyboard()
        )
    except Exception as e:
        logger.error(f"PDF error: {e}")
        await bot.send_message(
            message.chat.id,
            "*❌ couldn't create the pdf. please try again.*",
            reply_markup=channel_keyboard()
        )


async def handle_code(message: Message, text: str):
    try:
        # Extract code from backticks if present
        code_match = re.search(r"```(?:\w+)?\n?([\s\S]*?)```", text)
        if code_match:
            code = code_match.group(1).strip()
        else:
            # Remove intent keywords and use the rest
            clean = re.sub(
                r"(format this code|show this code|format code|code block|"
                r"highlight code|pretty print|beautify code|fix indentation|"
                r"show code properly|format this)",
                "", text, flags=re.IGNORECASE
            ).strip()
            code = clean if clean else text

        lang = detect_language(code)
        formatted = f"```{lang}\n{code}\n```"

        await bot.send_message(
            message.chat.id,
            formatted,
            reply_markup=channel_keyboard()
        )
    except Exception as e:
        logger.error(f"Code error: {e}")
        await bot.send_message(
            message.chat.id,
            "*❌ couldn't format the code. please try again.*",
            reply_markup=channel_keyboard()
        )


@bot.message_handler(commands=["start"])
async def start_handler(message: Message):
    await bot.send_message(
        message.chat.id,
        WELCOME_MESSAGE,
        reply_markup=channel_keyboard()
    )
    logger.info(f"New user: {message.from_user.id} | @{message.from_user.username}")


@bot.message_handler(commands=["clear"])
async def clear_handler(message: Message):
    ai.clear_history(message.from_user.id)
    await bot.send_message(
        message.chat.id,
        "*🗑 conversation history cleared.*",
        reply_markup=channel_keyboard()
    )


@bot.message_handler(content_types=["text"])
async def message_handler(message: Message):
    user_id = message.from_user.id
    text = message.text.strip()

    if not text:
        return

    # Anti-spam check
    allowed, reason = spam_guard.check(user_id)
    if not allowed:
        await bot.send_message(message.chat.id, f"*{reason}*")
        return

    logger.info(f"User {user_id}: {text[:60]}")

    # Detect intent
    intent = detect_intent(text)
    prompt = extract_prompt(text, intent)

    # Send loading message
    loading_msg = await bot.send_message(
        message.chat.id,
        loading_text(intent)
    )

    # Route to handler
    if intent == "image":
        await handle_image(message, prompt or text)
    elif intent == "voice":
        await handle_voice(message, prompt or text)
    elif intent == "pdf":
        await handle_pdf(message, prompt or text)
    elif intent == "code":
        await handle_code(message, text)
    else:
        await handle_chat(message, text)

    # Delete loading message
    try:
        await bot.delete_message(message.chat.id, loading_msg.message_id)
    except Exception:
        pass


async def main():
    logger.info("🤖 Mr Volt ChatBot starting...")
    await bot.infinity_polling(timeout=20, request_timeout=30)


if __name__ == "__main__":
    asyncio.run(main())
