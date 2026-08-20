from sqlalchemy.orm import Session

from src.persistence.context import PersistenceContext
from src.persistence.services.session_service import SessionService
from src.persistence.services.user_service import UserService


class ContextService:
    """
    Serviço responsável por criar e recuperar
    o contexto persistente de execução.
    """

    def __init__(self, session: Session):
        self.session = session

        self.user_service = UserService(session)
        self.session_service = SessionService(session)

    def create_context(
        self,
        external_id: str,
    ) -> PersistenceContext:
        """
        Cria uma nova sessão para o usuário.

        Deve ser utilizado somente quando uma nova sessão
        de conversa for realmente necessária.
        """

        user = self.user_service.get_or_create_user(
            external_id
        )

        db_session = self.session_service.create_session(
            user.id
        )

        self.session.commit()

        return PersistenceContext.from_entities(
            user,
            db_session,
        )

    def get_or_create_context(
        self,
        external_id: str,
    ) -> PersistenceContext:
        """
        Recupera a sessão existente mais recente do usuário.

        Caso o usuário ainda não possua nenhuma sessão,
        cria uma nova.
        """

        user = self.user_service.get_or_create_user(
            external_id
        )

        sessions = self.session_service.list_user_sessions(
            user.id
        )

        if sessions:
            db_session = sessions[-1]

            return PersistenceContext.from_entities(
                user,
                db_session,
            )

        db_session = self.session_service.create_session(
            user.id
        )

        self.session.commit()

        return PersistenceContext.from_entities(
            user,
            db_session,
        )