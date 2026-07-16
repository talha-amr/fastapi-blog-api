from pydantic import BaseModel,ConfigDict,EmailStr
from datetime import datetime
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = False

class PostCreate(PostBase):
    pass

class PostResponse(PostBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class User(BaseModel):
    email: EmailStr
    password:str

class UserResponse(BaseModel):
    email: EmailStr
    id:int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)