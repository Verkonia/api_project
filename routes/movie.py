from fastapi import APIRouter, Depends, HTTPException
from dbs.session import get_session
from models.models import Movie, Rating, User
from schemas.schemas import MovieCreate, RatingCreate, MovieResponse, RatingResponse
from core.security import get_current_user
from sqlmodel import select, func


router = APIRouter()

@router.post("/movies/")
def create_movie(movie: MovieCreate, user=Depends(get_current_user), session = Depends(get_session)):

    db_movie = Movie(title=movie.title, description=movie.description, release_year=movie.release_year,genre =movie.genre, director=movie.director, added_by=user.id)
    session.add(db_movie)
    session.commit()
    session.refresh(db_movie)
    return {"message": f"Фильм{movie.title} успешно добавлен"}

@router.post("/ratings/", response_model=RatingResponse)
def create_rating(rating: RatingCreate, session = Depends(get_session)):
    db_movie = session.get(Movie, rating.movie_id)
    if not db_movie:
        raise HTTPException(status_code=404, detail="Фильм не найден")
    db_user = session.get(User, rating.user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    db_rating = Rating(rating=rating.rating, user_id=rating.user_id, movie_id=rating.movie_id)
    session.add(db_rating)
    session.commit()
    session.refresh(db_rating)
    return db_rating

@router.put("/movies/{movie_id}/")
def update_movie(movie_id: int, movie: MovieCreate, session=Depends(get_session)):
    db_movie = session.get(Movie, movie_id)
    if not db_movie:
        raise HTTPException(status_code=404, detail="Фильм не найден")
    db_movie.title = movie.title
    db_movie.description = movie.description
    db_movie.release_year = movie.release_year
    db_movie.genre = movie.genre
    db_movie.director = movie.director
    session.commit()
    return db_movie

@router.get("/movies/{movie_id}/", response_model=MovieResponse)
def get_movie(movie_id: int, session=Depends(get_session)):
    db_movie = session.get(Movie, movie_id)
    if not db_movie:
        raise HTTPException(status_code=404, detail="Фильм не найден")
    result = session.exec(
        select(func.avg(Rating.rating))
        .where(Rating.movie_id == movie_id)
    ).one()
    avg_rating = result or 0

    # Возвращаем объект MovieResponse с добавленным рейтингом
    return MovieResponse(
        **db_movie.dict(),
        average_rating=round(avg_rating, 2)
    )