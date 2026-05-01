from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from fitcopilot.modules.body_profile.domain.value_objects import (
    ActivityLevel,
    GoalType,
    Sex,
)


class CreateBodyProfileInput(BaseModel):
    user_id: UUID
    weight_kg: float
    height_cm: float
    age_years: int
    sex: Sex
    activity_level: ActivityLevel
    goal: GoalType
    measured_at: datetime


class BodyProfileOutput(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID
    weight_kg: float
    height_cm: float
    age_years: int
    sex: Sex
    activity_level: ActivityLevel
    goal: GoalType
    measured_at: datetime
    created_at: datetime
