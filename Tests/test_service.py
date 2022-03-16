import datetime

from Domain.client_card import ClientCard
from Domain.client_card_validator import ClientCardValidator
from Domain.medicine import Medicine
from Domain.medicine_validator import MedicineValidator
from Domain.transaction import Transaction
from Domain.transaction_validator import TransactionValidator
from Repository.repository_json import RepositoryJson
from Service.client_card_service import ClientCardService
from Service.medicine_service import MedicineService
from Service.transaction_service import TransactionService
from Service.undo_redo_service import UndoRedoService


def clear_file(filename: str) -> None:
    with open(filename, "w") as f:
        pass


def test_medicine_service():
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

    medicineService.create("1", "Nurofen", "Reckitt Benckiser", 12, "nu")
    assert len(medicineService.get_all()) == 1
    medicineService.update("1", "Nurofen", "Zenit", 12, "da")
    assert medicineService.get_all()[0] == Medicine(
        "1", "Nurofen", "Zenit", 12, "da"
    )
    medicineService.delete("1")
    assert len(medicineService.get_all()) == 0


def test_client_card_service():
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

    clientCardService.create(
        "1",
        "Mircea",
        "Avram",
        "5030523330500",
        datetime.date(2023, 3, 23),
        datetime.date(2010, 5, 12),
    )
    assert len(clientCardService.get_all()) == 1
    clientCardService.update(
        "1",
        "Dan",
        "Ionut",
        "5030523330501",
        datetime.date(2023, 3, 23),
        datetime.date(2010, 5, 12),
    )
    assert clientCardService.get_all()[0] == ClientCard(
        "1",
        "Dan",
        "Ionut",
        "5030523330501",
        datetime.date(2023, 3, 23),
        datetime.date(2010, 5, 12),
    )
    clientCardService.delete("1")
    assert len(clientCardService.get_all()) == 0


def test_transaction_service():
    clear_file("test_transactions.json")
    clear_file("test_client_cards.json")
    clear_file("test_medicines.json")

    transactionValidator = TransactionValidator()
    transactionRepository = RepositoryJson("test_transactions.json")

    clientCardValidator = ClientCardValidator()
    clientCardRepository = RepositoryJson("test_client_cards.json")

    medicineValidator = MedicineValidator()
    medicineRepository = RepositoryJson("test_medicines.json")

    undoRedoService = UndoRedoService()

    transactionService = TransactionService(
        transactionRepository,
        clientCardRepository,
        medicineRepository,
        transactionValidator,
        undoRedoService,
    )

    medicineService = MedicineService(
        medicineRepository,
        medicineValidator,
        transactionRepository,
        undoRedoService,
    )

    clientCardService = ClientCardService(
        clientCardRepository,
        clientCardValidator,
        transactionRepository,
        undoRedoService,
    )

    medicineService.create("1", "Nurofen", "Reckitt Benckiser", 10, "nu")
    medicineService.create("2", "Paracetamol", "Zenit", 10, "da")
    clientCardService.create(
        "1",
        "Mircea",
        "Avram",
        "5030523330500",
        datetime.date(2023, 3, 23),
        datetime.date(2010, 5, 12),
    )
    transactionService.create(
        "1", "1", "1", 20, datetime.datetime(2021, 11, 1, 21, 4, 00)
    )
    assert len(transactionService.get_all()) == 1
    assert transactionService.get_all()[0] == Transaction(
        "1", "1", "1", 20, 180, 20, datetime.datetime(2021, 11, 1, 21, 4, 00)
    )
    transactionService.create(
        "2", "2", "1", 10, datetime.datetime(2021, 11, 10, 21, 4, 00)
    )
    assert len(transactionService.get_all()) == 2
    assert transactionService.get_all()[1] == Transaction(
        "2", "2", "1", 10, 85, 15, datetime.datetime(2021, 11, 10, 21, 4, 00)
    )
    transactionService.create(
        "3", "1", "3", 10, datetime.datetime(2021, 11, 15, 21, 4, 00)
    )
    assert len(transactionService.get_all()) == 3
    assert transactionService.get_all()[2] == Transaction(
        "3", "1", "3", 10, 100, 0, datetime.datetime(2021, 11, 15, 21, 4, 00)
    )
    transactionService.delete("2")
    assert len(transactionService.get_all()) == 2
    transactionService.delete("3")
    assert len(transactionService.get_all()) == 1
    transactionService.update(
        "1", "2", "1", 10, datetime.datetime(2021, 11, 15, 21, 4, 00)
    )
    assert transactionService.get_all()[0] == Transaction(
        "1", "2", "1", 10, 85, 15, datetime.datetime(2021, 11, 15, 21, 4, 00)
    )
    transactionService.delete("1")
    medicineService.delete("1")
    medicineRepository.delete("2")
    clientCardService.delete("1")

    medicineService.create("1", "Nurofen", "Reckitt Benckiser", 10, "nu")
    transactionService.create(
        "1", "1", "1", 20, datetime.datetime(2021, 11, 1, 21, 4, 00)
    )
    transactionService.create(
        "2", "1", "1", 10, datetime.datetime(2021, 11, 10, 21, 4, 00)
    )
    assert len(transactionService.get_all()) == 2

    medicineService.delete("1")
    assert len(transactionService.get_all()) == 0

    undoRedoService.undo()
    assert medicineService.get_all()[0].entity_id == "1"
    assert len(transactionService.get_all()) == 2

    undoRedoService.redo()
    assert len(medicineService.get_all()) == 0
    assert len(transactionService.get_all()) == 0

    undoRedoService.undo()
    assert medicineService.get_all()[0].entity_id == "1"
    assert len(transactionService.get_all()) == 2

    medicineService.delete("1")


