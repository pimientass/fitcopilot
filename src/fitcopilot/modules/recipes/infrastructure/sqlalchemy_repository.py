import json
from uuid import UUID

from sqlalchemy.orm import Session

from fitcopilot.modules.recipes.domain.entities import Recipe, RecipeIngredient, RecipeStep
from fitcopilot.modules.recipes.domain.repositories import RecipeRepository
from fitcopilot.modules.recipes.domain.value_objects import (
    IngredientName,
    QuantityGrams,
    RecipeName,
    StepNumber,
    StepText,
)
from fitcopilot.modules.recipes.infrastructure.sqlalchemy_models import RecipeModel


class SqlAlchemyRecipeRepository(RecipeRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def save(self, recipe: Recipe) -> None:
        model = RecipeModel(
            id=str(recipe.id),
            name=recipe.name.value,
            description=recipe.description,
            servings=recipe.servings,
            ingredients_json=json.dumps(
                [{"name": i.name.value, "quantity_g": i.quantity_g.value} for i in recipe.ingredients]
            ),
            steps_json=json.dumps(
                [
                    {"number": s.number.value, "text": s.text.value, "time_minutes": s.time_minutes}
                    for s in recipe.steps
                ]
            ),
            calories_total=recipe.calories_total,
            protein_total_g=recipe.protein_total_g,
            carbs_total_g=recipe.carbs_total_g,
            fat_total_g=recipe.fat_total_g,
            created_at=recipe.created_at,
        )
        self._session.add(model)
        self._session.commit()

    def get_by_id(self, recipe_id: UUID) -> Recipe | None:
        model = self._session.get(RecipeModel, str(recipe_id))
        if model is None:
            return None

        ingredients_data = json.loads(model.ingredients_json)
        steps_data = json.loads(model.steps_json)

        return Recipe(
            id=UUID(model.id),
            name=RecipeName(model.name),
            description=model.description,
            servings=model.servings,
            ingredients=[
                RecipeIngredient(
                    name=IngredientName(item["name"]),
                    quantity_g=QuantityGrams(item["quantity_g"]),
                )
                for item in ingredients_data
            ],
            steps=[
                RecipeStep(
                    number=StepNumber(item["number"]),
                    text=StepText(item["text"]),
                    time_minutes=item["time_minutes"],
                )
                for item in steps_data
            ],
            calories_total=model.calories_total,
            protein_total_g=model.protein_total_g,
            carbs_total_g=model.carbs_total_g,
            fat_total_g=model.fat_total_g,
            created_at=model.created_at,
        )
