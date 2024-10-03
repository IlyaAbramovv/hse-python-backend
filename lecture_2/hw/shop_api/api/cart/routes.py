from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, HTTPException, Query
from pydantic import PositiveInt, NonNegativeInt

from lecture_2.hw.shop_api.api.cart.contracts import CartResponse
from lecture_2.hw.shop_api.store.cart.dao import cart_dao
from lecture_2.hw.shop_api.store.cart.models import CartInfo, CartItem
from lecture_2.hw.shop_api.store.item.dao import item_dao
from lecture_2.hw.shop_api.store.item.models import ItemEntity

router = APIRouter(prefix="/cart")


@router.post(
    "/",
    status_code=HTTPStatus.CREATED,
)
async def post_cart():
    entity = cart_dao.add(CartInfo([], 0))
    return CartResponse.from_entity(entity)


@router.get(
    '/{id}',
    status_code=HTTPStatus.OK,
)
async def get_cart(id: int):
    entity = cart_dao.get(id)
    if not entity:
        raise HTTPException(
            HTTPStatus.NOT_FOUND,
            f"Request resource /item/{id} was not found",
        )
    return CartResponse.from_entity(entity)


@router.get(
    '/',
    status_code=HTTPStatus.OK,
)
async def get_batch(
        limit: Annotated[PositiveInt, Query()],
        offset: Annotated[NonNegativeInt, Query()],
        min_price: Annotated[float, Query()] = None,
        max_price: Annotated[float, Query()] = None,
        min_quantity: Annotated[NonNegativeInt, Query()] = None,
        max_quantity: Annotated[NonNegativeInt, Query()] = None,
) -> list[CartResponse]:
    entities = cart_dao.get_batch(limit, offset, min_price, max_price, min_quantity, max_quantity)
    return [CartResponse.from_entity(entity) for entity in entities]


@router.post(
    '/{cart_id}/add/{item_id}'
)
async def add_item_to_cart(cart_id: int, item_id: int):
    cart = cart_dao.get(cart_id)
    if not cart:
        raise HTTPException(
            HTTPStatus.NOT_FOUND,
            f"Request resource /{cart_id}/add/{item_id} was not found",
        )
    item = item_dao.get(item_id)
    if not item:
        raise HTTPException(
            HTTPStatus.NOT_FOUND,
            f"Request resource /{cart_id}/add/{item_id} was not found",
        )
    if item_id not in map(lambda x: x.id, cart.info.items):
        entity = cart_dao.add_item(cart_id, __item_entity_to_cart_item(item))
        return CartResponse.from_entity(entity)
    entity = cart_dao.inc_quantity_for_item(cart_id, __item_entity_to_cart_item(item))
    return CartResponse.from_entity(entity)


def __item_entity_to_cart_item(item: ItemEntity) -> CartItem:
    return CartItem(item.id, item.info.name, 1, True)
