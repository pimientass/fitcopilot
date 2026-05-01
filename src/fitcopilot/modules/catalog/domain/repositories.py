from abc import ABC, abstractmethod
from uuid import UUID

from fitcopilot.modules.catalog.domain.entities import Product


class ProductRepository(ABC):
    @abstractmethod
    def save(self, product: Product) -> None:
        raise NotImplementedError

    @abstractmethod
    def search(self, query: str) -> list[Product]:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, product_id: UUID) -> Product | None:
        raise NotImplementedError
