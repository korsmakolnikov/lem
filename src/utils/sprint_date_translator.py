from typing import Protocol
from dataclasses import dataclass
import numpy as np


@dataclass
class SprintDateData:
    year: np.short
    quarter: np.short
    sprint: np.short
    sprint_length: np.short


class SprintDateTranslator(Protocol):
    def translate(self, value: str) -> SprintDateData:
        ...
