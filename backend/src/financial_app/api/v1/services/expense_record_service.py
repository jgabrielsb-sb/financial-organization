from datetime import UTC, date, datetime
from math import ceil

from sqlalchemy.orm import Session

from financial_app.api.v1.models import dto_expense_record, dto_responses
from financial_app.api.v1.repos import category_repo, expense_record_repo
from financial_app.api.v1.services.exceptions import NotFoundException


def create_expense_record(
    expense_record_create: dto_expense_record.ExpenseRecordCreate,
    session: Session,
) -> dto_expense_record.ExpenseRecordResponse:
    category = category_repo.get_by_id(expense_record_create.category_id, session)
    if not category:
        raise NotFoundException(
            resource="id",
            identifier=str(expense_record_create.category_id),
            object="category",
        )

    now = datetime.now(UTC)
    db_expense_record = expense_record_repo.create(
        expense_record_create,
        now=now,
        session=session,
    )
    response = dto_expense_record.ExpenseRecordResponse.model_validate(db_expense_record)
    session.commit()
    return response


def get_all_expense_records(
    session: Session,
    *,
    category_id: int | None = None,
    date_from: date | None = None,
    date_to: date | None = None,
    page: int = 1,
    per_page: int = 20,
) -> dto_responses.PaginatedResponse[dto_expense_record.ExpenseRecordResponse]:
    records, total = expense_record_repo.get_all(
        session,
        category_id=category_id,
        date_from=date_from,
        date_to=date_to,
        page=page,
        per_page=per_page,
    )
    total_pages = ceil(total / per_page) if total > 0 else 1
    return dto_responses.PaginatedResponse(
        data=[dto_expense_record.ExpenseRecordResponse.model_validate(r) for r in records],
        meta=dto_responses.PageMeta(
            page=page,
            per_page=per_page,
            total_items=total,
            total_pages=total_pages,
            has_next=page < total_pages,
            has_previous=page > 1,
        ),
    )


def get_expense_record_by_id(
    expense_record_id: int,
    session: Session,
) -> dto_expense_record.ExpenseRecordResponse:
    db_expense_record = expense_record_repo.get_by_id(expense_record_id, session)

    if not db_expense_record:
        raise NotFoundException(
            resource="id",
            identifier=str(expense_record_id),
            object="expense_record",
        )

    return dto_expense_record.ExpenseRecordResponse.model_validate(db_expense_record)


def update_expense_record(
    expense_record_id: int,
    expense_record_update: dto_expense_record.ExpenseRecordUpdate,
    session: Session,
) -> dto_expense_record.ExpenseRecordResponse:
    db_expense_record = expense_record_repo.get_by_id(expense_record_id, session)
    if not db_expense_record:
        raise NotFoundException(
            resource="id",
            identifier=str(expense_record_id),
            object="expense_record",
        )

    category = category_repo.get_by_id(expense_record_update.category_id, session)
    if not category:
        raise NotFoundException(
            resource="id",
            identifier=str(expense_record_update.category_id),
            object="category",
        )

    now = datetime.now(UTC)
    updated = expense_record_repo.update(db_expense_record, expense_record_update, now=now, session=session)
    response = dto_expense_record.ExpenseRecordResponse.model_validate(updated)
    session.commit()
    return response


def delete_expense_record(expense_record_id: int, session: Session) -> None:
    db_expense_record = expense_record_repo.get_by_id(expense_record_id, session)

    if not db_expense_record:
        raise NotFoundException(
            resource="id",
            identifier=str(expense_record_id),
            object="expense_record",
        )

    expense_record_repo.delete(db_expense_record, session)
    session.commit()
