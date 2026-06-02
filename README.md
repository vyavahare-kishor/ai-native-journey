# 🚀 AI Native Journey — FastAPI Foundation

> A production-structured FastAPI backend with PostgreSQL, async AI chat, and SSE streaming — built as the foundation of an AI-native engineering portfolio.

![Python](https://img.shields.io/badge/Python-3.11+-blue?style=flat-square&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-green?style=flat-square&logo=fastapi)
![PostgreSQL](https://img.shields.io/badge/Database-PostgreSQL-blue?style=flat-square&logo=postgresql)
![Groq](https://img.shields.io/badge/LLM-Groq%20%7C%20LLaMA%203.3-orange?style=flat-square)
![SQLAlchemy](https://img.shields.io/badge/ORM-SQLAlchemy-red?style=flat-square)

---

## 🎯 What It Is

This is the **core API layer** of an AI-native application stack — combining a real database-backed REST API with a live AI chat interface powered by LLaMA 3.3 (via Groq).

Think of it as two things working together:

- **Users API** — full CRUD with PostgreSQL, UUID primary keys, input validation, and duplicate detection
- **AI Chat API** — stateless multi-turn chat with optional system prompts, plus real-time streaming via SSE

Built with production architecture patterns from day one — not a tutorial throwaway.

---

## ✨ Features

- **Full CRUD REST API** — Create, Read, Update (PATCH), Delete users backed by PostgreSQL
- **Pydantic v2 validation** — strict request/response schemas with auto OpenAPI docs
- **AI Chat endpoint** — multi-turn conversation with system prompt support
- **SSE Streaming** — real-time token streaming from LLM to client
- **Provider-agnostic AI layer** — swap LLM providers by editing one file
- **UUID primary keys** — production-standard, no sequential ID leakage
- **Partial updates** — PATCH only updates sent fields, leaves others untouched
- **Duplicate detection** — 409 conflict on duplicate email
- **Auto Swagger UI** — interactive docs at `/docs`, zero config

---

## 📡 API Reference

### Users

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/users/` | Create a new user |
| `GET` | `/users/` | List all users |
| `GET` | `/users/{id}` | Get user by UUID |
| `PATCH` | `/users/{id}` | Partial update (only sent fields change) |
| `DELETE` | `/users/{id}` | Delete user |

**Create user — example:**
```json
POST /users/
{
  "name": "Kishor",
  "email": "kishor@example.com",
  "age": 32
}
```
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "Kishor",
  "email": "kishor@example.com",
  "age": 32
}
```

**Partial update — example:**
```json
PATCH /users/{id}
{ "name": "Kishor V" }
```
Only `name` updates. `email` and `age` stay untouched.

---

### AI Chat

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/ai/chat` | Full response AI chat |
| `POST` | `/ai/chat/stream` | Real-time SSE streaming chat |

**Chat — example:**
```json
POST /ai/chat
{
  "messages": [
    { "role": "user", "content": "Explain async/await in Python in 2 lines." }
  ],
  "system": "You are a concise senior Python engineer."
}
```
```json
{ "reply": "async/await lets you write non-blocking code that waits for I/O without freezing the thread. Use async def for coroutines and await to pause execution until a result is ready." }
```

**Streaming — SSE response:**
```
data: async/await
data:  lets you
data:  write non-blocking
data: ...
data: [DONE]
```

---

## 🏗️ Architecture

```
┌────────────┐    ┌─────────────────────────────────┐
│   Client   │───▶│           FastAPI App            │
└────────────┘    │                                 │
                  │  ┌──────────┐  ┌─────────────┐  │
                  │  │  Users   │  │   AI Chat   │  │
                  │  │  Router  │  │   Router    │  │
                  │  └────┬─────┘  └──────┬──────┘  │
                  └───────┼───────────────┼──────────┘
                          │               │
              ┌───────────▼──┐    ┌───────▼────────┐
              │  PostgreSQL  │    │   AI Service   │
              │  SQLAlchemy  │    │  (Groq/LLaMA)  │
              └──────────────┘    └────────────────┘
```

**Key design decisions:**

- **Router → Service separation** — business logic lives in `services/`, routers stay thin. Same pattern as Rails controllers + service objects.
- **Pydantic schemas decoupled from ORM models** — `schemas/` handles API shapes, `models/` handles DB shapes. Changing one doesn't break the other.
- **`Depends(get_db)`** — FastAPI's dependency injection for DB sessions, auto-closes after request. Equivalent to Rails' `ApplicationController` giving controllers DB access.
- **Provider-agnostic AI service** — during development this project swapped Anthropic → Gemini → Groq. Only `services/ai.py` changed. Zero impact on routers or schemas.

---

## 🗂️ Project Structure

```
ai-native-journey/
├── main.py                  # App entry, router registration, DB init
├── database.py              # Engine, SessionLocal, get_db dependency
├── models/
│   ├── __init__.py          # Barrel exports — import User from models
│   └── user.py              # SQLAlchemy User model
├── schemas/
│   ├── __init__.py
│   └── user.py              # UserCreate, UserResponse, UserUpdate
├── routers/
│   ├── __init__.py
│   ├── users.py             # CRUD endpoints
│   └── ai.py                # Chat + streaming endpoints
├── services/
│   ├── __init__.py
│   └── ai.py                # LLM client — swap providers here only
├── .env.example
└── pyproject.toml
```

---

## 🧠 Technical Highlights

**Partial PATCH — only update what's sent**
```python
# exclude_unset=True is the key — ignores fields not in the request body
update_fields = user_data.model_dump(exclude_unset=True)
for field, value in update_fields.items():
    setattr(user, field, value)
db.commit()
```

**SSE Streaming — real-time LLM output**
```python
def generate():
    for chunk in stream_chat(messages, system):
        yield f"data: {chunk}\n\n"   # SSE format
    yield "data: [DONE]\n\n"

return StreamingResponse(generate(), media_type="text/event-stream")
```

**Provider-agnostic AI service**
```python
# services/ai.py — one file, full LLM abstraction
# Swap model/provider here. Nothing else in the codebase changes.
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL = "llama-3.3-70b-versatile"
```

**Dependency injection — DB session per request**
```python
# FastAPI handles open/close automatically
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- PostgreSQL
- [Groq API key](https://console.groq.com) — free tier, no credit card

### Installation

```bash
git clone https://github.com/yourusername/ai-native-journey
cd ai-native-journey

# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Setup environment
uv venv
source .venv/bin/activate
uv install
```

### Configuration

```bash
cp .env.example .env
```

```bash
# .env
DATABASE_URL=postgresql://localhost/ai_native_dev
GROQ_API_KEY=your_groq_api_key_here
```

### Database setup

```bash
createdb ai_native_dev
```

Tables are created automatically on server start via SQLAlchemy.

### Run

```bash
uvicorn main:app --reload
```

Open **http://localhost:8000/docs** — everything is interactive. ✅

---

## 🗺️ Roadmap

- [ ] JWT authentication — protect routes with bearer tokens
- [ ] Alembic migrations — version-controlled schema changes
- [ ] Conversation persistence — save chat history to PostgreSQL
- [ ] Rate limiting — per-user request throttling on AI endpoints
- [ ] Docker + docker-compose setup
- [ ] Deploy to Railway / Render

---

## 🔗 Related Projects

This project is part of an AI-native engineering portfolio:

| Project | Description |
|---------|-------------|
| **ai-native-journey** (this) | FastAPI foundation — REST API + AI chat + streaming |
| [**ai-pr-reviewer**](https://github.com/yourusername/ai-pr-reviewer) | AI-powered GitHub PR code reviewer — LLaMA + GitHub API |

---

## 👨‍💻 Author

**Kishor Vyavahare**
Senior Software Engineer → AI Native Engineer

11+ years of backend engineering (Ruby on Rails, PostgreSQL, AWS).
Transitioning into AI-native engineering — building real systems with Python, FastAPI, and LLMs.

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue?style=flat-square&logo=linkedin)](https://linkedin.com/in/vyavahare-kishor)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-black?style=flat-square&logo=github)](https://github.com/vyavahare-kishor)

---

## 📄 License

MIT License — use it, fork it, build on it.
