from datetime import date, datetime

from sqlalchemy.orm import Session

from financial_app.api.v1.models import dto_expense_record
from financial_app.db.schemas.schemas import ExpenseRecordSchema


def create(
    expense_record: dto_expense_record.ExpenseRecordCreate,
    *,
    now: datetime,
    session: Session,
) -> ExpenseRecordSchema:
    db_expense_record = ExpenseRecordSchema(
        category_id=expense_record.category_id,
        total=expense_record.total,
        description=expense_record.description,
        notes=expense_record.notes,
        day=expense_record.day,
        fixed=expense_record.fixed,
        essential=expense_record.essential,
        created_at=now,
        updated_at=now,
    )
    session.add(db_expense_record)
    session.flush()
    return db_expense_record


def get_by_id(expense_record_id: int, session: Session) -> ExpenseRecordSchema | None:
    return (
        session.query(ExpenseRecordSchema)
        .filter(ExpenseRecordSchema.id == expense_record_id)
        .first()
    )


def get_all(
    session: Session,
    *,
    category_id: int | None = None,
    date_from: date | None = None,
    date_to: date | None = None,
    page: int = 1,
    per_page: int = 20,
) -> tuple[list[ExpenseRecordSchema], int]:
    query = session.query(ExpenseRecordSchema)
    if category_id is not None:
        query = query.filter(ExpenseRecordSchema.category_id == category_id)
    if date_from is not None:
        query = query.filter(ExpenseRecordSchema.day >= date_from)
    if date_to is not None:
        query = query.filter(ExpenseRecordSchema.day <= date_to)
    total = query.count()
    records = (
        query.order_by(ExpenseRecordSchema.day.desc())
        .offset((page - 1) * per_page)
        .limit(per_page)
        .all()
    )
    return records, total


def update(
    expense_record: ExpenseRecordSchema,
    data: dto_expense_record.ExpenseRecordUpdate,
    *,
    now: datetime,
    session: Session,
) -> ExpenseRecordSchema:
    expense_record.category_id = data.category_id
    expense_record.total = data.total
    expense_record.description = data.description
    expense_record.notes = data.notes
    expense_record.day = data.day
    expense_record.fixed = data.fixed
    expense_record.essential = data.essential
    expense_record.updated_at = now
    session.flush()
    return expense_record


def delete(expense_record: ExpenseRecordSchema, session: Session) -> None:
    session.delete(expense_record)
    session.flush()
