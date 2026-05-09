from datetime import datetime

from sqlalchemy.orm import Session

from financial_app.api.v1.models import dto_category
from financial_app.db.schemas.schemas import CategorySchema


def create(
    category: dto_category.CategoryCreate,
    *,
    now: datetime,
    session: Session,
) -> CategorySchema:
    db_category = CategorySchema(
        name=category.name,
        created_at=now,
        updated_at=now,
    )
    session.add(db_category)
    session.flush()
    return db_category


def get_by_id(category_id: int, session: Session) -> CategorySchema | None:
    return (
        session.query(CategorySchema)
        .filter(CategorySchema.id == category_id)
        .first()
    )


def get_by_name(name: str, session: Session) -> CategorySchema | None:
    return (
        session.query(CategorySchema)
        .filter(CategorySchema.name == name)
        .first()
    )


def get_all(session: Session) -> list[CategorySchema]:
    return session.query(CategorySchema).order_by(CategorySchema.name).all()
