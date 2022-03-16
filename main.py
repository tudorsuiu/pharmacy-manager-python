from Domain.client_card_validator import ClientCardValidator
from Domain.medicine_validator import MedicineValidator
from Domain.transaction_validator import TransactionValidator
from Repository.repository_json import RepositoryJson
from Service.client_card_service import ClientCardService
from Service.medicine_service import MedicineService
from Service.transaction_service import TransactionService
from Service.undo_redo_service import UndoRedoService
from Tests.test_all import test_all
from UserInterface.console import Console


def main():
    test_all()
    medicineValidator = MedicineValidator()
    medicineRepositoryJson = RepositoryJson("medicine.json")
    clientCardValidator = ClientCardValidator()
    clientCardRepositoryJson = RepositoryJson("client_cards.json")
    transactionValidator = TransactionValidator()
    transactionRepositoryJson = RepositoryJson("transactions.json")
    undoRedoService = UndoRedoService()
    medicineService = MedicineService(
        medicineRepositoryJson,
        medicineValidator,
        transactionRepositoryJson,
        undoRedoService,
    )
    clientCardService = ClientCardService(
        clientCardRepositoryJson,
        clientCardValidator,
        transactionRepositoryJson,
        undoRedoService,
    )
    transactionService = TransactionService(
        transactionRepositoryJson,
        clientCardRepositoryJson,
        medicineRepositoryJson,
        transactionValidator,
        undoRedoService,
    )
    consola = Console(
        medicineService, clientCardService, transactionService, undoRedoService
    )
    consola.run_menu()


if __name__ == "__main__":
    main()
