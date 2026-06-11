from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
import pydantic_model
import models
from database import sessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import JWTError, jwt
from util.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRY_MIN

router = APIRouter()
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/login"
)

def getDb():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()

dbObject = Annotated[Session, Depends(getDb)]

def create_access_token(username:str, user_id:int):
    payload = {
        "sub": username,
        "id": user_id
    }
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRY_MIN)
    payload["exp"] = expire
    encoded_jwt = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(token:str = Depends(oauth2_scheme)):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code = 401,
                detail = "Invalid token"
            )
        return {
            "username" : payload.get("sub"),
            "user_id" : payload.get("id")
        }
    
    except JWTError:
        raise HTTPException(
            status_code = 401,
            detail = "Invalid or expired token"
        )



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

@router.post("/login", response_model = pydantic_model.Token_res)
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
    token = create_access_token(user.username, user.id)
    return {
        "access_token":token,
        "token_type":'bearer'
    }


    
