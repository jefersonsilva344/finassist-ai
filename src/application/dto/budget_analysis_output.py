from dataclasses import dataclass


@dataclass(frozen=True)
class BudgetAnalysisOutput:
    """
    Resultado da análise financeira de um orçamento.
    """

    balance: float
    savings_rate: float
    commitment: float