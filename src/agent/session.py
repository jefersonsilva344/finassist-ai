from .category import normalize_category


class SessionState:
    """
    Armazena informações financeiras da sessão atual.
    """

    def __init__(self) -> None:
        self.income: float | None = None
        self.expenses: float | None = None

        self.expense_categories: dict[str, float] = {}

        self.financial_goals: list[dict[str, float | str]] = []

    # ==========================================================
    # RENDA
    # ==========================================================

    def update_income(
        self,
        income: float,
    ) -> None:
        self.income = income

    # ==========================================================
    # DESPESAS
    # ==========================================================

    def update_expenses(
        self,
        expenses: float,
    ) -> None:
        """
        Atualiza o total de despesas.

        Se já existem despesas categorizadas,
        elas permanecem como fonte de verdade.
        """

        if self.expense_categories:
            self.sync_expenses_from_categories()
            return

        self.expenses = expenses


    def add_expense_category(
        self,
        category: str,
        amount: float,
    ) -> None:
        """
        Adiciona uma despesa a uma categoria.

        Se a categoria já existir, soma o novo valor.
        """

        normalized_category = normalize_category(
            category
        )

        current_value = self.expense_categories.get(
            normalized_category,
            0.0,
        )

        self.expense_categories[
            normalized_category
        ] = current_value + amount

        self.sync_expenses_from_categories()

    def sync_expenses_from_categories(self) -> None:
        """
        Sincroniza o total de despesas com as categorias
        armazenadas na sessão.

        As categorias são consideradas a fonte de verdade
        quando existem despesas categorizadas.
        """

        if not self.expense_categories:
            return

        self.expenses = sum(
            self.expense_categories.values()
        )    

    # ==========================================================
    # METAS
    # ==========================================================

    def add_financial_goal(
        self,
        name: str,
        amount: float,
    ) -> None:
        self.financial_goals.append(
            {
                "name": name,
                "amount": amount,
            }
        )

    # ==========================================================
    # CONSULTAS
    # ==========================================================

    def get_category_expense(
        self,
        category: str,
    ) -> float | None:

        from .memory import normalize_category

        normalized_category = normalize_category(
            category
        )

        return self.expense_categories.get(
            normalized_category
        )

    def get_total_categorized_expenses(
        self,
    ) -> float:

        return sum(
            self.expense_categories.values()
        )

    def has_income(self) -> bool:
        return self.income is not None

    def has_expenses(self) -> bool:
        return self.expenses is not None

    def has_complete_budget(self) -> bool:
        return (
            self.income is not None
            and self.expenses is not None
        )

    def has_categorized_expenses(self) -> bool:
        """
        Retorna True quando existe pelo menos uma
        despesa categorizada.
        """

        return bool(self.expense_categories)

    # ==========================================================
    # LIMPEZA
    # ==========================================================

    def clear(self) -> None:
        self.income = None
        self.expenses = None
        self.expense_categories.clear()
        self.financial_goals.clear()