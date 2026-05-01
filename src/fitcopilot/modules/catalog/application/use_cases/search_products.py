from fitcopilot.modules.catalog.application.dto import ProductOutput
from fitcopilot.modules.catalog.domain.repositories import ProductRepository


class SearchProducts:
    def __init__(self, repository: ProductRepository) -> None:
        self._repository = repository

    def execute(self, query: str) -> list[ProductOutput]:
        products = self._repository.search(query)

        return [
            ProductOutput(
                id=product.id,
                name=product.name.value,
                brand=product.brand.value if product.brand else None,
                store=product.store.value if product.store else None,
                category=product.category,
                barcode=product.barcode,
                serving_size_g=product.serving_size_g,
                calories_per_100g=product.calories_per_100g,
                protein_per_100g=product.protein_per_100g,
                carbs_per_100g=product.carbs_per_100g,
                fat_per_100g=product.fat_per_100g,
                created_at=product.created_at,
            )
            for product in products
        ]
