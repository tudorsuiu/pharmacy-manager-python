from dataclasses import dataclass

from Domain.medicine import Medicine


@dataclass
class MedsSales:
    medicament: Medicine
    vanzari: int

    def __str__(self):
        return (
            f"{self.medicament} s-a vandut intr-o "
            f"cantitate de {self.vanzari} bucati."
        )
