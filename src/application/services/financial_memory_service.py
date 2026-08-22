from src.agent.session import SessionState
from src.tools.extractor import (
    extract_budget_values,
    extract_categorized_expenses,
)


class FinancialMemoryService:
    """
    Serviço de aplicação responsável pela memória
    financeira da sessão.

    Centraliza:
    - atualização de renda;
    - atualização de despesas;
    - registro de despesas categorizadas;
    - sincronização do orçamento;
    - leitura do estado financeiro atual.

    O serviço encapsula o SessionState para evitar que
    outras camadas dependam diretamente da implementação
    da memória.
    """

    def __init__(
        self,
        session: SessionState | None = None,
    ) -> None:

        self.session = session or SessionState()

    # ==========================================================
    # ATUALIZAÇÃO
    # ==========================================================

    def update_from_message(
        self,
        user_message: str,
    ) -> None:
        """
        Extrai informações financeiras da mensagem e
        atualiza a memória da sessão.
        """

        budget_data = extract_budget_values(
            user_message
        )

        if budget_data is not None:

            income = budget_data.get(
                "income"
            )

            expenses = budget_data.get(
                "expenses"
            )

            if income is not None:
                self.session.update_income(
                    income
                )

            if expenses is not None:
                self.session.update_expenses(
                    expenses
                )

        categorized_expenses = (
            extract_categorized_expenses(
                user_message
            )
        )

        for category, amount in categorized_expenses:

            self.session.add_expense_category(
                category=category,
                amount=amount,
            )

            # ======================================================
            # SINCRONIZAÇÃO DO TOTAL
            # ======================================================

            if self.session.has_categorized_expenses():
                self.session.sync_expenses_from_categories()

    # ==========================================================
    # LEITURA
    # ==========================================================

    @property
    def income(self) -> float | None:
        """
        Retorna a renda atualmente armazenada.
        """

        return self.session.income

    @property
    def expenses(self) -> float | None:
        """
        Retorna as despesas atualmente armazenadas.
        """

        return self.session.expenses

    def get_budget_data(
        self,
    ) -> dict[str, float | None]:
        """
        Retorna o orçamento atual da sessão.
        """

        return {
            "income": self.session.income,
            "expenses": self.session.expenses,
        }

    # ==========================================================
    # CATEGORIAS
    # ==========================================================

    def get_category_expense(
        self,
        category: str,
    ) -> float | None:
        """
        Retorna o valor acumulado de uma categoria.
        """

        return self.session.get_category_expense(
            category
        )

    def has_categorized_expenses(
        self,
    ) -> bool:
        """
        Indica se existem despesas categorizadas.
        """

        return self.session.has_categorized_expenses()

    # ==========================================================
    # SESSÃO
    # ==========================================================

    def has_complete_budget(self) -> bool:
        """
        Indica se renda e despesas estão disponíveis.
        """

        return self.session.has_complete_budget()

    def clear(self) -> None:
        """
        Limpa toda a memória financeira da sessão.
        """

        self.session.clear()