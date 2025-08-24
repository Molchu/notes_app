from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select
from application.interfaces.note_repository import NoteRepository
from core.entities.note import Note
from .models import NoteModel
from .mappers import to_domain_note, to_model_note

class SqlAlchemyNoteRepository(NoteRepository):
    def __init__(self, session: Session):
        self.session = session

    def add(self, note: Note) -> Note:
        m = to_model_note(note)
        self.session.add(m)
        self.session.flush()
        return to_domain_note(m)

    def get_by_id(self, note_id: int) -> Optional[Note]:
        m = self.session.get(NoteModel, note_id)
        return to_domain_note(m) if m else None

    def list_by_user(self, user_id: int) -> List[Note]:
        stmt = select(NoteModel).where(NoteModel.user_id == user_id).order_by(NoteModel.created_at.desc())
        return [to_domain_note(m) for m in self.session.scalars(stmt).all()]

    def update(self, note: Note) -> Note:
        # asumimos que viene del dominio ya validado
        m = self.session.get(NoteModel, note.id)
        if not m:
            return None  # o lanza excepción de aplicación
        m.title = note.title
        m.content = note.content
        m.group_id = note.group_id
        m.color_hex = str(note.color) if note.color else None
        # updated_at se auto-actualiza
        self.session.flush()
        return to_domain_note(m)

    def delete(self, note_id: int) -> None:
        m = self.session.get(NoteModel, note_id)
        if m:
            self.session.delete(m)
