from typing import Protocol, Optional
from core.entities.group import Group

class GroupRepository(Protocol):
    """Contrato para operaciones de persistencia de grupos."""

    # CRUD básico
    def add(self, group: Group) -> Group:
        """Crea un nuevo grupo y devuelve la entidad persistida (con ID)."""
        ...

    def get_by_id(self, group_id: int) -> Optional[Group]:
        """Obtiene un grupo por ID, o None si no existe."""
        ...

    def list_by_user(self, user_id: int) -> list[Group]:
        """Lista todos los grupos pertenecientes a un usuario."""
        ...

    def rename(self, group_id: int, new_name: str) -> Group:
        """Cambia el nombre del grupo y devuelve la entidad actualizada."""
        ...

    def delete(self, group_id: int) -> None:
        """Elimina el grupo (y sus relaciones con notas)."""
        ...

    # Relaciones grupo ↔ notas (sin traer ORM aquí)
    def add_note(self, group_id: int, note_id: int) -> None:
        """Asocia una nota existente al grupo."""
        ...

    def remove_note(self, group_id: int, note_id: int) -> None:
        """Desasocia una nota del grupo."""
        ...