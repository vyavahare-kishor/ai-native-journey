from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import uuid

app = FastAPI(title="AI Native Journey API")


class UserCreate(BaseModel):
    name: str
    email: str
    age: Optional[int] = None


class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    age: Optional[int] = None


class UserResponse(BaseModel):
    id: str
    name: str
    email: str
    age: Optional[int] = None


users_db: dict = {}


@app.get("/")
def root():
    return {"message": "Kishor's AI Native journey begins 🚀"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/users", response_model=list[UserResponse])
def list_users():
    print(users_db)
    return list(users_db.values())


@app.post("/users", response_model=UserResponse, status_code=201)
def create_user(user: UserCreate):
    user_id = str(uuid.uuid4())
    new_user = {"id": user_id, **user.model_dump()}
    users_db[user_id] = new_user
    return new_user


@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: str):
    user = users_db.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.put("/users/{user_id}", response_model=UserResponse)
def update_user(user_id: str, user_update: UserUpdate):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")

    current_user = users_db[user_id]
    # Extract only the fields that the client actually provided
    # exclude_unset=True ignores fields that weren't explicitly passed in the request JSON
    update_data = user_update.model_dump(exclude_unset=True)

    # Merge the updates into the existing user data
    updated_user = {**current_user, **update_data}

    # 4. Save back to the database
    users_db[user_id] = updated_user

    return updated_user


@app.delete("/users/{user_id}", status_code=204)
def delete_user(user_id: str):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    del users_db[user_id]
