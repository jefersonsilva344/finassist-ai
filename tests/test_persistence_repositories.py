from decimal import Decimal

from src.persistence.models import (
    ConversationMessage,
    Expense,
    FinancialPeriod,
    MessageRole,
    Session,
    User,
)
from src.persistence.repositories import (
    ConversationRepository,
    ExpenseRepository,
    FinancialPeriodRepository,
    SessionRepository,
    UserRepository,
)




def test_user_repository_add_and_get(db_session):
    db = db_session

    repository = UserRepository(db)

    user = User(
        external_id="test-user-001"
    )

    repository.add(user)

    db.commit()
    db.refresh(user)

    assert user.id is not None

    found = repository.get_by_id(user.id)

    assert found is not None
    assert found.id == user.id


def test_session_repository_list_by_user(db_session):
    db = db_session

    user_repository = UserRepository(db)
    session_repository = SessionRepository(db)

    user = User(
        external_id="test-user-001"
    )

    user_repository.add(user)

    db.commit()
    db.refresh(user)

    session = Session(
        user_id=user.id,
    )

    session_repository.add(session)

    db.commit()

    sessions = session_repository.list_by_user(
        user.id
    )

    assert len(sessions) == 1
    assert sessions[0].user_id == user.id


def test_financial_period_repository(db_session):
    db = db_session

    user = User(
        external_id="test-user-001"
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    session = Session(
        user_id=user.id,
    )

    db.add(session)
    db.commit()
    db.refresh(session)

    repository = FinancialPeriodRepository(db)

    period = FinancialPeriod(
        session_id=session.id,
        year=2026,
        month=8,
        income=Decimal("5000.00"),
    )

    repository.add(period)

    db.commit()
    db.refresh(period)

    found = repository.get_by_session_and_month(
        session.id,
        2026,
        8,
    )

    assert found is not None
    assert found.income == Decimal("5000.00")



def test_expense_repository_list_by_period(db_session):
    db = db_session

    user = User(
        external_id="test-user-001"
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    session = Session(
        user_id=user.id,
    )

    db.add(session)
    db.commit()
    db.refresh(session)

    period = FinancialPeriod(
        session_id=session.id,
        year=2026,
        month=8,
        income=Decimal("5000.00"),
    )

    db.add(period)
    db.commit()
    db.refresh(period)

    repository = ExpenseRepository(db)

    repository.add(
        Expense(
            period_id=period.id,
            category="moradia",
            amount=Decimal("1500.00"),
        )
    )

    repository.add(
        Expense(
            period_id=period.id,
            category="alimentacao",
            amount=Decimal("800.00"),
        )
    )

    db.commit()

    expenses = repository.list_by_period(
        period.id
    )

    assert len(expenses) == 2


def test_conversation_repository_list_by_session(db_session):
    db = db_session

    user = User(
        external_id="test-user-001"
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    session = Session(
        user_id=user.id,
    )

    db.add(session)
    db.commit()
    db.refresh(session)

    repository = ConversationRepository(db)

    repository.add(
        ConversationMessage(
            session_id=session.id,
            role=MessageRole.USER,
            content="Recebo R$ 5.000",
        )
    )

    repository.add(
        ConversationMessage(
            session_id=session.id,
            role=MessageRole.ASSISTANT,
            content="Entendi sua renda.",
        )
    )

    db.commit()

    messages = repository.list_by_session(
        session.id
    )

    assert len(messages) == 2

    assert messages[0].role == MessageRole.USER
    assert messages[1].role == MessageRole.ASSISTANT


def test_expense_repository_get_by_id_and_delete(
    db_session,
):
    db = db_session

    user = User(
        external_id="test-user-expense"
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    session = Session(
        user_id=user.id,
    )

    db.add(session)
    db.commit()
    db.refresh(session)

    period = FinancialPeriod(
        session_id=session.id,
        year=2026,
        month=8,
        income=Decimal("5000.00"),
    )

    db.add(period)
    db.commit()
    db.refresh(period)

    repository = ExpenseRepository(db)

    expense = Expense(
        period_id=period.id,
        category="moradia",
        amount=Decimal("1500.00"),
    )

    repository.add(expense)

    db.commit()
    db.refresh(expense)

    found = repository.get_by_id(
        expense.id
    )

    assert found is not None
    assert found.id == expense.id
    assert found.category == "moradia"

    repository.delete(expense)

    db.commit()

    deleted = repository.get_by_id(
        expense.id
    )

    assert deleted is None


def test_expense_repository_list_by_category(
    db_session,
):
    db = db_session

    user = User(
        external_id="test-user-category"
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    session = Session(
        user_id=user.id,
    )

    db.add(session)
    db.commit()
    db.refresh(session)

    period = FinancialPeriod(
        session_id=session.id,
        year=2026,
        month=8,
        income=Decimal("5000.00"),
    )

    db.add(period)
    db.commit()
    db.refresh(period)

    repository = ExpenseRepository(db)

    repository.add(
        Expense(
            period_id=period.id,
            category="moradia",
            amount=Decimal("1500.00"),
        )
    )

    repository.add(
        Expense(
            period_id=period.id,
            category="moradia",
            amount=Decimal("500.00"),
        )
    )

    repository.add(
        Expense(
            period_id=period.id,
            category="transporte",
            amount=Decimal("300.00"),
        )
    )

    db.commit()

    expenses = repository.list_by_category(
        period.id,
        "moradia",
    )

    assert len(expenses) == 2

    assert all(
        expense.category == "moradia"
        for expense in expenses
    )


def test_conversation_repository_list_by_role(
    db_session,
):
    db = db_session

    user = User(
        external_id="test-user-role"
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    session = Session(
        user_id=user.id,
    )

    db.add(session)
    db.commit()
    db.refresh(session)

    repository = ConversationRepository(db)

    repository.add(
        ConversationMessage(
            session_id=session.id,
            role=MessageRole.USER,
            content="Recebo R$ 5.000",
        )
    )

    repository.add(
        ConversationMessage(
            session_id=session.id,
            role=MessageRole.ASSISTANT,
            content="Entendi sua renda.",
        )
    )

    repository.add(
        ConversationMessage(
            session_id=session.id,
            role=MessageRole.USER,
            content="Também pago aluguel.",
        )
    )

    db.commit()

    user_messages = repository.list_by_role(
        session.id,
        MessageRole.USER,
    )

    assistant_messages = repository.list_by_role(
        session.id,
        MessageRole.ASSISTANT,
    )

    assert len(user_messages) == 2
    assert len(assistant_messages) == 1

    assert all(
        message.role == MessageRole.USER
        for message in user_messages
    )

    assert all(
        message.role == MessageRole.ASSISTANT
        for message in assistant_messages
    )


def test_conversation_repository_get_by_id(
    db_session,
):
    db = db_session

    user = User(
        external_id="test-user-message-id"
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    session = Session(
        user_id=user.id,
    )

    db.add(session)
    db.commit()
    db.refresh(session)

    repository = ConversationRepository(db)

    message = ConversationMessage(
        session_id=session.id,
        role=MessageRole.USER,
        content="Minha renda é R$ 5.000",
    )

    repository.add(message)

    db.commit()
    db.refresh(message)

    found = repository.get_by_id(
        message.id
    )

    assert found is not None
    assert found.id == message.id
    assert found.content == "Minha renda é R$ 5.000"
    assert found.role == MessageRole.USER


def test_financial_period_repository_get_by_id_and_list_by_session(
    db_session,
):
    db = db_session

    user = User(
        external_id="test-user-periods"
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    session = Session(
        user_id=user.id,
    )

    db.add(session)
    db.commit()
    db.refresh(session)

    repository = FinancialPeriodRepository(db)

    period_1 = FinancialPeriod(
        session_id=session.id,
        year=2026,
        month=7,
        income=Decimal("5000.00"),
    )

    period_2 = FinancialPeriod(
        session_id=session.id,
        year=2026,
        month=8,
        income=Decimal("5500.00"),
    )

    repository.add(period_1)
    repository.add(period_2)

    db.commit()

    db.refresh(period_1)
    db.refresh(period_2)

    found = repository.get_by_id(
        period_1.id
    )

    assert found is not None
    assert found.id == period_1.id

    periods = repository.list_by_session(
        session.id
    )

    assert len(periods) == 2

    assert periods[0].month == 7
    assert periods[1].month == 8


