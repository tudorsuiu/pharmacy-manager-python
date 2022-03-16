from Domain.entity import Entity
from Domain.undo_redo_operation import UndoRedoOperation
from Repository.repository import Repository


class DeleteOperation(UndoRedoOperation):
    def __init__(self, repository: Repository, deletedEntity: Entity):
        self.__repository = repository
        self.__deletedEntity = deletedEntity

    def do_undo(self):
        self.__repository.create(self.__deletedEntity)

    def do_redo(self):
        self.__repository.delete(self.__deletedEntity.entity_id)
