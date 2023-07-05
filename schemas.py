from pydantic import BaseModel, EmailStr
from typing import Optional


class token(BaseModel):
    username: str
    password: str


class User(BaseModel):
    id: int
    name: str
    email: EmailStr
    password: str
    # book: Book_To_Get_User

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    name: Optional[str]
    email: Optional[EmailStr]
    password: Optional[str]

    class Config:
        orm_mode = True


# ---------- BOOKS ----------------


class User_To_Get_Book(BaseModel):
    id: int
    name: str
    email: EmailStr

    class Config:
        orm_mode = True


class Book(BaseModel):
    book_id: int
    title: str
    author: str
    user: User_To_Get_Book

    class Config:
        orm_mode = True


class BookCreate(BaseModel):
    id: int
    title: str
    author: str

    class Config:
        orm_mode = True
