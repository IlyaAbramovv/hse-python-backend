from dataclasses import dataclass
from decimal import Decimal


@dataclass(slots=True)
class ItemInfo:
    name: str
    price: Decimal
    deleted: bool


@dataclass(slots=True)
class ItemEntity:
    id: int
    info: ItemInfo
