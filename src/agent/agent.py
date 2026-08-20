
from src.knowledge.retriever import retrieve_knowledge
from src.tools.calculator import (
    calculate_balance,
    calculate_income_commitment,
    calculate_savings_rate,
)

from ..prompts.prompts import SYSTEM_PROMPT, RESPONSE_PROMPT
from .intent import classify_intent

from .decision import make_decision
from src.tools.extractor import extract_budget_values
from .sufficiency import check_budget_sufficiency

from .session import SessionState

from .context import (
    detect_follow_up,
    detect_category_query,
    detect_category_percentage_query,
    detect_category_summary_query
)

from src.tools.category_analyzer import (
    calculate_category_percentages,
    get_category_summary,
)

from src.tools.extractor import (
    extract_categorized_expenses,
)

from .memory import add_expense

from src.tools.formatters import format_brl

import os

from openai import OpenAI

OPENAI_MODEL = os.getenv(
    "OPENAI_MODEL",
    "gpt-4o-mini",
)


class FinAssistAgent:
    """
    Orquestrador principal do FinAssist AI.

    Responsabilidades:
    - identificar a intenção;
    - recuperar conhecimento;
    - executar cálculos determinísticos;
    - enviar contexto para o LLM;
    - gerar a resposta final.
    """

    def __init__(
        self,
        client: OpenAI,
    )-> None:

        self.client = client
        self.session = SessionState()



    def _update_session(
        self,
        user_message: str,
    ) -> None:
        """
        Atualiza a memória financeira da sessão.

        Prioridade:
        1. Receita/despesa geral
        2. Despesa categorizada
        """

        # ------------------------------------------------------
        # Receita / despesa geral
        # ------------------------------------------------------

        budget_data = extract_budget_values(
            user_message
        )

        if budget_data is not None:

            income = budget_data.get("income")
            expenses = budget_data.get("expenses")

            if income is not None:
                self.session.update_income(
                    income
                )

            if expenses is not None:
                self.session.update_expenses(
                    expenses
                )

        # ------------------------------------------------------
        # Despesa categorizada
        # ------------------------------------------------------

        categorized_expenses = extract_categorized_expenses(
        user_message
        )

        for category, amount in categorized_expenses:

            add_expense(
                session=self.session,
                category=category,
                amount=amount,
            )

        
    def _get_budget_data(
        self,
        user_message: str,
    ) -> dict[str, float | None]:
        """
        Retorna o estado financeiro atual da sessão.

        A atualização da memória acontece exclusivamente
        em _update_session().
        """

        return {
            "income": self.session.income,
            "expenses": self.session.expenses,
        }


    def _handle_category_query(
        self,
        user_message: str,
    ) -> str | None:
        """
        Responde consultas sobre despesas categorizadas
        usando exclusivamente a memória estruturada.
        """

        category = detect_category_query(
            message=user_message,
            session=self.session,
        )

        if category is None:
            return None

        amount = self.session.get_category_expense(
            category
        )

        if amount is None:
            return (
                f"Não encontrei despesas registradas "
                f"na categoria {category}."
            )

        return (
            f"Você está gastando "
            f"{format_brl(amount)} "
            f"com {category}."
        )



    def _handle_category_percentage_query(
        self,
        user_message: str,
    ) -> str | None:
        """
        Responde consultas sobre o percentual da renda
        comprometido com uma categoria.

        O cálculo é realizado exclusivamente pelo
        category_analyzer.
        """

        category = detect_category_percentage_query(
            message=user_message,
            session=self.session,
        )

        if category is None:
            return None

        amount = self.session.get_category_expense(
            category
        )

        if amount is None:
            return (
                f"Não encontrei despesas registradas "
                f"na categoria {category}."
            )

        percentages = calculate_category_percentages(
            self.session
        )

        percentage = percentages.get(
            category
        )

        if percentage is None:
            return None

        return (
            f"Você gasta "
            f"{format_brl(amount)} "
            f"com {category}, "
            f"o que representa "
            f"{percentage:.2f}% "
            f"da sua renda mensal."
        )


    def _handle_category_summary(
        self,
        user_message: str,
    ) -> str | None:
        """
        Responde solicitações de resumo das despesas
        por categoria.

        Os dados são obtidos diretamente da memória
        financeira e processados deterministicamente.
        """

        is_summary_query = detect_category_summary_query(
            message=user_message,
            session=self.session,
        )

        if not is_summary_query:
            return None

        summary = get_category_summary(
            self.session
        )

        if not summary:
            return (
                "Ainda não existem despesas "
                "categorizadas registradas."
            )

        lines = [
            "Resumo das suas despesas por categoria:"
        ]

        for item in summary:
            lines.append(
                f"- {item['category'].capitalize()}: "
                f"{format_brl(item['amount'])} "
                f"({item['percentage']:.2f}% da renda)"
            )

        return "\n".join(lines)
    


    def _handle_follow_up(
        self,
        user_message: str,
    ) -> str | None:
        """
        Processa perguntas de continuação usando os dados
        armazenados na memória da sessão.
        """

        action = detect_follow_up(
            message=user_message,
            session=self.session,
        )

        if action is None:
            return None

        if (
            self.session.income is None
            or self.session.expenses is None
        ):
            return None

        results = self._calculate_budget(
            income=self.session.income,
            expenses=self.session.expenses,
        )

        if action == "balance":
            return (
                f"Com base na sua renda de "
                f"{format_brl(self.session.income)} "
                f"e despesas de "
                f"{format_brl(self.session.expenses)}, "
                f"seu saldo mensal é de "
                f"{format_brl(results['balance'])}."
            )

        if action == "savings_rate":
            return (
                f"Sua taxa de economia é de "
                f"{results['savings_rate']:.2f}%."
            )

        if action == "commitment":
            return (
                f"Seu comprometimento da renda é de "
                f"{results['commitment']:.2f}%."
            )

        return None

    # ==========================================================
    # CÁLCULOS
    # ==========================================================

    def _calculate_budget(
        self,
        income: float,
        expenses: float,
    ) -> dict[str, float]:
        """
        Executa os cálculos financeiros de forma determinística.
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


    def _check_information(
        self,
        intent: str,
        user_message: str,
    ):
        if intent != "budget_analysis":
            return None

        budget_data = self._get_budget_data(
            user_message
        )

        return check_budget_sufficiency(
            budget_data
        )

    def _execute_tools(
        self,
        decision,
        user_message: str,
    ) -> str:

        if not decision.requires_tool:
            return ""

        if decision.intent != "budget_analysis":
            return ""

        budget_data = self._get_budget_data(
            user_message
        )

        sufficiency = check_budget_sufficiency(
            budget_data
        )

        if not sufficiency.sufficient:
            return ""

        results = self._calculate_budget(
            income=budget_data["income"],
            expenses=budget_data["expenses"],
        )

        return (
            "CÁLCULO FINANCEIRO DETERMINÍSTICO:\n"
            f"Receita: R$ {budget_data['income']:.2f}\n"
            f"Despesas: R$ {budget_data['expenses']:.2f}\n"
            f"Saldo: R$ {results['balance']:.2f}\n"
            f"Taxa de economia: "
            f"{results['savings_rate']:.2f}%\n"
            f"Comprometimento da renda: "
            f"{results['commitment']:.2f}%"
        )

    # ==========================================================
    # PROCESSAMENTO
    # ==========================================================

    def answer(
        self,
        user_message: str,
        tool_results: str = "",
    ) -> str:


        # 1.1 Atualizar memória
        self._update_session(
            user_message
        )

        # 1.2 Verificar se é uma pergunta de continuação
        follow_up_response = self._handle_follow_up(
            user_message
        )

        if follow_up_response is not None:
            return follow_up_response

        # 1.3 Consultar percentual de categoria
        category_percentage_response = (
            self._handle_category_percentage_query(
                user_message
            )
        )

        if category_percentage_response is not None:
            return category_percentage_response

        # 1.4 Consultar valor de categoria
        category_response = self._handle_category_query(
            user_message
        )

        if category_response is not None:
            return category_response

        # 1.5 Consultar resumo das categorias
        category_summary_response = (
            self._handle_category_summary(
                user_message
            )
        )

        if category_summary_response is not None:
            return category_summary_response

        # 1.6 Intent
        intent = classify_intent(
            user_message
        )


        # 2. Knowledge
        knowledge_context = retrieve_knowledge(
            user_message
        )

        # 3. Decision
        decision = make_decision(
            intent=intent,
            user_message=user_message,
            knowledge_context=knowledge_context,
        )


        sufficiency = self._check_information(
            intent=intent,
            user_message=user_message,
        )

        # 4. Tools
        calculated_results = self._execute_tools(
            decision=decision,
            user_message=user_message,
        )

        if calculated_results:
            tool_results = calculated_results


        information_status = ""

        if sufficiency is not None:

            if sufficiency.sufficient:

                information_status = (
                    "INFORMAÇÕES SUFICIENTES.\n"
                    "Os dados necessários estão disponíveis."
                )

            else:

                missing = ", ".join(
                    sufficiency.missing_information
                )

                information_status = (
                    "INFORMAÇÕES INSUFICIENTES.\n"
                    f"Dados ausentes: {missing}\n"
                    f"Motivo: {sufficiency.reason}"
                )    

        # 5. LLM context
        prompt = RESPONSE_PROMPT.format(
            knowledge_context=knowledge_context,
            user_message=user_message,
            tool_results=tool_results,
        )

        # 6. LLM
        response = self.client.responses.create(
            model=OPENAI_MODEL,
            instructions=SYSTEM_PROMPT,
            input=(
                f"INTENÇÃO IDENTIFICADA:\n"
                f"{decision.intent}\n\n"
                f"DECISÃO DO AGENTE:\n"
                f"{decision.reason}\n\n"
                f"REQUER CONHECIMENTO:\n"
                f"{decision.requires_knowledge}\n\n"
                f"REQUER FERRAMENTA:\n"
                f"{decision.requires_tool}\n\n"
                f"STATUS DAS INFORMAÇÕES:\n"
                f"{information_status}\n\n"
                f"{prompt}"
            ),
        )

        return response.output_text