from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class ExpenseRecordCreate(BaseModel):
    category_id: int = Field(..., description="ID of the category")
    total: Decimal = Field(..., gt=0, decimal_places=2, description="Total amount (positive)")
    description: str = Field(..., min_length=1, description="Short description of the expense")
    notes: str | None = Field(None, description="Optional additional notes")
    day: date = Field(..., description="Date of the expense (day/month/year)")
    fixed: bool = Field(False, description="Whether this is a fixed recurring expense")
    essential: bool = Field(False, description="Whether this is an essential expense")


class ExpenseRecordUpdate(BaseModel):
    category_id: int = Field(..., description="ID of the category")
    total: Decimal = Field(..., gt=0, decimal_places=2, description="Total amount (positive)")
    description: str = Field(..., min_length=1, description="Short description of the expense")
    notes: str | None = Field(None, description="Optional additional notes")
    day: date = Field(..., description="Date of the expense (day/month/year)")
    fixed: bool = Field(False, description="Whether this is a fixed recurring expense")
    essential: bool = Field(False, description="Whether this is an essential expense")


class ExpenseRecordResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="Expense record id")
    category_id: int = Field(..., description="ID of the category")
    total: Decimal = Field(..., description="Total amount")
    description: str = Field(..., description="Short description of the expense")
    notes: str | None = Field(None, description="Optional additional notes")
    day: date = Field(..., description="Date of the expense")
    fixed: bool = Field(..., description="Whether this is a fixed recurring expense")
    essential: bool = Field(..., description="Whether this is an essential expense")
    created_at: datetime = Field(..., description="Creation timestamp (UTC)")
    updated_at: datetime = Field(..., description="Last update timestamp (UTC)")
