from dataclasses import dataclass


@dataclass
class SufficiencyResult:
    sufficient: bool
    missing_information: list[str]
    reason: str


def check_budget_sufficiency(
    budget_data: dict | None,
) -> SufficiencyResult:

    if budget_data is None:
        return SufficiencyResult(
            sufficient=False,
            missing_information=[
                "renda mensal",
                "despesas mensais",
            ],
            reason="Não foi possível identificar os dados do orçamento.",
        )

    missing = []

    if budget_data.get("income") is None:
        missing.append("renda mensal")

    if budget_data.get("expenses") is None:
        missing.append("despesas mensais")

    if missing:
        return SufficiencyResult(
            sufficient=False,
            missing_information=missing,
            reason="Existem dados essenciais ausentes.",
        )

    return SufficiencyResult(
        sufficient=True,
        missing_information=[],
        reason="Todos os dados necessários para a análise foram fornecidos.",
    )