import re

IMAGE_KEYWORDS = [
    "create an image", "generate image", "make image", "generate picture",
    "create picture", "make picture", "draw", "ai image", "generate art",
    "create art", "make art", "image of", "picture of", "photo of",
    "generate a photo", "create a photo", "make a photo", "dall-e",
    "visualize", "show me", "render", "illustrate"
]

VOICE_KEYWORDS = [
    "convert to voice", "convert this to voice", "send voice", "make audio",
    "text to speech", "tts", "voice message", "speak this", "read this",
    "say this", "audio message", "make it audio", "voice this"
]

PDF_KEYWORDS = [
    "create a pdf", "make a pdf", "generate pdf", "create document",
    "make document", "generate document", "create a file", "make a file",
    "pdf of", "save as pdf", "write a document", "create report",
    "make report", "generate report"
]

CODE_KEYWORDS = [
    "format this code", "show this code", "format code", "code block",
    "highlight code", "pretty print", "beautify code", "fix indentation",
    "show code properly", "format this", "```"
]

CODE_PATTERNS = [
    r"```[\s\S]*```",
    r"def\s+\w+\s*\(",
    r"function\s+\w+\s*\(",
    r"class\s+\w+[:\{]",
    r"import\s+\w+",
    r"#include\s*<",
    r"public\s+static\s+void",
    r"console\.log\(",
    r"print\s*\(",
    r"var\s+\w+\s*=",
    r"const\s+\w+\s*=",
    r"let\s+\w+\s*=",
]


def detect_intent(message: str) -> str:
    text = message.lower().strip()

    for keyword in IMAGE_KEYWORDS:
        if keyword in text:
            return "image"

    for keyword in VOICE_KEYWORDS:
        if keyword in text:
            return "voice"

    for keyword in PDF_KEYWORDS:
        if keyword in text:
            return "pdf"

    for keyword in CODE_KEYWORDS:
        if keyword in text:
            return "code"

    for pattern in CODE_PATTERNS:
        if re.search(pattern, message):
            return "code"

    return "chat"


def extract_prompt(message: str, intent: str) -> str:
    text = message.strip()

    if intent == "image":
        for kw in IMAGE_KEYWORDS:
            text = re.sub(re.escape(kw), "", text, flags=re.IGNORECASE)
        text = re.sub(r"(please|can you|could you|i want|i need|a|an|the)\s+", " ", text, flags=re.IGNORECASE)
        return text.strip(" .,!?") or message

    if intent == "voice":
        for kw in VOICE_KEYWORDS:
            text = re.sub(re.escape(kw), "", text, flags=re.IGNORECASE)
        return text.strip(" .,!?") or message

    if intent == "pdf":
        for kw in PDF_KEYWORDS:
            text = re.sub(re.escape(kw), "", text, flags=re.IGNORECASE)
        return text.strip(" .,!?") or message

    return message
