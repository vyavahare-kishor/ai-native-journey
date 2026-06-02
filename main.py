from fastapi import FastAPI
from database import Base, engine
from routers import users, ai

# This creates tables — like `rails db:migrate` but auto
Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Native Journey API")

app.include_router(users.router)
app.include_router(ai.router)


@app.get("/")
def root():
    return {"message": "Kishor's AI Native journey begins 🚀"}


@app.get("/health")
def health():
    return {"status": "ok"}
