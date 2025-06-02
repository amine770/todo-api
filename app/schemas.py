from pydantic import BaseModel

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

class Todo(TodoCreate):
    id : int
    owner_id : int

    class Confing:
        from_attributes = True