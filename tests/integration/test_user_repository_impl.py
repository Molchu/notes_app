import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from infrastructure.db.models import Base
from infrastructure.db.user_repository_impl import SqlAlchemyUserRepository
from core.entities.user import User
from core.value_objects.email import Email

@pytest.fixture()
def session():
    engine = create_engine("sqlite+pysqlite:///:memory:", future=True)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine, future=True)
    with Session() as s:
        yield s

def test_add_and_get_user(session):
    repo = SqlAlchemyUserRepository(session)
    user = User(id=None, username="nicolas", email=Email("nico@test.com"), password_hash="hash:1234")
    saved = repo.add(user)
    assert saved.id is not None

    fetched = repo.get_by_id(saved.id)
    assert fetched.email.value == "nico@test.com"
