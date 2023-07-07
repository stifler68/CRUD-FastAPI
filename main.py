from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

import crud, models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
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


@app.get("/users", response_model=schemas.User)
def get_all_user(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: str = Depends(crud.verify_token),
):
    # print(db)
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}")
def get_user_by_ID(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(crud.verify_token),
):
    db_user = crud.get_user_by_id(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.put("/users/{user_id}")
def update_user(
    user: schemas.UserUpdate,
    user_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(crud.verify_token),
):
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
def create_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(crud.verify_token),
):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.delete("/users/{user_id}", response_model=schemas.User)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(crud.verify_token),
):
    db_user = crud.delete_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


# ----------- Books ----------------


# Get All Books
@app.get("/books", response_model=list[schemas.Book])
def get_all_books(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: str = Depends(crud.verify_token),
):
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
def add_book_for_user(
    book: schemas.BookCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(crud.verify_token),
):
    # print(book.user_id)
    return crud.add_user_book(db=db, book=book)


@app.post("/token")
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db=Depends(get_db)
):
    user = db.query(models.User).filter(models.User.name == form_data.username).first()
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    if not crud.verify_password(form_data.password, user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    access_token = crud.create_access_token(data={"sub": user.name})
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me")
def read_user_me(current_user: str = Depends(crud.verify_token)):
    return current_user
