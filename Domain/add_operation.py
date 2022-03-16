from Domain.entity import Entity
from Domain.undo_redo_operation import UndoRedoOperation
from Repository.repository import Repository


class AddOperation(UndoRedoOperation):
    def __init__(self, repository: Repository, addedEntity: Entity):
        self.__repository = repository
        self.__addedEntity = addedEntity

    def do_undo(self):
        self.__repository.delete(self.__addedEntity.entity_id)

    def do_redo(self):
        self.__repository.create(self.__addedEntity)
