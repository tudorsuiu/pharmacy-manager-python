from typing import List

from Domain.undo_redo_operation import UndoRedoOperation
from Repository.repository import Repository


class MultiAddOperation(UndoRedoOperation):
    def __init__(self, repository: Repository, addedEntities: List):
        self.__repository = repository
        self.__addedEntities = addedEntities

    def do_undo(self):
        for entitate in self.__addedEntities:
            self.__repository.create(entitate)

    def do_redo(self):
        for entitate in self.__addedEntities:
            self.__repository.delete(entitate.entity_id)
