from lecture_2.hw.shop_api.store.base import Dao
from lecture_2.hw.shop_api.store.cart.models import CartEntity, CartInfo, CartItem


class CartDao(Dao[CartEntity, CartInfo]):
    def get_batch(self,
                  limit: int,
                  offset: int,
                  min_price: float | None = None,
                  max_price: float | None = None,
                  min_quantity: float | None = None,
                  max_quantity: float | None = None) -> list[CartEntity]:
        filtered = list(filter(lambda x: self.filter_item(x, min_price, max_price, min_quantity, max_quantity), self._data.values()))
        return filtered[offset:offset + limit]

    def add_item(self, cart_id: int, item: CartItem) -> CartEntity:
        self._data[cart_id].info.items.append(item)
        return self._data[cart_id]

    def inc_quantity_for_item(self, cart_id: int, item: CartItem) -> CartEntity:
        idx = list(map(lambda x: x.id, self._data[cart_id].info.items)).index(item.id)
        self._data[cart_id].info.items[idx].quantity += 1
        return self._data[cart_id]

    @staticmethod
    def filter_item(cart: CartEntity, min_price: float | None = None, max_price: float | None = None,
                    min_quantity: float | None = None, max_quantity: float | None = None) -> bool:
        return (min_price is None or cart.info.price >= min_price) \
            and (max_price is None or cart.info.price <= max_price) \
            and (min_quantity is None or all(map(lambda c: c.quantity >= min_quantity, cart.info.items))) \
            and (max_quantity is None or all(map(lambda c: c.quantity <= max_quantity, cart.info.items)))


cart_dao = CartDao(CartEntity)
