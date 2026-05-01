from dataclasses import dataclass
from enum import StrEnum


class Sex(StrEnum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"


class ActivityLevel(StrEnum):
    SEDENTARY = "sedentary"
    LIGHT = "light"
    MODERATE = "moderate"
    HIGH = "high"
    VERY_HIGH = "very_high"


class GoalType(StrEnum):
    CUT = "cut"
    MAINTAIN = "maintain"
    BULK = "bulk"


@dataclass(frozen=True, slots=True)
class WeightKg:
    value: float

    def __post_init__(self) -> None:
        if self.value <= 0:
            raise ValueError("weight_kg must be greater than 0")
        if self.value < 25 or self.value > 400:
            raise ValueError("weight_kg is outside a realistic range")


@dataclass(frozen=True, slots=True)
class HeightCm:
    value: float

    def __post_init__(self) -> None:
        if self.value <= 0:
            raise ValueError("height_cm must be greater than 0")
        if self.value < 100 or self.value > 260:
            raise ValueError("height_cm is outside a realistic range")


@dataclass(frozen=True, slots=True)
class AgeYears:
    value: int

    def __post_init__(self) -> None:
        if self.value <= 0:
            raise ValueError("age_years must be greater than 0")
        if self.value < 14 or self.value > 100:
            raise ValueError("age_years is outside supported range")
