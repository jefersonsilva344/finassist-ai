from datetime import datetime
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.orm import Session as DBSession

from src.agent.session import SessionState
from src.persistence.models import (
    ConversationMessage,
    Expense,
    FinancialPeriod,
    MessageRole,
)


class FinancialPersistenceService:
    """
    Serviço responsável por persistir e recuperar
    o estado financeiro de uma sessão do agente.
    """

    def __init__(self, db: DBSession):
        self.db = db

    def persist_agent_state(
        self,
        session_id: int,
        state: SessionState,
        user_message: str,
        assistant_response: str,
        year: int | None = None,
        month: int | None = None,
    ) -> FinancialPeriod | None:

        now = datetime.now()

        year = year or now.year
        month = month or now.month

        period = (
            self.db.query(FinancialPeriod)
            .filter(
                FinancialPeriod.session_id == session_id,
                FinancialPeriod.year == year,
                FinancialPeriod.month == month,
            )
            .first()
        )

        # ======================================================
        # SEM DADOS FINANCEIROS
        # ======================================================

        if (
            period is None
            and state.income is None
            and state.expenses is None
        ):
            self._persist_conversation(
                session_id=session_id,
                user_message=user_message,
                assistant_response=assistant_response,
            )

            self.db.commit()

            return None

        # ======================================================
        # CRIAR PERÍODO
        # ======================================================

        if period is None:

            period = FinancialPeriod(
                session_id=session_id,
                year=year,
                month=month,
                income=(
                    Decimal(str(state.income))
                    if state.income is not None
                    else None
                ),
                total_expenses=(
                    Decimal(str(state.expenses))
                    if state.expenses is not None
                    else None
                ),
            )

            self.db.add(period)
            self.db.flush()

        # ======================================================
        # ATUALIZAR PERÍODO EXISTENTE
        # ======================================================

        else:

            if state.income is not None:
                period.income = Decimal(
                    str(state.income)
                )

            if state.expenses is not None:
                period.total_expenses = Decimal(
                    str(state.expenses)
                )

        # ======================================================
        # DESPESAS CATEGORIZADAS
        # ======================================================

        self.db.query(Expense).filter(
            Expense.period_id == period.id
        ).delete(
            synchronize_session=False
        )

        for category, amount in state.expense_categories.items():

            self.db.add(
                Expense(
                    period_id=period.id,
                    category=category,
                    amount=Decimal(str(amount)),
                )
            )

        # ======================================================
        # CONVERSA
        # ======================================================

        self._persist_conversation(
            session_id=session_id,
            user_message=user_message,
            assistant_response=assistant_response,
        )

        self.db.commit()
        self.db.refresh(period)

        return period


    def _persist_conversation(
        self,
        session_id: int,
        user_message: str,
        assistant_response: str,
    ) -> None:

        user_message_entity = ConversationMessage(
            session_id=session_id,
            role=MessageRole.USER,
            content=user_message,
        )

        assistant_message_entity = ConversationMessage(
            session_id=session_id,
            role=MessageRole.ASSISTANT,
            content=assistant_response,
        )

        self.db.add_all(
            [
                user_message_entity,
                assistant_message_entity,
            ]
        )



    def load_agent_state(
        self,
        session_id: int,
    ) -> SessionState:

        period = (
            self.db.query(FinancialPeriod)
            .filter(
                FinancialPeriod.session_id == session_id
            )
            .order_by(
                FinancialPeriod.year.desc(),
                FinancialPeriod.month.desc(),
            )
            .first()
        )

        state = SessionState()

        if period is None:
            return state

        # ======================================================
        # RENDA
        # ======================================================

        if period.income is not None:
            state.update_income(
                float(period.income)
            )

        # ======================================================
        # DESPESAS CATEGORIZADAS
        # ======================================================

        for expense in period.expenses:

            state.add_expense_category(
                category=expense.category,
                amount=float(expense.amount),
            )

        # ======================================================
        # TOTAL DE DESPESAS
        # ======================================================

        if period.total_expenses is not None:

            state.update_expenses(
                float(period.total_expenses)
            )

        elif state.expense_categories:

            state.sync_expenses_from_categories()

        return state