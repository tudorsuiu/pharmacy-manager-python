from dataclasses import dataclass

from Domain.entity import Entity


@dataclass
class Medicine(Entity):
    """
    This is the description of a medicine.
    """

    name_medicine: str
    producer_medicine: str
    price_medicine: float
    prescription_medicine: str
