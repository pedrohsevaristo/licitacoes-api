from collections.abc import Generator
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine, make_url
from sqlalchemy.orm import Session
from sqlalchemy.schema import CreateSchema, DropSchema

from app.core.config import settings
from app.core.database import Base, get_db
from app.models.licitacao import Licitacao
from main import app


if settings.test_database_url is None:
    raise RuntimeError(
        "TEST_DATABASE_URL não está configurada no arquivo .env"
    )

test_database_url = make_url(settings.test_database_url)
if (
    test_database_url.get_backend_name() != "postgresql"
    or not test_database_url.database
):
    raise RuntimeError("Informe um banco PostgreSQL explícito em TEST_DATABASE_URL")

if test_database_url.database == make_url(settings.database_url).database:
    raise RuntimeError(
        "O banco de testes precisa ter um nome diferente do banco de desenvolvimento"
    )


@pytest.fixture(scope="session")
def test_engine() -> Generator[Engine, None, None]:
    schema = f"licitacoes_test_{uuid4().hex}"
    engine = create_engine(
        test_database_url,
        execution_options={"schema_translate_map": {None: schema}},
    )

    try:
        with engine.begin() as connection:
            connection.execute(CreateSchema(schema))

        try:
            yield engine
        finally:
            with engine.begin() as connection:
                connection.execute(DropSchema(schema))
    finally:
        engine.dispose()


@pytest.fixture()
def db_session(test_engine: Engine) -> Generator[Session, None, None]:
    Base.metadata.create_all(bind=test_engine)

    session = Session(bind=test_engine, autoflush=False)

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