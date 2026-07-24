from pydantic import BaseModel,ConfigDict,EmailStr
from datetime import datetime
from typing import Optional
from typing import Literal

class User(BaseModel):
    email: EmailStr
    password:str

class UserResponse(BaseModel):
    email: EmailStr
    id:int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = False

class PostCreate(PostBase):
    pass

class PostResponse(PostBase):
    id: int
    user_id: int
    owner: UserResponse
    model_config = ConfigDict(from_attributes=True)

class PostVoteResponse(BaseModel):
    Post: PostResponse
    votes: int

    model_config = ConfigDict(from_attributes=True)



class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None


class Vote(BaseModel):
    post_id:int
    dir: Literal[0,1]