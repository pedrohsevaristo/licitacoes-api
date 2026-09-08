from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import settings
from app.core.database import Base, get_db
from app.models.licitacao import Licitacao
from main import app


if settings.test_database_url is None:
    raise RuntimeError(
        "TEST_DATABASE_URL não está configurada no arquivo .env"
    )

if settings.test_database_url == settings.database_url:
    raise RuntimeError(
        "O banco de testes não pode ser o mesmo banco de desenvolvimento"
    )


test_engine = create_engine(
    settings.test_database_url
)


TestingSessionLocal = sessionmaker(
    bind=test_engine,
    autoflush=False,
    autocommit=False,
)


@pytest.fixture()
def db_session() -> Generator[Session, None, None]:
    Base.metadata.create_all(bind=test_engine)

    session = TestingSessionLocal()

    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=test_engine)


@pytest.fixture()
def client(
    db_session: Session,
) -> Generator[TestClient, None, None]:

    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()