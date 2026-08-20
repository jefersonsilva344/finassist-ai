from src.tools.formatters import format_brl


def test_format_brl_integer():
    assert format_brl(2300.0) == "R$ 2.300,00"


def test_format_brl_decimal():
    assert format_brl(1500.50) == "R$ 1.500,50"


def test_format_brl_thousands():
    assert format_brl(5000.0) == "R$ 5.000,00"


def test_format_brl_small_value():
    assert format_brl(25.75) == "R$ 25,75"