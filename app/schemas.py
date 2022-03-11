from pydantic import BaseModel, EmailStr, conint
from datetime import datetime
from typing import Optional

#user schemas
class UserCreate(BaseModel):
  email: EmailStr
  password: str
  
class UserResponse(BaseModel):
  id: int
  email: EmailStr
  created_at: datetime
  
  class Config:
    orm_mode = True
    
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    # rating: Optional[int] = None
    
class PostCreate(PostBase):
  pass

class PostResponse(PostBase):
  id: int
  created_at: datetime
  owner_id: int
  owner: UserResponse
  
  class Config:
    orm_mode = True
    
    
class PostResponseWithVote(BaseModel):
  Post: PostResponse
  votes: int
    
  class Config:
    orm_mode = True

    
class UserLogin(BaseModel):
  email: EmailStr
  password: str
  
class Token(BaseModel):
  access_token: str
  token_type: str
  
class TokenData(BaseModel):
  id: Optional[str] = None
  
  
#vote schema
class Vote(BaseModel):
  post_id: int
  direction: conint(ge=0,le=1)