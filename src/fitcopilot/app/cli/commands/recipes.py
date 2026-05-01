from typing import Annotated

import typer

from fitcopilot.app.bootstrap.container import build_container
from fitcopilot.infrastructure.db.session import new_session
from fitcopilot.modules.recipes.application.dto import (
    CreateRecipeInput,
    RecipeIngredientInput,
    RecipeStepInput,
)
from fitcopilot.modules.recipes.application.use_cases.create_recipe import CreateRecipe
from fitcopilot.modules.recipes.infrastructure.sqlalchemy_repository import (
    SqlAlchemyRecipeRepository,
)

app = typer.Typer(help="Recipes commands")


@app.command("add")
def add_recipe(
    name: Annotated[str, typer.Option("--name")],
    servings: Annotated[int, typer.Option("--servings")] = 1,
) -> None:
    build_container()
    session = new_session()

    try:
        repository = SqlAlchemyRecipeRepository(session)
        use_case = CreateRecipe(repository)

        result = use_case.execute(
            CreateRecipeInput(
                name=name,
                servings=servings,
                ingredients=[
                    RecipeIngredientInput(
                        name="Yogur griego natural",
                        quantity_g=170,
                    )
                ],
                steps=[
                    RecipeStepInput(
                        number=1,
                        text="Mezclar y servir",
                        time_minutes=2,
                    )
                ],
            )
        )

        typer.echo(result.model_dump_json(indent=2))
    finally:
        session.close()
