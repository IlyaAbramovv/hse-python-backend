from abc import ABC
from typing import TypeVar, Generic, Iterable, Type


def int_id_generator() -> Iterable[int]:
    i = 0
    while True:
        yield i
        i += 1


Entity = TypeVar('Entity')
Info = TypeVar('Info')


class Dao(Generic[Entity, Info], ABC):

    def __init__(self, entity_type: Type[Entity]):
        self._id_generator = int_id_generator()
        self._data = dict[int, Entity]()
        self._entity_type = entity_type

    def add(self, info: Info) -> Entity:
        _id = next(self._id_generator)
        self._data[_id] = self._entity_type(_id, info)

        return self._data[_id]

    def get(self, id: int) -> Entity:
        return self._data.get(id, None)
