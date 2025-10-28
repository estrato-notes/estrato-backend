"""Arquivo de configuração global dos testes com as fixtures"""

import time
import uuid

import alembic.command
import alembic.config
import pytest
from fastapi.testclient import TestClient
from jose import jwt
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.core.config import settings
from src.core.database import get_db
from src.main import app

TEST_DATABASE_URL = settings.DATABASE_URL
engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

TEST_USER_ID = uuid.uuid4()


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """Cria e limpa as tabelas do banco de testes para cada sessão"""
    alembic_cfg = alembic.config.Config("alembic.ini")

    alembic.command.upgrade(alembic_cfg, "head")
    yield
    alembic.command.downgrade(alembic_cfg, "base")


@pytest.fixture
def db_session():
    """Fornece uma sessão limpa do banco para cada teste"""
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    if transaction.is_active:
        transaction.rollback()
    session.close()
    connection.close()


@pytest.fixture
def client(db_session):
    """Fornece um TestClient com a dependência do Banco sobrescrita"""

    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    del app.dependency_overrides[get_db]


def create_test_access_token(user_id: uuid.UUID) -> str:
    """Cria um token de teste válido para o user_id fornecido"""
    expire = int(time.time()) + (settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60)
    to_encode = {"sub": str(user_id), "exp": expire}
    return jwt.encode(to_encode, settings.SECRET_KEY, settings.ALGORITHM)


@pytest.fixture
def auth_headers() -> dict[str, str]:
    """Fixture que retorna headers de autenticação para o TEST_USER_ID"""
    token = create_test_access_token(TEST_USER_ID)
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def created_notebook(client: TestClient, auth_headers: dict) -> dict:
    """
    Fixture que cria um notebook via API e retorna os dados do notebook criado.
    """
    response = client.post(
        "/notebooks/", json={"name": "Caderno Teste para Notas"}, headers=auth_headers
    )
    assert response.status_code == 201
    return response.json()


@pytest.fixture
def created_note(
    client: TestClient, created_notebook: dict, auth_headers: dict
) -> dict:
    """
    Fixture que cria uma nota via API e retorna os dados da nota criado.
    """
    notebook_id = created_notebook["id"]
    note_payload = {"title": "Titulo da nota inicial"}
    response = client.post(
        f"/notebooks/{notebook_id}/notes/", json=note_payload, headers=auth_headers
    )
    assert response.status_code == 201
    return response.json()


@pytest.fixture
def created_template(client: TestClient, auth_headers: dict) -> dict:
    """
    Fixture que cria um template via API e retorna os dados do template criado.
    """
    template_payload = {
        "name": "Template de Teste",
        "content": "Conteúdo do template de teste.",
    }
    response = client.post("/templates/", json=template_payload, headers=auth_headers)
    assert response.status_code == 201
    return response.json()
