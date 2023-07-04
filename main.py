from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

import crud, models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Configure CORS
origins = [
    "http://localhost",
    "http://127.0.0.1:5500",
    "http://localhost:5500",
    "https://example.com",
    "http://test.example.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/users")
def get_all_user(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)

    # for i in users:
    #     print("userid:- ", i.id)

    return users


@app.get("/users/{user_id}")
def get_user_by_ID(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_id(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.put("/users/{user_id}")
def update_user(user: schemas.UserUpdate, user_id: int, db: Session = Depends(get_db)):
    db_user = crud.update_user(db, user_id=user_id, user=user)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "Updated Successful"}


# @app.put("/users/{user_id}")
# def update_user(data: dict, user_id: int, db: Session = Depends(get_db)):
#     db_user = crud.update_user(db, user_id=user_id, user=data)
#     if db_user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return db_user


@app.post("/users", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.delete("/users/{user_id}", response_model=schemas.User)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.delete_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


# ----------- Books ----------------


# Get All Books
@app.get("/books", response_model=list[schemas.Book])
def get_all_books(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    book = crud.get_all_Books(db, skip=skip, limit=limit)
    return book


# @app.get("/users/{user_id}", response_model=schemas.User)
# def get_user_by_ID(user_id: int, db: Session = Depends(get_db)):
#     db_user = crud.get_user_by_id(db, user_id=user_id)
#     if db_user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return db_user


@app.get("/books/{book_id}", response_model=schemas.Book)
def get_Book_By_ID(book_id: int, db: Session = Depends(get_db)):
    db_book = crud.get_book_by_Id(db, book_id=book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book


#  Add book
@app.post("/books", response_model=schemas.BookCreate)
def add_book_for_user(book: schemas.BookCreate, db: Session = Depends(get_db)):
    # print(book.user_id)
    return crud.add_user_book(db=db, book=book)
