import datetime

from Domain.client_card import ClientCard
from Domain.medicine import Medicine
from Domain.transaction import Transaction


def test_medicine():
    medicine = Medicine("1", "Nurofen", "Reckitt Benckiser", 12, "nu")
    assert medicine.entity_id == "1"
    assert medicine.name_medicine == "Nurofen"
    assert medicine.producer_medicine == "Reckitt Benckiser"
    assert medicine.price_medicine == 12
    assert medicine.prescription_medicine == "nu"
    medicine.name_medicine = "Paracetamol"
    medicine.producer_medicine = "Zentiva"
    medicine.price_medicine = 20
    assert medicine.entity_id == "1"
    assert medicine.name_medicine == "Paracetamol"
    assert medicine.producer_medicine == "Zentiva"
    assert medicine.price_medicine == 20
    assert medicine.prescription_medicine == "nu"


def test_client_card():
    clientCard = ClientCard(
        "1",
        "Mircea",
        "Avram",
        "5030523330500",
        datetime.date(2023, 3, 23),
        datetime.date(2010, 5, 12),
    )
    assert clientCard.entity_id == "1"
    assert clientCard.first_name == "Mircea"
    assert clientCard.last_name == "Avram"
    assert clientCard.CNP == "5030523330500"
    assert clientCard.birthday == datetime.date(2023, 3, 23)
    assert clientCard.inregistration == datetime.date(2010, 5, 12)
    clientCard.first_name = "Ionut"
    clientCard.last_name = "Dan"
    clientCard.CNP = "5020721330211"
    clientCard.birthday = datetime.date(2021, 4, 21)
    clientCard.inregistration = datetime.date(2010, 10, 12)
    assert clientCard.entity_id == "1"
    assert clientCard.first_name == "Ionut"
    assert clientCard.last_name == "Dan"
    assert clientCard.CNP == "5020721330211"
    assert clientCard.birthday == datetime.date(2021, 4, 21)
    assert clientCard.inregistration == datetime.date(2010, 10, 12)


def test_transaction():
    transaction = Transaction(
        "1", "1", "1", 20, 0, 0, datetime.datetime(2021, 11, 15, 21, 4, 00)
    )
    assert transaction.entity_id == "1"
    assert transaction.id_medicine == "1"
    assert transaction.id_client_card == "1"
    assert transaction.amount == 20
    assert transaction.dateandtime == datetime.datetime(2021, 11, 15, 21, 4, 0)
    transaction.id_client_card = "3"
    transaction.id_medicine = "2"
    transaction.amount = 15
    transaction.dateandtime = datetime.datetime(2020, 11, 15, 10, 4, 0)
    assert transaction.entity_id == "1"
    assert transaction.id_medicine == "2"
    assert transaction.id_client_card == "3"
    assert transaction.amount == 15
    assert transaction.dateandtime == datetime.datetime(2020, 11, 15, 10, 4, 0)


def test_domain():
    test_medicine()
    test_client_card()
    test_transaction()
