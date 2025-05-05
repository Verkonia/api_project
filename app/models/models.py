from sqlmodel import SQLModel, Field, Relationship 
from typing import Optional, List, TYPE_CHECKING

#пользователь
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    hashed_password: str
    ratings: List["Rating"] = Relationship(back_populates="user")
    
#фильм
class Movie(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: Optional[str] = None
    release_year: Optional[int] = None
    genre: Optional[str] = None
    director: Optional[str] = None
    ratings: List["Rating"] = Relationship(back_populates="movie")
    added_by: int
    
#рейтинг - связывает пользователя и фильм
class Rating(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    movie_id: int = Field(foreign_key="movie.id")
    rating: float = Field(ge=0, le=10)
    
    user: Optional["User"] = Relationship(back_populates="ratings")
    movie: Optional["Movie"] = Relationship(back_populates="ratings")
    
class UserCreate(SQLModel):
    username: str
    password: str

# Модель для валидации данных при добавлении фильма
class MovieCreate(SQLModel):
    title: str
    description: Optional[str] = None
    release_year: Optional[int] = None
    genre: Optional[str] = None
    director: Optional[str] = None
    

# Модель для валидации данных при добавлении рейтинга
class RatingCreate(SQLModel):
    user_id: int
    movie_id: int
    rating: float
    
class MovieResponse(SQLModel):
    id: int
    title: str
    description: Optional[str]
    release_year: Optional[int]
    genre: Optional[str]
    director: Optional[str] 
    average_rating: Optional[float]

    class Config:
        orm_mode = True  # Для работы с SQLAlchemy/SQLModel
    
    
    
