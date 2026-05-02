from fitcopilot.modules.ai.infrastructure.ollama.schemas import GeneratedRecipePayload


def test_generated_recipe_payload_schema_is_valid() -> None:
    payload = GeneratedRecipePayload.model_validate(
        {
            "name": "Bowl fitness de yogur",
            "description": "Receta simple alta en proteína",
            "servings": 1,
            "ingredients": [
                {"name": "Yogur griego natural", "quantity_g": 170},
                {"name": "Avena", "quantity_g": 40},
            ],
            "steps": [
                {"number": 1, "text": "Añadir el yogur al bol", "time_minutes": 1},
                {"number": 2, "text": "Agregar la avena y mezclar", "time_minutes": 1},
            ],
        }
    )

    assert payload.name == "Bowl fitness de yogur"
    assert len(payload.ingredients) == 2
    assert len(payload.steps) == 2
