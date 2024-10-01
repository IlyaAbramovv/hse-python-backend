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


class Repository(Generic[Entity, Info], ABC):

    def __init__(self):
        self._id_generator = int_id_generator()
        self._data = dict[int, Entity]()

    def add(self, info: Info) -> Entity:
        _id = next(self._id_generator)
        self._data[_id] = info

        return Entity(_id, info)

    def delete(self, id: int) -> None:
        if id in self._data:
            del self._data[id]

