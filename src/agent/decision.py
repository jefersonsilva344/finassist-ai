from dataclasses import dataclass


@dataclass
class Decision:
    intent: str
    requires_knowledge: bool
    requires_tool: bool
    requires_more_information: bool
    reason: str


def make_decision(
    intent: str,
    user_message: str,
    knowledge_context: str,
) -> Decision:

    if intent == "out_of_scope":
        return Decision(
            intent=intent,
            requires_knowledge=False,
            requires_tool=False,
            requires_more_information=False,
            reason="Solicitação fora do escopo.",
        )

    if intent == "financial_security":
        return Decision(
            intent=intent,
            requires_knowledge=True,
            requires_tool=False,
            requires_more_information=False,
            reason="Solicitação relacionada à segurança financeira.",
        )

    if intent == "calculation":
        return Decision(
            intent=intent,
            requires_knowledge=False,
            requires_tool=True,
            requires_more_information=True,
            reason="Cálculo deve ser executado por ferramenta determinística.",
        )

    if intent == "budget_analysis":
        return Decision(
            intent=intent,
            requires_knowledge=True,
            requires_tool=True,
            requires_more_information=True,
            reason="Análise de orçamento pode exigir cálculos determinísticos.",
        )

    if intent == "financial_goal":
        return Decision(
            intent=intent,
            requires_knowledge=True,
            requires_tool=True,
            requires_more_information=True,
            reason="Meta financeira pode exigir informações adicionais e cálculos.",
        )

    if intent == "investment_education":
        return Decision(
            intent=intent,
            requires_knowledge=True,
            requires_tool=False,
            requires_more_information=False,
            reason="Pergunta educacional sobre investimentos.",
        )

    if intent == "financial_education":
        return Decision(
            intent=intent,
            requires_knowledge=True,
            requires_tool=False,
            requires_more_information=False,
            reason="Pergunta educacional financeira.",
        )

    return Decision(
        intent=intent,
        requires_knowledge=bool(knowledge_context),
        requires_tool=False,
        requires_more_information=False,
        reason="Fluxo padrão.",
    )