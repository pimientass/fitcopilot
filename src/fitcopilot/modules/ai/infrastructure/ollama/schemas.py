from pydantic import BaseModel, Field


class GeneratedRecipeIngredient(BaseModel):
    name: str = Field(min_length=1)
    quantity_g: float = Field(gt=0)


class GeneratedRecipeStep(BaseModel):
    number: int = Field(gt=0)
    text: str = Field(min_length=1)
    time_minutes: int | None = Field(default=None, ge=0)


class GeneratedRecipePayload(BaseModel):
    name: str = Field(min_length=1)
    description: str | None = None
    servings: int = Field(gt=0)
    ingredients: list[GeneratedRecipeIngredient] = Field(min_length=1)
    steps: list[GeneratedRecipeStep] = Field(min_length=1)
