from fastapi import FastAPI

app = FastAPI()

books = [
    {'title':"alchemist",'author':'Paul', 'pages':170}
]

@app.get("/home")
def getHomeValue():
    return {"message":"Welcome to fastapi"}

@app.get("/allBooks")
def getAllBooks():
    return books