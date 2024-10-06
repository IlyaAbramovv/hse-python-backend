from dataclasses import dataclass


@dataclass(slots=True)
class ItemInfo:
    name: str
    price: float
    deleted: bool


@dataclass(slots=True)
class ItemEntity:
    id: int
    info: ItemInfo
