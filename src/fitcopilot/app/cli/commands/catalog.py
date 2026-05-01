from typing import Annotated

import typer

from fitcopilot.app.bootstrap.container import build_container
from fitcopilot.infrastructure.db.session import new_session
from fitcopilot.modules.catalog.application.dto import CreateProductInput
from fitcopilot.modules.catalog.application.use_cases.create_product import CreateProduct
from fitcopilot.modules.catalog.application.use_cases.search_products import SearchProducts
from fitcopilot.modules.catalog.infrastructure.sqlalchemy_repository import (
    SqlAlchemyProductRepository,
)

app = typer.Typer(help="Catalog commands")


@app.command("add")
def add_product(
    name: Annotated[str, typer.Option("--name")],
    brand: Annotated[str | None, typer.Option("--brand")] = None,
    store: Annotated[str | None, typer.Option("--store")] = None,
    category: Annotated[str | None, typer.Option("--category")] = None,
    barcode: Annotated[str | None, typer.Option("--barcode")] = None,
    serving_size_g: Annotated[float | None, typer.Option("--serving-size-g")] = None,
    calories_per_100g: Annotated[int | None, typer.Option("--calories-per-100g")] = None,
    protein_per_100g: Annotated[int | None, typer.Option("--protein-per-100g")] = None,
    carbs_per_100g: Annotated[int | None, typer.Option("--carbs-per-100g")] = None,
    fat_per_100g: Annotated[int | None, typer.Option("--fat-per-100g")] = None,
) -> None:
    build_container()
    session = new_session()

    try:
        repository = SqlAlchemyProductRepository(session)
        use_case = CreateProduct(repository)

        result = use_case.execute(
            CreateProductInput(
                name=name,
                brand=brand,
                store=store,
                category=category,
                barcode=barcode,
                serving_size_g=serving_size_g,
                calories_per_100g=calories_per_100g,
                protein_per_100g=protein_per_100g,
                carbs_per_100g=carbs_per_100g,
                fat_per_100g=fat_per_100g,
            )
        )

        typer.echo("Product created:")
        typer.echo(result.model_dump_json(indent=2))
    finally:
        session.close()


@app.command("search")
def search_products(
    query: Annotated[str, typer.Option("--query")],
) -> None:
    build_container()
    session = new_session()

    try:
        repository = SqlAlchemyProductRepository(session)
        use_case = SearchProducts(repository)

        result = use_case.execute(query)
        typer.echo(result[0].model_dump_json(indent=2) if result else "[]")
    finally:
        session.close()
