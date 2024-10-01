from dataclasses import dataclass
from decimal import Decimal

from lecture_2.hw.shop_api.store.item.models import ItemEntity


@dataclass(slots=True)
class CartInfo:
    items: list[ItemEntity]
    price: Decimal
    deleted: bool


@dataclass(slots=True)
class CartEntity:
    id: int
    info: CartInfo
