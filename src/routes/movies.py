import math

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from database import get_db, MovieModel
from schemas import MovieListResponseSchema, MovieDetailResponseSchema

router = APIRouter()


@router.get("/movies/", response_model=MovieListResponseSchema)
async def get_movies(
        db: AsyncSession = Depends(get_db),
        page: int = Query(1, ge=1),
        per_page: int = Query(10, ge=1, le=20)
):
    offset = (page - 1) * per_page
    result = await db.execute(select(MovieModel).limit(per_page).offset(offset))
    movies = result.scalars().all()

    if not movies:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No movies found.")

    total_result = await db.execute(select(func.count()).select_from(MovieModel))
    total_items = total_result.scalars()
    total_pages = math.cell(total_items / per_page) if total_items else 1

    return {
        "movies": movies,
        "prev_page": page - 1 if page > 1 else None,
        "next_page": page + 1 if page < total_pages else None,
        "total_pages": total_pages,
        "total_items": total_items
    }


@router.get("/movies/{movie_id}", response_model=MovieDetailResponseSchema)
async def get_movie(db: AsyncSession = Depends(get_db), movie_id: int | None = None):
    result = await db.execute(select(MovieModel).where(MovieModel.id == movie_id))
    movie = result.scalars().first()

    if not movie:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie with the given ID was not found.")
    return movie
