from src.application.dto import BudgetAnalysisOutput
from src.application.services.budget_analysis_service import (
    BudgetAnalysisService,
)


class AnalyzeBudget:
    """
    Caso de uso responsável por analisar
    os principais indicadores de um orçamento.
    """

    def __init__(
        self,
        service: BudgetAnalysisService | None = None,
    ) -> None:
        self.service = service or BudgetAnalysisService()

    def execute(
        self,
        income: float,
        expenses: float,
    ) -> BudgetAnalysisOutput:
        result = self.service.analyze(
            income=income,
            expenses=expenses,
        )

        return BudgetAnalysisOutput(
            balance=result["balance"],
            savings_rate=result["savings_rate"],
            commitment=result["commitment"],
        )