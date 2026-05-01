from datetime import datetime
from typing import Annotated
from uuid import UUID

import typer

from fitcopilot.modules.body_profile.application.dto import CreateBodyProfileInput
from fitcopilot.modules.body_profile.application.use_cases.create_body_profile import (
    CreateBodyProfile,
)
from fitcopilot.modules.body_profile.infrastructure.repositories.in_memory import (
    InMemoryBodyProfileRepository,
)

app = typer.Typer(help="Body profile commands")


@app.command("create")
def create_body_profile(
    user_id: Annotated[UUID, typer.Option("--user-id")],
    weight_kg: Annotated[float, typer.Option("--weight-kg")],
    height_cm: Annotated[float, typer.Option("--height-cm")],
    age_years: Annotated[int, typer.Option("--age-years")],
    sex: Annotated[str, typer.Option("--sex")],
    activity_level: Annotated[str, typer.Option("--activity-level")],
    goal: Annotated[str, typer.Option("--goal")],
    measured_at: Annotated[str, typer.Option("--measured-at")],
) -> None:
    repository = InMemoryBodyProfileRepository()
    use_case = CreateBodyProfile(repository)

    result = use_case.execute(
        CreateBodyProfileInput(
            user_id=user_id,
            weight_kg=weight_kg,
            height_cm=height_cm,
            age_years=age_years,
            sex=sex,
            activity_level=activity_level,
            goal=goal,
            measured_at=datetime.fromisoformat(measured_at),
        )
    )

    typer.echo("Body profile created:")
    typer.echo(result.model_dump_json(indent=2))
