from decimal import Decimal

from src.persistence.models import (
    ConversationMessage,
    Expense,
    FinancialPeriod,
    MessageRole,
    Session,
    User,
)


def test_complete_financial_flow_can_be_persisted(db_session):
    """
    Valida o fluxo completo:

    User
      -> Session
      -> FinancialPeriod
      -> Expenses
      -> ConversationMessages
    """

    db = db_session

    # ---------------------------------------------------------
    # 1. Criar usuário
    # ---------------------------------------------------------

    user = User(
        external_id="integration-user-001",
    )

    db.add(user)
    db.flush()

    assert user.id is not None

    # ---------------------------------------------------------
    # 2. Criar sessão
    # ---------------------------------------------------------

    session = Session(
        user_id=user.id,
    )

    db.add(session)
    db.flush()

    assert session.id is not None

    # ---------------------------------------------------------
    # 3. Criar período financeiro
    # ---------------------------------------------------------

    period = FinancialPeriod(
        session_id=session.id,
        year=2026,
        month=8,
        income=Decimal("5000.00"),
    )

    db.add(period)
    db.flush()

    assert period.id is not None

    # ---------------------------------------------------------
    # 4. Criar despesas
    # ---------------------------------------------------------

    rent = Expense(
        period_id=period.id,
        category="moradia",
        amount=Decimal("1500.00"),
        description="Aluguel",
    )

    food = Expense(
        period_id=period.id,
        category="alimentação",
        amount=Decimal("800.00"),
        description="Supermercado",
    )

    transport = Expense(
        period_id=period.id,
        category="transporte",
        amount=Decimal("400.00"),
        description="Combustível",
    )

    db.add_all([
        rent,
        food,
        transport,
    ])

    # ---------------------------------------------------------
    # 5. Criar histórico da conversa
    # ---------------------------------------------------------

    user_message = ConversationMessage(
        session_id=session.id,
        role=MessageRole.USER,
        content="Minha renda é R$ 5.000 e meu aluguel é R$ 1.500.",
    )

    assistant_message = ConversationMessage(
        session_id=session.id,
        role=MessageRole.ASSISTANT,
        content="Entendi. Vou registrar essas informações.",
    )

    db.add_all([
        user_message,
        assistant_message,
    ])

    # ---------------------------------------------------------
    # 6. Persistir transação
    # ---------------------------------------------------------

    db.commit()

    # ---------------------------------------------------------
    # 7. Recarregar entidades
    # ---------------------------------------------------------

    db.refresh(user)
    db.refresh(session)
    db.refresh(period)

    # ---------------------------------------------------------
    # 8. Validar User -> Session
    # ---------------------------------------------------------

    assert len(user.sessions) == 1
    assert user.sessions[0].id == session.id

    # ---------------------------------------------------------
    # 9. Validar Session -> FinancialPeriod
    # ---------------------------------------------------------

    assert len(session.financial_periods) == 1

    persisted_period = session.financial_periods[0]

    assert persisted_period.id == period.id
    assert persisted_period.year == 2026
    assert persisted_period.month == 8
    assert persisted_period.income == Decimal("5000.00")

    # ---------------------------------------------------------
    # 10. Validar FinancialPeriod -> Expenses
    # ---------------------------------------------------------

    assert len(period.expenses) == 3

    expenses_by_category = {
        expense.category: expense
        for expense in period.expenses
    }

    assert expenses_by_category["moradia"].amount == Decimal(
        "1500.00"
    )

    assert expenses_by_category["alimentação"].amount == Decimal(
        "800.00"
    )

    assert expenses_by_category["transporte"].amount == Decimal(
        "400.00"
    )

    # ---------------------------------------------------------
    # 11. Validar Session -> ConversationMessages
    # ---------------------------------------------------------

    assert len(session.conversation_messages) == 2

    roles = [
        message.role
        for message in session.conversation_messages
    ]

    assert MessageRole.USER in roles
    assert MessageRole.ASSISTANT in roles


