from src.agent.session import SessionState
from src.application.services.financial_memory_service import (
    FinancialMemoryService,
)


def test_memory_service_stores_income():

    service = FinancialMemoryService(
        session=SessionState()
    )

    service.update_from_message(
        "Recebo R$ 4000"
    )

    assert service.income == 4000.0


def test_memory_service_stores_expenses():

    service = FinancialMemoryService(
        session=SessionState()
    )

    service.update_from_message(
        "Gasto R$ 3000"
    )

    assert service.expenses == 3000.0


def test_memory_service_combines_budget():

    service = FinancialMemoryService(
        session=SessionState()
    )

    service.update_from_message(
        "Recebo R$ 4000"
    )

    service.update_from_message(
        "Gasto R$ 3000"
    )

    budget = service.get_budget_data()

    assert budget["income"] == 4000.0
    assert budget["expenses"] == 3000.0


def test_memory_service_registers_categorized_expense():

    service = FinancialMemoryService(
        session=SessionState()
    )

    service.update_from_message(
        "Gasto R$ 800 com alimentação"
    )

    assert (
        service.get_category_expense(
            "alimentacao"
        )
        == 800.0
    )


def test_memory_service_accumulates_category():

    service = FinancialMemoryService(
        session=SessionState()
    )

    service.update_from_message(
        "Gasto R$ 500 com alimentação"
    )

    service.update_from_message(
        "Gasto R$ 300 com alimentação"
    )

    assert (
        service.get_category_expense(
            "alimentacao"
        )
        == 800.0
    )


def test_memory_service_detects_complete_budget():

    service = FinancialMemoryService(
        session=SessionState()
    )

    assert not service.has_complete_budget()

    service.update_from_message(
        "Recebo R$ 5000"
    )

    service.update_from_message(
        "Gasto R$ 3000"
    )

    assert service.has_complete_budget()


def test_memory_service_clear():

    service = FinancialMemoryService(
        session=SessionState()
    )

    service.update_from_message(
        "Recebo R$ 5000"
    )

    service.update_from_message(
        "Gasto R$ 3000"
    )

    service.clear()

    assert service.income is None
    assert service.expenses is None


def test_memory_service_updates_from_message():
    service = FinancialMemoryService(
        session=SessionState()
    )

    service.update_from_message(
        (
            "Minha renda é R$ 5.000, "
            "pago R$ 1.500 de aluguel, "
            "R$ 800 com alimentação "
            "e R$ 400 com transporte."
        )
    )

    assert service.income == 5000
    assert service.expenses == 2700

    assert service.get_category_expense(
        "moradia"
    ) == 1500

    assert service.get_category_expense(
        "alimentacao"
    ) == 800

    assert service.get_category_expense(
        "transporte"
    ) == 400