from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from database import get_db, MovieModel
from schemas import MovieListResponseSchema, MovieDetailResponseSchema

router = APIRouter()


@router.get("/movies/", response_model=MovieListResponseSchema)
async def get_movies(db: AsyncSession = Depends(get_db), page: int = Query(1, ge=1), per_page: int = Query(10, ge=1, le=20)):
    result = await db.execute(select(MovieModel).limit(per_page).offset((page - 1) * per_page))
    movies = result.scalars().all()

    if not movies:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "No movies found.")

    return movies


@router.get("/movies/{movie_id}", response_model=MovieDetailResponseSchema)
async def get_movie(db: AsyncSession = Depends(get_db), movie_id: int | None = None):
    result = await db.exeute(select(MovieModel).where(MovieModel.id == movie_id))
    movie = result.scalars().first()

    if not movie:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie with the given ID was not found")
    return movie
