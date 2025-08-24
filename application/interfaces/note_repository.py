from typing import Protocol, Optional
from core.entities.note import Note

class NoteRepository(Protocol):
    def add(self, note: Note) -> Note:
        ...

    def get_by_id(self, note_id: int) -> Optional[Note]:
        ...

    def list_by_user(self, user_id: int) -> list[Note]:
        ...