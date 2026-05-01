from uuid import UUID

from fitcopilot.modules.recipes.application.dto import (
    RecipeIngredientInput,
    RecipeOutput,
    RecipeStepInput,
)
from fitcopilot.modules.recipes.domain.repositories import RecipeRepository


class GetRecipe:
    def __init__(self, repository: RecipeRepository) -> None:
        self._repository = repository

    def execute(self, recipe_id: UUID) -> RecipeOutput | None:
        recipe = self._repository.get_by_id(recipe_id)
        if recipe is None:
            return None

        return RecipeOutput(
            id=recipe.id,
            name=recipe.name.value,
            description=recipe.description,
            servings=recipe.servings,
            ingredients=[
                RecipeIngredientInput(
                    name=ingredient.name.value,
                    quantity_g=ingredient.quantity_g.value,
                )
                for ingredient in recipe.ingredients
            ],
            steps=[
                RecipeStepInput(
                    number=step.number.value,
                    text=step.text.value,
                    time_minutes=step.time_minutes,
                )
                for step in recipe.steps
            ],
            calories_total=recipe.calories_total,
            protein_total_g=recipe.protein_total_g,
            carbs_total_g=recipe.carbs_total_g,
            fat_total_g=recipe.fat_total_g,
            created_at=recipe.created_at,
        )
