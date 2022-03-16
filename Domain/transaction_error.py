from dataclasses import dataclass
from typing import List


@dataclass
class TransactionError(Exception):
    error_message: List[str]

    def __str__(self):
        return f"TransactionError: {self.error_message}"
