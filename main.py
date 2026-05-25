from fastapi import FastAPI, Path, Query, HTTPException
from pydantic import BaseModel
import models as model


app = FastAPI()

books = [
    model.Books(id = 1, title = "book 1", author = 'a',description = "book 1 desc",rating = 4),
    model.Books(id = 2,  title = "book 2", author =  'b',description = "book 2 desc",rating =  3),
    model.Books(id = 3, title =  "book 3",  author = 'c',description = "book 3 desc",rating =  5),
    model.Books(id = 4,  title = "book 4",  author = 'd',description = "book 14 desc", rating = 4),
    model.Books(id = 5,  title = "book 5",  author = 'e',description = "book 5 desc",rating =  2)
]

# class Book(BaseModel):
#     title:str
#     author:str
#     page:int

@app.get("/home")
def getHomeValue():
    return {"message":"Welcome to fastapi"}

@app.get("/allBooks")
def getAllBooks():
    return books

@app.get("/book/{title}/")
def getBookAuthor(title:str = Path(max_length=5), author:str = Query(min_length=3)):
    for book in books:
        if book.title == title and book.author == author:
            return book
        
@app.post("/book/addBook")
def addBook(book:model.Books):
    # books.append(book)
    newBook = model.Books(**book.model_dump())
    books.append(newBook)
    return {
        "message":"Book created",
        "data": books
    }

@app.put('/book/updateBook')
def updateBook(book:model.Books):
    # here we can write update function
    for index,bookVal in enumerate(books):
        if bookVal.id == book.id:
            books[index] = book
            return books
        
    raise HTTPException(status_code = 404, detail = "id not found")

@app.delete('/book/deleteBook')
def updateBook(book:model.Books):
    # here we can write update function
    for index,bookVal in enumerate(books):
        if bookVal.id == book.id:
            books.pop(index)
            return books

    return {
        "messsage":"Books not found"
    }
