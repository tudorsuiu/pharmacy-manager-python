import random
import string
from typing import List

from Domain.add_operation import AddOperation
from Domain.cascade_delete_operation import CascadeDeleteOperation
from Domain.medicine import Medicine
from Domain.medicine_validator import MedicineValidator
from Domain.modify_operation import ModifyOperation
from Domain.multi_delete_operation import MultiDeleteOperation
from Domain.multi_modify_operation import MultiModifyOperation
from Repository.repository import Repository
from Service.undo_redo_service import UndoRedoService
from ViewModels.MedsSalesViewModel import MedsSales
from my_sort import my_sort


class MedicineService:
    def __init__(
        self,
        medicineRepository: Repository,
        medicineValidator: MedicineValidator,
        transactionRepository: Repository,
        undoRedoService: UndoRedoService,
    ):
        self.__medicineRepository = medicineRepository
        self.__medicineValidator = medicineValidator
        self.__transactionRepository = transactionRepository
        self.__undoRedoService = undoRedoService

    def get_all(self) -> List[Medicine]:
        """
        Returneaza intr-o lista toate medicamentele existente.
        """
        return self.__medicineRepository.read()

    def create(
        self,
        entity_id: str,
        name_medicine: str,
        producer_medicine: str,
        price_medicine: float,
        prescription_medicine: str,
    ) -> None:
        """
        Creeaza un obiect de tip Medicine.
        """
        medicine = Medicine(
            entity_id,
            name_medicine,
            producer_medicine,
            price_medicine,
            prescription_medicine,
        )
        self.__medicineValidator.validate(medicine)
        self.__medicineRepository.create(medicine)
        self.__undoRedoService.add_undo_operation(
            AddOperation(self.__medicineRepository, medicine)
        )

    def delete(self, entity_id: str) -> None:
        """
        Sterge un obiect de tip Medicine.
        """

        cascade = []

        transactions = self.__transactionRepository.read()
        for transaction in transactions:
            if transaction.id_medicine == entity_id:
                cascade.append(transaction)
                self.__transactionRepository.delete(transaction.entity_id)

        medicine = self.__medicineRepository.read(entity_id)
        cascade.append(medicine)

        self.__medicineRepository.delete(entity_id)

        self.__undoRedoService.add_undo_operation(
            CascadeDeleteOperation(
                self.__medicineRepository,
                self.__transactionRepository,
                cascade,
            )
        )

    def update(
        self,
        entity_id: str,
        name_medicine: str,
        producer_medicine: str,
        price_medicine: float,
        prescription_medicine: str,
    ) -> None:
        """
        Modifica un obiect de tip Medicine.
        """
        old_medicine = self.__medicineRepository.read(entity_id)
        new_medicine = Medicine(
            entity_id,
            name_medicine,
            producer_medicine,
            price_medicine,
            prescription_medicine,
        )
        self.__medicineValidator.validate(new_medicine)
        self.__medicineRepository.update(new_medicine)
        self.__undoRedoService.add_undo_operation(
            ModifyOperation(
                self.__medicineRepository, old_medicine, new_medicine
            )
        )

    def full_text_search_medicine(self, search_this: str) -> List[Medicine]:
        """
        Cauta sirul de caractere dat in toate atributele obiectelor de tip
        Medicine, indiferent de natura acestora.
        :param search_this: string - sirul de caractere cautat
        :return: lista cu obiectele de tip Medicine ce contin stringul dat
        """

        def is_found(med: Medicine, search_lower: str) -> bool:
            return (
                search_lower.lower() in med.name_medicine.lower()
                or search_lower.lower() in med.producer_medicine.lower()
                or search_lower.lower() in str(med.price_medicine).lower()
                or search_lower.lower() in med.prescription_medicine.lower()
            )

        meds = self.__medicineRepository.read()

        search = search_this.lower()

        result = list(filter(lambda med: is_found(med, search), meds))

        return result

    def sort_meds_by_sales(self) -> List:
        """
        Cauta si ordoneaza descrescator medicamentele in functie de numarul
        bucatilor vandute
        :return: lista cu obiectele de tip Medicine ordonate descrescator in
        functie de numarul bucatilor vandute
        """
        sales_per_med = {}
        for med in self.__medicineRepository.read():
            sales_per_med[med.entity_id] = 0
        for transaction in self.__transactionRepository.read():
            sales_per_med[transaction.id_medicine] += transaction.amount
        result = []
        for id_medicine in sales_per_med:
            result.append(
                MedsSales(
                    self.__medicineRepository.read(id_medicine),
                    sales_per_med[id_medicine],
                )
            )
        return my_sort(result, key=lambda sales: sales.vanzari, reverse=True)

    def increase_by_percentage(self, below: float, increase_by: float) -> None:
        """
        Cauta medicamentele care au pretul de vanzare mai mic decat o valoare
        data si il va scumpi cu procentaj dat
        """
        old_medicines = self.__medicineRepository.read()

        medicines_below = list(
            filter(
                lambda x: (True if x.price_medicine < below else False),
                old_medicines,
            )
        )

        def increase(med: Medicine, increase_price: float):
            med = Medicine(
                med.entity_id,
                med.name_medicine,
                med.producer_medicine,
                med.price_medicine
                + med.price_medicine * (increase_price / 100),
                med.prescription_medicine,
            )
            return med

        new_medicines = list(
            map(lambda x: increase(x, increase_by), medicines_below)
        )

        for med in new_medicines:
            self.__medicineRepository.update(med)

        self.__undoRedoService.add_undo_operation(
            MultiModifyOperation(
                self.__medicineRepository, old_medicines, new_medicines
            )
        )

    def random_medicine(self, n: int):
        """
        Genereaza n obiecte de tip medicament aleatoriu, toate atributele sale
        fiind valide
        """

        random_meds = []

        for i in range(n):
            meds = int(len(self.__medicineRepository.read()))
            id_med = str(meds + 1)
            name_med = "".join(random.choices(string.ascii_letters, k=5))
            prod_med = "".join(random.choices(string.ascii_letters, k=5))
            price_med = round(random.uniform(0, 300), 2)
            prescription_med = random.choice(["da", "nu"])
            random_med = Medicine(
                id_med, name_med, prod_med, price_med, prescription_med
            )
            random_meds.append(random_med)
            self.__medicineValidator.validate(random_med)
            self.__medicineRepository.create(random_med)

        self.__undoRedoService.add_undo_operation(
            MultiDeleteOperation(self.__medicineRepository, random_meds)
        )
