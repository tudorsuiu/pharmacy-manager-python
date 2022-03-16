from Domain.medicine import Medicine
from Domain.medicine_error import MedicineError


class MedicineValidator:
    def validate(self, medicine: Medicine):
        errors = []
        if medicine.entity_id.isdigit() is False:
            errors.append("Id-ul nu poate contine litere")
        if medicine.price_medicine < 0:
            errors.append("Pretul nu poate fi un numar negativ.")
        if medicine.prescription_medicine not in ["da", "nu"]:
            errors.append(
                "Daca necesita reteta trebuie " "specificat 'da' sau 'nu'."
            )
        if len(errors) > 0:
            raise MedicineError(errors)
