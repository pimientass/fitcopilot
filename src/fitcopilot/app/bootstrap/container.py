from dataclasses import dataclass

from fitcopilot.config.settings import Settings, get_settings
from fitcopilot.infrastructure.db.init_db import init_db


@dataclass(frozen=True)
class Container:
    settings: Settings


def build_container() -> Container:
    init_db()
    return Container(settings=get_settings())
