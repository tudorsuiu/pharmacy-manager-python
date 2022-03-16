from dataclasses import dataclass
from typing import List


@dataclass
class ClientCardError(Exception):
    error_message: List[str]

    def __str__(self):
        return f"ClientCardError: {self.error_message}"
