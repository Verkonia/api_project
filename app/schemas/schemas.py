from typing import Optional
from pydantic import BaseModel

#для создания пользователя (для регистрации)
class UserCreate(BaseModel):
    username: str
    password: str

#для ответа о пользователе 
    id: int
    username: str

    class Config:
        orm_mode = True 

#для создания фильма
class MovieCreate(BaseModel):
    title: str
    description: Optional[str] = None
    release_year: Optional[int] = None
    genre: Optional[str] = None
    director: Optional[str] = None

# для ответа о фильме
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
        orm_mode = True 

#для создания рейтинга
class RatingCreate(BaseModel):
    title: str
    rating: float  # Рейтинг от 0 до 10

# для ответа о рейтинге
class RatingResponse(BaseModel):
    id: int
    user_id: int
    movie_id: int
    rating: float

    class Config:
        orm_mode = True  

#для входа пользователя (токен)
class Token(BaseModel):
    access_token: str
    token_type: str

#для валидации при авторизации
class OAuth2PasswordRequestForm(BaseModel):
    username: str
    password: str