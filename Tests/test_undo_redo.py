import datetime

from Domain.client_card import ClientCard
from Domain.client_card_validator import ClientCardValidator
from Domain.medicine import Medicine
from Domain.medicine_validator import MedicineValidator
from Domain.transaction_validator import TransactionValidator
from Repository.repository_json import RepositoryJson
from Service.client_card_service import ClientCardService
from Service.medicine_service import MedicineService
from Service.transaction_service import TransactionService
from Service.undo_redo_service import UndoRedoService


def clear_file(filename: str) -> None:
    with open(filename, "w") as f:
        pass


def test_service_medicine_undo_redo():

    clear_file("test_medicines.json")
    clear_file("test_transactions.json")

    medicineValidator = MedicineValidator()

    medicineRepository = RepositoryJson("test_medicines.json")

    transactionRepository = RepositoryJson("test_transactions.json")

    undoRedoService = UndoRedoService()

    medicineService = MedicineService(
        medicineRepository,
        medicineValidator,
        transactionRepository,
        undoRedoService,
    )

    # TEST UNDO/REDO CREATE

    medicineService.create("1", "Nurofen", "Reckitt Benckiser", 12, "nu")

    medicineService.create("2", "Paracetamol", "Zenit", 10, "da")

    medicines = medicineService.get_all()
    last = len(medicines) - 1
    assert len(medicines) == 2
    assert medicines[last].entity_id == "2"

    undoRedoService.undo()
    medicines = medicineService.get_all()
    last = len(medicines) - 1
    assert len(medicines) == 1
    assert medicines[last].entity_id == "1"

    undoRedoService.undo()
    medicines = medicineService.get_all()
    assert len(medicines) == 0

    undoRedoService.redo()
    medicines = medicineService.get_all()
    last = len(medicines) - 1
    assert len(medicines) == 1
    assert medicines[last].entity_id == "1"

    undoRedoService.redo()
    medicines = medicineService.get_all()
    last = len(medicines) - 1
    assert len(medicines) == 2
    assert medicines[last].entity_id == "2"

    # TEST UNDO/REDO DELETE

    medicineService.delete("2")
    medicineService.delete("1")

    medicines = medicineService.get_all()
    assert len(medicines) == 0

    undoRedoService.undo()
    medicines = medicineService.get_all()
    last = len(medicines) - 1
    assert len(medicines) == 1
    assert medicines[last].entity_id == "1"

    undoRedoService.undo()
    medicines = medicineService.get_all()
    last = len(medicines) - 1
    assert len(medicines) == 2
    assert medicines[last].entity_id == "2"

    undoRedoService.redo()
    medicines = medicineService.get_all()

    last = len(medicines) - 1
    assert len(medicines) == 1
    assert medicines[last].entity_id == "1"

    undoRedoService.redo()
    medicines = medicineService.get_all()
    assert len(medicines) == 0

    undoRedoService.undo()
    medicines = medicineService.get_all()
    last = len(medicines) - 1
    assert len(medicines) == 1
    assert medicines[last].entity_id == "1"

    # TEST UNDO/REDO UPDATE

    medicineService.update("1", "N", "R", 1, "da")

    medicines = medicineService.get_all()
    assert medicines[0] == Medicine("1", "N", "R", 1, "da")

    undoRedoService.undo()
    medicines = medicineService.get_all()
    assert medicines[0] == Medicine(
        "1", "Nurofen", "Reckitt Benckiser", 12, "nu"
    )

    undoRedoService.redo()
    medicines = medicineService.get_all()
    assert medicines[0] == Medicine("1", "N", "R", 1, "da")

    medicineService.delete("1")
    medicines = medicineService.get_all()
    assert len(medicines) == 0

    # TEST UNDO/REDO INCREASE_BY_PERCENTAGE

    medicineService.create("1", "Nurofen", "Reckitt Benckiser", 12, "nu")

    medicineService.create("2", "Paracetamol", "Zenit", 10, "da")

    medicineService.increase_by_percentage(15, 10)

    medicines = medicineService.get_all()
    assert medicines[0] == Medicine(
        "1", "Nurofen", "Reckitt Benckiser", 13.2, "nu"
    )
    assert medicines[1] == Medicine("2", "Paracetamol", "Zenit", 11, "da")

    undoRedoService.undo()
    medicines = medicineService.get_all()
    assert medicines[0] == Medicine(
        "1", "Nurofen", "Reckitt Benckiser", 12, "nu"
    )
    assert medicines[1] == Medicine("2", "Paracetamol", "Zenit", 10, "da")

    undoRedoService.redo()
    medicines = medicineService.get_all()
    assert medicines[0] == Medicine(
        "1", "Nurofen", "Reckitt Benckiser", 13.2, "nu"
    )
    assert medicines[1] == Medicine("2", "Paracetamol", "Zenit", 11, "da")

    undoRedoService.undo()
    medicines = medicineService.get_all()
    assert medicines[0] == Medicine(
        "1", "Nurofen", "Reckitt Benckiser", 12, "nu"
    )
    assert medicines[1] == Medicine("2", "Paracetamol", "Zenit", 10, "da")

    medicineService.delete("1")
    medicineService.delete("2")

    # TEST UNDO/REDO RANDOM_MEDICINE

    medicineService.random_medicine(5)

    assert len(medicineService.get_all()) == 5

    undoRedoService.undo()
    assert len(medicineService.get_all()) == 0

    undoRedoService.redo()
    assert len(medicineService.get_all()) == 5

    undoRedoService.undo()
    assert len(medicineService.get_all()) == 0


