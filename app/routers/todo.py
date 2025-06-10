from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import asc, desc
from sqlalchemy.orm import Session
from typing import Optional
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

#read endpoints
@router.get("/todos", response_model=list[TodoSchema])
def read_todo(current_user: User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    return db.query(Todo).filter(Todo.owner_id == current_user.id).all()

@router.get("/todos/sorted", response_model=list[TodoSchema])
def sorted_todo(sorted_by: Optional[str] = None, sorted_order: Optional[str] = "asc", current_user: User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    query = db.query(Todo).filter(Todo.owner_id == current_user.id)

    if sorted_by:
        if not hasattr(Todo, sorted_by):
            raise HTTPException(
                status_code = 400,
                detail = f"Invalid sort filed : {sorted_by}"
            )
        
        if sorted_order.lower() == "desc":
            sort_func = desc
        else:
            sort_func = asc
        
        query = query.order_by(sort_func(getattr(Todo, sorted_by)))
    
    return query.all()

@router.get("/todos/{filter_chars}", response_model=list[TodoSchema])
def filter_todo(filter_chars: str, current_user: User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    return db.query(Todo).filter(Todo.title.startswith(filter_chars), current_user.id == Todo.owner_id)


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

    