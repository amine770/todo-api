from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from .schemas import User
from .database import get_db
from .models import User
from .auth import oauth2_sheme, verify_token

def get_current_user(token: str = Depends(oauth2_sheme), db: Session = Depends(get_db)):
    credintial_exception = HTTPException( 
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid crediantials",
        headers={"WWW-Authenticate" : "Bearer"}
    )
    token_data =  verify_token(token, credintial_exception)
    user = db.query(User).filter(User.email == token_data.email).first()
    if not user:
        raise credintial_exception
    return user

def get_current_active_user(current_user: User = Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Inactive user")
    return current_user