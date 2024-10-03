from dataclasses import dataclass
from decimal import Decimal


@dataclass(slots=True)
class CartItem:
    id: int
    name: str
    quantity: int
    available: bool


@dataclass(slots=True)
class CartInfo:
    items: list[CartItem]
    price: Decimal


@dataclass(slots=True)
class CartEntity:
    id: int
    info: CartInfo
