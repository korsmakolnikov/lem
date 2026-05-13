import numpy as np
from sprint_date_translator import SprintDateData


class FakeSprintDateTranslator:
    def translate(self, value: str) -> SprintDateData:
        return SprintDateData(
            year=np.short(2026),
            quarter=np.short(2),
            sprint=np.short(3),
            sprint_length=np.short(2),
        )
