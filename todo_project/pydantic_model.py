from pydantic import BaseModel, Field
class Book_req(BaseModel):
    title: str
    description: str
    priority: int
    complete: bool