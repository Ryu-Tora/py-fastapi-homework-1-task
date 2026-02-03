import math

from fastapi import APIRouter, Depends, HTTPException, Query
from httpx import Request, request
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from database import get_db, MovieModel
from schemas import MovieListResponseSchema, MovieDetailResponseSchema

router = APIRouter()


def build_page_url(request: Request, page: int, per_page: int) -> str:
    return (
        f"{request.url.path}"
        f"?page={page}&per_page={per_page}"
    )


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
    total_items = total_result.scalar()
    total_pages = math.ceil(total_items / per_page) if total_items else 1

    prev_page = (
        build_page_url(request, page - 1, per_page)
        if page > 1
        else None
    )

    next_page = (
        build_page_url(request, page + 1, per_page)
        if page < total_pages
        else None
    )

    return {
        "movies": movies,
        "prev_page": prev_page,
        "next_page": next_page,
        "total_pages": total_pages,
        "total_items": total_items
    }


@router.get("/movies/{movie_id}/", response_model=MovieDetailResponseSchema)
async def get_movie(movie_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(MovieModel).where(MovieModel.id == movie_id))
    movie = result.scalars().first()

    if not movie:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie with the given ID was not found.")
    return movie
