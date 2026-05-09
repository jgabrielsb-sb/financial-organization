from datetime import UTC, datetime

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from financial_app.api.v1.models import dto_category
from financial_app.api.v1.repos import category_repo
from financial_app.api.v1.services.exceptions import ConflictException, NotFoundException
from financial_app.utils import normalize_name


def create_category(
    category_create: dto_category.CategoryCreate,
    session: Session,
) -> dto_category.CategoryResponse:
    normalized_name = normalize_name(category_create.name)

    existing = category_repo.get_by_name(normalized_name, session)
    if existing:
        raise ConflictException(
            resource="name",
            identifier=normalized_name,
            object="category",
        )

    try:
        now = datetime.now(UTC)
        db_category = category_repo.create(
            dto_category.CategoryCreate(name=normalized_name),
            now=now,
            session=session,
        )
        response = dto_category.CategoryResponse.model_validate(db_category)
        session.commit()
        return response
    except IntegrityError:
        session.rollback()
        raise ConflictException(
            resource="name",
            identifier=normalized_name,
            object="category",
        ) from None


def get_all_categories(
    session: Session,
) -> list[dto_category.CategoryResponse]:
    return [dto_category.CategoryResponse.model_validate(c) for c in category_repo.get_all(session)]


def get_category_by_id(
    category_id: int,
    session: Session,
) -> dto_category.CategoryResponse:
    db_category = category_repo.get_by_id(category_id, session)

    if not db_category:
        raise NotFoundException(
            resource="id",
            identifier=str(category_id),
            object="category",
        )

    return dto_category.CategoryResponse.model_validate(db_category)
