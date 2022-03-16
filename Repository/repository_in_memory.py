from typing import List

from Domain.entity import Entity
from Repository.repository import Repository


class RepositoryInMemory(Repository):
    def __init__(self):
        self.entities = {}

    def read(self, entity_id=None) -> List or Entity or None:
        """
        Citeste din memorie un obiect de tip Entity dupa id-ul dat.
        """
        if entity_id is None:
            return list(self.entities.values())

        if entity_id in self.entities:
            return self.entities[entity_id]
        else:
            return None

    def create(self, entity: Entity) -> None:
        """
        Creeaza in memorie un obiect de tip Entity.
        """
        if self.read(entity.entity_id) is not None:
            raise KeyError("Exista deja o entitate cu id-ul dat!")
        self.entities[entity.entity_id] = entity

    def update(self, medicine: Entity) -> None:
        """
        Modifica in memorie un obiect de tip Entity.
        """
        if self.read(medicine.entity_id) is None:
            raise KeyError("Nu exista o entitate cu id-ul dat!")
        self.entities[medicine.entity_id] = medicine

    def delete(self, id_medicine: str) -> None:
        """
        Sterge din memorie un obiect de tip Entity.
        """
        if self.read(id_medicine) is None:
            raise KeyError("Nu exista o entitate cu id-ul dat!")
        del self.entities[id_medicine]
