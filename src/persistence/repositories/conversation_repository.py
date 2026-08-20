from sqlalchemy import select
from sqlalchemy.orm import Session as DBSession

from src.persistence.models import (
    ConversationMessage,
    MessageRole,
)


class ConversationRepository:
    """
    Repository responsável pelo histórico
    de mensagens das conversas.
    """

    def __init__(self, db: DBSession):
        self.db = db

    def add(
        self,
        message: ConversationMessage,
    ) -> ConversationMessage:
        """
        Adiciona uma mensagem.
        """

        self.db.add(message)

        return message

    def get_by_id(
        self,
        message_id: int,
    ) -> ConversationMessage | None:
        """
        Busca uma mensagem pelo ID.
        """

        statement = select(
            ConversationMessage
        ).where(
            ConversationMessage.id == message_id
        )

        return self.db.scalar(statement)

    def list_by_session(
        self,
        session_id: int,
    ) -> list[ConversationMessage]:
        """
        Retorna o histórico completo de uma sessão.
        """

        statement = (
            select(ConversationMessage)
            .where(
                ConversationMessage.session_id == session_id
            )
            .order_by(
                ConversationMessage.created_at
            )
        )

        return list(
            self.db.scalars(statement).all()
        )

    def list_by_role(
        self,
        session_id: int,
        role: MessageRole,
    ) -> list[ConversationMessage]:
        """
        Retorna mensagens filtradas por papel.
        """

        statement = (
            select(ConversationMessage)
            .where(
                ConversationMessage.session_id == session_id,
                ConversationMessage.role == role,
            )
            .order_by(
                ConversationMessage.created_at
            )
        )

        return list(
            self.db.scalars(statement).all()
        )