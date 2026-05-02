from datetime import UTC, datetime
from uuid import uuid4

from fitcopilot.modules.catalog.domain.entities import Product
from fitcopilot.modules.catalog.domain.repositories import ProductRepository
from fitcopilot.modules.catalog.domain.value_objects import BrandName, ProductName, StoreName
from fitcopilot.modules.recipes.application.dto import (
    CreateRecipeInput,
    RecipeIngredientInput,
    RecipeStepInput,
)
from fitcopilot.modules.recipes.application.use_cases.create_recipe import CreateRecipe
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


def test_create_recipe_calculates_and_persists_totals() -> None:
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
        created_at=datetime(2026, 5, 1, 22, 0, 0, tzinfo=UTC),
    )

    recipe_repository = FakeRecipeRepository()
    product_repository = FakeProductRepository([product])
    calculator = RecipeNutritionCalculator(product_repository)
    use_case = CreateRecipe(recipe_repository, calculator)

    result = use_case.execute(
        CreateRecipeInput(
            name="Bowl fitness",
            servings=1,
            ingredients=[
                RecipeIngredientInput(
                    name="Yogur griego natural",
                    quantity_g=170,
                )
            ],
            steps=[
                RecipeStepInput(
                    number=1,
                    text="Mezclar y servir",
                    time_minutes=2,
                )
            ],
        )
    )

    assert result.calories_total == 165
    assert result.protein_total_g == 15
    assert result.carbs_total_g == 5
    assert result.fat_total_g == 7

    assert recipe_repository.saved is not None
    assert recipe_repository.saved.calories_total == 165
