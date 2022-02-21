from datetime import datetime
from typing import Optional
from pydantic import BaseModel,EmailStr, conint

class PostBase(BaseModel):
    title: str
    content: str
    published : bool = True

class PostCreate(PostBase):
    pass

class UserOut(BaseModel):
    id : int
    email : EmailStr
    created_at : datetime

    class Config:
        orm_mode = True
#---------------------------------------------------
#Response class
#---------------------------------------------------
class Post(PostBase):
    id : int
    created_at : datetime
    owner_id: int
    #link to the another object
    #owner: UserOut

    class Config:
        orm_mode = True

class PostOut(BaseModel):
    Post : Post
    votes : int

class UserCreate(BaseModel):
    email : EmailStr
    password : str

# class UserOut(BaseModel):
#     id : int
#     email : EmailStr
#     created_at : datetime

#     class Config:
#         orm_mode = True


class UserLogin(BaseModel):
    email : EmailStr
    password : str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None
    

class Vote(BaseModel):
    post_id : int
    dir : conint(le=1)
