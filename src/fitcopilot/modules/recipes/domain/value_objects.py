from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RecipeName:
    value: str

    def __post_init__(self) -> None:
        if not self.value.strip():
            raise ValueError("recipe name cannot be empty")


@dataclass(frozen=True, slots=True)
class IngredientName:
    value: str

    def __post_init__(self) -> None:
        if not self.value.strip():
            raise ValueError("ingredient name cannot be empty")


@dataclass(frozen=True, slots=True)
class QuantityGrams:
    value: float

    def __post_init__(self) -> None:
        if self.value <= 0:
            raise ValueError("quantity must be greater than 0")


@dataclass(frozen=True, slots=True)
class StepNumber:
    value: int

    def __post_init__(self) -> None:
        if self.value <= 0:
            raise ValueError("step number must be greater than 0")


@dataclass(frozen=True, slots=True)
class StepText:
    value: str

    def __post_init__(self) -> None:
        if not self.value.strip():
            raise ValueError("step text cannot be empty")
