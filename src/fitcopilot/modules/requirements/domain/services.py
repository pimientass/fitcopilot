from fitcopilot.modules.body_profile.domain.entities import BodyProfile
from fitcopilot.modules.body_profile.domain.value_objects import ActivityLevel, GoalType, Sex
from fitcopilot.modules.requirements.domain.entities import NutritionRequirements
from fitcopilot.modules.requirements.domain.value_objects import (
    Calories,
    CarbsGrams,
    FatGrams,
    ProteinGrams,
)


class RequirementsCalculator:
    ACTIVITY_FACTORS = {
        ActivityLevel.SEDENTARY: 1.2,
        ActivityLevel.LIGHT: 1.375,
        ActivityLevel.MODERATE: 1.55,
        ActivityLevel.HIGH: 1.725,
        ActivityLevel.VERY_HIGH: 1.9,
    }

    def calculate(self, profile: BodyProfile) -> NutritionRequirements:
        maintenance = self._calculate_maintenance(profile)
        target = self._apply_goal_adjustment(maintenance, profile.goal)

        protein_per_kg = 2.0 if profile.goal == GoalType.CUT else 1.8
        protein_grams = round(profile.weight_kg.value * protein_per_kg)
        fat_grams = round(profile.weight_kg.value * 0.8)

        protein_calories = protein_grams * 4
        fat_calories = fat_grams * 9
        carb_calories = max(target - protein_calories - fat_calories, 0)
        carbs_grams = round(carb_calories / 4)

        return NutritionRequirements(
            user_id=profile.user_id,
            maintenance_calories=Calories(maintenance),
            target_calories=Calories(target),
            protein_grams=ProteinGrams(protein_grams),
            carbs_grams=CarbsGrams(carbs_grams),
            fat_grams=FatGrams(fat_grams),
        )

    def _calculate_maintenance(self, profile: BodyProfile) -> int:
        if profile.sex == Sex.MALE:
            bmr = (
                10 * profile.weight_kg.value
                + 6.25 * profile.height_cm.value
                - 5 * profile.age_years.value
                + 5
            )
        else:
            bmr = (
                10 * profile.weight_kg.value
                + 6.25 * profile.height_cm.value
                - 5 * profile.age_years.value
                - 161
            )

        factor = self.ACTIVITY_FACTORS[profile.activity_level]
        return round(bmr * factor)

    def _apply_goal_adjustment(self, maintenance: int, goal: GoalType) -> int:
        if goal == GoalType.CUT:
            return round(maintenance * 0.85)
        if goal == GoalType.BULK:
            return round(maintenance * 1.10)
        return maintenance
