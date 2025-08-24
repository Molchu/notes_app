from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select
from application.interfaces.group_repository import GroupRepository
from core.entities.group import Group
from .models import GroupModel
from .mappers import to_domain_group, to_model_group

class SqlAlchemyGroupRepository(GroupRepository):
    def __init__(self, session: Session):
        self.session = session

    def add(self, group: Group) -> Group:
        m = to_model_group(group)
        self.session.add(m)
        self.session.flush()
        return to_domain_group(m)

    def get_by_id(self, group_id: int) -> Optional[Group]:
        m = self.session.get(GroupModel, group_id)
        return to_domain_group(m) if m else None

    def list_by_user(self, user_id: int) -> List[Group]:
        stmt = select(GroupModel).where(GroupModel.user_id == user_id).order_by(GroupModel.name.asc())
        return [to_domain_group(m) for m in self.session.scalars(stmt).all()]

    def rename(self, group_id: int, new_name: str) -> Optional[Group]:
        m = self.session.get(GroupModel, group_id)
        if not m:
            return None
        m.name = new_name
        self.session.flush()
        return to_domain_group(m)

    def delete(self, group_id: int) -> None:
        m = self.session.get(GroupModel, group_id)
        if m:
            self.session.delete(m)
