import typer

from fitcopilot.app.bootstrap.container import build_container

app = typer.Typer(help="System commands")


@app.command()
def doctor() -> None:
    """Basic health check for the local app."""
    container = build_container()
    settings = container.settings

    typer.echo(f"{settings.app_name} is alive.")
    typer.echo(f"Environment: {settings.app_env}")
    typer.echo(f"Database: {settings.db_path}")
    typer.echo(f"Ollama URL: {settings.ollama_base_url}")
    typer.echo(f"Ollama model: {settings.ollama_model}")
