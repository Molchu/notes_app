import pytest

from application.use_cases.create_note import CreateNote
from core.entities.note import Note
from core.exceptions import DomainError


# ---------- Fakes ----------
class InMemoryNoteRepo:
    def __init__(self):
        self._store = {}
        self._auto = 1

    def add(self, note: Note) -> Note:
        nid = self._auto
        self._auto += 1
        stored = Note(
            id=nid,
            user_id=note.user_id,
            title=note.title,
            content=note.content,
            color=note.color,
        )
        self._store[nid] = stored
        return stored

    def get_by_id(self, nid: int):
        return self._store.get(nid)


# ---------- Tests ----------
def test_create_note_success_default_color():
    repo = InMemoryNoteRepo()
    use_case = CreateNote(note_repo=repo)

    note = use_case.execute(user_id=1, title="Idea", content="Contenido…")

    assert note.id == 1
    assert note.user_id == 1
    assert note.title == "Idea"
    assert note.color  # debe existir color (por defecto "yellow")


def test_create_note_without_title_raises():
    repo = InMemoryNoteRepo()
    use_case = CreateNote(note_repo=repo)

    with pytest.raises(DomainError):
        use_case.execute(user_id=1, title="", content="sin título")
