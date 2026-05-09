from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class SubcategoryCreate(BaseModel):
    name: str = Field(..., description="Subcategory name (will be normalized to uppercase without accents)")


class SubcategoryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="Subcategory id")
    name: str = Field(..., description="Subcategory name (normalized)")
    created_at: datetime = Field(..., description="Creation timestamp (UTC)")
    updated_at: datetime = Field(..., description="Last update timestamp (UTC)")
