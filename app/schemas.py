from pydantic import BaseModel,ConfigDict,EmailStr

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = False

class PostCreate(PostBase):
    pass

class PostResponse(PostBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class UserCreate(BaseModel):
    email: EmailStr
    password:str