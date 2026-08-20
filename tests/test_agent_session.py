from src.agent.session import SessionState


def test_update_expenses_without_categories():
    session = SessionState()

    session.update_expenses(3000)

    assert session.expenses == 3000
    assert session.has_expenses()


def test_update_expenses_with_categories_uses_categories_as_source_of_truth():
    session = SessionState()

    session.add_expense_category("aluguel", 1500)
    session.add_expense_category("transporte", 500)

    session.update_expenses(10000)

    assert session.expenses == 2000


def test_sync_expenses_from_categories():
    session = SessionState()

    session.expense_categories = {
        "moradia": 1500,
        "transporte": 500,
        "lazer": 300,
    }

    session.sync_expenses_from_categories()

    assert session.expenses == 2300


def test_sync_expenses_from_categories_does_nothing_when_empty():
    session = SessionState()

    session.expenses = None

    session.sync_expenses_from_categories()

    assert session.expenses is None


def test_add_financial_goal():
    session = SessionState()

    session.add_financial_goal(
        "Reserva de emergência",
        10000,
    )

    assert len(session.financial_goals) == 1
    assert session.financial_goals[0]["name"] == (
        "Reserva de emergência"
    )
    assert session.financial_goals[0]["amount"] == 10000


def test_has_income_returns_false_without_income():
    session = SessionState()

    assert session.has_income() is False


def test_has_expenses_returns_false_without_expenses():
    session = SessionState()

    assert session.has_expenses() is False


def test_has_complete_budget_requires_income_and_expenses():
    session = SessionState()

    assert session.has_complete_budget() is False

    session.update_income(4000)

    assert session.has_complete_budget() is False

    session.update_expenses(3000)

    assert session.has_complete_budget() is True


def test_clear_resets_session():
    session = SessionState()

    session.update_income(4000)
    session.add_expense_category("aluguel", 1500)
    session.add_financial_goal(
        "Reserva",
        5000,
    )

    assert session.income == 4000
    assert session.expenses == 1500
    assert session.expense_categories
    assert session.financial_goals

    session.clear()

    assert session.income is None
    assert session.expenses is None
    assert session.expense_categories == {}
    assert session.financial_goals == []