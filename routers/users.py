from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import User
from schemas import UserCreate, UserResponse, UserUpdate
import uuid

router = APIRouter(prefix="/users", tags=["Users"])

# POST /users


@router.post("/", response_model=UserResponse, status_code=201)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # Check duplicate email — like Rails' validates :email, uniqueness: true
    existing = db.query(User).filter(User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=409, detail="Email already exists")

    new_user = User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# GET /users


@router.get("/", response_model=list[UserResponse])
def list_users(db: Session = Depends(get_db)):
    return db.query(User).all()

# GET /users/:id


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: uuid.UUID, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# DELETE /users/:id


@router.delete("/{user_id}", status_code=204)
def delete_user(user_id: uuid.UUID, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()

# PATCH /users/:id


@router.patch("/{user_id}", response_model=UserResponse)
def update_user(user_id: uuid.UUID, user_update: UserUpdate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Check duplicate email if email is being updated
    if user_update.email and user_update.email != user.email:
        existing = db.query(User).filter(
            User.email == user_update.email).first()
        if existing:
            raise HTTPException(status_code=409, detail="Email already exists")

    # Only update fields that were actually sent — like Rails' update with permit
    update_fields = user_update.model_dump(exclude_unset=True)
    for field, value in update_fields.items():
        setattr(user, field, value)

    db.commit()
    db.refresh(user)
    return user
