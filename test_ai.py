# import anthropic
# import os
# from dotenv import load_dotenv

# load_dotenv()

# client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# message = client.messages.create(
#     model="claude-opus-4-5",
#     max_tokens=1024,
#     messages=[
#         {"role": "user", "content": "Explain what FastAPI is in 2 lines."}
#     ]
# )

# print(message.content[0].text)

from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL = "llama-3.3-70b-versatile"  # free, powerful

# ── Test 1: Basic chat ──────────────────────────────────────────
print("=" * 50)
print("TEST 1: Basic Chat")
print("=" * 50)

response = client.chat.completions.create(
    model=MODEL,
    messages=[
        {"role": "user", "content": "Explain FastAPI in 2 lines."}
    ],
    max_tokens=256
)
print(response.choices[0].message.content)

# ── Test 2: With system prompt ──────────────────────────────────
print("\n" + "=" * 50)
print("TEST 2: With System Prompt")
print("=" * 50)

response = client.chat.completions.create(
    model=MODEL,
    messages=[
        {"role": "system", "content": "You are a senior Python engineer helping a Rails developer transition to Python. Be concise and practical."},
        {"role": "user", "content": "Give me one killer tip for a Rails dev learning Python."}
    ],
    max_tokens=256
)
print(response.choices[0].message.content)

# ── Test 3: Streaming ───────────────────────────────────────────
print("\n" + "=" * 50)
print("TEST 3: Streaming")
print("=" * 50)

stream = client.chat.completions.create(
    model=MODEL,
    messages=[
        {"role": "user", "content": "Count from 1 to 5 with a fun fact for each number."}
    ],
    max_tokens=512,
    stream=True
)

for chunk in stream:
    text = chunk.choices[0].delta.content
    if text:
        print(text, end="", flush=True)

print("\n\nAll tests passed! ✅")
