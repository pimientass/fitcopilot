from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ProductName:
    value: str

    def __post_init__(self) -> None:
        if not self.value.strip():
            raise ValueError("product name cannot be empty")


@dataclass(frozen=True, slots=True)
class BrandName:
    value: str

    def __post_init__(self) -> None:
        if not self.value.strip():
            raise ValueError("brand name cannot be empty")


@dataclass(frozen=True, slots=True)
class StoreName:
    value: str

    def __post_init__(self) -> None:
        if not self.value.strip():
            raise ValueError("store name cannot be empty")
