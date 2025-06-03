from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Todo
from ..schemas import TodoCreate, User, Todo as TodoSchema, TodoUpdate
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

@router.put("/todos/{todo_id}", response_model=TodoCreate)
def update_todo(todo_id: int, todo_data: TodoUpdate, current_user: User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == todo_id, Todo.owner_id == current_user.id).first()
    if not todo:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="todo not found")
    
    update_data = todo_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(todo, field, value)

    db.commit()
    db.refresh(todo)
    return todo

@router.delete("/todos/{todo_id}")
def delete_todo(todo_id: int, current_user: User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == todo_id, current_user.id == Todo.owner_id).first()
    if not todo:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="todo not found")
    
    db.delete(todo)
    db.commit()
    return {"message" : "todo deleted successfully"}

    