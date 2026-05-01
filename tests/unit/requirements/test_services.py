from datetime import UTC, datetime
from uuid import uuid4

from fitcopilot.modules.body_profile.domain.entities import BodyProfile
from fitcopilot.modules.body_profile.domain.value_objects import (
    ActivityLevel,
    AgeYears,
    GoalType,
    HeightCm,
    Sex,
    WeightKg,
)
from fitcopilot.modules.requirements.domain.services import RequirementsCalculator


def test_calculator_returns_valid_requirements_for_cut_goal() -> None:
    profile = BodyProfile(
        id=uuid4(),
        user_id=uuid4(),
        weight_kg=WeightKg(78.5),
        height_cm=HeightCm(178),
        age_years=AgeYears(31),
        sex=Sex.MALE,
        activity_level=ActivityLevel.MODERATE,
        goal=GoalType.CUT,
        measured_at=datetime(2026, 5, 1, 22, 0, 0, tzinfo=UTC),
        created_at=datetime(2026, 5, 1, 22, 0, 0, tzinfo=UTC),
    )

    result = RequirementsCalculator().calculate(profile)

    assert result.maintenance_calories.value > 0
    assert result.target_calories.value < result.maintenance_calories.value
    assert result.protein_grams.value > 0
    assert result.carbs_grams.value >= 0
    assert result.fat_grams.value > 0
