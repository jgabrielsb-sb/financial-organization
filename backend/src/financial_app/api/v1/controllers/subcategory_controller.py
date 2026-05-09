from typing import Any, Generator

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from financial_app.api.v1.models import dto_responses, dto_subcategory
from financial_app.api.v1.services import subcategory_service
from financial_app.db.session import get_db

router = APIRouter(
    prefix="/subcategories",
    tags=["v1/subcategories"],
)


@router.post(
    "/",
    response_model=dto_subcategory.SubcategoryResponse,
    status_code=201,
    summary="Create a subcategory",
    responses={
        409: {"description": "Conflict", "model": dto_responses.Error409Response},
        422: {"description": "Unprocessable Entity", "model": dto_responses.Error422Response},
    },
)
async def create_subcategory(
    subcategory_create: dto_subcategory.SubcategoryCreate,
    session: Generator[Session, Any, None] = Depends(get_db),
) -> dto_subcategory.SubcategoryResponse:
    return subcategory_service.create_subcategory(
        subcategory_create=subcategory_create,
        session=session,
    )


@router.get(
    "/{subcategory_id}",
    response_model=dto_subcategory.SubcategoryResponse,
    status_code=200,
    summary="Get subcategory by id",
    responses={
        404: {"description": "Subcategory not found", "model": dto_responses.Error404Response},
        422: {"description": "Unprocessable Entity", "model": dto_responses.Error422Response},
    },
)
async def get_subcategory_by_id(
    subcategory_id: int,
    session: Generator[Session, Any, None] = Depends(get_db),
) -> dto_subcategory.SubcategoryResponse:
    return subcategory_service.get_subcategory_by_id(
        subcategory_id=subcategory_id,
        session=session,
    )
