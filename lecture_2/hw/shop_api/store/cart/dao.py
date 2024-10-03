from lecture_2.hw.shop_api.store.base import Dao
from lecture_2.hw.shop_api.store.cart.models import CartEntity, CartInfo


class CartDao(Dao[CartEntity, CartInfo]):
    def __init__(self):
        super().__init__()


cart_dao = CartDao()
