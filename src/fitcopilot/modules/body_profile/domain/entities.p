from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from fitcopilot.modules.body_profile.domain.value_objects import (
    ActivityLevel,
    AgeYears,
    GoalType,
    HeightCm,
    Sex,
    WeightKg,
)


@dataclass(frozen=True, slots=True)
class BodyProfile:
    id: UUID
    user_id: UUID
    weight_kg: WeightKg
    height_cm: HeightCm
    age_years: AgeYears
    sex: Sex
    activity_level: ActivityLevel
    goal: GoalType
    measured_at: datetime
    created_at: datetime
