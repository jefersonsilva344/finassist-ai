from decimal import Decimal

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from src.persistence.database import Base
from src.persistence.models import (
    User,
)


class FakeResponse:
    def __init__(self, text: str):
        self.output_text = text


class FakeResponses:
    def create(
        self,
        *,
        model,
        instructions,
        input,
    ):
        return FakeResponse(
            "Análise financeira processada com sucesso."
        )


class FakeOpenAI:
    def __init__(self, *args, **kwargs):
        self.responses = FakeResponses()


def create_test_session():
    engine = create_engine(
        "sqlite:///:memory:",
        future=True,
        connect_args={
            "check_same_thread": False,
        },
        poolclass=StaticPool,
    )

    Base.metadata.create_all(engine)

    SessionLocal = sessionmaker(
        bind=engine,
        autoflush=False,
        autocommit=False,
    )

    return engine, SessionLocal


def test_complete_financial_business_flow():
    """
    Teste de integração orientado ao negócio.

    Valida o fluxo:

        API/Application
              ↓
        Composition Root
              ↓
        FinancialFlow
              ↓
        Agent
              ↓
        FinancialMemory
              ↓
        Persistence Services
              ↓
        SQLite
              ↓
        recuperação
              ↓
        novo Container
              ↓
        Agent
              ↓
        saldo financeiro
    """

    # ==========================================================
    # 1. Imports da composição da aplicação
    # ==========================================================

    from src.bootstrap.container import build_container

    # ==========================================================
    # 2. Criar banco de teste
    # ==========================================================

    engine, SessionLocal = create_test_session()

    db = SessionLocal()

    try:

        # ======================================================
        # 3. Criar aplicação através do Composition Root
        # ======================================================

        fake_openai = FakeOpenAI()

        container = build_container(
            db=db,
            openai_client=fake_openai,
        )

        flow = container.financial_flow

        # O Agent foi criado pelo Composition Root.
        agent = flow.agent

        # ======================================================
        # 4. Mensagem real do usuário
        # ======================================================

        message = (
            "Minha renda é R$ 5.000, "
            "pago R$ 1.500 de aluguel, "
            "R$ 800 com alimentação "
            "e R$ 400 com transporte."
        )

        # ======================================================
        # 5. Executar fluxo completo
        # ======================================================

        response = flow.process_message(
            external_user_id="business-user-001",
            message=message,
        )

        # ======================================================
        # 6. Validar resposta
        # ======================================================

        assert response is not None
        assert response != ""

        # ======================================================
        # 7. Validar memória do Agent
        # ======================================================

        assert agent.session.income == 5000.0

        assert (
            agent.session.expense_categories["moradia"]
            == 1500.0
        )

        assert (
            agent.session.expense_categories["alimentação"]
            == 800.0
        )

        assert (
            agent.session.expense_categories["transporte"]
            == 400.0
        )

        assert agent.session.expenses == 2700.0

        # ======================================================
        # 8. Validar User
        # ======================================================

        user = (
            db.query(User)
            .filter(
                User.external_id
                == "business-user-001"
            )
            .one()
        )

        assert user.id is not None

        # ======================================================
        # 9. Validar Session
        # ======================================================

        assert len(user.sessions) == 1

        persisted_session = user.sessions[0]

        # ======================================================
        # 10. Validar FinancialPeriod
        # ======================================================

        assert len(
            persisted_session.financial_periods
        ) == 1

        period = (
            persisted_session
            .financial_periods[0]
        )

        assert period.income == Decimal(
            "5000.00"
        )

        # ======================================================
        # 11. Validar Expenses
        # ======================================================

        expenses = {
            expense.category: expense
            for expense in period.expenses
        }

        assert expenses["moradia"].amount == Decimal(
            "1500.00"
        )

        assert expenses["alimentação"].amount == Decimal(
            "800.00"
        )

        assert expenses["transporte"].amount == Decimal(
            "400.00"
        )

        # ======================================================
        # 12. Validar total persistido
        # ======================================================

        total_expenses = sum(
            expense.amount
            for expense in period.expenses
        )

        assert total_expenses == Decimal(
            "2700.00"
        )

        # ======================================================
        # 13. Validar saldo de negócio
        # ======================================================

        balance = (
            period.income
            - total_expenses
        )

        assert balance == Decimal(
            "2300.00"
        )

        # ======================================================
        # 14. Validar histórico da conversa
        # ======================================================

        messages = (
            persisted_session
            .conversation_messages
        )

        assert len(messages) == 2

        assert any(
            message.content == (
                "Minha renda é R$ 5.000, "
                "pago R$ 1.500 de aluguel, "
                "R$ 800 com alimentação "
                "e R$ 400 com transporte."
            )
            for message in messages
        )

        # ======================================================
        # 15. Simular nova execução da aplicação
        # ======================================================

        db.close()

        db = SessionLocal()

        # Criamos NOVAMENTE o container.
        #
        # Não criamos FinAssistAgent ou FinancialFlow
        # diretamente. O Composition Root continua sendo
        # responsável pela montagem da aplicação.

        new_fake_openai = FakeOpenAI()

        new_container = build_container(
            db=db,
            openai_client=new_fake_openai,
        )

        new_flow = new_container.financial_flow
        new_agent = new_flow.agent

        # ======================================================
        # 16. Usuário pergunta depois
        # ======================================================

        follow_up = new_flow.process_message(
            external_user_id="business-user-001",
            message="Qual é o meu saldo?",
        )

        # ======================================================
        # 17. Validar recuperação da memória
        # ======================================================

        assert follow_up is not None
        assert follow_up != ""

        # ======================================================
        # 18. Validar resposta financeira
        # ======================================================

        assert "2.300" in follow_up

        # ======================================================
        # 19. Garantir que o novo Agent recuperou o estado
        # ======================================================

        assert new_agent.session.income == 5000.0

        assert (
            new_agent.session.expenses
            == 2700.0
        )

    finally:
        db.close()
        engine.dispose()