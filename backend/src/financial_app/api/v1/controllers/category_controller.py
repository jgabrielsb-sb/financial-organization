from typing import Any, Generator

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from financial_app.api.v1.models import dto_category, dto_responses
from financial_app.api.v1.services import category_service
from financial_app.db.session import get_db

router = APIRouter(
    prefix="/categories",
    tags=["v1/categories"],
)


@router.get(
    "/",
    response_model=list[dto_category.CategoryResponse],
    status_code=200,
    summary="List all categories",
)
async def get_all_categories(
    session: Generator[Session, Any, None] = Depends(get_db),
) -> list[dto_category.CategoryResponse]:
    return category_service.get_all_categories(session=session)


@router.post(
    "/",
    response_model=dto_category.CategoryResponse,
    status_code=201,
    summary="Create a category",
    responses={
        409: {"description": "Conflict", "model": dto_responses.Error409Response},
        422: {"description": "Unprocessable Entity", "model": dto_responses.Error422Response},
    },
)
async def create_category(
    category_create: dto_category.CategoryCreate,
    session: Generator[Session, Any, None] = Depends(get_db),
) -> dto_category.CategoryResponse:
    return category_service.create_category(
        category_create=category_create,
        session=session,
    )


@router.get(
    "/{category_id}",
    response_model=dto_category.CategoryResponse,
    status_code=200,
    summary="Get category by id",
    responses={
        404: {"description": "Category not found", "model": dto_responses.Error404Response},
        422: {"description": "Unprocessable Entity", "model": dto_responses.Error422Response},
    },
)
async def get_category_by_id(
    category_id: int,
    session: Generator[Session, Any, None] = Depends(get_db),
) -> dto_category.CategoryResponse:
    return category_service.get_category_by_id(
        category_id=category_id,
        session=session,
    )