def test_service_client_card_undo_redo():

    clear_file("test_client_cards.json")
    clear_file("test_transactions.json")

    clientCardValidator = ClientCardValidator()
    clientCardRepository = RepositoryJson("test_client_cards.json")

    transactionRepository = RepositoryJson("test_transactions.json")

    undoRedoService = UndoRedoService()
    clientCardService = ClientCardService(
        clientCardRepository,
        clientCardValidator,
        transactionRepository,
        undoRedoService,
    )

    # TEST UNDO/REDO CREATE

    clientCardService.create(
        "1",
        "Mircea",
        "Avram",
        "5030523330500",
        datetime.date(2023, 3, 23),
        datetime.date(2010, 5, 12),
    )

    clientCardService.create(
        "2",
        "Robert",
        "Ionescu",
        "5030523330501",
        datetime.date(2023, 3, 23),
        datetime.date(2010, 5, 12),
    )

    cards = clientCardService.get_all()
    last = len(cards) - 1
    assert len(cards) == 2
    assert cards[last].entity_id == "2"

    undoRedoService.undo()
    cards = clientCardService.get_all()
    last = len(cards) - 1
    assert len(cards) == 1
    assert cards[last].entity_id == "1"

    undoRedoService.undo()
    cards = clientCardService.get_all()
    assert len(cards) == 0

    undoRedoService.redo()
    cards = clientCardService.get_all()
    last = len(cards) - 1
    assert len(cards) == 1
    assert cards[last].entity_id == "1"

    undoRedoService.redo()
    cards = clientCardService.get_all()
    last = len(cards) - 1
    assert len(cards) == 2
    assert cards[last].entity_id == "2"

    # TEST UNDO/REDO DELETE

    clientCardService.delete("2")

    clientCardService.delete("1")

    cards = clientCardService.get_all()
    assert len(cards) == 0

    undoRedoService.undo()
    cards = clientCardService.get_all()
    last = len(cards) - 1
    assert len(cards) == 1
    assert cards[last].entity_id == "1"

    undoRedoService.undo()
    cards = clientCardService.get_all()
    last = len(cards) - 1
    assert len(cards) == 2
    assert cards[last].entity_id == "2"

    undoRedoService.redo()
    cards = clientCardService.get_all()
    last = len(cards) - 1
    assert len(cards) == 1
    assert cards[last].entity_id == "1"

    undoRedoService.redo()
    cards = clientCardService.get_all()
    assert len(cards) == 0

    undoRedoService.undo()
    cards = clientCardService.get_all()
    last = len(cards) - 1
    assert len(cards) == 1
    assert cards[last].entity_id == "1"

    # TEST UNDO/REDO UPDATE

    clientCardService.update(
        "1",
        "Mircea",
        "A",
        "5030523330501",
        datetime.date(2023, 3, 23),
        datetime.date(2010, 5, 12),
    )

    cards = clientCardService.get_all()
    assert cards[0] == ClientCard(
        "1",
        "Mircea",
        "A",
        "5030523330501",
        datetime.date(2023, 3, 23),
        datetime.date(2010, 5, 12),
    )

    undoRedoService.undo()
    cards = clientCardService.get_all()
    assert cards[0] == ClientCard(
        "1",
        "Mircea",
        "Avram",
        "5030523330500",
        datetime.date(2023, 3, 23),
        datetime.date(2010, 5, 12),
    )

    undoRedoService.redo()
    cards = clientCardService.get_all()
    assert cards[0] == ClientCard(
        "1",
        "Mircea",
        "A",
        "5030523330501",
        datetime.date(2023, 3, 23),
        datetime.date(2010, 5, 12),
    )

    clientCardService.delete("1")
    cards = clientCardService.get_all()
    assert len(cards) == 0


