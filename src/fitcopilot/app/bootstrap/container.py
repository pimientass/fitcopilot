from dataclasses import dataclass

from fitcopilot.config.settings import Settings, get_settings


@dataclass(frozen=True)
class Container:
    settings: Settings


def build_container() -> Container:
    return Container(settings=get_settings())
