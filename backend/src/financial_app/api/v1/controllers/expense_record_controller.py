from datetime import date
from typing import Any, Generator

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from financial_app.api.v1.models import dto_expense_record, dto_responses
from financial_app.api.v1.services import expense_record_service
from financial_app.db.session import get_db

router = APIRouter(
    prefix="/expense-records",
    tags=["v1/expense-records"],
)


@router.get(
    "/",
    response_model=dto_responses.PaginatedResponse[dto_expense_record.ExpenseRecordResponse],
    status_code=200,
    summary="List expense records (paginated, filterable)",
)
async def get_all_expense_records(
    category_id: int | None = Query(None, description="Filter by category ID"),
    date_from: date | None = Query(None, description="Filter by minimum day (inclusive)"),
    date_to: date | None = Query(None, description="Filter by maximum day (inclusive)"),
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(20, ge=1, le=100, description="Items per page"),
    session: Generator[Session, Any, None] = Depends(get_db),
) -> dto_responses.PaginatedResponse[dto_expense_record.ExpenseRecordResponse]:
    return expense_record_service.get_all_expense_records(
        session=session,
        category_id=category_id,
        date_from=date_from,
        date_to=date_to,
        page=page,
        per_page=per_page,
    )


@router.post(
    "/",
    response_model=dto_expense_record.ExpenseRecordResponse,
    status_code=201,
    summary="Create an expense record",
    responses={
        404: {"description": "Category not found", "model": dto_responses.Error404Response},
        422: {"description": "Unprocessable Entity", "model": dto_responses.Error422Response},
    },
)
async def create_expense_record(
    expense_record_create: dto_expense_record.ExpenseRecordCreate,
    session: Generator[Session, Any, None] = Depends(get_db),
) -> dto_expense_record.ExpenseRecordResponse:
    return expense_record_service.create_expense_record(
        expense_record_create=expense_record_create,
        session=session,
    )


@router.get(
    "/{expense_record_id}",
    response_model=dto_expense_record.ExpenseRecordResponse,
    status_code=200,
    summary="Get expense record by id",
    responses={
        404: {"description": "Expense record not found", "model": dto_responses.Error404Response},
        422: {"description": "Unprocessable Entity", "model": dto_responses.Error422Response},
    },
)
async def get_expense_record_by_id(
    expense_record_id: int,
    session: Generator[Session, Any, None] = Depends(get_db),
) -> dto_expense_record.ExpenseRecordResponse:
    return expense_record_service.get_expense_record_by_id(
        expense_record_id=expense_record_id,
        session=session,
    )


@router.put(
    "/{expense_record_id}",
    response_model=dto_expense_record.ExpenseRecordResponse,
    status_code=200,
    summary="Update an expense record",
    responses={
        404: {"description": "Expense record or category not found", "model": dto_responses.Error404Response},
        422: {"description": "Unprocessable Entity", "model": dto_responses.Error422Response},
    },
)
async def update_expense_record(
    expense_record_id: int,
    expense_record_update: dto_expense_record.ExpenseRecordUpdate,
    session: Generator[Session, Any, None] = Depends(get_db),
) -> dto_expense_record.ExpenseRecordResponse:
    return expense_record_service.update_expense_record(
        expense_record_id=expense_record_id,
        expense_record_update=expense_record_update,
        session=session,
    )


@router.delete(
    "/{expense_record_id}",
    status_code=204,
    summary="Delete an expense record",
    responses={
        404: {"description": "Expense record not found", "model": dto_responses.Error404Response},
        422: {"description": "Unprocessable Entity", "model": dto_responses.Error422Response},
    },
)
async def delete_expense_record(
    expense_record_id: int,
    session: Generator[Session, Any, None] = Depends(get_db),
) -> None:
    expense_record_service.delete_expense_record(
        expense_record_id=expense_record_id,
        session=session,
    )
