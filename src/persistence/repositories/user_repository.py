from sqlalchemy.orm import Session

from src.persistence.models import User


class UserRepository:
    """
    Repositório responsável pela persistência de usuários.
    """

    def __init__(self, session: Session):
        self.session = session

    def add(self, user: User) -> User:
        self.session.add(user)
        self.session.flush()
        return user

    def get_by_id(self, user_id: int) -> User | None:
        return (
            self.session.query(User)
            .filter(User.id == user_id)
            .first()
        )

    def get_by_external_id(
        self,
        external_id: str,
    ) -> User | None:
        return (
            self.session.query(User)
            .filter(User.external_id == external_id)
            .first()
        )