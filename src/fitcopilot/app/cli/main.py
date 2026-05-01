import typer

from fitcopilot.app.cli.commands.body_profile import app as body_profile_app
from fitcopilot.app.cli.commands.system import app as system_app

app = typer.Typer(
    help="Fitcopilot CLI",
    no_args_is_help=True,
)

app.add_typer(system_app, name="system")
app.add_typer(body_profile_app, name="body-profile")
