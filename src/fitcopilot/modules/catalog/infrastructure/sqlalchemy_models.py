from datetime import datetime
from uuid import uuid4

from sqlalchemy import DateTime, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from fitcopilot.infrastructure.db.base import Base


class ProductModel(Base):
    __tablename__ = "products"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    name: Mapped[str] = mapped_column(String(255), index=True)
    brand: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    store: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    category: Mapped[str | None] = mapped_column(String(255), nullable=True)
    barcode: Mapped[str | None] = mapped_column(String(64), nullable=True, index=True)
    serving_size_g: Mapped[float | None] = mapped_column(Float, nullable=True)
    calories_per_100g: Mapped[int | None] = mapped_column(Integer, nullable=True)
    protein_per_100g: Mapped[int | None] = mapped_column(Integer, nullable=True)
    carbs_per_100g: Mapped[int | None] = mapped_column(Integer, nullable=True)
    fat_per_100g: Mapped[int | None] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
