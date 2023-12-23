from pydantic import BaseModel
from datetime import datetime
from schema.user_schema import UserOut

class PostBase(BaseModel):
    title: str
    content: str 
    published: bool = True

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    created_at: datetime
    user_id: int
    user: UserOut
    

    class Config:
        orm_mode = True

class PostOut(PostBase):
    Post: Post
    vote: int

    class Config:
        orm_mode = True
