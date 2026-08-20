from sqlalchemy.orm import Session as DBSession

from src.persistence.models import Session as UserSession
from src.persistence.repositories.session_repository import SessionRepository


class SessionService:
    """
    Serviço responsável pelo ciclo de vida das sessões.
    """

    def __init__(self, db: DBSession):
        self.db = db
        self.repository = SessionRepository(db)

    def start_session(
        self,
        user_id: int,
    ) -> UserSession:
        """
        Inicia uma nova sessão para um usuário.
        """

        session = UserSession(
            user_id=user_id
        )

        return self.repository.add(session)

    def create_session(
        self,
        user_id: int,
    ) -> UserSession:
        """
        Alias de compatibilidade para criação de sessões.
        """

        return self.start_session(user_id)

    def get_session(
        self,
        session_id: int,
    ) -> UserSession | None:
        """
        Recupera uma sessão pelo ID.
        """

        return self.repository.get_by_id(session_id)

    def list_user_sessions(
        self,
        user_id: int,
    ) -> list[UserSession]:
        """
        Retorna todas as sessões pertencentes ao usuário.
        """

        return self.repository.list_by_user(user_id)