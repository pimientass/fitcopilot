from typing import Annotated
from uuid import UUID

import typer

from fitcopilot.app.bootstrap.container import build_container
from fitcopilot.infrastructure.db.session import new_session
from fitcopilot.modules.body_profile.infrastructure.sqlalchemy_repository import (
    SqlAlchemyBodyProfileRepository,
)
from fitcopilot.modules.requirements.application.dto import CalculateRequirementsInput
from fitcopilot.modules.requirements.application.use_cases.calculate_requirements import (
    CalculateRequirements,
)

app = typer.Typer(help="Nutrition requirements commands")


@app.command("calculate")
def calculate_requirements(
    user_id: Annotated[UUID, typer.Option("--user-id")],
) -> None:
    build_container()
    session = new_session()

    try:
        repository = SqlAlchemyBodyProfileRepository(session)
        use_case = CalculateRequirements(repository)

        result = use_case.execute(
            CalculateRequirementsInput(
                user_id=user_id,
            )
        )

        typer.echo("Nutrition requirements calculated:")
        typer.echo(result.model_dump_json(indent=2))
    finally:
        session.close()
