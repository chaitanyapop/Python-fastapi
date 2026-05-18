from typing import Optional

from pydantic import BaseModel, Field


class Books(BaseModel):
    id:Optional[int] = None
    title:str = Field(max_length=10)
    author:str = Field(max_length=10)
    description:str
    rating:int = Field(lt=6, gt=-1)

    # def __init__(self, id, title, author, description, rating):
    #     self.id = id
    #     self.title = title
    #     self.author = author
    #     self.description = description
    #     self.rating = rating
        
