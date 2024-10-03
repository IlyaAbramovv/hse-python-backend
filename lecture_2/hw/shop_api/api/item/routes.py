from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, HTTPException, Query
from pydantic import NonNegativeInt, PositiveInt

from lecture_2.hw.shop_api.api.item.contracts import ItemRequest, ItemResponse
from lecture_2.hw.shop_api.store.item.dao import item_dao

router = APIRouter(prefix="/item")


@router.post(
    "/",
    status_code=HTTPStatus.CREATED,
)
async def post_item(info: ItemRequest) -> ItemResponse:
    entity = item_dao.add(info.as_item_info())
    return ItemResponse.from_entity(entity)


@router.get(
    "/{id}",
    responses={HTTPStatus.OK: {}, HTTPStatus.NOT_FOUND: {}},
)
async def get_item(id: int) -> ItemResponse:
    entity = item_dao.get(id)
    if not entity:
        raise HTTPException(
            HTTPStatus.NOT_FOUND,
            f"Request resource /item/{id} was not found",
        )
    return ItemResponse.from_entity(entity)


@router.get(
    "/",
    status_code=HTTPStatus.OK,
)
async def get_batch(
        limit: Annotated[PositiveInt, Query()],
        offset: Annotated[NonNegativeInt, Query()],
        min_price: Annotated[float, Query()] = None,
        max_price: Annotated[float, Query()] = None,
        show_deleted: Annotated[bool, Query()] = False,
) -> list[ItemResponse]:
    entities = item_dao.get_batch(limit, offset, min_price, max_price, show_deleted)
    return [ItemResponse.from_entity(entity) for entity in entities]


@router.put(
    "/{id}",
    responses={HTTPStatus.OK: {}, HTTPStatus.NOT_FOUND: {}},
)
async def put_item(id: int, info: ItemRequest) -> ItemResponse:
    entity = item_dao.put(id, info.as_item_info())
    if not entity:
        raise HTTPException(
            HTTPStatus.NOT_FOUND,
            f"Request resource /item/{id} was not found",
        )
    return ItemResponse.from_entity(entity)


@router.patch(
    "/{id}",
    responses={HTTPStatus.OK: {}, HTTPStatus.NOT_FOUND: {}},
)
async def patch_item(id: int, info: ItemRequest) -> ItemResponse:
    entity = item_dao.patch(id, info.as_dict())
    if not entity:
        raise HTTPException(
            HTTPStatus.NOT_FOUND,
            f"Request resource /item/{id} was not found",
        )
    return ItemResponse.from_entity(entity)


@router.patch(
    "/{id}",
    responses={HTTPStatus.OK: {}, HTTPStatus.NOT_FOUND: {}},
)
async def patch_item(id: int, info: ItemRequest) -> ItemResponse:
    entity = item_dao.delete(id, info.as_dict())
    if not entity:
        raise HTTPException(
            HTTPStatus.NOT_FOUND,
            f"Request resource /item/{id} was not found",
        )
    return ItemResponse.from_entity(entity)
