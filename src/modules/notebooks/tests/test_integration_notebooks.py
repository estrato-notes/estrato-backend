import uuid

import pytest
from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)


class TestNotebookRoutes:
    """Agrupa todos os testes de integração para as rotas do módulo Cadernos."""

    def test_create_notebook(self, client: TestClient):
        """Testa a criação de um novo notebook (POST /notebooks/)."""
        response = client.post("/notebooks/", json={"name": "Caderno de Testes"})
        data = response.json()

        assert response.status_code == 201
        assert data["name"] == "Caderno de Testes"
        assert "id" in data

    @pytest.mark.parametrize(
        "payload, expected_detail_substring",
        [
            ({"name": "a"}, "String should have at least 3 characters"),
            ({"name": "a" * 101}, "String should have at most 100 characters"),
            ({}, "Field required"),
            ({"is_favorite": True}, "Field required"),
        ],
    )
    def test_create_notebook_with_invalid_data_fails(
        self, client: TestClient, payload: dict, expected_detail_substring: str
    ):
        """Testa que a criação de um notebook com dados errados falha (POST /notebooks/)."""
        response = client.post("/notebooks/", json=payload)
        assert response.status_code == 422
        assert expected_detail_substring in str(response.json())

    def test_create_duplicate_notebook_fails(self, client: TestClient):
        """Testa que a criação de um notebook com nome duplicado falha (POST /notebooks/)."""
        client.post("/notebooks/", json={"name": "Caderno Duplicado"})
        response = client.post("/notebooks/", json={"name": "Caderno Duplicado"})
        assert response.status_code == 409
        assert "Um caderno com esse nome já existe" in response.json()["detail"]

    def test_get_all_notebooks(self, client: TestClient):
        """Testa a listagem de todos os notebooks (GET /notebooks/)."""
        client.post("/notebooks/", json={"name": "Caderno A"})
        client.post("/notebooks/", json={"name": "Caderno B"})

        response = client.get("/notebooks/")
        data = response.json()

        assert response.status_code == 200
        assert isinstance(data, list)
        assert len(data) >= 2
        assert "Caderno A" in [item["name"] for item in data]

    def test_get_notebook_by_id(self, client: TestClient):
        """Testa a busca de um notebook específico por ID (GET /notebooks/{id})."""
        create_response = client.post("/notebooks/", json={"name": "Caderno A"})
        notebook_id = create_response.json()["id"]
        response = client.get(f"/notebooks/{notebook_id}")
        data = response.json()
        assert response.status_code == 200
        assert data["id"] == notebook_id
        assert data["name"] == "Caderno A"

    def test_get_notebook_by_id_fails(self, client: TestClient):
        """Testa a busca de um notebook específico por ID inexistente (GET /notebooks/{id})."""
        nonexisting_id = uuid.uuid4()
        response = client.get(f"/notebooks/{nonexisting_id}")
        assert response.status_code == 404
        assert "O caderno não foi encontrado" in response.json()["detail"]

    @pytest.mark.parametrize(
        "update_payload, expected_name, expected_favorite",
        [
            ({"name": "Apenas Nome Atualizado"}, "Apenas Nome Atualizado", False),
            ({"is_favorite": True}, "Caderno Original para Update", True),
            (
                {"name": "Ambos Atualizados", "is_favorite": True},
                "Ambos Atualizados",
                True,
            ),
        ],
    )
    def test_update_notebook(
        self,
        client: TestClient,
        update_payload: dict,
        expected_name: str,
        expected_favorite: bool,
    ):
        """Testa a atualização parcial de um notebook (PATCH /notebooks/{id})."""
        create_response = client.post(
            "/notebooks/", json={"name": "Caderno Original para Update"}
        )
        notebook_id = create_response.json()["id"]
        response = client.patch(f"/notebooks/{notebook_id}", json=update_payload)
        data = response.json()
        assert response.status_code == 200
        assert data["name"] == expected_name
        assert data["is_favorite"] == expected_favorite

    def test_delete_notebook(self, client: TestClient):
        """Testa a exclusão de um notebook (DELETE /notebooks/{id})."""
        create_response = client.post("/notebooks/", json={"name": "Caderno Original"})
        notebook_id = create_response.json()["id"]
        response = client.delete(f"/notebooks/{notebook_id}")
        assert response.status_code == 204
        get_response = client.get(f"/notebooks/{notebook_id}")
        assert get_response.status_code == 404
