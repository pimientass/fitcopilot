from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class CreateProductInput(BaseModel):
    name: str
    brand: str | None = None
    store: str | None = None
    category: str | None = None
    barcode: str | None = None
    serving_size_g: float | None = None
    calories_per_100g: int | None = None
    protein_per_100g: int | None = None
    carbs_per_100g: int | None = None
    fat_per_100g: int | None = None


class ProductOutput(BaseModel):
    id: UUID
    name: str
    brand: str | None
    store: str | None
    category: str | None
    barcode: str | None
    serving_size_g: float | None
    calories_per_100g: int | None
    protein_per_100g: int | None
    carbs_per_100g: int | None
    fat_per_100g: int | None
    created_at: datetime
