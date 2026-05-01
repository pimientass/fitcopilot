from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from fitcopilot.modules.catalog.domain.value_objects import BrandName, ProductName, StoreName


@dataclass(frozen=True, slots=True)
class Product:
    id: UUID
    name: ProductName
    brand: BrandName | None
    store: StoreName | None
    category: str | None
    barcode: str | None
    serving_size_g: float | None
    calories_per_100g: int | None
    protein_per_100g: int | None
    carbs_per_100g: int | None
    fat_per_100g: int | None
    created_at: datetime
