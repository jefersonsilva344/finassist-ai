from src.agent.agent import FinAssistAgent
from src.persistence.services.context_service import ContextService
from src.persistence.services.financial_service import (
    FinancialPersistenceService,
)


class FinancialFlow:
    """
    Orquestra o fluxo financeiro completo da aplicação.

    Responsabilidades:

    1. Recuperar/criar contexto persistente.
    2. Recuperar memória financeira.
    3. Enviar mensagem ao agente.
    4. Persistir estado atualizado.
    5. Retornar resposta ao usuário.
    """

    def __init__(
        self,
        agent: FinAssistAgent,
        context_service: ContextService,
        financial_persistence: FinancialPersistenceService,
    ):
        self.agent = agent
        self.context_service = context_service
        self.financial_persistence = (
            financial_persistence
        )

    def process_message(
        self,
        external_user_id: str,
        message: str,
    ) -> str:

        context = (
            self.context_service
            .get_or_create_context(
                external_user_id
            )
        )

        self.agent.session = (
            self.financial_persistence
            .load_agent_state(
                context.session_id
            )
        )

        response = self.agent.answer(
            message
        )

        self.financial_persistence.persist_agent_state(
            session_id=context.session_id,
            state=self.agent.session,
            user_message=message,
            assistant_response=response,
        )

        return response