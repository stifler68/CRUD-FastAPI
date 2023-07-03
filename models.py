from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    # book_id = Column(Integer, ForeignKey("books.book_id"))
    books = relationship("Book", back_populates="user")


class Book(Base):
    __tablename__ = "books"

    book_id = Column(Integer, primary_key=True, index=True)
    id = Column(Integer, ForeignKey("users.id"))
    title = Column(String(255))
    author = Column(String(255))

    user = relationship("User", back_populates="books")
