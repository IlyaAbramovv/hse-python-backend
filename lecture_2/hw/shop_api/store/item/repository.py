from lecture_2.hw.shop_api.store.base import Repository
from lecture_2.hw.shop_api.store.item.models import ItemEntity, ItemInfo


class ItemRepository(Repository[ItemEntity, ItemInfo]):
    def __init__(self):
        super().__init__()


itemRepository = ItemRepository()
