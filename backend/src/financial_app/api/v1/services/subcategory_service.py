from datetime import UTC, datetime

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from financial_app.api.v1.models import dto_subcategory
from financial_app.api.v1.repos import subcategory_repo
from financial_app.api.v1.services.exceptions import ConflictException, NotFoundException
from financial_app.utils import normalize_name


def create_subcategory(
    subcategory_create: dto_subcategory.SubcategoryCreate,
    session: Session,
) -> dto_subcategory.SubcategoryResponse:
    normalized_name = normalize_name(subcategory_create.name)

    existing = subcategory_repo.get_by_name(normalized_name, session)
    if existing:
        raise ConflictException(
            resource="name",
            identifier=normalized_name,
            object="subcategory",
        )

    try:
        now = datetime.now(UTC)
        db_subcategory = subcategory_repo.create(
            dto_subcategory.SubcategoryCreate(name=normalized_name),
            now=now,
            session=session,
        )
        response = dto_subcategory.SubcategoryResponse.model_validate(db_subcategory)
        session.commit()
        return response
    except IntegrityError:
        session.rollback()
        raise ConflictException(
            resource="name",
            identifier=normalized_name,
            object="subcategory",
        ) from None


def get_subcategory_by_id(
    subcategory_id: int,
    session: Session,
) -> dto_subcategory.SubcategoryResponse:
    db_subcategory = subcategory_repo.get_by_id(subcategory_id, session)

    if not db_subcategory:
        raise NotFoundException(
            resource="id",
            identifier=str(subcategory_id),
            object="subcategory",
        )

    return dto_subcategory.SubcategoryResponse.model_validate(db_subcategory)
