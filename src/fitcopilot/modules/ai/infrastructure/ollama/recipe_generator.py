from fitcopilot.config.settings import get_settings
from fitcopilot.modules.ai.application.ports.recipe_generator import RecipeGenerator
from fitcopilot.modules.ai.infrastructure.ollama.client import ollama_chat
from fitcopilot.modules.ai.infrastructure.ollama.prompts import build_recipe_prompt
from fitcopilot.modules.ai.infrastructure.ollama.schemas import GeneratedRecipePayload


class OllamaRecipeGenerator(RecipeGenerator):
    def __init__(self) -> None:
        settings = get_settings()
        self._model = settings.ollama_model

    def generate_recipe(
        self,
        *,
        goal: str,
        calories_target: int,
        protein_target: int,
        preferred_ingredients: list[str],
    ) -> GeneratedRecipePayload:
        prompt = build_recipe_prompt(
            goal=goal,
            calories_target=calories_target,
            protein_target=protein_target,
            preferred_ingredients=preferred_ingredients,
        )

        raw_json = ollama_chat(
            model=self._model,
            prompt=prompt,
            schema=GeneratedRecipePayload.model_json_schema(),
        )

        return GeneratedRecipePayload.model_validate_json(raw_json)
