from datetime import datetime
from uuid import uuid4

from sqlalchemy import DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from fitcopilot.infrastructure.db.base import Base


class RecipeModel(Base):
    __tablename__ = "recipes"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    name: Mapped[str] = mapped_column(String(255), index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    servings: Mapped[int] = mapped_column(Integer)
    ingredients_json: Mapped[str] = mapped_column(Text)
    steps_json: Mapped[str] = mapped_column(Text)
    calories_total: Mapped[int | None] = mapped_column(Integer, nullable=True)
    protein_total_g: Mapped[int | None] = mapped_column(Integer, nullable=True)
    carbs_total_g: Mapped[int | None] = mapped_column(Integer, nullable=True)
    fat_total_g: Mapped[int | None] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
