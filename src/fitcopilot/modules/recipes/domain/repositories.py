from abc import ABC, abstractmethod
from uuid import UUID

from fitcopilot.modules.recipes.domain.entities import Recipe


class RecipeRepository(ABC):
    @abstractmethod
    def save(self, recipe: Recipe) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, recipe_id: UUID) -> Recipe | None:
        raise NotImplementedError
