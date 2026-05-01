from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Calories:
    value: int

    def __post_init__(self) -> None:
        if self.value <= 0:
            raise ValueError("calories must be greater than 0")


@dataclass(frozen=True, slots=True)
class ProteinGrams:
    value: int

    def __post_init__(self) -> None:
        if self.value < 0:
            raise ValueError("protein grams must be >= 0")


@dataclass(frozen=True, slots=True)
class CarbsGrams:
    value: int

    def __post_init__(self) -> None:
        if self.value < 0:
            raise ValueError("carbs grams must be >= 0")


@dataclass(frozen=True, slots=True)
class FatGrams:
    value: int

    def __post_init__(self) -> None:
        if self.value < 0:
            raise ValueError("fat grams must be >= 0")
