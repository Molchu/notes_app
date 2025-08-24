from typing import Protocol, Optional # Protocol sirve para definir interfaces, optional para valores que pueden ser None
from core.entities.user import User
from core.value_objects.email import Email

class UserRepository(Protocol):
    """Contrato para operaciones relacionadas con User en la capa de aplicación."""

    def add(self, user: User) -> User:
        """Agrega un nuevo usuario al repositorio y devuelve el creado."""
        ...

    def get_by_id(self, user_id: int) -> Optional[User]:
        """Obtiene un usuario por su ID, o None si no existe."""
        ...

    def get_by_email(self, email: Email) -> Optional[User]:
        """Obtiene un usuario por su email, o None si no existe."""
        ...

    def list_all(self) -> list[User]:
        """Devuelve todos los usuarios almacenados."""
        ...
