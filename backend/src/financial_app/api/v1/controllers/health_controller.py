from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from financial_app.api.v1.models import dto_health, dto_responses
from financial_app.api.v1.services import health_service
from financial_app.db.session import get_db

router = APIRouter(
    prefix="/health",
    tags=["v1/health"],
)


@router.get(
    "",
    response_model=dto_health.HealthResponse,
    status_code=200,
    summary="Health check (includes database connectivity)",
    responses={
        422: {"description": "Unprocessable Entity", "model": dto_responses.Error422Response},
    },
)
async def get_health(
    session: Annotated[Session, Depends(get_db)],
) -> dto_health.HealthResponse:
    return health_service.get_health(session)
