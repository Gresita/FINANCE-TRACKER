from fastapi import APIRouter, Depends, HTTPException, status, Form
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from pydantic import BaseModel, ConfigDict, field_validator
from typing import Annotated
from app.models.database import User, get_db
from app.core.security import AuthService

router = APIRouter()

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

    @field_validator("username")
    @classmethod
    def validate_username(cls, v):
        if len(v) < 3:
            raise ValueError("Username too short")
        return v

    @field_validator("email")
    @classmethod
    def validate_email(cls, v):
        if "@" not in v:
            raise ValueError("Invalid email")
        return v

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    model_config = ConfigDict(from_attributes=True)

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    try:
        existing = db.query(User).filter(
            (User.username == user.username) | (User.email == user.email)
        ).first()

        if existing:
            raise HTTPException(status_code=400, detail="User already exists")

        auth = AuthService()
        new_user = User(
            username=user.username,
            email=user.email,
            hashed_password=auth.hash_password(user.password)
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return new_user

    except HTTPException:
        raise
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="User already exists")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Register error: {str(e)}")

@router.post("/login", response_model=TokenResponse)
async def login(
    username: Annotated[str, Form()],
    password: Annotated[str, Form()],
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.username == username).first()

    if not user or not AuthService().verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = AuthService().create_access_token({"sub": user.username})
    return TokenResponse(access_token=token)

@router.get("/me", response_model=UserResponse)
async def me(current_user: User = Depends(AuthService.get_current_user)):
    return current_user