def test_financial_data_survives_database_session_reload(
    db_engine,
    db_session_factory,
):
    """
    Valida que os dados financeiros permanecem persistidos
    após o encerramento da sessão SQLAlchemy original.

    Este teste utiliza o mesmo engine SQLite da fixture,
    mas cria explicitamente duas sessões diferentes para
    validar a persistência entre ciclos de sessão.
    """

    # =============================================================
    # PRIMEIRA SESSÃO
    # =============================================================

    db = db_session_factory()

    try:
        user = User(
            external_id="persistent-user-001",
        )

        db.add(user)
        db.flush()

        session = Session(
            user_id=user.id,
        )

        db.add(session)
        db.flush()

        period = FinancialPeriod(
            session_id=session.id,
            year=2026,
            month=8,
            income=Decimal("6000.00"),
        )

        db.add(period)
        db.flush()

        expense = Expense(
            period_id=period.id,
            category="moradia",
            amount=Decimal("1800.00"),
            description="Aluguel",
        )

        message = ConversationMessage(
            session_id=session.id,
            role=MessageRole.USER,
            content="Minha renda é R$ 6.000.",
        )

        db.add_all([
            expense,
            message,
        ])

        db.commit()

        user_id = user.id
        session_id = session.id
        period_id = period.id

    finally:
        db.close()

    # =============================================================
    # SEGUNDA SESSÃO
    # =============================================================

    db = db_session_factory()

    try:
        persisted_user = db.get(
            User,
            user_id,
        )

        persisted_session = db.get(
            Session,
            session_id,
        )

        persisted_period = db.get(
            FinancialPeriod,
            period_id,
        )

        # ---------------------------------------------------------
        # User
        # ---------------------------------------------------------

        assert persisted_user is not None
        assert persisted_user.external_id == "persistent-user-001"

        # ---------------------------------------------------------
        # Session
        # ---------------------------------------------------------

        assert persisted_session is not None
        assert persisted_session.user_id == persisted_user.id

        # ---------------------------------------------------------
        # FinancialPeriod
        # ---------------------------------------------------------

        assert persisted_period is not None
        assert persisted_period.session_id == persisted_session.id
        assert persisted_period.income == Decimal("6000.00")

        # ---------------------------------------------------------
        # Expense
        # ---------------------------------------------------------

        assert len(persisted_period.expenses) == 1

        persisted_expense = persisted_period.expenses[0]

        assert persisted_expense.category == "moradia"
        assert persisted_expense.amount == Decimal("1800.00")

        # ---------------------------------------------------------
        # Conversation
        # ---------------------------------------------------------

        assert len(persisted_session.conversation_messages) == 1

        persisted_message = (
            persisted_session.conversation_messages[0]
        )

        assert persisted_message.role == MessageRole.USER
        assert persisted_message.content == (
            "Minha renda é R$ 6.000."
        )

    finally:
        db.close()


