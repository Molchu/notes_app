from flask import Blueprint, request, jsonify
from infrastructure.db.session import get_session
from infrastructure.db.group_repository_impl import SqlAlchemyGroupRepository
from application.use_cases.group_notes import GroupNotes  # caso de uso tuyo
from core.entities.group import Group

bp = Blueprint("groups", __name__, url_prefix="/groups")

@bp.post("/")
def create_group():
    data = request.get_json()
    with get_session() as s:
        repo = SqlAlchemyGroupRepository(s)
        # dominio: entidad Group
        group = Group(id=None, user_id=data["user_id"], name=data["name"])
        saved = repo.add(group)
        return jsonify({"id": saved.id, "name": saved.name}), 201


@bp.get("/user/<int:user_id>")
def list_groups(user_id: int):
    with get_session() as s:
        repo = SqlAlchemyGroupRepository(s)
        groups = repo.list_by_user(user_id)
        return jsonify([{"id": g.id, "name": g.name} for g in groups])


@bp.put("/<int:group_id>")
def rename_group(group_id: int):
    data = request.get_json()
    with get_session() as s:
        repo = SqlAlchemyGroupRepository(s)
        updated = repo.rename(group_id, data["new_name"])
        if not updated:
            return jsonify({"error": "Group not found"}), 404
        return jsonify({"id": updated.id, "name": updated.name})


@bp.delete("/<int:group_id>")
def delete_group(group_id: int):
    with get_session() as s:
        repo = SqlAlchemyGroupRepository(s)
        repo.delete(group_id)
        return "", 204
