from fitcopilot.modules.ai.application.ports.recipe_generator import RecipeGenerator
from fitcopilot.modules.recipes.application.dto import (
    CreateRecipeInput,
    RecipeIngredientInput,
    RecipeOutput,
    RecipeStepInput,
)
from fitcopilot.modules.recipes.application.use_cases.create_recipe import CreateRecipe
from fitcopilot.modules.requirements.application.dto import NutritionRequirementsOutput


class GenerateRecipeWithAI:
    def __init__(
        self,
        recipe_generator: RecipeGenerator,
        create_recipe_use_case: CreateRecipe,
    ) -> None:
        self._recipe_generator = recipe_generator
        self._create_recipe_use_case = create_recipe_use_case

    def execute(
        self,
        *,
        requirements: NutritionRequirementsOutput,
        goal: str,
        preferred_ingredients: list[str],
    ) -> RecipeOutput:
        generated = self._recipe_generator.generate_recipe(
            goal=goal,
            calories_target=requirements.target_calories,
            protein_target=requirements.protein_grams,
            preferred_ingredients=preferred_ingredients,
        )

        return self._create_recipe_use_case.execute(
            CreateRecipeInput(
                name=generated.name,
                description=generated.description,
                servings=generated.servings,
                ingredients=[
                    RecipeIngredientInput(
                        name=item.name,
                        quantity_g=item.quantity_g,
                    )
                    for item in generated.ingredients
                ],
                steps=[
                    RecipeStepInput(
                        number=step.number,
                        text=step.text,
                        time_minutes=step.time_minutes,
                    )
                    for step in generated.steps
                ],
            )
        )
