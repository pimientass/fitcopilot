import typer

from fitcopilot.app.cli.commands.body_profile import app as body_profile_app
from fitcopilot.app.cli.commands.catalog import app as catalog_app
from fitcopilot.app.cli.commands.recipes import app as recipes_app
from fitcopilot.app.cli.commands.requirements import app as requirements_app
from fitcopilot.app.cli.commands.system import app as system_app

app = typer.Typer(help="Fitcopilot CLI", no_args_is_help=True)

app.add_typer(system_app, name="system")
app.add_typer(body_profile_app, name="body-profile")
app.add_typer(requirements_app, name="requirements")
app.add_typer(catalog_app, name="catalog")
app.add_typer(recipes_app, name="recipes")
