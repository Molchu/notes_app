from core.exceptions import DomainError
from application.interfaces.group_repository import GroupRepository
from application.interfaces.note_repository import NoteRepository


class GroupNotes:
    def __init__(self, group_repo: GroupRepository, note_repo: NoteRepository):
        self.group_repo = group_repo
        self.note_repo = note_repo

    def execute(self, group_id: int, note_ids: list[int]):
        group = self.group_repo.get_by_id(group_id)
        if not group:
            raise DomainError("Grupo no encontrado")

        notes = [self.note_repo.get_by_id(nid) for nid in note_ids]
        if not all(notes):
            raise DomainError("Alguna nota no existe")

        group.add_notes(notes)
        return self.group_repo.update(group)
