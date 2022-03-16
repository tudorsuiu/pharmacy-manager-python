from datetime import datetime
from typing import List

from Domain.add_operation import AddOperation
from Domain.delete_operation import DeleteOperation
from Domain.modify_operation import ModifyOperation
from Domain.multi_add_operation import MultiAddOperation
from Domain.transaction import Transaction
from Domain.transaction_validator import TransactionValidator
from Repository.repository import Repository
from Service.undo_redo_service import UndoRedoService


class TransactionService:
    def __init__(
        self,
        transactionRepository: Repository,
        clientCardRepository: Repository,
        medicineRepository: Repository,
        transactionValidator: TransactionValidator,
        undoRedoService: UndoRedoService,
    ):
        self.__transactionRepository = transactionRepository
        self.__transactionValidator = transactionValidator
        self.__clientCardRepository = clientCardRepository
        self.__medicineRepository = medicineRepository
        self.__undoRedoService = undoRedoService

    def get_all(self) -> List[Transaction]:
        """
        Returneaza intr-o lista toate tranzactiile existente.
        """
        return self.__transactionRepository.read()

    def create(
        self,
        entity_id: str,
        id_medicine: str,
        id_client_card: str,
        amount: int,
        dateandtime: datetime,
    ) -> None:
        """
        Creeaza un obiect de tip Transaction.
        """

        if self.__clientCardRepository.read(id_client_card) is not None:
            price = self.__medicineRepository.read(id_medicine).price_medicine
            if (
                self.__medicineRepository.read(
                    id_medicine
                ).prescription_medicine
                == "da"
            ):
                total = price * amount
                sale = (price * amount) * 0.15
                total_sale = total - sale
            else:
                total = price * amount
                sale = (price * amount) * 0.10
                total_sale = total - sale
        else:
            price = self.__medicineRepository.read(id_medicine).price_medicine
            total_sale = price * amount
            sale = 0

        transaction = Transaction(
            entity_id,
            id_medicine,
            id_client_card,
            amount,
            total_sale,
            sale,
            dateandtime,
        )

        self.__transactionValidator.validate(transaction)
        self.__transactionRepository.create(transaction)

        self.__undoRedoService.add_undo_operation(
            AddOperation(self.__transactionRepository, transaction)
        )

    def delete(self, entity_id: str) -> None:
        """
        Sterge un obiect de tip Transaction.
        """

        transaction = self.__transactionRepository.read(entity_id)

        self.__transactionRepository.delete(entity_id)

        self.__undoRedoService.add_undo_operation(
            DeleteOperation(self.__transactionRepository, transaction)
        )

    def update(
        self,
        entity_id: str,
        id_medicine: str,
        id_client_card: str,
        amount: int,
        dateandtime: datetime,
    ) -> None:
        """
        Modifica un obiect de tip Transaction.
        """

        old_transaction = self.__transactionRepository.read(entity_id)

        idm = old_transaction.id_medicine
        idc = old_transaction.id_client_card

        total_sale = old_transaction.total
        sale = 0

        if idm != id_medicine or idc != id_client_card:
            if self.__clientCardRepository.read(id_client_card) is not None:
                price = self.__medicineRepository.read(
                    id_medicine
                ).price_medicine
                if (
                    self.__medicineRepository.read(
                        id_medicine
                    ).prescription_medicine
                    == "da"
                ):
                    total = price * amount
                    sale = (price * amount) * 0.15
                    total_sale = total - sale
                else:
                    total = price * amount
                    sale = (price * amount) * 0.10
                    total_sale = total - sale
            else:
                price = self.__medicineRepository.read(
                    id_medicine
                ).price_medicine
                total_sale = price * amount
                sale = 0

        new_transaction = Transaction(
            entity_id,
            id_medicine,
            id_client_card,
            amount,
            total_sale,
            sale,
            dateandtime,
        )

        self.__transactionValidator.validate(new_transaction)
        self.__transactionRepository.update(new_transaction)

        self.__undoRedoService.add_undo_operation(
            ModifyOperation(
                self.__transactionRepository, old_transaction, new_transaction
            )
        )

    def show_interval(
        self, after_date: datetime, before_date: datetime
    ) -> List[Transaction]:
        """
        Cauta si creeaza o lista cu toate tranzactiile ce se afla intr-un
        interval dat
        :param after_date: datetime -
        :param before_date: datetime -
        :return: lista cu toate tranzactiile ce se afla intr-un interval dat
        """

        if after_date > before_date:
            raise KeyError(
                "Intervalul in care trebuie sa se caute "
                "tranzactia nu este valid!"
            )

        return [
            transaction
            for transaction in self.__transactionRepository.read()
            if after_date < transaction.dateandtime < before_date
        ]

    def delete_interval(
        self,
        transactions: List[Transaction],
        after_date: datetime,
        before_date: datetime,
        deleted=None,
        n: int = 0,
    ) -> None:
        """
        Sterge toate tranzactiile efectuate intr-un interval de zile dat.
        """
        if deleted is None:
            deleted = []
        if n == len(transactions):
            self.__undoRedoService.add_undo_operation(
                MultiAddOperation(self.__transactionRepository, deleted)
            )
            return None
        transaction = transactions[n]
        if after_date < transaction.dateandtime < before_date:
            deleted.append(transaction)
            self.__transactionRepository.delete(transaction.entity_id)
        self.delete_interval(
            transactions, after_date, before_date, deleted, n + 1
        )