def test_financial_data_is_isolated_between_users(db_session):
    """
    Garante que os dados financeiros de um usuário
    não sejam associados à sessão de outro usuário.
    """

    db = db_session

    # =========================================================
    # USUÁRIO A
    # =========================================================

    user_a = User(
        external_id="user-a",
    )

    db.add(user_a)
    db.flush()

    session_a = Session(
        user_id=user_a.id,
    )

    db.add(session_a)
    db.flush()

    period_a = FinancialPeriod(
        session_id=session_a.id,
        year=2026,
        month=8,
        income=Decimal("5000.00"),
    )

    db.add(period_a)
    db.flush()

    expense_a = Expense(
        period_id=period_a.id,
        category="moradia",
        amount=Decimal("1500.00"),
    )

    db.add(expense_a)

    # =========================================================
    # USUÁRIO B
    # =========================================================

    user_b = User(
        external_id="user-b",
    )

    db.add(user_b)
    db.flush()

    session_b = Session(
        user_id=user_b.id,
    )

    db.add(session_b)
    db.flush()

    period_b = FinancialPeriod(
        session_id=session_b.id,
        year=2026,
        month=8,
        income=Decimal("8000.00"),
    )

    db.add(period_b)
    db.flush()

    expense_b = Expense(
        period_id=period_b.id,
        category="transporte",
        amount=Decimal("700.00"),
    )

    db.add(expense_b)

    db.commit()

    # =========================================================
    # VALIDAR USUÁRIO A
    # =========================================================

    db.refresh(user_a)

    assert len(user_a.sessions) == 1
    assert user_a.sessions[0].id == session_a.id

    assert session_a.user_id == user_a.id
    assert session_a.user_id != user_b.id

    assert len(session_a.financial_periods) == 1

    assert (
        session_a.financial_periods[0].income
        == Decimal("5000.00")
    )

    # =========================================================
    # VALIDAR USUÁRIO B
    # =========================================================

    db.refresh(user_b)

    assert len(user_b.sessions) == 1
    assert user_b.sessions[0].id == session_b.id

    assert session_b.user_id == user_b.id
    assert session_b.user_id != user_a.id

    assert len(session_b.financial_periods) == 1

    assert (
        session_b.financial_periods[0].income
        == Decimal("8000.00")
    )

    # =========================================================
    # GARANTIR QUE OS PERÍODOS NÃO SE MISTURARAM
    # =========================================================

    assert period_a.session_id == session_a.id
    assert period_b.session_id == session_b.id

    assert period_a.session_id != period_b.session_id

    assert period_a.expenses[0].amount == Decimal(
        "1500.00"
    )

    assert period_b.expenses[0].amount == Decimal(
        "700.00"
    )


def test_user_deletion_cascades_to_financial_data(db_session):
    """
    Valida a exclusão em cascata de todo o agregado financeiro.
    """

    db = db_session

    user = User(
        external_id="cascade-user",
    )

    db.add(user)
    db.flush()

    session = Session(
        user_id=user.id,
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
        category="alimentação",
        amount=Decimal("600.00"),
    )

    message = ConversationMessage(
        session_id=session.id,
        role=MessageRole.USER,
        content="Gastei R$ 600 com alimentação.",
    )

    db.add_all([
        expense,
        message,
    ])

    db.commit()

    user_id = user.id
    session_id = session.id
    period_id = period.id
    expense_id = expense.id
    message_id = message.id

    # ---------------------------------------------------------
    # Excluir o usuário
    # ---------------------------------------------------------

    db.delete(user)
    db.commit()

    # ---------------------------------------------------------
    # Validar cascade
    # ---------------------------------------------------------

    assert db.get(User, user_id) is None
    assert db.get(Session, session_id) is None
    assert db.get(FinancialPeriod, period_id) is None
    assert db.get(Expense, expense_id) is None
    assert db.get(ConversationMessage, message_id) is None


def test_persisted_financial_data_can_be_used_for_balance_calculation(
    db_session,
):
    """
    Valida que os dados financeiros persistidos podem ser
    recuperados e utilizados para calcular o saldo mensal.
    """

    db = db_session

    user = User(
        external_id="calculation-user",
    )

    db.add(user)
    db.flush()

    session = Session(
        user_id=user.id,
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

    expenses = [
        Expense(
            period_id=period.id,
            category="moradia",
            amount=Decimal("1500.00"),
        ),
        Expense(
            period_id=period.id,
            category="alimentação",
            amount=Decimal("800.00"),
        ),
        Expense(
            period_id=period.id,
            category="transporte",
            amount=Decimal("400.00"),
        ),
    ]

    db.add_all(expenses)
    db.commit()

    # ---------------------------------------------------------
    # Recuperar período
    # ---------------------------------------------------------

    persisted_period = db.get(
        FinancialPeriod,
        period.id,
    )

    assert persisted_period is not None

    # ---------------------------------------------------------
    # Calcular total
    # ---------------------------------------------------------

    total_expenses = sum(
        expense.amount
        for expense in persisted_period.expenses
    )

    balance = (
        persisted_period.income
        - total_expenses
    )

    # ---------------------------------------------------------
    # Validar
    # ---------------------------------------------------------

    assert total_expenses == Decimal("2700.00")
    assert balance == Decimal("2300.00")

