import pytest

from src.tools.calculator import (
    calculate_balance,
    calculate_income_commitment,
    calculate_savings_rate,
    calculate_compound_growth,
    calculate_compound_profit,
)


def test_calculate_balance():
    result = calculate_balance(4000, 3200)

    assert result == 800


def test_calculate_savings_rate():
    result = calculate_savings_rate(4000, 3200)

    assert result == pytest.approx(20)


def test_calculate_income_commitment():
    result = calculate_income_commitment(4000, 3200)

    assert result == pytest.approx(80)


def test_income_cannot_be_zero():
    with pytest.raises(ValueError):
        calculate_savings_rate(0, 100)

def test_calculate_compound_growth():
    result = calculate_compound_growth(
        principal=1000,
        annual_rate=0.10,
        years=10,
    )

    assert result == pytest.approx(
        2593.7424601
    )


def test_calculate_compound_profit():
    result = calculate_compound_profit(
        principal=1000,
        annual_rate=0.10,
        years=10,
    )

    assert result == pytest.approx(
        1593.7424601
    )

