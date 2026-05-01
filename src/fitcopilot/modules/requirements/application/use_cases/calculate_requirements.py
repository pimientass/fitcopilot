from fitcopilot.modules.body_profile.domain.repositories import BodyProfileRepository
from fitcopilot.modules.requirements.application.dto import (
    CalculateRequirementsInput,
    NutritionRequirementsOutput,
)
from fitcopilot.modules.requirements.domain.services import RequirementsCalculator


class CalculateRequirements:
    def __init__(self, repository: BodyProfileRepository) -> None:
        self._repository = repository
        self._calculator = RequirementsCalculator()

    def execute(self, data: CalculateRequirementsInput) -> NutritionRequirementsOutput:
        profile = self._repository.get_current_by_user_id(data.user_id)

        if profile is None:
            raise ValueError("body profile not found")

        requirements = self._calculator.calculate(profile)

        return NutritionRequirementsOutput(
            user_id=requirements.user_id,
            maintenance_calories=requirements.maintenance_calories.value,
            target_calories=requirements.target_calories.value,
            protein_grams=requirements.protein_grams.value,
            carbs_grams=requirements.carbs_grams.value,
            fat_grams=requirements.fat_grams.value,
        )
