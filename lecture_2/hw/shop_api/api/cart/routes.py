from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, HTTPException, Query
from pydantic import PositiveInt, NonNegativeInt

from lecture_2.hw.shop_api.api.cart.contracts import CartResponse
from lecture_2.hw.shop_api.store.cart.dao import cart_dao
from lecture_2.hw.shop_api.store.cart.models import CartInfo

router = APIRouter(prefix="/cart")


@router.post(
    "/",
    status_code=HTTPStatus.CREATED,
)
def post_cart():
    entity = cart_dao.add(CartInfo([], 0))
    return CartResponse.from_entity(entity)


@router.get(
    '/{id}',
    status_code=HTTPStatus.OK,
)
def get_cart(id: int):
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
def get_batch(
        limit: Annotated[PositiveInt, Query()],
        offset: Annotated[NonNegativeInt, Query()],
        min_price: Annotated[float, Query()] = None,
        max_price: Annotated[float, Query()] = None,
        min_quantity: Annotated[NonNegativeInt, Query()] = None,
        max_quantity: Annotated[NonNegativeInt, Query()] = None,
) -> list[CartResponse]:
    entity = cart_dao.get(id)
    if not entity:
        raise HTTPException(
            HTTPStatus.NOT_FOUND,
            f"Request resource /item/{id} was not found",
        )
    return CartResponse.from_entity(entity)
