from datetime import UTC, datetime
from uuid import uuid4

from fitcopilot.modules.recipes.application.dto import (
    CreateRecipeInput,
    RecipeOutput,
)
from fitcopilot.modules.recipes.domain.entities import Recipe, RecipeIngredient, RecipeStep
from fitcopilot.modules.recipes.domain.repositories import RecipeRepository
from fitcopilot.modules.recipes.domain.value_objects import (
    IngredientName,
    QuantityGrams,
    RecipeName,
    StepNumber,
    StepText,
)


class CreateRecipe:
    def __init__(self, repository: RecipeRepository) -> None:
        self._repository = repository

    def execute(self, data: CreateRecipeInput) -> RecipeOutput:
        recipe = Recipe(
            id=uuid4(),
            name=RecipeName(data.name),
            description=data.description,
            servings=data.servings,
            ingredients=[
                RecipeIngredient(
                    name=IngredientName(item.name),
                    quantity_g=QuantityGrams(item.quantity_g),
                )
                for item in data.ingredients
            ],
            steps=[
                RecipeStep(
                    number=StepNumber(step.number),
                    text=StepText(step.text),
                    time_minutes=step.time_minutes,
                )
                for step in data.steps
            ],
            calories_total=data.calories_total,
            protein_total_g=data.protein_total_g,
            carbs_total_g=data.carbs_total_g,
            fat_total_g=data.fat_total_g,
            created_at=datetime.now(UTC),
        )
        self._repository.save(recipe)

        return RecipeOutput(
            id=recipe.id,
            name=recipe.name.value,
            description=recipe.description,
            servings=recipe.servings,
            ingredients=data.ingredients,
            steps=data.steps,
            calories_total=recipe.calories_total,
            protein_total_g=recipe.protein_total_g,
            carbs_total_g=recipe.carbs_total_g,
            fat_total_g=recipe.fat_total_g,
            created_at=recipe.created_at,
        )
