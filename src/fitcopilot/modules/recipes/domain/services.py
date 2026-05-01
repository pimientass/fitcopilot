from fitcopilot.modules.catalog.domain.repositories import ProductRepository
from fitcopilot.modules.recipes.domain.entities import Recipe


class RecipeNutritionCalculator:
    def __init__(self, product_repository: ProductRepository) -> None:
        self._product_repository = product_repository

    def calculate_totals(self, recipe: Recipe) -> tuple[int, int, int, int]:
        calories = 0
        protein = 0
        carbs = 0
        fat = 0

        for ingredient in recipe.ingredients:
            products = self._product_repository.search(ingredient.name.value)
            if not products:
                continue

            product = products[0]
            factor = ingredient.quantity_g.value / 100.0

            if product.calories_per_100g is not None:
                calories += round(product.calories_per_100g * factor)
            if product.protein_per_100g is not None:
                protein += round(product.protein_per_100g * factor)
            if product.carbs_per_100g is not None:
                carbs += round(product.carbs_per_100g * factor)
            if product.fat_per_100g is not None:
                fat += round(product.fat_per_100g * factor)

        return calories, protein, carbs, fat
