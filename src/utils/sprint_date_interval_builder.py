from sprint_date_translator import SprintDateTranslator
from sprint_date_interval import SprintDateInterval


class SprintDateIntervalBuilder:
    def __init__(self, translator: SprintDateTranslator):
        self.translator = translator

    def build(self, value: str) -> SprintDateInterval:
        data = self.translator.translate(value)
        return SprintDateInterval(
            year=data.year,
            quarter=data.quarter,
            sprint=data.sprint,
            sprint_length=data.sprint_length,
        )
