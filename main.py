from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

books = [
    {'title':"alchemist",'author':'Paul', 'pages':170},
    {'title':"atomic habits",'author':'Cnp', 'pages':170}
]

class Book(BaseModel):
    title:str
    author:str
    page:int

@app.get("/home")
def getHomeValue():
    return {"message":"Welcome to fastapi"}

@app.get("/allBooks")
def getAllBooks():
    return books

@app.get("/book/{title}/")
def getBookAuthor(title, author):
    for book in books:
        if book.get('title') == title and book.get('author') == author:
            return book
        
@app.post("/book/addBook")
def addBook(book:Book):
    books.append(book)
    return {
        "message":"Book created",
        "data": books
    }

@app.put('/book/updateBook')
def updateBook(book:Book):
    # here we can write update function
    return

@app.delete('/book/deleteBook')
def updateBook(book:Book):
    # here we can write delete function
    return