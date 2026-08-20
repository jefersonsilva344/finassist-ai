from sqlalchemy import select
from sqlalchemy.orm import Session

from src.persistence.models import Session as UserSession


class SessionRepository:
    """
    Repository responsável pelas operações de persistência
    relacionadas às sessões de utilização.
    """

    def __init__(self, session: Session) -> None:
        self.session = session

    def add(self, user_session: UserSession) -> UserSession:
        """
        Adiciona uma sessão à sessão transacional atual.
        """

        self.session.add(user_session)
        self.session.flush()

        return user_session

    def get_by_id(
        self,
        session_id: int,
    ) -> UserSession | None:
        """
        Recupera uma sessão pelo ID.
        """

        return self.session.get(UserSession, session_id)

    def list_by_user(
        self,
        user_id: int,
    ) -> list[UserSession]:
        """
        Retorna todas as sessões pertencentes a um usuário.
        """

        statement = (
            select(UserSession)
            .where(UserSession.user_id == user_id)
            .order_by(UserSession.created_at)
        )

        return list(
            self.session.scalars(statement).all()
        )