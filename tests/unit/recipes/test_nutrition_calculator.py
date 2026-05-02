from datetime import UTC, datetime
from uuid import uuid4

from fitcopilot.modules.catalog.domain.entities import Product
from fitcopilot.modules.catalog.domain.repositories import ProductRepository
from fitcopilot.modules.catalog.domain.value_objects import BrandName, ProductName, StoreName
from fitcopilot.modules.recipes.domain.entities import Recipe, RecipeIngredient, RecipeStep
from fitcopilot.modules.recipes.domain.services import RecipeNutritionCalculator
from fitcopilot.modules.recipes.domain.value_objects import (
    IngredientName,
    QuantityGrams,
    RecipeName,
    StepNumber,
    StepText,
)


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


def test_calculate_totals_from_catalog_products() -> None:
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

    recipe = Recipe(
        id=uuid4(),
        name=RecipeName("Bowl fitness"),
        description=None,
        servings=1,
        ingredients=[
            RecipeIngredient(
                name=IngredientName("Yogur griego natural"),
                quantity_g=QuantityGrams(170),
            )
        ],
        steps=[
            RecipeStep(
                number=StepNumber(1),
                text=StepText("Mezclar y servir"),
                time_minutes=2,
            )
        ],
        calories_total=None,
        protein_total_g=None,
        carbs_total_g=None,
        fat_total_g=None,
        created_at=datetime(2026, 5, 1, 22, 0, 0, tzinfo=UTC),
    )

    calculator = RecipeNutritionCalculator(FakeProductRepository([product]))

    calories, protein, carbs, fat = calculator.calculate_totals(recipe)

    assert calories == 165
    assert protein == 15
    assert carbs == 5
    assert fat == 7