def test_service_transaction_undo_redo():
    clear_file("test_transactions.json")
    clear_file("test_client_cards.json")
    clear_file("test_medicines.json")

    transactionValidator = TransactionValidator()
    transactionRepository = RepositoryJson("test_transactions.json")

    clientCardRepository = RepositoryJson("test_client_cards.json")

    medicineRepository = RepositoryJson("test_medicines.json")

    undoRedoService = UndoRedoService()
    transactionService = TransactionService(
        transactionRepository,
        clientCardRepository,
        medicineRepository,
        transactionValidator,
        undoRedoService,
    )

    # TEST UNDO/REDO CREATE

    medicineRepository.create(
        Medicine("1", "Nurofen", "Reckitt Benckiser", 10, "nu")
    )
    medicineRepository.create(Medicine("2", "Paracetamol", "Zenit", 10, "da"))
    clientCardRepository.create(
        ClientCard(
            "1",
            "Mircea",
            "Avram",
            "5030523330500",
            datetime.date(2023, 3, 23),
            datetime.date(2010, 5, 12),
        )
    )
    transactionService.create(
        "1", "1", "1", 20, datetime.datetime(2021, 11, 1, 21, 4, 00)
    )
    transactionService.create(
        "2", "2", "1", 10, datetime.datetime(2021, 11, 10, 21, 4, 00)
    )

    transactions = transactionService.get_all()
    last = len(transactions) - 1
    assert len(transactions) == 2
    assert transactions[last].entity_id == "2"

    undoRedoService.undo()
    transactions = transactionService.get_all()
    last = len(transactions) - 1
    assert len(transactions) == 1
    assert transactions[last].entity_id == "1"

    undoRedoService.undo()
    transactions = transactionService.get_all()
    assert len(transactions) == 0

    undoRedoService.redo()
    transactions = transactionService.get_all()
    last = len(transactions) - 1
    assert len(transactions) == 1
    assert transactions[last].entity_id == "1"

    undoRedoService.redo()
    transactions = transactionService.get_all()
    last = len(transactions) - 1
    assert len(transactions) == 2
    assert transactions[last].entity_id == "2"

    # TEST UNDO/REDO DELETE

    transactionService.delete("2")

    transactionService.delete("1")

    transactions = transactionService.get_all()
    assert len(transactions) == 0

    undoRedoService.undo()
    transactions = transactionService.get_all()
    last = len(transactions) - 1
    assert len(transactions) == 1
    assert transactions[last].entity_id == "1"

    undoRedoService.undo()
    transactions = transactionService.get_all()
    last = len(transactions) - 1
    assert len(transactions) == 2
    assert transactions[last].entity_id == "2"

    undoRedoService.redo()
    transactions = transactionService.get_all()
    last = len(transactions) - 1
    assert len(transactions) == 1
    assert transactions[last].entity_id == "1"

    undoRedoService.redo()
    transactions = transactionService.get_all()
    assert len(transactions) == 0

    undoRedoService.undo()
    transactions = transactionService.get_all()
    last = len(transactions) - 1
    assert len(transactions) == 1
    assert transactions[last].entity_id == "1"

    # TEST UNDO/REDO UPDATE

    transactionService.update(
        "1", "1", "1", 15, datetime.datetime(2021, 11, 1, 21, 4, 00)
    )

    transactions = transactionService.get_all()
    assert transactions[0].amount == 15

    undoRedoService.undo()
    transactions = transactionService.get_all()
    assert transactions[0].amount == 20

    undoRedoService.redo()
    transactions = transactionService.get_all()
    assert transactions[0].amount == 15

    transactionService.delete("1")
    transactions = transactionService.get_all()
    assert len(transactions) == 0

    # TEST UNDO/REDO DELETE INTERVAL

    transactionService.create(
        "1", "1", "1", 10, datetime.datetime(2021, 11, 15, 21, 4, 00)
    )
    transactionService.create(
        "2", "1", "1", 10, datetime.datetime(2021, 10, 15, 21, 4, 00)
    )
    transactionService.create(
        "3", "1", "1", 10, datetime.datetime(2021, 11, 27, 21, 4, 00)
    )
    transactionService.create(
        "4", "1", "1", 10, datetime.datetime(2021, 10, 30, 21, 4, 00)
    )

    transactionService.delete_interval(
        transactionService.get_all(),
        datetime.datetime(2021, 10, 28, 21, 4, 00),
        datetime.datetime(2021, 11, 17, 21, 4, 00),
    )
    assert len(transactionService.get_all()) == 2

    undoRedoService.undo()
    assert len(transactionService.get_all()) == 4

    undoRedoService.redo()
    assert len(transactionService.get_all()) == 2

    undoRedoService.undo()
    assert len(transactionService.get_all()) == 4

    transactionService.delete("1")
    transactionService.delete("2")
    transactionService.delete("3")
    transactionService.delete("4")


def test_undo_redo():
    test_service_medicine_undo_redo()
    test_service_client_card_undo_redo()
    test_service_transaction_undo_redo()
