from typing import Optional
from pydantic import BaseModel

# Схема для создания пользователя (для регистрации)
class UserCreate(BaseModel):
    username: str
    password: str

# Схема для ответа о пользователе (будет использоваться в response_model)
class UserResponse(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True  # Для работы с SQLAlchemy/SQLModel

# Схема для создания фильма
class MovieCreate(BaseModel):
    title: str
    description: Optional[str] = None
    release_year: Optional[int] = None
    genre: Optional[str] = None
    director: Optional[str] = None

# Схема для ответа о фильме (будет использоваться в response_model)
class MovieResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    release_year: Optional[int] = None
    genre: Optional[str] = None
    director: Optional[str] = None
    average_rating: Optional[float] 
    added_by: int

    class Config:
        orm_mode = True  # Для работы с SQLAlchemy/SQLModel

# Схема для создания рейтинга
class RatingCreate(BaseModel):
    title: str
    rating: float  # Рейтинг от 0 до 10

# Схема для ответа о рейтинге (будет использоваться в response_model)
class RatingResponse(BaseModel):
    id: int
    user_id: int
    movie_id: int
    rating: float

    class Config:
        orm_mode = True  # Для работы с SQLAlchemy/SQLModel

# Модель для входа пользователя (токен)
class Token(BaseModel):
    access_token: str
    token_type: str

# Модель для валидации при авторизации
class OAuth2PasswordRequestForm(BaseModel):
    username: str
    password: str