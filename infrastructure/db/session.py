from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from config import DevelopmentConfig  # o seleccionar según ENV

_engine = create_engine(
    DevelopmentConfig.SQLALCHEMY_DATABASE_URI,
    echo=DevelopmentConfig.SQL_ECHO,
    future=True,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(bind=_engine, autoflush=False, autocommit=False, future=True)

# Patrón de contexto para transacciones atómicas

@contextmanager
def get_session():
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except:  # noqa: E722 — dejamos que pytest capture excepciones
        session.rollback()
        raise
    finally:
        session.close()
