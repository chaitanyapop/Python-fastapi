from fastapi import FastAPI, Path, Query, HTTPException, Depends

from pydantic import BaseModel
import models
import pydantic_model
from database import engine, sessionLocal
from sqlalchemy.orm import Session
from router import auth, todos

app = FastAPI()
#models.Base.metadata.create_all(bind=engine)
app.include_router(auth.router)
app.include_router(todos.router)

    


