from lecture_2.hw.shop_api.store.base import Dao
from lecture_2.hw.shop_api.store.item.models import ItemEntity, ItemInfo


class ItemDao(Dao[ItemEntity, ItemInfo]):
    def __init__(self):
        super().__init__()

    def get_batch(self, limit: int,
                  offset: int,
                  min_price: float | None = None,
                  max_price: float | None = None,
                  show_deleted: bool = False) -> list[ItemEntity] | None:
        if offset > len(self._data):
            return None
        filtered = list(filter(lambda x: self.filter_item(x, min_price, max_price, show_deleted), self._data.values()))
        return filtered[offset:offset + limit]

    def put(self, id, item_info: ItemInfo) -> ItemEntity | None:
        if id not in self._data:
            return None
        self._data[id] = ItemEntity(id, item_info)
        return self._data[id]

    def patch(self, id, patch: dict) -> ItemEntity | None:
        if id not in self._data:
            return None
        if 'name' in patch:
            self._data[id].name = patch['name']
        if 'price' in patch:
            self._data[id].price = patch['price']

    def delete(self, id) -> ItemEntity | None:
        if id not in self._data:
            return None
        self._data[id].deleted = True
        return self._data[id]

    @staticmethod
    def filter_item(item: ItemEntity, min_price: float | None = None, max_price: float | None = None, show_deleted: bool = False):
        return (min_price is None or item.info.price >= min_price) \
            and (max_price is None or item.info.price <= max_price) \
            and (show_deleted or not item.info.deleted)


item_dao = ItemDao()
