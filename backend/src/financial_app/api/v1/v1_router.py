from fastapi import APIRouter

from financial_app.config import settings

from .controllers.category_controller import router as category_router
from .controllers.expense_record_controller import router as expense_record_router
from .controllers.health_controller import router as health_router
from .controllers.subcategory_controller import router as subcategory_router

v1_router = APIRouter(prefix=f"{settings.API_PREFIX}/v1")

v1_router.include_router(health_router)
v1_router.include_router(category_router)
v1_router.include_router(subcategory_router)
v1_router.include_router(expense_record_router)
