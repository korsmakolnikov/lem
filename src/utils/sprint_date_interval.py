from datetime import date, timedelta
import numpy as np
from sprint_exceptions import InvalidYearError, InvalidQuarterError, InvalidSprintError, InvalidSprintLengthError


class SprintDateInterval:
    def __init__(self, year: np.short, quarter: np.short, sprint: np.short, sprint_length: np.short):
        current_year = date.today().year
        if year < current_year - 50:
            raise InvalidYearError(f"year must be >= {current_year - 50}")
        if quarter < 1 or quarter > 4:
            raise InvalidQuarterError("quarter must be between 1 and 4")
        if sprint_length < 1:
            raise InvalidSprintLengthError("sprint_length must be > 0")
        max_sprint = np.short(13 // sprint_length)
        if sprint < 1 or sprint > max_sprint:
            raise InvalidSprintError(f"sprint must be between 1 and {max_sprint} for sprint_length={sprint_length}")

        self.year = np.short(year)
        self.quarter = np.short(quarter)
        self.sprint = np.short(sprint)
        self.sprint_length = np.short(sprint_length)

    def get_start(self) -> date:
        q1_start = date(int(self.year), 1, 1)
        days = int(((self.quarter - 1) * 13 + (self.sprint - 1) * self.sprint_length) * 7)
        return q1_start + timedelta(days=days)

    def get_end(self) -> date:
        return self.get_start() + timedelta(weeks=int(self.sprint_length))
