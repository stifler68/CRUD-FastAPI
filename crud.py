from sqlalchemy.orm import Session

from database import SessionLocal
import models, schemas
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


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


# find a better way to add and update the data in db
