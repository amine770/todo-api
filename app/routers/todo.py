from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Todo
from ..schemas import TodoCreate, User, Todo as TodoSchema
from ..dependencies import get_current_active_user

router = APIRouter(tags=["todos"])

@router.post("/todos", response_model=TodoSchema)
def create_todo(todo: TodoCreate ,current_user: User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    new_todo = Todo(**todo.dict(), owner_id=current_user.id)
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return new_todo

@router.get("/todos", response_model=list[TodoSchema])
def read_todo(current_user: User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    return db.query(Todo).filter(Todo.owner_id == current_user.id).all()