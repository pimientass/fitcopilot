from datetime import UTC, datetime
from uuid import uuid4

from fitcopilot.modules.catalog.application.dto import CreateProductInput, ProductOutput
from fitcopilot.modules.catalog.domain.entities import Product
from fitcopilot.modules.catalog.domain.repositories import ProductRepository
from fitcopilot.modules.catalog.domain.value_objects import BrandName, ProductName, StoreName


class CreateProduct:
    def __init__(self, repository: ProductRepository) -> None:
        self._repository = repository

    def execute(self, data: CreateProductInput) -> ProductOutput:
        product = Product(
            id=uuid4(),
            name=ProductName(data.name),
            brand=BrandName(data.brand) if data.brand else None,
            store=StoreName(data.store) if data.store else None,
            category=data.category,
            barcode=data.barcode,
            serving_size_g=data.serving_size_g,
            calories_per_100g=data.calories_per_100g,
            protein_per_100g=data.protein_per_100g,
            carbs_per_100g=data.carbs_per_100g,
            fat_per_100g=data.fat_per_100g,
            created_at=datetime.now(UTC),
        )
        self._repository.save(product)

        return ProductOutput(
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
