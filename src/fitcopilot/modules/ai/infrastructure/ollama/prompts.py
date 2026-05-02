from fitcopilot.modules.ai.infrastructure.ollama.schemas import GeneratedRecipePayload


def build_recipe_prompt(
    *,
    goal: str,
    calories_target: int,
    protein_target: int,
    preferred_ingredients: list[str],
) -> str:
    ingredients_text = ", ".join(preferred_ingredients) if preferred_ingredients else "none"

    return f"""
You are generating a structured fitness recipe.

Return only data that matches the provided JSON schema.

Recipe goal: {goal}
Calories target: around {calories_target}
Protein target: at least {protein_target} grams
Preferred ingredients: {ingredients_text}

Requirements:
- recipe should be simple
- ingredients should be realistic
- steps should be short and clear
- use grams for ingredients
- keep it practical for a local fitness meal app

JSON schema:
{GeneratedRecipePayload.model_json_schema()}
""".strip()
