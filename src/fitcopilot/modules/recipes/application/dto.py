from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class RecipeIngredientInput(BaseModel):
    name: str
    quantity_g: float


class RecipeStepInput(BaseModel):
    number: int
    text: str
    time_minutes: int | None = None


class CreateRecipeInput(BaseModel):
    name: str
    description: str | None = None
    servings: int = 1
    ingredients: list[RecipeIngredientInput]
    steps: list[RecipeStepInput]
    calories_total: int | None = None
    protein_total_g: int | None = None
    carbs_total_g: int | None = None
    fat_total_g: int | None = None


class RecipeOutput(BaseModel):
    id: UUID
    name: str
    description: str | None
    servings: int
    ingredients: list[RecipeIngredientInput]
    steps: list[RecipeStepInput]
    calories_total: int | None
    protein_total_g: int | None
    carbs_total_g: int | None
    fat_total_g: int | None
    created_at: datetime
