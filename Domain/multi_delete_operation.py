from typing import List

from Domain.undo_redo_operation import UndoRedoOperation
from Repository.repository import Repository


class MultiDeleteOperation(UndoRedoOperation):
    def __init__(self, repository: Repository, deletedEntities: List):
        self.__repository = repository
        self.__deletedEntities = deletedEntities

    def do_undo(self):
        for entitate in self.__deletedEntities:
            self.__repository.delete(entitate.entity_id)

    def do_redo(self):
        for entitate in self.__deletedEntities:
            self.__repository.create(entitate)
