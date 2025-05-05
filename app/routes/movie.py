from fastapi import APIRouter, Depends, HTTPException,Query
from app.dbs.session import get_session
from app.models.models import Movie, Rating, User
from app.schemas.schemas import MovieCreate, RatingCreate, MovieResponse, RatingResponse
from app.core.security import get_current_user
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
def create_rating(
    rating: RatingCreate,
    current_user: User = Depends(get_current_user),
    session=Depends(get_session)
):
    movie = session.exec(select(Movie).where(Movie.title == rating.title)).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Фильм не найден")

    db_rating = Rating(rating=rating.rating, user_id=current_user.id, movie_id=movie.id)
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

@router.get("/movies/get/", response_model=list[MovieResponse])
def get_movie(
    title: str = Query(..., min_length=1),
    session=Depends(get_session)
):
    movies = session.exec(
        select(Movie).where(func.lower(Movie.title).like(f"%{title.lower()}%"))
    ).all()

    if not movies:
        raise HTTPException(status_code=404, detail="Фильмы не найдены")

    result = []
    for movie in movies:
        avg_rating = session.exec(
            select(func.avg(Rating.rating)).where(Rating.movie_id == movie.id)
        ).one() or 0

        result.append(MovieResponse(
            **movie.dict(),
            average_rating=round(avg_rating, 2)
        ))

    return result