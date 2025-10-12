import uuid

import pytest
from fastapi.testclient import TestClient


class TestTagRoutes:
    """Agrupa todos os testes de integração para as rotas do módulo Tags."""

    def test_create_tag(self, client: TestClient):
        """Testa a criação de uma nova tag (POST /tags/)."""
        response = client.post("/tags/", json={"name": "Tag de Teste"})
        data = response.json()

        assert response.status_code == 201
        assert data["name"] == "Tag de Teste"
        assert "id" in data

    @pytest.mark.parametrize(
        "payload, expected_detail_substring",
        [
            ({"name": ""}, "String should have at least 1 character"),
            ({"name": "a" * 21}, "String should have at most 20 characters"),
            ({}, "Field required"),
        ],
    )
    def test_create_tag_with_invalid_data_fails(
        self, client: TestClient, payload: dict, expected_detail_substring: str
    ):
        """Testa que a criação de uma tag com dados inválidos falha (422)."""
        response = client.post("/tags/", json=payload)
        assert response.status_code == 422
        assert expected_detail_substring in str(response.json())

    def test_create_duplicate_tag_fails(self, client: TestClient):
        """Testa que a criação de uma tag com nome duplicado falha (409)."""
        client.post("/tags/", json={"name": "Tag Duplicada"})
        response = client.post("/tags/", json={"name": "Tag Duplicada"})
        assert response.status_code == 409
        assert "Uma tag com esse nome já existe" in response.json()["detail"]

    def test_get_all_tags(self, client: TestClient):
        """Testa a listagem de todas as tags (GET /tags/)."""
        client.post("/tags/", json={"name": "Tag A"})
        client.post("/tags/", json={"name": "Tag B"})

        response = client.get("/tags/")
        data = response.json()

        assert response.status_code == 200
        assert isinstance(data, list)
        assert len(data) >= 2

    def test_get_tag_by_id(self, client: TestClient):
        """Testa a busca de uma tag específica por ID."""
        create_response = client.post("/tags/", json={"name": "Tag para Busca"})
        tag_id = create_response.json()["id"]

        response = client.get(f"/tags/{tag_id}")
        data = response.json()

        assert response.status_code == 200
        assert data["id"] == tag_id
        assert data["name"] == "Tag para Busca"

    def test_get_tag_by_id_not_found_fails(self, client: TestClient):
        """Testa a busca de uma tag com ID inexistente (404)."""
        non_existent_id = uuid.uuid4()
        response = client.get(f"/tags/{non_existent_id}")
        assert response.status_code == 404
        assert "A tag não foi encontrada" in response.json()["detail"]

    def test_update_tag(self, client: TestClient):
        """Testa a atualização do nome de uma tag."""
        create_response = client.post("/tags/", json={"name": "Nome Antigo"})
        tag_id = create_response.json()["id"]

        response = client.patch(f"/tags/{tag_id}", json={"name": "Nome Novo"})
        data = response.json()

        assert response.status_code == 200
        assert data["name"] == "Nome Novo"

    def test_delete_tag(self, client: TestClient):
        """Testa a exclusão de uma tag."""
        create_response = client.post("/tags/", json={"name": "Tag para Deletar"})
        tag_id = create_response.json()["id"]

        delete_response = client.delete(f"/tags/{tag_id}")
        assert delete_response.status_code == 204

        get_response = client.get(f"/tags/{tag_id}")
        assert get_response.status_code == 404
