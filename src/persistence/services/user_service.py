from uuid import uuid4

from sqlalchemy.orm import Session

from src.persistence.models import User
from src.persistence.repositories.user_repository import UserRepository


class UserService:
    """
    Serviço responsável pelo ciclo de vida dos usuários.
    """

    def __init__(self, session: Session):
        self.repository = UserRepository(session)

    def create_user(
        self,
        external_id: str,
    ) -> User:
      
        user = User(
            external_id=external_id
        )

        return self.repository.add(user)

    def get_user(
        self,
        user_id: int,
    ) -> User | None:
        return self.repository.get_by_id(user_id)

    def get_user_by_external_id(
        self,
        external_id: str,
    ) -> User | None:
        return self.repository.get_by_external_id(
            external_id
        )

    def get_or_create_user(
        self,
        external_id: str,
    ) -> User:
        user = self.get_user_by_external_id(
            external_id
        )

        if user is not None:
            return user

        return self.create_user(
            external_id=external_id
        )

    def get_or_create(
        self,
        external_id: str,
    ) -> User:
        """
        Alias de compatibilidade para o ContextService.
        """
        return self.get_or_create_user(
            external_id
        )