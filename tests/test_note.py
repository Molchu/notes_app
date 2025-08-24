import pytest
from core.entities.note import Note
from core.value_objects.color_hex import ColorHex
from core.exceptions import DomainValidationError

def test_create_note_valid():
    note = Note(id=1, user_id=1, title="Mi Nota", content="Contenido")
    assert note.title == "Mi Nota"
    assert note.preview() == "Contenido"

def test_change_color():
    note = Note(id=2, user_id=1, title="Nota", content="x")
    note.change_color(ColorHex("#FFAA00"))
    assert str(note.color) == "#FFAA00"

def test_invalid_title():
    with pytest.raises(DomainValidationError):
        Note(id=3, user_id=1, title="", content="contenido")
