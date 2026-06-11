from pydantic import BaseModel, Field
class todo_req(BaseModel):
    title: str
    description: str
    priority: int
    complete: bool
    owner_id: int

class User_req(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    hashed_password: str
    role: str
    mobile_number: str

class Token_res(BaseModel):
    access_token: str
    token_type: str