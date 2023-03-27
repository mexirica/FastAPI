from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel

from db.enums import Role


class UserBase(BaseModel):
  username: str
  email: str
  password: str
  role: Role
  class Config():
    orm_mode = True

class UserDisplay(BaseModel):
  id: int
  username: str
  email: str
  role: Role
  class Config():
    orm_mode = True


class User(BaseModel):
  id: int
  username: str
  role: Role
  class Config():
    orm_mode = True

  class Token(BaseModel):
    access_token: str
    token_type: str
    refresh_token: str
    expires_in: Optional[int]
    expires_at: Optional[datetime]

    class Config:
      orm_mode = True