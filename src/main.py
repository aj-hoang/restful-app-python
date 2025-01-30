import logging
import sys
from contextlib import asynccontextmanager
from typing import List, Annotated

from database import get_session, create_db_and_tables
from fastapi import FastAPI, status, HTTPException, Depends
from fastapi.responses import JSONResponse
from sqlmodel import Session, select
from models import Movie, MovieCreate, MovieUpdate
from utils import clean_genre


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    "%(asctime)s [%(processName)s: %(process)d] [%(threadName)s: %(thread)d] [%(levelname)s] %(name)s: %(message)s"
)

stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setFormatter(formatter)
file_handler = logging.FileHandler("info.log")
file_handler.setFormatter(formatter)

logger.addHandler(stream_handler)
logger.addHandler(file_handler)


# Create tables on startup
@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)

SessionDep = Annotated[Session, Depends(get_session)]


@app.get("/")
async def get_root():
    return {"Welcome": "Hello"}


@app.get("/movies/", response_model=List[Movie])
async def get_movies(*, session: SessionDep):
    """
    Get Movies
    """
    logger.info("Getting Movies..")
    statement = select(Movie)
    movies = session.exec(statement)

    return movies


@app.get("/movies/{movie_id}", response_model=Movie)
async def get_movie(*, session: SessionDep, movie_id: int):
    """
    Get Movie for a supplied movie id
    """
    logger.info(f"Getting Movie with movie_id: {movie_id}")
    session_movie = session.get(Movie, movie_id)

    if not session_movie:
        raise HTTPException(status_code=404, detail="Movie not found.")

    return session_movie


@app.post("/movies/", response_model=Movie)
async def create_movie(*, session: SessionDep, movie_in: MovieCreate):
    """
    Create Movie
    """
    logger.info("Creating Movie..")
    db_movie = Movie.model_validate(
        movie_in, update={"genre": clean_genre(movie_in.genre)}
    )
    session.add(db_movie)
    session.commit()
    session.refresh(db_movie)

    return db_movie


@app.put("/movies/{movie_id}")
async def update_movie(
    *, session: SessionDep, movie_id: int, movie_in: MovieUpdate
):
    """
    Update movie
    """
    logger.info(f"Updating movie, movie_id: {movie_id}")
    db_movie: Movie = session.get(Movie, movie_id)

    if not db_movie:
        raise HTTPException(status_code=404, detail="Movie not found.")

    validated_movie_in = Movie.model_validate(
        movie_in, update={"genre": clean_genre(movie_in.genre)}
    )
    movie_data = validated_movie_in.model_dump(exclude_unset=True)
    db_movie.sqlmodel_update(movie_data)

    session.add(db_movie)
    session.commit()
    session.refresh(db_movie)

    return db_movie


@app.delete("/movies/{movie_id}")
async def delete_movie(*, session: SessionDep, movie_id: int):
    """
    Delete Movie
    """
    logger.info(f"Deleting Movie, movie_id: {movie_id}")
    session_movie = session.get(Movie, movie_id)

    if not session_movie:
        raise HTTPException(status_code=404, detail="Movie not found.")

    session.delete(session_movie)
    session.commit()

    return {"Deleted"}
