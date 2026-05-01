from uuid import UUID

from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from fitcopilot.modules.catalog.domain.entities import Product
from fitcopilot.modules.catalog.domain.repositories import ProductRepository
from fitcopilot.modules.catalog.domain.value_objects import BrandName, ProductName, StoreName
from fitcopilot.modules.catalog.infrastructure.sqlalchemy_models import ProductModel

class SqlAlchemyProductRepository(ProductRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def save(self, product: Product) -> None:
        model = ProductModel(
            id=str(product.id),
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
        self._session.add(model)
        self._session.commit()

    def search(self, query: str) -> list[Product]:
        stmt = (
            select(ProductModel)
            .where(
                or_(
                    ProductModel.name.ilike(f"%{query}%"),
                    ProductModel.brand.ilike(f"%{query}%"),
                    ProductModel.store.ilike(f"%{query}%"),
                    ProductModel.category.ilike(f"%{query}%"),
                )
            )
            .order_by(ProductModel.name.asc())
            .limit(20)
        )

        models = self._session.execute(stmt).scalars().all()
        return [self._to_domain(model) for model in models]

    def get_by_id(self, product_id: UUID) -> Product | None:
        model = self._session.get(ProductModel, str(product_id))
        if model is None:
            return None
        return self._to_domain(model)

    def _to_domain(self, model: ProductModel) -> Product:
        return Product(
            id=UUID(model.id),
            name=ProductName(model.name),
            brand=BrandName(model.brand) if model.brand else None,
            store=StoreName(model.store) if model.store else None,
            category=model.category,
            barcode=model.barcode,
            serving_size_g=model.serving_size_g,
            calories_per_100g=model.calories_per_100g,
            protein_per_100g=model.protein_per_100g,
            carbs_per_100g=model.carbs_per_100g,
            fat_per_100g=model.fat_per_100g,
            created_at=model.created_at,
        )
