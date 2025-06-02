from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..models import User
from ..schemas import Token, UserCreate
from ..auth import create_token
from ..utils import get_password_hash, verify_password
from ..database import get_db


router = APIRouter(tags=["auth"])

@router.post("/login", response_model=Token)
def login(user: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    #authenticate user
    user_db = db.query(User).filter(User.email == user.username).first()
    if not user_db or not verify_password(user.password, user_db.hashed_password):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Incorect password or email")
    
    access_token = create_token(data={"sub": user_db.email})
    return {"access_token" : access_token, "token_type" : "bearer"}

@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    user_db = db.query(User).filter(User.email == user.email).first()
    if user_db:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Email already exist")
    
    hashed_password = get_password_hash(user.password)
    new_user = User(email = user.email, hashed_password = hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


