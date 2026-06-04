from langchain.chat_models import init_chat_model

from config.settings import (
    MODEL,
    FALLBACK_MODEL
)

def get_model():
    primary = init_chat_model(MODEL)
    fallback = init_chat_model(FALLBACK_MODEL)

    return primary.with_fallbacks(
        [fallback]
    )