from dataclasses import dataclass
from typing import List


@dataclass
class MedicineError(Exception):
    error_message: List[str]

    def __str__(self):
        return f"MedicineError: {self.error_message}"
