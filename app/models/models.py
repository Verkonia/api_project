"""Модели данных для пользователей, фильмов и рейтингов с использованием SQLModel"""

from typing import Optional, List

from sqlmodel import SQLModel, Field, Relationship

class User(SQLModel, table=True):
    """Модель пользователя"""
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    hashed_password: str
    ratings: List["Rating"] = Relationship(back_populates="user")
    
class Movie(SQLModel, table=True):
    """Модель фильма"""
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: Optional[str] = None
    release_year: Optional[int] = None
    genre: Optional[str] = None
    director: Optional[str] = None
    ratings: List["Rating"] = Relationship(back_populates="movie")
    added_by: int
    
class Rating(SQLModel, table=True):
    """Модель рейтинга, связывающая пользователей и фильмы"""
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    movie_id: int = Field(foreign_key="movie.id")
    rating: float = Field(ge=0, le=10)
    user: Optional["User"] = Relationship(back_populates="ratings")
    movie: Optional["Movie"] = Relationship(back_populates="ratings")
    
class UserCreate(SQLModel):
    """Модель для создания нового пользователя"""
    username: str
    password: str

class MovieCreate(SQLModel):
    """Модель для создания нового фильма"""
    title: str
    description: Optional[str] = None
    release_year: Optional[int] = None
    genre: Optional[str] = None
    director: Optional[str] = None
    
class RatingCreate(SQLModel):
    """Модель для создания рейтинга""" 
    user_id: int
    movie_id: int
    rating: float
    
class MovieResponse(SQLModel):
    """Ответ с данными о фильме, включая средний рейтинг"""
    id: int
    title: str
    description: Optional[str]
    release_year: Optional[int]
    genre: Optional[str]
    director: Optional[str]
    average_rating: Optional[float]

    class Config:
        orm_mode = True
