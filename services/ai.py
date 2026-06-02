from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL = "llama-3.3-70b-versatile"


def chat(messages: list[dict], system: str = None) -> str:
    """
    Basic chat — returns full response string.
    messages = [{"role": "user", "content": "hello"}]
    """
    all_messages = []

    if system:
        all_messages.append({"role": "system", "content": system})

    all_messages.extend(messages)

    response = client.chat.completions.create(
        model=MODEL,
        messages=all_messages,
        max_tokens=1024
    )
    return response.choices[0].message.content


def stream_chat(messages: list[dict], system: str = None):
    """
    Streaming chat — yields text chunks as they arrive.
    """
    all_messages = []

    if system:
        all_messages.append({"role": "system", "content": system})

    all_messages.extend(messages)

    stream = client.chat.completions.create(
        model=MODEL,
        messages=all_messages,
        max_tokens=1024,
        stream=True
    )

    for chunk in stream:
        text = chunk.choices[0].delta.content
        if text:
            yield text
