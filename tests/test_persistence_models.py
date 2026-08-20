import pytest

from decimal import Decimal

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.persistence.database import Base
from src.persistence.models import (
    ConversationMessage,
    Expense,
    FinancialPeriod,
    MessageRole,
    Session,
    User,
)



def test_user_can_be_created():
    """
    Um usuário deve poder ser criado sem
    um ID antes da persistência.
    """

    user = User(
        external_id="test-user-001"
    )

    assert user.id is None
    assert user.external_id == "test-user-001"
    assert user.created_at is not None
    assert user.updated_at is not None


def test_session_belongs_to_user():
    """
    Uma sessão deve armazenar a referência
    ao usuário proprietário.
    """

    session = Session(
        user_id=10
    )

    assert session.user_id == 10
    assert session.id is None


def test_financial_period_stores_monthly_data():
    """
    Um período financeiro deve representar
    um determinado ano e mês.
    """

    period = FinancialPeriod(
        session_id=1,
        year=2026,
        month=8,
        income=Decimal("4000.00"),
    )

    assert period.session_id == 1
    assert period.year == 2026
    assert period.month == 8
    assert period.income == Decimal("4000.00")


def test_financial_period_rejects_invalid_month():
    """
    O mês deve estar entre janeiro e dezembro.
    """

    with pytest.raises(ValueError):
        FinancialPeriod(
            session_id=1,
            year=2026,
            month=13,
        )


def test_financial_period_rejects_invalid_income():
    """
    A renda não pode ser zero ou negativa.
    """

    with pytest.raises(ValueError):
        FinancialPeriod(
            session_id=1,
            year=2026,
            month=8,
            income=Decimal("0"),
        )


def test_expense_stores_financial_data():
    """
    Uma despesa deve armazenar período,
    categoria, valor e descrição.
    """

    expense = Expense(
        period_id=1,
        category="moradia",
        amount=Decimal("1500.00"),
        description="aluguel",
    )

    assert expense.period_id == 1
    assert expense.category == "moradia"
    assert expense.amount == Decimal("1500.00")
    assert expense.description == "aluguel"


def test_expense_rejects_empty_category():
    """
    Uma despesa não pode existir sem categoria.
    """

    with pytest.raises(ValueError):
        Expense(
            period_id=1,
            category="",
            amount=Decimal("100.00"),
        )


def test_expense_rejects_non_positive_amount():
    """
    Uma despesa deve possuir valor positivo.
    """

    with pytest.raises(ValueError):
        Expense(
            period_id=1,
            category="alimentação",
            amount=Decimal("0"),
        )


def test_conversation_message_stores_user_message():
    """
    Mensagens devem armazenar sessão,
    papel e conteúdo.
    """

    message = ConversationMessage(
        session_id=1,
        role=MessageRole.USER,
        content="Recebo R$ 4.000",
    )

    assert message.session_id == 1
    assert message.role == MessageRole.USER
    assert message.content == "Recebo R$ 4.000"


def test_conversation_message_stores_assistant_message():
    """
    O histórico também deve representar
    mensagens produzidas pelo agente.
    """

    message = ConversationMessage(
        session_id=1,
        role=MessageRole.ASSISTANT,
        content="Qual é sua despesa mensal?",
    )

    assert message.role == MessageRole.ASSISTANT


def test_conversation_message_rejects_empty_content():
    """
    Uma mensagem sem conteúdo não deve ser persistida.
    """

    with pytest.raises(ValueError):
        ConversationMessage(
            session_id=1,
            role=MessageRole.USER,
            content="",
        )


def test_user_has_sessions_relationship():
    user = User(
        external_id="test-user-001"
    )

    session = Session(
        user_id=1
    )

    user.sessions.append(session)

    assert session.user is user
    assert session in user.sessions



def test_session_has_financial_periods_relationship():
    session = Session(
        user_id=1
    )
    

    period = FinancialPeriod(
        session_id=1,
        year=2026,
        month=8,
    )

    session.financial_periods.append(period)

    assert period.session is session
    assert period in session.financial_periods


def test_financial_period_has_expenses_relationship():
    period = FinancialPeriod(
        session_id=1,
        year=2026,
        month=8,
    )

    expense = Expense(
        period_id=1,
        category="moradia",
        amount=Decimal("1500.00"),
    )

    period.expenses.append(expense)

    assert expense.period is period
    assert expense in period.expenses


def test_session_has_conversation_messages_relationship():
    session = Session(
        user_id=1
    )

    message = ConversationMessage(
        session_id=1,
        role=MessageRole.USER,
        content="Recebo R$ 5.000",
    )

    session.conversation_messages.append(message)

    assert message.session is session
    assert message in session.conversation_messages


def test_persistence_relationships_are_navigable(db_session):
    db = db_session

    user = User(
        external_id="relationship-test"
    )

    db.add(user)
    db.flush()

    session = Session(
        user_id=user.id
    )

    db.add(session)
    db.flush()

    period = FinancialPeriod(
        session_id=session.id,
        year=2026,
        month=8,
        income=Decimal("5000.00"),
    )

    db.add(period)
    db.flush()

    expense = Expense(
        period_id=period.id,
        category="moradia",
        amount=Decimal("1500.00"),
    )

    message = ConversationMessage(
        session_id=session.id,
        role=MessageRole.USER,
        content="Minha renda é R$ 5.000",
    )

    db.add_all([expense, message])
    db.commit()

    db.refresh(user)
    db.refresh(session)
    db.refresh(period)

    assert len(user.sessions) == 1
    assert user.sessions[0] is session

    assert session.user is user

    assert len(session.financial_periods) == 1
    assert session.financial_periods[0] is period

    assert period.session is session

    assert len(period.expenses) == 1
    assert period.expenses[0] is expense

    assert expense.period is period

    assert len(session.conversation_messages) == 1
    assert session.conversation_messages[0] is message

    assert message.session is session

