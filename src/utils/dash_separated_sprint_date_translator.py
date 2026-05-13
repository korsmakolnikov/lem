import numpy as np
from sprint_date_translator import SprintDateData
from sprint_exceptions import InvalidSprintStringError


class DashSeparatedSprintDateTranslator:
    def translate(self, value: str) -> SprintDateData:
        parts = value.split("-")
        if len(parts) < 3 or len(parts) > 4:
            raise InvalidSprintStringError(f"invalid sprint string '{value}': expected format 'YYYY-QN-S' or 'YYYY-QN-S-L'")

        try:
            year = np.short(int(parts[0]))
        except ValueError:
            raise InvalidSprintStringError(f"invalid year '{parts[0]}': must be a number")

        try:
            quarter = np.short(int(parts[1][1:]))  # strip the "Q"
        except ValueError:
            raise InvalidSprintStringError(f"invalid quarter '{parts[1]}': must be in format 'QN'")

        try:
            sprint = np.short(int(parts[2]))
        except ValueError:
            raise InvalidSprintStringError(f"invalid sprint '{parts[2]}': must be a number")

        if len(parts) == 4:
            try:
                sprint_length = np.short(int(parts[3]))
            except ValueError:
                raise InvalidSprintStringError(f"invalid sprint_length '{parts[3]}': must be a number")
        else:
            sprint_length = np.short(2)

        return SprintDateData(year=year, quarter=quarter, sprint=sprint, sprint_length=sprint_length)
