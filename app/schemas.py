from pydantic import BaseModel
from typing import Optional

class Token(BaseModel):
    access_token : str
    token_type : str

class TokenData(BaseModel):
    email : str | None=None


class UserCreate(BaseModel):
    email : str
    password : str

class User(BaseModel):
    id : str
    email : str
    role : str
    is_active : bool

    class Config:
        from_attributes = True

class TodoCreate(BaseModel):
    title : str
    description : str = None
    completed : bool = False

class TodoUpdate(BaseModel):
    title : Optional[str] = None
    description : Optional[str] = None
    completed : Optional[bool] = None

class Todo(TodoCreate):
    id : int
    owner_id : int

    class Confing:
        from_attributes = True