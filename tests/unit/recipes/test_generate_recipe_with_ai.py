from datetime import UTC, datetime
from uuid import uuid4

from fitcopilot.modules.ai.application.ports.recipe_generator import RecipeGenerator
from fitcopilot.modules.ai.infrastructure.ollama.schemas import (
    GeneratedRecipeIngredient,
    GeneratedRecipePayload,
    GeneratedRecipeStep,
)
from fitcopilot.modules.catalog.domain.entities import Product
from fitcopilot.modules.catalog.domain.repositories import ProductRepository
from fitcopilot.modules.catalog.domain.value_objects import BrandName, ProductName, StoreName
from fitcopilot.modules.requirements.application.dto import NutritionRequirementsOutput
from fitcopilot.modules.recipes.application.use_cases.create_recipe import CreateRecipe
from fitcopilot.modules.recipes.application.use_cases.generate_recipe_with_ai import (
    GenerateRecipeWithAI,
)
from fitcopilot.modules.recipes.domain.entities import Recipe
from fitcopilot.modules.recipes.domain.repositories import RecipeRepository
from fitcopilot.modules.recipes.domain.services import RecipeNutritionCalculator


class FakeRecipeRepository(RecipeRepository):
    def __init__(self) -> None:
        self.saved: Recipe | None = None

    def save(self, recipe: Recipe) -> None:
        self.saved = recipe

    def get_by_id(self, recipe_id):
        if self.saved and self.saved.id == recipe_id:
            return self.saved
        return None


class FakeProductRepository(ProductRepository):
    def __init__(self, products: list[Product]) -> None:
        self._products = products

    def save(self, product: Product) -> None:
        self._products.append(product)

    def search(self, query: str) -> list[Product]:
        return [p for p in self._products if query.lower() in p.name.value.lower()]

    def get_by_id(self, product_id):
        for product in self._products:
            if product.id == product_id:
                return product
        return None


class FakeRecipeGenerator(RecipeGenerator):
    def generate_recipe(
        self,
        *,
        goal: str,
        calories_target: int,
        protein_target: int,
        preferred_ingredients: list[str],
    ) -> GeneratedRecipePayload:
        return GeneratedRecipePayload(
            name="Bowl fitness AI",
            description="Receta generada por IA",
            servings=1,
            ingredients=[
                GeneratedRecipeIngredient(
                    name="Yogur griego natural",
                    quantity_g=170,
                )
            ],
            steps=[
                GeneratedRecipeStep(
                    number=1,
                    text="Mezclar y servir",
                    time_minutes=2,
                )
            ],
        )


def test_generate_recipe_with_ai_creates_recipe_from_structured_output() -> None:
    product = Product(
        id=uuid4(),
        name=ProductName("Yogur griego natural"),
        brand=BrandName("Hacendado"),
        store=StoreName("Mercadona"),
        category="Dairy",
        barcode=None,
        serving_size_g=170,
        calories_per_100g=97,
        protein_per_100g=9,
        carbs_per_100g=3,
        fat_per_100g=4,
        created_at=datetime(2026, 5, 2, 10, 0, 0, tzinfo=UTC),
    )

    recipe_repository = FakeRecipeRepository()
    product_repository = FakeProductRepository([product])
    calculator = RecipeNutritionCalculator(product_repository)
    create_recipe = CreateRecipe(recipe_repository, calculator)
    recipe_generator = FakeRecipeGenerator()

    use_case = GenerateRecipeWithAI(
        recipe_generator=recipe_generator,
        create_recipe_use_case=create_recipe,
    )

    requirements = NutritionRequirementsOutput(
        user_id=uuid4(),
        maintenance_calories=2709,
        target_calories=2303,
        protein_grams=157,
        carbs_grams=277,
        fat_grams=63,
    )

    result = use_case.execute(
        requirements=requirements,
        goal="cut",
        preferred_ingredients=["Yogur griego natural"],
    )

    assert result.name == "Bowl fitness AI"
    assert result.calories_total == 165
    assert result.protein_total_g == 15
    assert recipe_repository.saved is not None
