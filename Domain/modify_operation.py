from Domain.entity import Entity
from Domain.undo_redo_operation import UndoRedoOperation
from Repository.repository import Repository


class ModifyOperation(UndoRedoOperation):
    def __init__(
        self, repository: Repository, oldEntity: Entity, newEntity: Entity
    ):
        self.__repository = repository
        self.__oldEntity = oldEntity
        self.__newEntity = newEntity

    def do_undo(self):
        self.__repository.update(self.__oldEntity)

    def do_redo(self):
        self.__repository.update(self.__newEntity)
