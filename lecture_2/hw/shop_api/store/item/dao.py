from lecture_2.hw.shop_api.store.base import Dao
from lecture_2.hw.shop_api.store.item.models import ItemEntity, ItemInfo


class ItemDao(Dao[ItemEntity, ItemInfo]):
    def get_batch(self, limit: int,
                  offset: int,
                  min_price: float | None = None,
                  max_price: float | None = None,
                  show_deleted: bool = False) -> list[ItemEntity]:
        filtered = list(filter(lambda x: self.filter_item(x, min_price, max_price, show_deleted), self._data.values()))
        return filtered[offset:offset + limit]

    def put(self, id, item_info: ItemInfo) -> ItemEntity | None:
        if id not in self._data:
            return None
        self._data[id] = ItemEntity(id, item_info)
        return self._data[id]

    def patch(self, id, patch: dict) -> ItemEntity | None:
        if id not in self._data or self._data[id].info.deleted:
            return None
        if 'name' in patch:
            self._data[id].info.name = patch['name']
        if 'price' in patch:
            self._data[id].info.price = patch['price']
        return self._data[id]

    def delete(self, id) -> ItemEntity | None:
        if id not in self._data:
            return None
        self._data[id].info.deleted = True
        return self._data[id]

    def get(self, id: int) -> ItemEntity | None:
        if id not in self._data or self._data[id].info.deleted:
            return None
        return self._data[id]

    @staticmethod
    def filter_item(item: ItemEntity, min_price: float | None, max_price: float | None, show_deleted: bool) -> bool:
        return (min_price is None or item.info.price >= min_price) \
            and (max_price is None or item.info.price <= max_price) \
            and (show_deleted or not item.info.deleted)


item_dao = ItemDao(ItemEntity)
