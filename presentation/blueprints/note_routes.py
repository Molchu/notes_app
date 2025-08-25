from flask import Blueprint, request, jsonify, render_template
from infrastructure.db.session import get_session
from infrastructure.db.note_repository_impl import SqlAlchemyNoteRepository
from application.use_cases.create_note import CreateNote

bp = Blueprint("notes", __name__, url_prefix="/notes")

@bp.get("/list")
def list_notes_html():
    user_id = 1  # TODO: reemplazar por el usuario logueado
    with get_session() as s:
        repo = SqlAlchemyNoteRepository(s)
        notes = repo.list_by_user(user_id=user_id)
    # Jinja buscará templates/note/list.html
    return render_template("note/list.html", notes=notes)

@bp.post("/create")
def create_note():
    data = request.get_json()
    with get_session() as s:
        repo = SqlAlchemyNoteRepository(s)
        uc = CreateNote(note_repo=repo)
        note = uc.execute(
            user_id=data["user_id"],
            title=data["title"],
            content=data["content"],
            group_id=data.get("group_id"),
            color=data.get("color")  # "#RRGGBB" o None
        )
        return jsonify({"id": note.id, "title": note.title}), 201

@bp.get("/user/<int:user_id>")
def list_user_notes(user_id: int):
    from sqlalchemy import select
    from infrastructure.db.models import NoteModel
    with get_session() as s:
        rows = s.execute(select(NoteModel).where(NoteModel.user_id == user_id)).scalars().all()
        return jsonify([{"id": n.id, "title": n.title, "color": n.color_hex} for n in rows])
