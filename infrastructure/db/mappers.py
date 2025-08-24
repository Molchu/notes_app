from typing import Optional
from core.entities.user import User
from core.entities.note import Note
from core.entities.group import Group
from core.value_objects.email import Email
from core.value_objects.color_hex import ColorHex  # tu VO
from .models import UserModel, NoteModel, GroupModel

# ---------- User ----------
def to_domain_user(m: UserModel) -> User:
    return User(
        id=m.id,
        username=m.username,
        email=Email(m.email),
        password_hash=m.password_hash,
    )

def to_model_user(e: User) -> UserModel:
    return UserModel(
        id=e.id,
        username=e.username,
        email=str(e.email),
        password_hash=e.password_hash,
    )

# ---------- Group ----------
def to_domain_group(m: GroupModel) -> Group:
    return Group(id=m.id, user_id=m.user_id, name=m.name)

def to_model_group(e: Group) -> GroupModel:
    return GroupModel(id=e.id, user_id=e.user_id, name=e.name)

# ---------- Note ----------
def to_domain_note(m: NoteModel) -> Note:
    color: Optional[ColorHex] = ColorHex(m.color_hex) if m.color_hex else None
    return Note(
        id=m.id,
        user_id=m.user_id,
        title=m.title,
        content=m.content,
        group_id=m.group_id,
        color=color,
        created_at=m.created_at,
        updated_at=m.updated_at,
    )

def to_model_note(e: Note) -> NoteModel:
    return NoteModel(
        id=e.id,
        user_id=e.user_id,
        title=e.title,
        content=e.content,
        group_id=e.group_id,
        color_hex=str(e.color) if e.color else None,
        created_at=e.created_at,
        updated_at=e.updated_at,
    )
