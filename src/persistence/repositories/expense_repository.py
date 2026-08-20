from sqlalchemy import select
from sqlalchemy.orm import Session as DBSession

from src.persistence.models import Expense


class ExpenseRepository:
    """
    Repository responsável pela persistência de despesas.
    """

    def __init__(self, db: DBSession):
        self.db = db

    def add(self, expense: Expense) -> Expense:
        """
        Adiciona uma despesa.
        """

        self.db.add(expense)

        return expense

    def get_by_id(
        self,
        expense_id: int,
    ) -> Expense | None:
        """
        Busca uma despesa pelo ID.
        """

        statement = select(Expense).where(
            Expense.id == expense_id
        )

        return self.db.scalar(statement)

    def list_by_period(
        self,
        period_id: int,
    ) -> list[Expense]:
        """
        Lista todas as despesas de um período.
        """

        statement = (
            select(Expense)
            .where(Expense.period_id == period_id)
            .order_by(Expense.created_at)
        )

        return self.db.scalars(statement).all()


    def list_by_category(
        self,
        period_id: int,
        category: str,
    ) -> list[Expense]:
        """
        Lista despesas de determinada categoria.
        """

        statement = (
            select(Expense)
            .where(
                Expense.period_id == period_id,
                Expense.category == category,
            )
            .order_by(Expense.created_at)
        )

        return self.db.scalars(statement).all()

    def delete(self, expense: Expense) -> None:
        """
        Remove uma despesa.
        """

        self.db.delete(expense)