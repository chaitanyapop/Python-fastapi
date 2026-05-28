from fastapi import FastAPI, Path, Query, HTTPException, Depends
from typing import Annotated
from pydantic import BaseModel
import models
import pydantic_model
from database import engine, sessionLocal
from sqlalchemy.orm import Session
from router import auth, todos

app = FastAPI()
models.Base.metadata.create_all(bind=engine)
app.include_router(auth.router)
app.include_router(todos.router)

# def getDb():
#     db = sessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# dbObject = Annotated[Session, Depends(getDb)]

# @app.get("/getAllTodos")
# def getAllTodos(db: dbObject ):
#     return db.query(models.Todos).all()

# @app.get("/book/{book_id}")
# def getBookById(db:dbObject, book_id:int = Path(gt=0)):
#     book = db.query(models.Todos).filter(
#         models.Todos.id == book_id
#     ).first()

#     if book is None:
#         raise HTTPException(
#             status_code = 404,
#             detail = "Book not found"
#         )
#     return book

# @app.post("/book/addBook")
# def addBook(db: dbObject, bookDetails:pydantic_model.Book_req):
#     try:
#         newBook = models.Todos(**bookDetails.model_dump())
#         db.add(newBook)
#         db.commit()
#         db.refresh(newBook)
#         return {
#             'book':newBook,
#             'status_code':200,
#             'message':'Book added successfully'
#             }
#     except Exception as e:
#         db.rollback()
#         raise HTTPException(
#             status_code = 500,
#             detail = f"Error creating book:{str(e)}"
#         )
    
# @app.put("/book/updateBook/{book_id}")
# def updateBook(db:dbObject, book_req:pydantic_model.Book_req, book_id:int):
#     try:
#         existing_book = db.query(models.Todos).filter(models.Todos.id == book_id).first()
#         if existing_book is None:
#             raise HTTPException(
#                 status = 404,
#                 message = "Book not found"
#             )
#         update_data = book_req.model_dump()
#         for key,value in update_data.items():
#             setattr(existing_book, key, value)
        
#         db.commit()
#         db.refresh(existing_book)
#         return {
#             'book':existing_book,
#             'status_code':200,
#             'message':'Book updated successfully'
#             }
#     except Exception as e:
#         db.rollback()
#         raise HTTPException(
#             status_code = 500,
#             detail = f"Error updating book:{str(e)}"
#         )

# @app.delete("/book/delete/{book_id}")
# def updateBook(db:dbObject, book_id:int):
#     try:
#         existing_book = db.query(models.Todos).filter(models.Todos.id == book_id).first()
#         if existing_book is None:
#             raise HTTPException(
#                 status = 404,
#                 message = "Book not found"
#             )
#         db.delete(existing_book)
#         db.commit()
#         return {
#             'status_code':200,
#             'message':'Book deleted successfully'
#             }
#     except Exception as e:
#         db.rollback()
#         raise HTTPException(
#             status_code = 500,
#             detail = f"Error deleting book:{str(e)}"
#         )
    


