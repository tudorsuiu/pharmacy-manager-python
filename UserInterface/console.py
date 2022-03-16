from datetime import date, datetime

from Service.client_card_service import ClientCardService
from Service.medicine_service import MedicineService
from Service.transaction_service import TransactionService
from Service.undo_redo_service import UndoRedoService


class Console:
    def __init__(
        self,
        medicineService: MedicineService,
        clientCardService: ClientCardService,
        transactionService: TransactionService,
        undoRedoService: UndoRedoService,
    ):
        self.__medicineService = medicineService
        self.__clientCardService = clientCardService
        self.__transactionService = transactionService
        self.__undoRedoService = undoRedoService

    # \/ \/ \/ CRUD MEDICINE
    def ui_create_medicine(self) -> None:
        try:
            id_medicine = input("Dati id-ul medicamentului: ")
            name_medicine = input("Dati numele medicamentului: ")
            producer_medicine = input("Dati producatorul medicamentului: ")
            price_medicine = float(input("Dati pretul medicamentului: "))
            prescription_medicine = input(
                "Are nevoie de " "prescriptie? (da/nu) "
            )
            self.__medicineService.create(
                id_medicine,
                name_medicine,
                producer_medicine,
                price_medicine,
                prescription_medicine,
            )
        except ValueError as ve:
            print(ve)
        except KeyError as ke:
            print(ke)
        except Exception as e:
            print(e)

    def ui_delete_medicine(self) -> None:
        try:
            id_medicine = input("Dati id-ul medicamentului de sters: ")
            self.__medicineService.delete(id_medicine)
        except KeyError as ke:
            print(ke)
        except Exception as e:
            print(e)

    def ui_update_medicine(self) -> None:
        try:
            id_medicine = input("Dati id-ul al medicamentului de modificat: ")
            name_medicine = input("Dati noul nume al medicamentului: ")
            producer_medicine = input(
                "Dati noul producator al " "medicamentului: "
            )
            price_medicine = float(input("Dati noul pret al medicamentului: "))
            prescription_medicine = input(
                "Are nevoie de " "prescriptie? (da/nu) "
            )
            self.__medicineService.update(
                id_medicine,
                name_medicine,
                producer_medicine,
                price_medicine,
                prescription_medicine,
            )
        except ValueError as ve:
            print(ve)
        except KeyError as ke:
            print(ke)
        except Exception as e:
            print(e)

    def ui_random_medicine(self) -> None:
        try:
            n = int(input("Dati nr. medicamentelor generate aleatoriu: "))
            self.__medicineService.random_medicine(n)
        except ValueError as ve:
            print(ve)
        except KeyError as ke:
            print(ke)
        except Exception as e:
            print(e)

    def showall_medicines(self) -> None:
        for medicine in self.__medicineService.get_all():
            print(medicine)

    def run_CRUD_medicine_menu(self) -> None:
        while True:
            print("1. Adauga medicament")
            print("2. Sterge medicament")
            print("3. Modifica medicament")
            print(
                "4. Afisarea medicamentelor ordonate descrescator "
                "dupa numarul de vanzari"
            )
            print(
                "5. Scumpirea cu un procetaj dat a tuturor medicamentelor "
                "cu pretul mai mic decat o valoare data"
            )
            print("n. Creeaza n medicamente aleatorii")
            print("u. Undo")
            print("r. Redo")
            print("a. Afiseaza toate medicamentele")
            print("x. Iesire")
            option = input("Dati optiunea: ")
            if option == "1":
                self.ui_create_medicine()
            elif option == "2":
                self.ui_delete_medicine()
            elif option == "3":
                self.ui_update_medicine()
            elif option == "4":
                self.ui_sort_meds_by_sales()
            elif option == "5":
                self.ui_increase_by_percentage()
            elif option == "n":
                self.ui_random_medicine()
            elif option == "u":
                self.__undoRedoService.undo()
            elif option == "r":
                self.__undoRedoService.redo()
            elif option == "a":
                self.showall_medicines()
            elif option == "x":
                break
            else:
                print("Optiune gresita! Reincercati!")

    # /\ /\ /\ CRUD MEDICINE

    # \/ \/ \/ CRUD CLIENT CARD
    def read_date(self, dateandtime: str) -> date or None:
        try:
            date_str = dateandtime
            date_split = date_str.split(".")
            dd = int(date_split[0])
            mm = int(date_split[1])
            yyyy = int(date_split[2])
            return date(yyyy, mm, dd)
        except ValueError:
            return None

    def ui_create_client_card(self) -> None:
        try:
            entity_id = input("Dati id-ul cardului de client: ")
            first_name = input("Dati prenumele clientului: ")
            last_name = input("Dati numele clientului: ")
            CNP = input("Dati CNP-ul clientului: ")
            birthday_str = input(
                "Dati data de nastere a " "clientului (dd.mm.yyyy): "
            )
            birthday = self.read_date(birthday_str)
            inregistration_str = input(
                "Dati data de inregistrare a " "clientului (dd.mm.yyyy): "
            )
            inregistration = self.read_date(inregistration_str)
            self.__clientCardService.create(
                entity_id, first_name, last_name, CNP, birthday, inregistration
            )
        except ValueError as ve:
            print(ve)
        except KeyError as ke:
            print(ke)
        except Exception as e:
            print(e)

    def ui_delete_client_card(self) -> None:
        try:
            entity_id = input("Dati id-ul de sters: ")
            self.__clientCardService.delete(entity_id)
        except ValueError as ve:
            print(ve)
        except KeyError as ke:
            print(ke)
        except Exception as e:
            print(e)

    def ui_update_client_card(self) -> None:
        try:
            entity_id = input("Dati id-ul cardului de client de modificat: ")
            first_name = input("Modificati prenumele clientului: ")
            last_name = input("Modificati numele clientului: ")
            CNP = input("Modificati CNP-ul clientului: ")
            birthday_str = input(
                "Modificati data de nastere a " "clientului (dd.mm.yyyy): "
            )
            birthday = self.read_date(birthday_str)
            inregistration_str = input(
                "Modificati data de inregistrare a "
                "clientului (dd.mm.yyyy): "
            )
            inregistration = self.read_date(inregistration_str)
            self.__clientCardService.update(
                entity_id, first_name, last_name, CNP, birthday, inregistration
            )
        except ValueError as ve:
            print(ve)
        except KeyError as ke:
            print(ke)
        except Exception as e:
            print(e)

    def showall_client_cards(self) -> None:
        for client in self.__clientCardService.get_all():
            print(client)

    def run_CRUD_client_card_menu(self) -> None:
        while True:
            print("1. Adauga card client")
            print("2. Sterge card client")
            print("3. Modifica card client")
            print(
                "4. Afisarea cardurilor client ordonate descrescator dupa "
                "valoarea reducerilor obtinute"
            )
            print("u. Undo")
            print("r. Redo")
            print("a. Afiseaza toate cardurile client")
            print("x. Iesire")
            option = input("Dati optiunea: ")
            if option == "1":
                self.ui_create_client_card()
            elif option == "2":
                self.ui_delete_client_card()
            elif option == "3":
                self.ui_update_client_card()
            elif option == "4":
                self.ui_sort_by_discount()
            elif option == "u":
                self.__undoRedoService.undo()
            elif option == "r":
                self.__undoRedoService.redo()
            elif option == "a":
                self.showall_client_cards()
            elif option == "x":
                break
            else:
                print("Optiune gresita! Reincercati!")

    # /\ /\ /\ CRUD CLIENT CARD

    # \/ \/ \/ CRUD TRANSACTION
    def read_dateandtime(self, dateandtime: str) -> datetime or None:
        try:
            datetime_str = dateandtime
            datetime_str_split = datetime_str.split(" ")
            date_str = datetime_str_split[0]
            date_str_split = date_str.split(".")
            time_str = datetime_str_split[1]
            time_str_split = time_str.split(":")
            dd = int(date_str_split[0])
            mm = int(date_str_split[1])
            yyyy = int(date_str_split[2])
            HH = int(time_str_split[0])
            MM = int(time_str_split[1])
            SS = int(time_str_split[2])
            return datetime(yyyy, mm, dd, HH, MM, SS)
        except ValueError:
            return None

    def ui_create_transaction(self) -> None:
        try:
            entity_id = input("Dati id-ul tranzactiei: ")
            id_medicine = input("Dati id-ul medicamentului: ")
            id_client_card = input("Dati id-ul cardului clientului: ")
            amount = int(input("Dati numarul de bucati: "))
            dateandtime_str = input(
                "Dati data si ora tranzactiei " "(dd.mm.yyyy HH:MM:SS): "
            )
            dateandtime = self.read_dateandtime(dateandtime_str)
            self.__transactionService.create(
                entity_id, id_medicine, id_client_card, amount, dateandtime
            )
        except ValueError as ve:
            print(ve)
        except KeyError as ke:
            print(ke)
        except Exception as e:
            print(e)

    def ui_delete_transaction(self) -> None:
        try:
            entity_id = input("Dati id-ul tranzactiei de sters: ")
            self.__transactionService.delete(entity_id)
        except ValueError as ve:
            print(ve)
        except KeyError as ke:
            print(ke)
        except Exception as e:
            print(e)

    def ui_update_transaction(self) -> None:
        try:
            entity_id = input("Dati id-ul tranzactiei de modificat: ")
            id_medicine = input("Modificati id-ul medicamentului: ")
            id_client_card = input("Modificati id-ul cardului de client: ")
            amount = int(input("Modificati numarul de bucati: "))
            dateandtime_str = input(
                "Modificati data si ora tranzactiei " "(dd.mm.yyyy HH:MM:SS): "
            )
            dateandtime = self.read_dateandtime(dateandtime_str)
            self.__transactionService.update(
                entity_id, id_medicine, id_client_card, amount, dateandtime
            )
        except ValueError as ve:
            print(ve)
        except KeyError as ke:
            print(ke)
        except Exception as e:
            print(e)

    def showall_transactions(self) -> None:
        for transaction in self.__transactionService.get_all():
            print(transaction)

    def run_CRUD_transaction_menu(self) -> None:
        while True:
            print("1. Adauga tranzactie")
            print("2. Sterge tranzactie")
            print("3. Modifica tranzactie")
            print(
                "4. Afisarea tuturor tranzactiilor dintr-un interval de "
                "zile dat"
            )
            print(
                "5. Stergerea tuturor tranzactiilor dintr-un "
                "interval de zile dat"
            )
            print("u. Undo")
            print("r. Redo")
            print("a. Afiseaza toate tranzactiile")
            print("x. Iesire")
            option = input("Dati optiunea: ")
            if option == "1":
                self.ui_create_transaction()
            elif option == "2":
                self.ui_delete_transaction()
            elif option == "3":
                self.ui_update_transaction()
            elif option == "4":
                self.ui_show_transactions_in_interval()
            elif option == "5":
                self.ui_delete_transactions_in_interval()
            elif option == "u":
                self.__undoRedoService.undo()
            elif option == "r":
                self.__undoRedoService.redo()
            elif option == "a":
                self.showall_transactions()
            elif option == "x":
                break
            else:
                print("Optiune gresita! Reincercati!")

    # /\ /\ /\ CRUD TRANSACTION

    # \/ \/ \/ FUNCTIONALITIES
    """ CERINTA 1.4 """

    def ui_full_text_search(self) -> None:
        search_this = input("Cautati in lista de medicamente si clienti: ")
        med_res = self.__medicineService.full_text_search_medicine(search_this)
        cc_res = self.__clientCardService.full_text_search_clients(search_this)
        for med in med_res:
            print(med)
        for card in cc_res:
            print(card)

    """ CERINTA 1.5 """

    def ui_show_transactions_in_interval(self) -> None:
        try:
            interval = input(
                "Dati intervalul de zile si orele intre"
                " care sa se caute (dd.mm.yyyy HH:MM:SS/"
                "dd.mm.yyyy HH:MM:SS): "
            )
            interval_split = interval.split("/")
            after_date = self.read_dateandtime(interval_split[0])
            before_date = self.read_dateandtime(interval_split[1])
            between = self.__transactionService.show_interval(
                after_date, before_date
            )
            if between:
                for transaction in between:
                    print(transaction)
            else:
                print("Nu se afla nicio tranzactie in intervalul dat!")
        except ValueError as ve:
            print(ve)
        except KeyError as ke:
            print(ke)
        except Exception as e:
            print(e)

    """ CERINTA 1.6 """

    def ui_sort_meds_by_sales(self) -> None:
        try:
            for med_sales in self.__medicineService.sort_meds_by_sales():
                print(med_sales)
        except ValueError as ve:
            print(ve)
        except KeyError as ke:
            print(ke)
        except Exception as e:
            print(e)

    """ CERINTA 1.7 """

    def ui_sort_by_discount(self) -> None:
        try:
            for card in self.__clientCardService.sort_by_discount():
                print(card)
        except ValueError as ve:
            print(ve)
        except KeyError as ke:
            print(ke)
        except Exception as e:
            print(e)

    """ CERINTA 1.8 """

    def ui_delete_transactions_in_interval(self) -> None:
        try:
            interval = input(
                "Dati intervalul de zile si orele din care"
                " care sa se stearga (dd.mm.yyyy HH:MM:SS/"
                "dd.mm.yyyy HH:MM:SS): "
            )
            interval_split = interval.split("/")
            after_date = self.read_dateandtime(interval_split[0])
            before_date = self.read_dateandtime(interval_split[1])
            self.__transactionService.delete_interval(
                self.__transactionService.get_all(), after_date, before_date
            )
        except ValueError as ve:
            print(ve)
        except KeyError as ke:
            print(ke)
        except Exception as e:
            print(e)

    """ CERINTA 1.9 """

    def ui_increase_by_percentage(self) -> None:
        try:
            below = float(
                input("Scumpirea medicamentelor cu pretul " "mai mic decat:")
            )
            increase_by = int(input("Dati procentul scumpirii pretului: "))
            self.__medicineService.increase_by_percentage(below, increase_by)
        except ValueError as ve:
            print(ve)
        except KeyError as ke:
            print(ke)
        except Exception as e:
            print(e)

    # /\ /\ /\ FUNCTIONALITIES

    def run_menu(self) -> None:
        while True:
            print("1. CRUD medicamente")
            print("2. CRUD carduri client")
            print("3. CRUD tranzactii")
            print("4. Cautare in medicamente si cardurile clienti")
            print("x. Iesire")
            option = input("Dati optiunea: ")
            if option == "1":
                self.run_CRUD_medicine_menu()
            elif option == "2":
                self.run_CRUD_client_card_menu()
            elif option == "3":
                self.run_CRUD_transaction_menu()
            elif option == "4":
                self.ui_full_text_search()
            elif option == "x":
                break
            else:
                print("Optiune gresita! Reincercati!")
