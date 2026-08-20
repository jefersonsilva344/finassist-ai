from sqlalchemy import select
from sqlalchemy.orm import Session as DBSession

from src.persistence.models import FinancialPeriod


class FinancialPeriodRepository:
    """
    Repository responsável pelos períodos financeiros.
    """

    def __init__(self, db: DBSession):
        self.db = db

    def add(
        self,
        period: FinancialPeriod,
    ) -> FinancialPeriod:
        """
        Adiciona um período financeiro.
        """

        self.db.add(period)

        return period

    def get_by_id(
        self,
        period_id: int,
    ) -> FinancialPeriod | None:
        """
        Busca um período pelo ID.
        """

        statement = select(FinancialPeriod).where(
            FinancialPeriod.id == period_id
        )

        return self.db.scalar(statement)

    def get_by_session_and_month(
        self,
        session_id: int,
        year: int,
        month: int,
    ) -> FinancialPeriod | None:
        """
        Busca o período financeiro de uma sessão
        para determinado ano e mês.
        """

        statement = (
            select(FinancialPeriod)
            .where(
                FinancialPeriod.session_id == session_id,
                FinancialPeriod.year == year,
                FinancialPeriod.month == month,
            )
        )

        return self.db.scalar(statement)

    def list_by_session(
        self,
        session_id: int,
    ) -> list[FinancialPeriod]:
        """
        Lista os períodos financeiros de uma sessão.
        """

        statement = (
            select(FinancialPeriod)
            .where(
                FinancialPeriod.session_id == session_id
            )
            .order_by(
                FinancialPeriod.year,
                FinancialPeriod.month,
            )
        )

        return list(
            self.db.scalars(statement).all()
        )
