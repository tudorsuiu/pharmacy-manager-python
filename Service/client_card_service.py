from datetime import datetime, date
from typing import List

from Domain.add_operation import AddOperation
from Domain.cascade_delete_operation import CascadeDeleteOperation
from Domain.client_card import ClientCard
from Domain.client_card_validator import ClientCardValidator
from Domain.modify_operation import ModifyOperation
from Repository.repository import Repository
from Service.undo_redo_service import UndoRedoService
from ViewModels.ClientCardDiscountsViewModel import CardDiscounts
from my_sort import my_sort


class ClientCardService:
    def __init__(
        self,
        clientCardRepository: Repository,
        clientCardValidator: ClientCardValidator,
        transactionRepository: Repository,
        undoRedoService: UndoRedoService,
    ):
        self.__clientCardRepository = clientCardRepository
        self.__clientCardValidator = clientCardValidator
        self.__transactionRepository = transactionRepository
        self.__undoRedoService = undoRedoService

    def get_all(self) -> List[ClientCard]:
        """
        Returneaza intr-o lista toate cardurile client existente.
        """
        return self.__clientCardRepository.read()

    def create(
        self,
        entity_id: str,
        first_name: str,
        last_name: str,
        CNP: str,
        birthday: datetime.date,
        inregistration: datetime.date,
    ) -> None:
        """
        Creeaza un obiect de tip ClientCard.
        """

        for card in self.__clientCardRepository.read():
            if card.CNP == CNP:
                raise KeyError("Clientul cu CNP-ul dat are deja un card!")

        clientCard = ClientCard(
            entity_id, first_name, last_name, CNP, birthday, inregistration
        )

        self.__clientCardValidator.validate(clientCard)
        self.__clientCardRepository.create(clientCard)

        self.__undoRedoService.add_undo_operation(
            AddOperation(self.__clientCardRepository, clientCard)
        )

    def delete(self, entity_id: str) -> None:
        """
        Sterge un obiect de tip ClientCard.
        """

        cascade = []

        transactions = self.__transactionRepository.read()

        for transaction in transactions:
            if transaction.id_client_card == entity_id:
                cascade.append(transaction)
                self.__transactionRepository.delete(transaction.entity_id)

        clientCard = self.__clientCardRepository.read(entity_id)
        cascade.append(clientCard)

        self.__clientCardRepository.delete(entity_id)

        self.__undoRedoService.add_undo_operation(
            CascadeDeleteOperation(
                self.__clientCardRepository,
                self.__transactionRepository,
                cascade,
            )
        )

    def update(
        self,
        entity_id: str,
        first_name: str,
        last_name: str,
        CNP: str,
        birthday: datetime.date,
        inregistration: datetime.date,
    ) -> None:
        """
        Modifica un obiect de tip ClientCard.
        """

        for card in self.__clientCardRepository.read():
            if card.CNP == CNP and card.entity_id != id:
                raise KeyError("CNP-ul introdus deja exista!")

        old_clientCard = self.__clientCardRepository.read(entity_id)
        new_clientCard = ClientCard(
            entity_id, first_name, last_name, CNP, birthday, inregistration
        )

        self.__clientCardValidator.validate(new_clientCard)
        self.__clientCardRepository.update(new_clientCard)

        self.__undoRedoService.add_undo_operation(
            ModifyOperation(
                self.__clientCardRepository, old_clientCard, new_clientCard
            )
        )

    def full_text_search_clients(self, search_this: str):
        """
        Cauta sirul de caractere dat in toate atributele obiectelor de tip
        ClientCard, indiferent de natura acestora.
        :param search_this: string - sirul de caractere cautat
        :return: lista cu obiectele de tip ClientCard ce contin stringul dat
        """

        def is_found(card: ClientCard, search_lower: str) -> bool:
            birthday_str = card.birthday.strftime("%d.%m.%Y")
            inregistration_str = card.inregistration.strftime("%d.%m.%Y")
            return (
                search_lower in card.first_name.lower()
                or search_lower in card.last_name.lower()
                or search_lower in card.CNP
                or search_lower in birthday_str
                or search_lower in inregistration_str
            )

        cards = self.__clientCardRepository.read()

        search = search_this.lower()

        result = list(filter(lambda card: is_found(card, search), cards))

        return result

    def sort_by_discount(self) -> List:
        """
        Cauta si ordoneaza descrescator cardurile client in functie de valoarea
        reducerilor obtinute
        :return: lista cu obiectele de tip ClientCard ordonate descrescator
        dupa valoarea reducerilor obtinute
        """

        discount_per_card = {}
        for card in self.__transactionRepository.read():
            discount_per_card[card.id_client_card] = 0
        for transaction in self.__transactionRepository.read():
            if (
                self.__clientCardRepository.read(transaction.id_client_card)
                is None
            ):
                discount_per_card[transaction.id_client_card] = 0
            else:
                discount_per_card[
                    transaction.id_client_card
                ] += transaction.sale

        result = []

        for id_client_card in discount_per_card:
            if self.__clientCardRepository.read(id_client_card):
                result.append(
                    CardDiscounts(
                        self.__clientCardRepository.read(id_client_card),
                        discount_per_card[id_client_card],
                    )
                )
            else:
                result.append(
                    CardDiscounts(
                        ClientCard(
                            id_client_card,
                            "NO CLIENT CARD",
                            "NO CLIENT CARD",
                            "NO CLIENT CARD",
                            date(1, 1, 1),
                            date(1, 1, 1),
                        ),
                        discount_per_card[id_client_card],
                    )
                )

        return my_sort(
            result, key=lambda discounts: discounts.discount, reverse=True
        )
