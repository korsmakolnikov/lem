import pytest
from dash_separated_sprint_date_translator import DashSeparatedSprintDateTranslator
from sprint_exceptions import InvalidSprintStringError


def test_translate_valid_string():
    translator = DashSeparatedSprintDateTranslator()
    data = translator.translate("2026-Q2-3")
    assert data.year == 2026
    assert data.quarter == 2
    assert data.sprint == 3
    assert data.sprint_length == 2


def test_invalid_format_too_short():
    with pytest.raises(InvalidSprintStringError):
        DashSeparatedSprintDateTranslator().translate("2026-Q2")


def test_invalid_format_too_long():
    with pytest.raises(InvalidSprintStringError):
        DashSeparatedSprintDateTranslator().translate("2026-Q2-3-2-extra")


def test_non_numeric_year():
    with pytest.raises(InvalidSprintStringError):
        DashSeparatedSprintDateTranslator().translate("ABCD-Q2-3")


def test_non_numeric_quarter():
    with pytest.raises(InvalidSprintStringError):
        DashSeparatedSprintDateTranslator().translate("2026-QX-3")


def test_non_numeric_sprint():
    with pytest.raises(InvalidSprintStringError):
        DashSeparatedSprintDateTranslator().translate("2026-Q2-X")
