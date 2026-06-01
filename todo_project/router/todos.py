from fastapi import APIRouter, Path, Query, HTTPException, Depends
from typing import Annotated
from pydantic import BaseModel
import models
import pydantic_model
from database import engine, sessionLocal
from sqlalchemy.orm import Session
from .auth import get_current_user

router = APIRouter()

def getDb():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()

dbObject = Annotated[Session, Depends(getDb)]

@router.get("/getAllTodos")
def getAllTodos(db: dbObject , user = Depends(get_current_user)):
    print("this is user id", user)
    return db.query(models.Todos).filter(models.Todos.owner_id == user.get("user_id")).all()

@router.get("/todo/{todo_id}")
def getBookById(db:dbObject, todo_id:int = Path(gt=0), user = Depends(get_current_user)):
    todo = db.query(models.Todos).filter(
        models.Todos.id == todo_id,
        models.Todos.owner_id == user.get("user_id")
    ).first()

    if todo is None:
        raise HTTPException(
            status_code = 404,
            detail = "Book not found"
        )
    return todo

@router.post("/todo/addTodo")
def addBook(db: dbObject, todoDetails:pydantic_model.todo_req, user = Depends(get_current_user)):
    try: 
        newTodo = models.Todos(**todoDetails.model_dump())
        userInfo = db.query(models.Users).filter(models.Users.id == newTodo.owner_id).first()
        if userInfo is None:
            raise HTTPException(
                status_code = 500,
                detail = f"user not found:{str(e)}"
            )
        db.add(newTodo)
        db.commit()
        db.refresh(newTodo)
        return {
            'todo':newTodo,
            'status_code':200,
            'message':'todo added successfully'
            }
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code = 500,
            detail = f"Error creating todo:{str(e)}"
        )
    
@router.put("/todo/updateTodo/{todo_id}")
def updateBook(db:dbObject, todo_req:pydantic_model.todo_req, todo_id:int, user = Depends(get_current_user)):
    try:
        existing_todo = db.query(models.Todos).filter(models.Todos.id == todo_id, models.Todos.owner_id == user.get("user_id")).first()
        if existing_todo is None:
            raise HTTPException(
                status = 404,
                message = "todo not found"
            )
        update_data = todo_req.model_dump()
        for key,value in update_data.items():
            setattr(existing_todo, key, value)
        
        db.commit()
        db.refresh(existing_todo)
        return {
            'todo':existing_todo,
            'status_code':200,
            'message':'todo updated successfully'
            }
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code = 500,
            detail = f"Error updating todo:{str(e)}"
        )

@router.delete("/todo/delete/{todo_id}")
def updateBook(db:dbObject, todo_id:int, user = Depends(get_current_user)):
    try:
        existing_todo = db.query(models.Todos).filter(models.Todos.id == todo_id, models.Todos.owner_id == user.get("user_id")).first()
        if existing_todo is None:
            raise HTTPException(
                status = 404,
                message = "todo not found"
            )
        db.delete(existing_todo)
        db.commit()
        return {
            'status_code':200,
            'message':'todo deleted successfully'
            }
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code = 500,
            detail = f"Error deleting todo:{str(e)}"
        )
    


