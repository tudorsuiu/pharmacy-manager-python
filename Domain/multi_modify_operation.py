from typing import List

from Domain.undo_redo_operation import UndoRedoOperation
from Repository.repository import Repository


class MultiModifyOperation(UndoRedoOperation):
    def __init__(
        self, repository: Repository, oldEntities: List, newEntities: List
    ):
        self.__repository = repository
        self.__oldEntities = oldEntities
        self.__newEntities = newEntities

    def do_undo(self):
        for entitate in self.__oldEntities:
            self.__repository.update(entitate)

    def do_redo(self):
        for entitate in self.__newEntities:
            self.__repository.update(entitate)
