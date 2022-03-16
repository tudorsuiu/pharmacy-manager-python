from dataclasses import dataclass
from datetime import datetime

from Domain.entity import Entity


@dataclass
class ClientCard(Entity):
    """
    This is the description of a client card.
    """

    first_name: str
    last_name: str
    CNP: str
    birthday: datetime.date
    inregistration: datetime.date
