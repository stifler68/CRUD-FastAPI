from sqlalchemy.orm import Session

from database import SessionLocal
import models, schemas
from passlib.context import CryptContext


# Authentication
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from jwt import InvalidTokenError, ExpiredSignatureError

#
import os
from dotenv import load_dotenv

load_dotenv()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# try push
def get_user_by_id(db: Session, user_id: int):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    book_list = db.query(models.Book).filter(models.Book.id == user_id).all()
    user_data = {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "password": user.password,
        "books": book_list,
    }
    return user_data


def get_users(db: Session, skip: int = 0, limit: int = 100):
    user_list = db.query(models.User).offset(skip).limit(limit).all()
    user_res_list = []
    for user in user_list:
        user_res_list.append(
            {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "books": [],
            }
        )
        book_list = db.query(models.Book).filter(models.Book.id == user.id).all()
        user_res_list[-1]["books"] = book_list

    return user_res_list


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def delete_user(db: Session, user_id: int):
    user_found = db.query(models.User).filter(models.User.id == user_id).first()
    if not user_found:
        return user_found
    db.delete(user_found)
    db.commit()
    return user_found


def update_user(db: Session, user_id: int, user: schemas.UserUpdate):
    # if db.query(models.User).filter(models.User.id == user_id).first() is None:
    #     return {"Error": "User Not Found "}

    if user.password:
        user.password = pwd_context.hash(user.password)

    filtered_payload = {
        key: value for key, value in dict(user).items() if value != None
    }
    # print("temp", filtered_payload)
    val = (
        db.query(models.User).filter(models.User.id == user_id).update(filtered_payload)
    )

    db.commit()
    return val

    # user_found = db.query(models.User).filter(models.User.id == user_id).first()

    # if user_found:
    #     for field, value in user.dict(exclude_unset=True).items():
    #         setattr(user_found, field, value)
    #     db.commit()
    #     db.refresh(user_found)
    #     return {"message": "User updated successfully"}
    # else:
    #     return {"message": "User not found"}

    # user_found.email = user.email
    # user_found.name = user.name
    # user_found.password = user.password

    # db.commit()
    # db.refresh(user_found)
    # return user_found


def create_user(db: Session, user: schemas.UserCreate):
    if user.password:
        user.password = pwd_context.hash(user.password)
    db_user = models.User(email=user.email, name=user.name, password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# ------------------------- BOOKS --------------------------


def get_all_Books(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Book).offset(skip).limit(limit).all()


def get_book_by_Id(db: Session, book_id: int):
    return db.query(models.Book).filter(models.Book.book_id == book_id).first()


def get_book_user_ID(db: Session, book_id: int):
    return db.query(models.Book).filter(models.Book.id == book_id).all()


def add_user_book(db: Session, book: schemas.BookCreate):
    db_book = models.Book(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh((db_book))
    return db_book


#  ------------   Authentication   ------------


# Configure JWT setting
# getting data from .env file
SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES")


# Generate a JWT access token
def create_access_token(data: dict):
    to_encode = data.copy()
    access_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return access_token


# Verify the JWT access token
def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload["sub"]
        if username is None:
            return {"Error": " Username not Found"}
        return username
    except JWTError:
        return {"Error": " Username not Found"}


# Hash a password
def get_password_hash(password):
    return pwd_context.hash(password)


# Verify a password
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
