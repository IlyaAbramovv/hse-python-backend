from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, HTTPException, Query
from pydantic import NonNegativeInt, PositiveInt, NonNegativeFloat

from ...api.item.contracts import ItemRequest, ItemResponse
from ...store.item.dao import item_dao

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
    responses={
        HTTPStatus.OK: {
            "description": "Successfully returned requested item",
        },
        HTTPStatus.NOT_FOUND: {
            "description": "Request resource was not found"
        }
    },
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
        limit: Annotated[PositiveInt, Query()] = 10,
        offset: Annotated[NonNegativeInt, Query()] = 0,
        min_price: Annotated[NonNegativeFloat, Query()] = None,
        max_price: Annotated[NonNegativeFloat, Query()] = None,
        show_deleted: Annotated[bool, Query()] = False,
) -> list[ItemResponse]:
    entities = item_dao.get_batch(limit, offset, min_price, max_price, show_deleted)
    return [ItemResponse.from_entity(entity) for entity in entities]


@router.put(
    "/{id}",
    responses={
        HTTPStatus.OK: {
            "description": "Successfully upserted"
        },
        HTTPStatus.NOT_FOUND: {
            "description": "Request resource was not found"
        }
    },
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
    responses={
        HTTPStatus.OK: {
            "description": "Patch applied successfully"
        },
        HTTPStatus.NOT_MODIFIED: {
            "description": "Request resource was not found"
        },
        HTTPStatus.UNPROCESSABLE_ENTITY: {
            "description": "Unprocessable data provided"
        }
    },
)
async def patch_item(id: int, info: dict) -> ItemResponse:
    if info.keys() > {'name', 'price'}:
        raise HTTPException(
            HTTPStatus.UNPROCESSABLE_ENTITY,
            "Unprocessable data provided",
        )
    entity = item_dao.patch(id, info)
    if not entity:
        raise HTTPException(
            HTTPStatus.NOT_MODIFIED,
            f"Request resource was not found",
        )
    return ItemResponse.from_entity(entity)


@router.delete(
    "/{id}",
    responses={
        HTTPStatus.OK: {
            "description": "Deleted successfully"
        },
        HTTPStatus.NOT_FOUND: {
            "description": "Request resource was not found"
        }
    },
)
async def delete_item(id: int) -> ItemResponse:
    entity = item_dao.delete(id)
    if not entity:
        raise HTTPException(
            HTTPStatus.NOT_FOUND,
            f"Request resource /item/{id} was not found",
        )
    return ItemResponse.from_entity(entity)
