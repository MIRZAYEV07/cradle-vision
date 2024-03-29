from datetime import datetime
from typing import Union

from pydantic import BaseModel, EmailStr
from sqlmodel import Field, Relationship, SQLModel


# Shared properties
class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True)
    is_active: bool = True
    is_superuser: bool = False
    full_name: Union[str, None] = None


# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str


class UserCreateOpen(SQLModel):
    email: EmailStr
    password: str
    full_name: Union[str, None] = None


# Properties to receive via API on update, all are optional
class UserUpdate(UserBase):
    email: Union[EmailStr, None] = None
    password: Union[str, None] = None


class UserUpdateMe(BaseModel):
    password: Union[str, None] = None
    full_name: Union[str, None] = None
    email: Union[EmailStr, None] = None

# Database model, database table inferred from class name
class User(UserBase, table=True):
    id: Union[int, None] = Field(default=None, primary_key=True)
    hashed_password: str
    items: list["Item"] = Relationship(back_populates="owner")


# Properties to return via API, id is always required
class UserOut(UserBase):
    id: int


# Shared properties
class RtspUrlBase(SQLModel):
    title: str
    description: Union[str, None] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


# Properties to receive on item creation
class RtspUrlCreate(RtspUrlBase):
    id: int
    rtsp_url: str


# Properties to receive on item update
class RtspUrlUpdate(RtspUrlBase):
    title: Union[str, None] = None


# Database model, database table inferred from class name
class RtspUrl(RtspUrlBase, table=True):
    id: Union[int, None] = Field(default=None, primary_key=True)
    rtsp_url: str
    owner_id: Union[int, None] = Field(
        default=None, foreign_key="user.id", nullable=False
    )
    owner: Union[User, None] = Relationship(back_populates="items")


# Properties to return via API, id is always required
class RtspUrlOut(RtspUrlBase):
    id: int


# Generic message
class Message(BaseModel):
    message: str


# JSON payload containing access token
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


# Contents of JWT token
class TokenPayload(BaseModel):
    sub: Union[int, None] = None


class NewPassword(BaseModel):
    token: str
    new_password: str