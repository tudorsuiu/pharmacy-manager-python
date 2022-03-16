from typing import Protocol, List

from Domain.entity import Entity


class Repository(Protocol):
    def read(self, entity_id=None) -> List or Entity or None:
        ...

    def create(self, entity: Entity) -> None:
        ...

    def update(self, entity: Entity) -> None:
        ...

    def delete(self, entity_id) -> None:
        ...
