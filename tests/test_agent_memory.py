from src.agent.agent import FinAssistAgent
from src.agent.session import SessionState
from src.agent.memory import add_expense


def test_agent_session_stores_income():
    agent = FinAssistAgent.__new__(
        FinAssistAgent
    )

    from src.agent.session import SessionState

    agent.session = SessionState()

    agent._update_session(
        "Recebo R$ 4000"
    )

    assert agent.session.income == 4000
    assert agent.session.expenses is None


def test_agent_session_stores_expenses():
    agent = FinAssistAgent.__new__(
        FinAssistAgent
    )

    from src.agent.session import SessionState

    agent.session = SessionState()

    agent._update_session(
        "Gasto R$ 3000"
    )

    assert agent.session.income is None
    assert agent.session.expenses == 3000


def test_agent_session_combines_budget():
    agent = FinAssistAgent.__new__(
        FinAssistAgent
    )

    from src.agent.session import SessionState

    agent.session = SessionState()

    agent._update_session(
        "Recebo R$ 4000"
    )

    agent._update_session(
        "Gasto R$ 3000"
    )

    assert agent.session.income == 4000
    assert agent.session.expenses == 3000
    assert agent.session.has_complete_budget()


def test_agent_combines_budget_from_multiple_messages():
    agent = FinAssistAgent.__new__(
        FinAssistAgent
    )

    from src.agent.session import SessionState

    agent.session = SessionState()

    agent._update_session(
        "Recebo R$ 4000"
    )

    first = agent._get_budget_data(
        "Recebo R$ 4000"
    )

    assert first["income"] == 4000
    assert first["expenses"] is None

    agent._update_session(
        "Gasto R$ 3000"
    )

    second = agent._get_budget_data(
        "Gasto R$ 3000"
    )

    assert second["income"] == 4000
    assert second["expenses"] == 3000



def test_expenses_sync_after_category_accumulation():
    """
    O total de despesas deve continuar sincronizado
    quando uma categoria recebe novos gastos.
    """

    session = SessionState()

    add_expense(
        session,
        "aluguel",
        1500,
    )

    add_expense(
        session,
        "alimentação",
        600,
    )

    add_expense(
        session,
        "alimentação",
        200,
    )

    assert session.expense_categories["alimentação"] == 800
    assert session.expenses == 2300


def test_expenses_sync_after_category_accumulation():
    """
    O total de despesas deve continuar sincronizado
    quando uma categoria recebe novos gastos.
    """

    session = SessionState()

    add_expense(
        session,
        "aluguel",
        1500,
    )

    add_expense(
        session,
        "alimentação",
        600,
    )

    add_expense(
        session,
        "alimentação",
        200,
    )

    assert session.expense_categories["alimentação"] == 800
    assert session.expenses == 2300


def test_aliases_are_reflected_in_total_expenses():
    """
    Categorias equivalentes devem ser acumuladas
    e refletidas corretamente no total.
    """

    session = SessionState()

    add_expense(
        session,
        "aluguel",
        1500,
    )

    add_expense(
        session,
        "moradia",
        500,
    )

    assert session.expense_categories["moradia"] == 2000
    assert session.expenses == 2000