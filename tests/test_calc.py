import pytest

import calc


def test_basic_percentage():
    assert calc.percentage(25, 200) == 12.5
    assert calc.percentage("50", "200") == 25


def test_comma_decimal_and_spaces():
    assert calc.parse_number(" 1 234,5 ") == 1234.5


@pytest.mark.parametrize("bad", ["", "abc", None, "nan", "inf", True])
def test_invalid_inputs(bad):
    assert calc.parse_number(bad) is None


def test_zero_total():
    assert calc.percentage(10, 0) is None
    s = calc.summarize(0, [10])
    assert not s["valid_total"] and s["rows"][0]["percent"] is None
    assert s["remaining"] is None


def test_summary():
    s = calc.summarize(200, [50, "30", "", "x"])
    assert s["sum"] == 80
    assert s["remaining"] == 120
    assert s["remaining_percent"] == 60
    assert s["sum_percent"] == 40
    assert [r["valid"] for r in s["rows"]] == [True, True, True, False]
    assert not s["over"]


def test_over_total():
    s = calc.summarize(100, [70, 50])
    assert s["over"] and s["remaining"] == -20
