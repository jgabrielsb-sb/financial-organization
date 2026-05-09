from datetime import datetime

from sqlalchemy.orm import Session

from financial_app.api.v1.models import dto_subcategory
from financial_app.db.schemas.schemas import SubcategorySchema


def create(
    subcategory: dto_subcategory.SubcategoryCreate,
    *,
    now: datetime,
    session: Session,
) -> SubcategorySchema:
    db_subcategory = SubcategorySchema(
        name=subcategory.name,
        created_at=now,
        updated_at=now,
    )
    session.add(db_subcategory)
    session.flush()
    return db_subcategory


def get_by_id(subcategory_id: int, session: Session) -> SubcategorySchema | None:
    return (
        session.query(SubcategorySchema)
        .filter(SubcategorySchema.id == subcategory_id)
        .first()
    )


def get_by_name(name: str, session: Session) -> SubcategorySchema | None:
    return (
        session.query(SubcategorySchema)
        .filter(SubcategorySchema.name == name)
        .first()
    )
