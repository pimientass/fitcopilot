from uuid import UUID

from pydantic import BaseModel


class CalculateRequirementsInput(BaseModel):
    user_id: UUID


class NutritionRequirementsOutput(BaseModel):
    user_id: UUID
    maintenance_calories: int
    target_calories: int
    protein_grams: int
    carbs_grams: int
    fat_grams: int
