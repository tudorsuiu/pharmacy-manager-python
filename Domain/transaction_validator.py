from Domain.transaction import Transaction
from Domain.transaction_error import TransactionError


class TransactionValidator:
    def validate(self, transaction: Transaction):
        errors = []
        if transaction.entity_id.isdigit() is False:
            errors.append("Id-ul nu poate contine litere.")
        if transaction.id_medicine.isdigit() is False:
            errors.append("Id-ul medicamentului nu poate contine litere.")
        if transaction.id_client_card.isdigit() is False:
            errors.append("Id-ul cardului de client nu poate contine litere.")
        if transaction.amount < 0:
            errors.append("Numarul bucatilor nu poate fi negativ.")
        if transaction.dateandtime is None:
            errors.append("Data si ora efectuarii tranzactiei nu sunt valide!")
        if len(errors) > 0:
            raise TransactionError(errors)
