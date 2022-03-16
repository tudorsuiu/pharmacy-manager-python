from typing import List

from Domain.undo_redo_operation import UndoRedoOperation
from Repository.repository import Repository


class CascadeDeleteOperation(UndoRedoOperation):
    def __init__(
        self,
        repository: Repository,
        transactionRepository: Repository,
        cascadeList: List,
    ):
        self.__repository = repository
        self.__transactionRepository = transactionRepository
        self.__cascadeList = cascadeList

    def do_undo(self):
        for i in range(len(self.__cascadeList) - 1):
            self.__transactionRepository.create(self.__cascadeList[i])
        self.__repository.create(
            self.__cascadeList[len(self.__cascadeList) - 1]
        )

    def do_redo(self):
        for i in range(len(self.__cascadeList) - 1):
            self.__transactionRepository.delete(
                self.__cascadeList[i].entity_id
            )
        self.__repository.delete(
            self.__cascadeList[len(self.__cascadeList) - 1].entity_id
        )
