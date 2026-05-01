from datetime import datetime, UTC
from uuid import uuid4

from fitcopilot.modules.body_profile.application.dto import (
    BodyProfileOutput,
    CreateBodyProfileInput,
)
from fitcopilot.modules.body_profile.domain.entities import BodyProfile
from fitcopilot.modules.body_profile.domain.repositories import BodyProfileRepository
from fitcopilot.modules.body_profile.domain.value_objects import (
    ActivityLevel,
    AgeYears,
    GoalType,
    HeightCm,
    Sex,
    WeightKg,
)


class CreateBodyProfile:
    def __init__(self, repository: BodyProfileRepository) -> None:
        self._repository = repository

    def execute(self, data: CreateBodyProfileInput) -> BodyProfileOutput:
        profile = BodyProfile(
            id=uuid4(),
            user_id=data.user_id,
            weight_kg=WeightKg(data.weight_kg),
            height_cm=HeightCm(data.height_cm),
            age_years=AgeYears(data.age_years),
            sex=Sex(data.sex),
            activity_level=ActivityLevel(data.activity_level),
            goal=GoalType(data.goal),
            measured_at=data.measured_at,
            created_at=datetime.now(UTC),
        )

        self._repository.save(profile)

        return BodyProfileOutput(
            id=profile.id,
            user_id=profile.user_id,
            weight_kg=profile.weight_kg.value,
            height_cm=profile.height_cm.value,
            age_years=profile.age_years.value,
            sex=profile.sex,
            activity_level=profile.activity_level,
            goal=profile.goal,
            measured_at=profile.measured_at,
            created_at=profile.created_at,
        )
