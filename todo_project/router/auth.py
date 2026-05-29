from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
import pydantic_model
import models
from database import sessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from passlib.context import CryptContext

router = APIRouter()
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")

def getDb():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()

dbObject = Annotated[Session, Depends(getDb)]

@router.get("/auth/")
async def getUser():
    return {
        'user':"User authenticated"
    }

@router.post("/createUser")
async def createUser(db:dbObject, userData:pydantic_model.User_req):
    try:
        userData.hashed_password = bcrypt_context.hash(userData.hashed_password)
        userInfo = models.Users(**userData.model_dump())
        db.add(userInfo)
        db.commit()
        db.refresh(userInfo)
        return {
            "message":'User created successfully',
            "user":userInfo
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code = 500,
            detail = f"Error creating User:{str(e)}"
        )

@router.post("/login")
async def loginUser(db:dbObject, loginData:Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = db.query(models.Users).filter(
        models.Users.username == loginData.username
    ).first()
    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )
    if not bcrypt_context.verify(
        loginData.password,
        user.hashed_password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )
    return {
        "message": "Login successful"
    }


    
