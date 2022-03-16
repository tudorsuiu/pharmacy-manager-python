from dataclasses import dataclass

from Domain.client_card import ClientCard


@dataclass
class CardDiscounts:
    clientCard: ClientCard
    discount: float

    def __str__(self):
        return (
            f"{self.clientCard} a economisit in total " f"{self.discount} lei."
        )
