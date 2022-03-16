import datetime

from Domain.client_card import ClientCard
from Domain.medicine import Medicine
from Domain.transaction import Transaction
from Repository.repository_in_memory import RepositoryInMemory
from Repository.repository_json import RepositoryJson


def clear_file(filename: str) -> None:
    with open(filename, "w") as f:
        pass


def test_medicine_file_repository():
    clear_file("test_medicines.json")
    repo = RepositoryJson("test_medicines.json")
    repo.create(Medicine("1", "Nurofen", "Reckitt Benckiser", 12, "nu"))
    assert len(repo.read()) == 1
    repo.update(Medicine("1", "Nurofen", "Pfizer", 20, "da"))
    assert repo.read("1").producer_medicine == "Pfizer"
    assert repo.read("1").price_medicine == 20
    assert repo.read("1").prescription_medicine == "da"
    repo.delete("1")
    assert len(repo.read()) == 0


def test_client_card_file_repository():
    clear_file("test_client_cards.json")
    repo = RepositoryJson("test_client_cards.json")
    repo.create(
        ClientCard(
            "1",
            "Mircea",
            "Avram",
            "5030523330500",
            datetime.date(2023, 3, 23),
            datetime.date(2010, 5, 12),
        )
    )
    assert len(repo.read()) == 1
    repo.update(
        ClientCard(
            "1",
            "Dan",
            "Ionut",
            "5030523330500",
            datetime.date(2023, 3, 23),
            datetime.date(2010, 5, 12),
        )
    )
    assert repo.read("1").first_name == "Dan"
    assert repo.read("1").last_name == "Ionut"
    repo.delete("1")
    assert len(repo.read()) == 0


def test_transaction_file_repository():
    clear_file("test_transactions.json")
    repo = RepositoryJson("test_transactions.json")
    repo.create(
        Transaction(
            "1", "1", "1", 20, 0, 0, datetime.datetime(2021, 11, 15, 21, 4, 00)
        )
    )
    assert len(repo.read()) == 1
    repo.update(
        Transaction(
            "1", "3", "2", 15, 0, 0, datetime.datetime(2020, 11, 15, 21, 4, 00)
        )
    )
    assert repo.read("1").id_medicine == "3"
    assert repo.read("1").id_client_card == "2"
    assert repo.read("1").amount == 15
    data = datetime.datetime(2020, 11, 15, 21, 4, 00)
    assert repo.read("1").dateandtime == data
    repo.delete("1")
    assert len(repo.read()) == 0


def test_medicine_repository():
    repo = RepositoryInMemory()
    repo.create(Medicine("1", "Nurofen", "Reckitt Benckiser", 12, "nu"))
    assert len(repo.read()) == 1
    repo.update(Medicine("1", "Paracetamol", "Reckitt Benckiser", 12, "da"))
    assert repo.read("1").producer_medicine == "Reckitt Benckiser"
    assert repo.read("1").prescription_medicine == "da"
    repo.delete("1")
    assert len(repo.read()) == 0


def test_client_card_repository():
    repo = RepositoryInMemory()
    repo.create(
        ClientCard(
            "1",
            "Mircea",
            "Avram",
            "5030523330500",
            datetime.date(2023, 3, 23),
            datetime.date(2010, 5, 12),
        )
    )
    assert len(repo.read()) == 1
    repo.update(
        ClientCard(
            "1",
            "Dan",
            "Ionut",
            "5030523330500",
            datetime.date(2023, 3, 23),
            datetime.date(2010, 5, 12),
        )
    )
    assert repo.read("1").first_name == "Dan"
    assert repo.read("1").last_name == "Ionut"
    repo.delete("1")
    assert len(repo.read()) == 0


def test_transactions_repository():
    repo = RepositoryInMemory()
    repo.create(
        Transaction(
            "1", "1", "1", 20, 0, 0, datetime.datetime(2021, 11, 15, 21, 4, 00)
        )
    )
    assert len(repo.read()) == 1
    repo.update(
        Transaction(
            "1", "3", "2", 15, 0, 0, datetime.datetime(2020, 11, 15, 21, 4, 00)
        )
    )
    assert repo.read("1").id_medicine == "3"
    assert repo.read("1").id_client_card == "2"
    assert repo.read("1").amount == 15
    data = datetime.datetime(2020, 11, 15, 21, 4, 00)
    assert repo.read("1").dateandtime == data
    repo.delete("1")
    assert len(repo.read()) == 0


def test_repository():
    test_medicine_file_repository()
    test_client_card_file_repository()
    test_transaction_file_repository()
    test_medicine_repository()
    test_client_card_repository()
    test_transactions_repository()
