from datetime import datetime
from uuid import uuid4

from sqlalchemy import DateTime, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from fitcopilot.infrastructure.db.base import Base


class BodyProfileModel(Base):
    __tablename__ = "body_profiles"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    user_id: Mapped[str] = mapped_column(String(36), index=True)
    weight_kg: Mapped[float] = mapped_column(Float)
    height_cm: Mapped[float] = mapped_column(Float)
    age_years: Mapped[int] = mapped_column(Integer)
    sex: Mapped[str] = mapped_column(String(20))
    activity_level: Mapped[str] = mapped_column(String(20))
    goal: Mapped[str] = mapped_column(String(20))
    measured_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
