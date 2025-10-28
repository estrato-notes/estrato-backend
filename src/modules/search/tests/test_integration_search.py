"""Arquivo com os testes de integração dos endpoints de Search"""

import pytest
from fastapi.testclient import TestClient


class TestSearchRoutes:
    """
    Agrupa todos os testes de integração para as rotas do módulo Search.
    """

    @pytest.fixture(autouse=True)
    def setup_search_data(
        self,
        client: TestClient,
        created_notebook: dict,
        created_note: dict,
        auth_headers: dict,
    ):
        """
        Prepara os dados necessários para os testes de busca,
        garantindo que existam entidades com um termo em comum.
        """
        client.patch(
            f"/notebooks/{created_note['notebook_id']}/notes/{created_note['id']}",
            json={"content": "Conteúdo com o termo BUSCA_UNICA"},
            headers=auth_headers,
        )
        client.post("/tags/", json={"name": "Tag BUSCA_UNICA"}, headers=auth_headers)
        client.post(
            "/templates/", json={"name": "Template BUSCA_UNICA"}, headers=auth_headers
        )
        client.post(
            "/notebooks/", json={"name": "Caderno BUSCA_UNICA"}, headers=auth_headers
        )

    def test_search_finds_all_types_of_items(
        self, client: TestClient, auth_headers: dict
    ):
        """
        Testa se a busca com um termo comum retorna resultados de todas as
        entidades (Note, Notebook, Tag, Template).
        """
        response = client.get("/search/?q=BUSCA_UNICA", headers=auth_headers)
        data = response.json()
        results = data.get("results", [])

        assert response.status_code == 200
        assert len(results) == 4, "Deveria encontrar 4 itens com o termo de busca"

        result_types = {item["type"] for item in results}
        assert "note" in result_types
        assert "notebook" in result_types
        assert "tag" in result_types
        assert "template" in result_types

    def test_search_with_no_results(self, client: TestClient, auth_headers: dict):
        """
        Testa se a busca por um termo inexistente retorna uma lista vazia.
        """
        response = client.get("/search/?q=termo_inexistente_xyz", headers=auth_headers)
        data = response.json()
        assert response.status_code == 200
        assert data["results"] == []

    def test_search_with_empty_query_returns_validation_error(
        self, client: TestClient, auth_headers: dict
    ):
        """
        Testa se a tentativa de buscar com um termo vazio falha com erro 422.
        """
        response = client.get("/search/?q=", headers=auth_headers)
        assert response.status_code == 422
