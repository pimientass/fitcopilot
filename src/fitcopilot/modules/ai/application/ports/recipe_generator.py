from abc import ABC, abstractmethod

from fitcopilot.modules.ai.infrastructure.ollama.schemas import GeneratedRecipePayload


class RecipeGenerator(ABC):
    @abstractmethod
    def generate_recipe(
        self,
        *,
        goal: str,
        calories_target: int,
        protein_target: int,
        preferred_ingredients: list[str],
    ) -> GeneratedRecipePayload:
        raise NotImplementedError
