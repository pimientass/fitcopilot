from datetime import UTC, datetime
from uuid import uuid4

from fitcopilot.modules.recipes.application.dto import (
    CreateRecipeInput,
    RecipeOutput,
    RecipeIngredientInput,
    RecipeStepInput,
)
from fitcopilot.modules.recipes.domain.entities import Recipe, RecipeIngredient, RecipeStep
from fitcopilot.modules.recipes.domain.repositories import RecipeRepository
from fitcopilot.modules.recipes.domain.services import RecipeNutritionCalculator
from fitcopilot.modules.recipes.domain.value_objects import (
    IngredientName,
    QuantityGrams,
    RecipeName,
    StepNumber,
    StepText,
)


class CreateRecipe:
    def __init__(
        self,
        repository: RecipeRepository,
        nutrition_calculator: RecipeNutritionCalculator,
    ) -> None:
        self._repository = repository
        self._nutrition_calculator = nutrition_calculator

    def execute(self, data: CreateRecipeInput) -> RecipeOutput:
        draft_recipe = Recipe(
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
            calories_total=None,
            protein_total_g=None,
            carbs_total_g=None,
            fat_total_g=None,
            created_at=datetime.now(UTC),
        )

        calories_total, protein_total_g, carbs_total_g, fat_total_g = (
            self._nutrition_calculator.calculate_totals(draft_recipe)
        )

        recipe = Recipe(
            id=draft_recipe.id,
            name=draft_recipe.name,
            description=draft_recipe.description,
            servings=draft_recipe.servings,
            ingredients=draft_recipe.ingredients,
            steps=draft_recipe.steps,
            calories_total=calories_total,
            protein_total_g=protein_total_g,
            carbs_total_g=carbs_total_g,
            fat_total_g=fat_total_g,
            created_at=draft_recipe.created_at,
        )

        self._repository.save(recipe)

        return RecipeOutput(
            id=recipe.id,
            name=recipe.name.value,
            description=recipe.description,
            servings=recipe.servings,
            ingredients=[
                RecipeIngredientInput(
                    name=item.name.value,
                    quantity_g=item.quantity_g.value,
                )
                for item in recipe.ingredients
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
