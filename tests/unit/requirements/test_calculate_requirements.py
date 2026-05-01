from datetime import UTC, datetime
from uuid import uuid4

import pytest

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
from fitcopilot.modules.requirements.application.dto import CalculateRequirementsInput
from fitcopilot.modules.requirements.application.use_cases.calculate_requirements import (
    CalculateRequirements,
)


class FakeBodyProfileRepository(BodyProfileRepository):
    def __init__(self, profile: BodyProfile | None) -> None:
        self._profile = profile

    def save(self, profile: BodyProfile) -> None:
        self._profile = profile

    def get_current_by_user_id(self, user_id):
        if self._profile and self._profile.user_id == user_id:
            return self._profile
        return None


def test_calculate_requirements_returns_values() -> None:
    profile = BodyProfile(
        id=uuid4(),
        user_id=uuid4(),
        weight_kg=WeightKg(80),
        height_cm=HeightCm(180),
        age_years=AgeYears(30),
        sex=Sex.MALE,
        activity_level=ActivityLevel.MODERATE,
        goal=GoalType.MAINTAIN,
        measured_at=datetime(2026, 5, 1, 22, 0, 0, tzinfo=UTC),
        created_at=datetime(2026, 5, 1, 22, 0, 0, tzinfo=UTC),
    )

    use_case = CalculateRequirements(FakeBodyProfileRepository(profile))

    result = use_case.execute(CalculateRequirementsInput(user_id=profile.user_id))

    assert result.user_id == profile.user_id
    assert result.maintenance_calories > 0
    assert result.target_calories == result.maintenance_calories
    assert result.protein_grams > 0
    assert result.carbs_grams >= 0
    assert result.fat_grams > 0


def test_calculate_requirements_raises_if_profile_not_found() -> None:
    use_case = CalculateRequirements(FakeBodyProfileRepository(None))

    with pytest.raises(ValueError, match="body profile not found"):
        use_case.execute(CalculateRequirementsInput(user_id=uuid4()))
