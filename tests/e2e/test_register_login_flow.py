import json
import pytest
from app import create_app
from infrastructure.db.models import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

@pytest.fixture(scope="session")
def app():
    class TestConfig:
        TESTING = True
        SQLALCHEMY_DATABASE_URI = "sqlite+pysqlite:///:memory:"
        SQL_ECHO = False
        SECRET_KEY = "test"
    app = create_app(TestConfig)
    # Crea tablas en esta DB temporal
    engine = create_engine(TestConfig.SQLALCHEMY_DATABASE_URI, future=True)
    Base.metadata.create_all(engine)
    yield app

@pytest.fixture
def client(app):
    return app.test_client()

def test_register_and_login(client):
    r = client.post("/users/register", data=json.dumps({
        "username": "nicolas",
        "email": "nico@test.com",
        "password": "1234"
    }), content_type="application/json")
    assert r.status_code == 201
    r2 = client.post("/users/login", data=json.dumps({
        "username_or_email": "nicolas",
        "password": "1234"
    }), content_type="application/json")
    assert r2.status_code == 200
