from src.tools.calculator import (
    calculate_balance,
    calculate_income_commitment,
    calculate_savings_rate,
)


class BudgetAnalysisService:
    """
    Serviço de aplicação responsável pela análise
    determinística do orçamento financeiro.
    """

    def analyze(
        self,
        income: float,
        expenses: float,
    ) -> dict[str, float]:
        """
        Calcula os principais indicadores financeiros
        do orçamento.
        """

        balance = calculate_balance(
            income,
            expenses,
        )

        savings_rate = calculate_savings_rate(
            income,
            expenses,
        )

        commitment = calculate_income_commitment(
            income,
            expenses,
        )

        return {
            "balance": balance,
            "savings_rate": savings_rate,
            "commitment": commitment,
        }