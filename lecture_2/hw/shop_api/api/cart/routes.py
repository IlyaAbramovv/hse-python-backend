from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, HTTPException, Query, Response
from pydantic import PositiveInt, NonNegativeInt, NonNegativeFloat

from ...api.cart.contracts import CartResponse
from ...store.cart.dao import cart_dao
from ...store.cart.models import CartInfo
from ...store.item.dao import item_dao

router = APIRouter(prefix="/cart")


@router.post(
    "/",
    status_code=HTTPStatus.CREATED,
)
async def post_cart(response: Response):
    entity = cart_dao.add(CartInfo([], 0))
    response.headers["location"] = f"/cart/{entity.id}"
    return CartResponse.from_entity(entity)


@router.get(
    '/{id}',
    responses={
        HTTPStatus.OK: {
            "description": "Successfully returned requested cart"
        },
        HTTPStatus.NOT_FOUND: {
            "description": "Request resource was not found"
        }
    },
)
async def get_cart(id: int):
    entity = cart_dao.get(id)
    if not entity:
        raise HTTPException(
            HTTPStatus.NOT_FOUND,
            f"Request resource /cart/{id} was not found",
        )
    return CartResponse.from_entity(entity)


@router.get(
    '/',
    status_code=HTTPStatus.OK,
)
async def get_batch(
        limit: Annotated[PositiveInt, Query()] = 10,
        offset: Annotated[NonNegativeInt, Query()] = 0,
        min_price: Annotated[NonNegativeFloat, Query()] = None,
        max_price: Annotated[NonNegativeFloat, Query()] = None,
        min_quantity: Annotated[NonNegativeInt, Query()] = None,
        max_quantity: Annotated[NonNegativeInt, Query()] = None,
) -> list[CartResponse]:
    entities = cart_dao.get_batch(limit, offset, min_price, max_price, min_quantity, max_quantity)
    return [CartResponse.from_entity(entity) for entity in entities]


@router.post(
    '/{cart_id}/add/{item_id}',
    responses={
        HTTPStatus.OK: {
            "description": "Successfully added item to cart"
        },
        HTTPStatus.NOT_FOUND: {
            "description": "Request resource was not found"
        }
    },
)
async def add_item_to_cart(cart_id: int, item_id: int):
    cart = cart_dao.get(cart_id)
    if not cart:
        raise HTTPException(
            HTTPStatus.NOT_FOUND,
            f"Request resource /cart/{cart_id} was not found",
        )
    item = item_dao.get(item_id)
    if not item:
        raise HTTPException(
            HTTPStatus.NOT_FOUND,
            f"Request resource /item/{item_id} was not found",
        )
    if item_id not in map(lambda x: x.id, cart.info.items):
        entity = cart_dao.add_item(cart_id, item)
        return CartResponse.from_entity(entity)
    entity = cart_dao.inc_quantity_for_item(cart_id, item)
    return CartResponse.from_entity(entity)

