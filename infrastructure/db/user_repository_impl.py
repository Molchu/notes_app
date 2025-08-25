from typing import Optional
from sqlalchemy.orm import Session
from application.interfaces.user_repository import UserRepository
from core.entities.user import User
from .models import UserModel
from .mappers import to_domain_user, to_model_user

class SqlAlchemyUserRepository(UserRepository):
    def __init__(self, session: Session):
        self.session = session

    def add(self, user: User) -> User:
        model = to_model_user(user)
        self.session.add(model)
        self.session.flush()  # asigna id
        return to_domain_user(model)

    def get_by_id(self, user_id: int) -> Optional[User]:
        m = self.session.get(UserModel, user_id)
        return to_domain_user(m) if m else None

    def get_by_email(self, email: str) -> Optional[User]:
        email_str = str(email)
        m = self.session.query(UserModel).filter_by(email=email_str).one_or_none()
        return to_domain_user(m) if m else None

    def get_by_username(self, username: str) -> Optional[User]:
        m = self.session.query(UserModel).filter_by(username=username).one_or_none()
        return to_domain_user(m) if m else None
