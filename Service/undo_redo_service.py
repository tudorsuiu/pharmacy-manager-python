from Domain.undo_redo_operation import UndoRedoOperation


class UndoRedoService:
    def __init__(self):
        self.__undoOperations = []
        self.__redoOperations = []

    def add_undo_operation(self, undoRedoOperation: UndoRedoOperation):
        self.__undoOperations.append(undoRedoOperation)
        self.__redoOperations.clear()

    def undo(self):
        if self.__undoOperations:
            operation = self.__undoOperations.pop()
            self.__redoOperations.append(operation)
            operation.do_undo()
        else:
            print("Nu se poate face undo!")

    def redo(self):
        if self.__redoOperations:
            operation = self.__redoOperations.pop()
            self.__undoOperations.append(operation)
            operation.do_redo()
        else:
            print("Nu se poate face redo!")
