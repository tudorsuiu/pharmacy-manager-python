from Domain.client_card import ClientCard
from Domain.client_card_error import ClientCardError


class ClientCardValidator:
    def validate(self, clientCard: ClientCard):
        errors = []
        if clientCard.entity_id.isdigit() is False:
            errors.append("Id-ul nu poate contine litere.")
        if clientCard.first_name.isalpha() is False:
            errors.append("Prenumele nu poate contine cifre.")
        if clientCard.last_name.isalpha() is False:
            errors.append("Numele nu poate contine cifre.")
        if clientCard.CNP.isdigit() is False:
            errors.append("CNP-ul nu poate contine litere.")
        if clientCard.birthday is None:
            errors.append("Data de nastere introdusa nu este valida!")
        if clientCard.inregistration is None:
            errors.append("Data si ora efectuarii tranzactiei nu sunt valide!")
        if len(clientCard.CNP) < 13:
            errors.append("CNP-ul nu are 13 cifre!")
        if len(errors) > 0:
            raise ClientCardError(errors)
