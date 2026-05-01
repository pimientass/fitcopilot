from dataclasses import dataclass
from uuid import UUID

from fitcopilot.modules.requirements.domain.value_objects import (
    Calories,
    CarbsGrams,
    FatGrams,
    ProteinGrams,
)


@dataclass(frozen=True, slots=True)
class NutritionRequirements:
    user_id: UUID
    maintenance_calories: Calories
    target_calories: Calories
    protein_grams: ProteinGrams
    carbs_grams: CarbsGrams
    fat_grams: FatGrams
