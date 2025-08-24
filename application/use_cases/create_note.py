from core.entities.note import Note
from core.exceptions import DomainError
from application.interfaces.note_repository import NoteRepository


class CreateNote:
    def __init__(self, note_repo: NoteRepository):
        self.note_repo = note_repo

    def execute(self, user_id: int, title: str, content: str, color: str = "yellow") -> Note:
        if not title:
            raise DomainError("La nota debe tener título")

        note = Note(id=None, user_id=user_id, title=title, content=content, color=color)
        return self.note_repo.add(note)
