from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from fitcopilot.modules.recipes.domain.value_objects import (
    IngredientName,
    QuantityGrams,
    RecipeName,
    StepNumber,
    StepText,
)


@dataclass(frozen=True, slots=True)
class RecipeIngredient:
    name: IngredientName
    quantity_g: QuantityGrams


@dataclass(frozen=True, slots=True)
class RecipeStep:
    number: StepNumber
    text: StepText
    time_minutes: int | None = None


@dataclass(frozen=True, slots=True)
class Recipe:
    id: UUID
    name: RecipeName
    description: str | None
    servings: int
    ingredients: list[RecipeIngredient]
    steps: list[RecipeStep]
    calories_total: int | None
    protein_total_g: int | None
    carbs_total_g: int | None
    fat_total_g: int | None
    created_at: datetime
