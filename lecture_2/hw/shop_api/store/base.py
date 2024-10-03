from _typeshed import SupportsNext
from abc import ABC
from typing import TypeVar, Generic


def int_id_generator() -> SupportsNext[int]:
    i = 0
    while True:
        yield i
        i += 1


Entity = TypeVar('Entity')
Info = TypeVar('Info')


class Dao(Generic[Entity, Info], ABC):

    def __init__(self):
        self._id_generator = int_id_generator()
        self._data = dict[int, Entity]()

    def add(self, info: Info) -> Entity:
        _id = next(self._id_generator)
        self._data[_id] = Entity(_id, info)

        return Entity(_id, info)

    def get(self, id: int) -> Entity:
        return self._data.get(id, None)
