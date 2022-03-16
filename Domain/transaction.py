from dataclasses import dataclass
from datetime import datetime

from Domain.entity import Entity


@dataclass
class Transaction(Entity):
    """
    This is the description of a Transaction.
    """

    id_medicine: str
    id_client_card: str
    amount: int
    total: float
    sale: float
    dateandtime: datetime
