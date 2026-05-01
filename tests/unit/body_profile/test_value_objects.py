import pytest

from fitcopilot.modules.body_profile.domain.value_objects import (
    AgeYears,
    HeightCm,
    WeightKg,
)


def test_weight_kg_accepts_valid_value() -> None:
    weight = WeightKg(78.5)
    assert weight.value == 78.5


@pytest.mark.parametrize("value", [0, -1, 10, 500])
def test_weight_kg_rejects_invalid_values(value: float) -> None:
    with pytest.raises(ValueError):
        WeightKg(value)


def test_height_cm_accepts_valid_value() -> None:
    height = HeightCm(178)
    assert height.value == 178


@pytest.mark.parametrize("value", [0, -10, 90, 300])
def test_height_cm_rejects_invalid_values(value: float) -> None:
    with pytest.raises(ValueError):
        HeightCm(value)


def test_age_years_accepts_valid_value() -> None:
    age = AgeYears(31)
    assert age.value == 31


@pytest.mark.parametrize("value", [0, -1, 10, 120])
def test_age_years_rejects_invalid_values(value: int) -> None:
    with pytest.raises(ValueError):
        AgeYears(value)
