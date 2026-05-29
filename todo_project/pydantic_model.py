from pydantic import BaseModel, Field
class Book_req(BaseModel):
    title: str
    description: str
    priority: int
    complete: bool

class User_req(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    hashed_password: str
    role: str