def test_service_functionalities():
    clear_file("test_client_cards.json")
    clear_file("test_transactions.json")
    clear_file("test_medicines.json")

    clientCardValidator = ClientCardValidator()
    clientCardRepository = RepositoryJson("test_client_cards.json")

    transactionRepository = RepositoryJson("test_transactions.json")
    transactionValidator = TransactionValidator()

    medicineRepository = RepositoryJson("test_medicines.json")
    medicineValidator = MedicineValidator()

    undoRedoService = UndoRedoService()

    clientCardService = ClientCardService(
        clientCardRepository,
        clientCardValidator,
        transactionRepository,
        undoRedoService,
    )

    transactionService = TransactionService(
        transactionRepository,
        clientCardRepository,
        medicineRepository,
        transactionValidator,
        undoRedoService,
    )

    medicineService = MedicineService(
        medicineRepository,
        medicineValidator,
        transactionRepository,
        undoRedoService,
    )

    # \/\/\/ Test pentru cerinta 1.4
    medicineService.create("1", "Nurofen", "Reckitt Benckiser", 10, "nu")
    medicineService.create("2", "Paracetamol", "Zenit", 10, "da")
    clientCardService.create(
        "1",
        "Mitcea",
        "Avram",
        "5030523330500",
        datetime.date(2023, 3, 23),
        datetime.date(2010, 5, 12),
    )
    search_this = "it"
    med_res = medicineService.full_text_search_medicine(search_this)
    cc_res = clientCardService.full_text_search_clients(search_this)
    assert len(med_res) == 2
    assert len(cc_res) == 1
    medicineService.delete("1")
    medicineService.delete("2")
    clientCardRepository.delete("1")
    # /\/\/\ Test pentru cerinta 1.4

    # \/\/\/ Test pentru cerinta 1.5
    medicineService.create("1", "Nurofen", "Reckitt Benckiser", 10, "nu")
    medicineService.create("2", "Paracetamol", "Zenit", 10, "da")
    clientCardService.create(
        "1",
        "Mircea",
        "Avram",
        "5030523330500",
        datetime.date(2023, 3, 23),
        datetime.date(2010, 5, 12),
    )
    transactionService.create(
        "1", "1", "1", 20, datetime.datetime(2021, 11, 1, 21, 4, 00)
    )
    transactionService.create(
        "2", "2", "1", 10, datetime.datetime(2021, 11, 10, 21, 4, 00)
    )
    transactionService.create(
        "3", "1", "3", 10, datetime.datetime(2021, 11, 15, 21, 4, 00)
    )
    after_date = datetime.datetime(2021, 10, 11, 00, 00, 00)
    before_date = datetime.datetime(2021, 11, 8, 21, 4, 00)
    interval = transactionService.show_interval(after_date, before_date)
    assert len(interval) == 1
    transactionService.delete("1")
    transactionService.delete("2")
    transactionService.delete("3")
    clientCardService.delete("1")
    medicineService.delete("1")
    medicineService.delete("2")
    # /\/\/\ Test pentru cerinta 1.5

    # \/\/\/ Test pentru cerinta 1.6
    medicineService.create("1", "Nurofen", "Reckitt Benckiser", 10, "nu")
    medicineService.create("2", "Paracetamol", "Zenit", 20, "da")
    transactionService.create(
        "1", "1", "1", 20, datetime.datetime(2021, 11, 1, 21, 4, 00)
    )
    transactionService.create(
        "2", "2", "1", 10, datetime.datetime(2021, 11, 10, 21, 4, 00)
    )
    transactionService.create(
        "3", "1", "3", 10, datetime.datetime(2021, 11, 15, 21, 4, 00)
    )
    result = medicineService.sort_meds_by_sales()
    assert result[0].medicament.name_medicine == "Nurofen"
    assert result[0].vanzari == 30
    assert result[1].medicament.name_medicine == "Paracetamol"
    assert result[1].vanzari == 10
    medicineService.delete("1")
    medicineService.delete("2")
    # /\/\/\ Test pentru cerinta 1.6

    # \/\/\/ Test pentru cerinta 1.7
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
        "Stefan",
        "Cherescu",
        "5030523330501",
        datetime.date(2023, 3, 23),
        datetime.date(2010, 5, 12),
    )
    medicineService.create("1", "Nurofen", "Reckitt Benckiser", 10, "nu")
    medicineService.create("2", "Paracetamol", "Zenit", 20, "da")
    transactionService.create(
        "1", "2", "2", 10, datetime.datetime(2021, 11, 15, 21, 4, 00)
    )
    transactionService.create(
        "2", "1", "3", 20, datetime.datetime(2021, 10, 15, 21, 4, 00)
    )
    transactionService.create(
        "3", "1", "1", 20, datetime.datetime(2021, 11, 27, 21, 4, 00)
    )
    transactionService.create(
        "4", "1", "2", 10, datetime.datetime(2021, 10, 30, 21, 4, 00)
    )
    result = clientCardService.sort_by_discount()
    assert len(result) == 3
    assert result[0].clientCard == ClientCard(
        "2",
        "Stefan",
        "Cherescu",
        "5030523330501",
        datetime.date(2023, 3, 23),
        datetime.date(2010, 5, 12),
    )
    assert result[0].discount == 40
    assert result[1].clientCard == ClientCard(
        "1",
        "Mircea",
        "Avram",
        "5030523330500",
        datetime.date(2023, 3, 23),
        datetime.date(2010, 5, 12),
    )
    assert result[1].discount == 20
    assert result[2].clientCard == ClientCard(
        "3",
        "NO CLIENT CARD",
        "NO CLIENT CARD",
        "NO CLIENT CARD",
        datetime.date(1, 1, 1),
        datetime.date(1, 1, 1),
    )
    assert result[2].discount == 0
    clientCardService.delete("1")
    clientCardService.delete("2")
    medicineService.delete("1")
    medicineService.delete("2")
    # /\/\/\ Test pentru cerinta 1.7

    # \/\/\/ Test pentru cerinta 1.8
    medicineRepository.create(
        Medicine("1", "Nurofen", "Reckitt Benckiser", 10, "nu")
    )
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
    assert transactionService.get_all()[0].entity_id == "2"
    assert transactionService.get_all()[1].entity_id == "3"
    transactionService.delete("2")
    transactionService.delete("3")
    medicineService.delete("1")
    # /\/\/\ Test pentru cerinta 1.8

    # \/\/\/ Test pentru cerinta 1.9
    medicineService.create("1", "Nurofen", "Reckitt Benckiser", 10, "nu")
    medicineService.create("2", "Paracetamol", "Zenit", 20, "da")
    medicineService.increase_by_percentage(15, 50)
    assert medicineService.get_all()[0].price_medicine == 15
    medicineService.delete("1")
    medicineService.delete("2")
    # /\/\/\ Test pentru cerinta 1.9


def test_service():
    test_medicine_service()
    test_client_card_service()
    test_transaction_service()
    test_service_functionalities()
