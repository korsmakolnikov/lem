import pytest
from datetime import date, timedelta
import numpy as np
from sprint_date_interval import SprintDateInterval
from sprint_date_interval_builder import SprintDateIntervalBuilder
from fake_sprint_date_translator import FakeSprintDateTranslator
from sprint_exceptions import InvalidYearError, InvalidQuarterError, InvalidSprintError, InvalidSprintLengthError


def test_get_start_day_sprint_4_q1():
    sprint = SprintDateInterval(year=2026, quarter=1, sprint=4, sprint_length=2)
    assert sprint.get_start().day == 12
    assert sprint.get_start().month == 2


def test_get_start_sprint_3_q4():
    sprint = SprintDateInterval(year=2026, quarter=4, sprint=3, sprint_length=2)
    assert sprint.get_start().day == 29
    assert sprint.get_start().month == 10


def test_get_end_sprint_4_q1():
    sprint = SprintDateInterval(year=2026, quarter=1, sprint=4, sprint_length=2)
    assert sprint.get_end() == sprint.get_start() + timedelta(weeks=2)


def test_get_start_sprint_3_q4_leap_year():
    sprint = SprintDateInterval(year=2028, quarter=4, sprint=3, sprint_length=2)
    assert sprint.get_start().day == 28
    assert sprint.get_start().month == 10


def test_get_end_sprint_3_q4_leap_year():
    sprint = SprintDateInterval(year=2028, quarter=4, sprint=3, sprint_length=2)
    assert sprint.get_end().day == 11
    assert sprint.get_end().month == 11


def test_builder_get_start():
    builder = SprintDateIntervalBuilder(translator=FakeSprintDateTranslator())
    sprint = builder.build("anything")
    assert sprint.get_start().day == 30
    assert sprint.get_start().month == 4


def test_get_start_sprint_3_q2():
    sprint = SprintDateInterval(year=2026, quarter=2, sprint=3, sprint_length=2)
    assert sprint.get_start().day == 30
    assert sprint.get_start().month == 4


def test_year_too_old():
    with pytest.raises(InvalidYearError):
        SprintDateInterval(year=1900, quarter=1, sprint=1, sprint_length=2)


def test_quarter_zero():
    with pytest.raises(InvalidQuarterError):
        SprintDateInterval(year=2026, quarter=0, sprint=1, sprint_length=2)


def test_quarter_too_high():
    with pytest.raises(InvalidQuarterError):
        SprintDateInterval(year=2026, quarter=5, sprint=1, sprint_length=2)


def test_sprint_zero():
    with pytest.raises(InvalidSprintError):
        SprintDateInterval(year=2026, quarter=1, sprint=0, sprint_length=2)


def test_sprint_too_high():
    with pytest.raises(InvalidSprintError):
        SprintDateInterval(year=2026, quarter=1, sprint=7, sprint_length=2)


def test_sprint_length_zero():
    with pytest.raises(InvalidSprintLengthError):
        SprintDateInterval(year=2026, quarter=1, sprint=1, sprint_length=0)
