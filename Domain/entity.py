from abc import ABC
from dataclasses import dataclass


@dataclass
class Entity(ABC):
    entity_id: str
