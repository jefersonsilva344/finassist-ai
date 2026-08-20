from dataclasses import dataclass

from src.persistence.models import Session, User


@dataclass
class PersistenceContext:
    """
    Contexto de persistência associado à execução atual.

    Mantém a identidade persistida do usuário
    e da sessão atual.
    """

    user_id: int
    session_id: int

    @classmethod
    def from_entities(
        cls,
        user: User,
        session: Session,
    ) -> "PersistenceContext":
        
        if user.id is None:
            raise ValueError(
                "O usuário precisa estar persistido."
            )

        if session.id is None:
            raise ValueError(
                "A sessão precisa estar persistida."
            )

        return cls(
            user_id=user.id,
            session_id=session.id,
        )