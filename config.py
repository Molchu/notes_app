import os

class BaseConfig:
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg://notes_user:notes_pass@localhost:5432/notes_db"
    )
    SQL_ECHO = os.getenv("SQL_ECHO", "false").lower() == "true"
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")

class DevelopmentConfig(BaseConfig):
    SQL_ECHO = True

class TestingConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = "sqlite+pysqlite:///:memory:"
    SQL_ECHO = False

class ProductionConfig(BaseConfig):
    DEBUG = False
