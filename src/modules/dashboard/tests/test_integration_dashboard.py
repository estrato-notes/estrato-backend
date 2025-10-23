from fastapi.testclient import TestClient


class TestDashboardRoutes:
    """
    Agrupa todos os testes de integração para as rotas do módulo Dashboard.
    """

    def test_get_dashboard_data_returns_200(
        self,
        client: TestClient,
        created_note: dict,
        created_notebook: dict,
        auth_headers: dict,
    ):
        """
        Testa a rota GET /dashboard/ e verifica a estrutura da resposta.
        """
        # --- Cenário ---
        # 1. Marcar o caderno e a nota criados como favoritos
        client.patch(
            f"/notebooks/{created_notebook['id']}",
            json={"is_favorite": True},
            headers=auth_headers,
        )
        client.patch(
            f"/notebooks/{created_note['notebook_id']}/notes/{created_note['id']}",
            json={"is_favorite": True},
            headers=auth_headers,
        )

        # 2. Criar uma tag e associá-la à nota para testar as tags populares
        tag_response = client.post(
            "/tags/", json={"name": "Tag Popular"}, headers=auth_headers
        )
        tag_id = tag_response.json()["id"]
        client.post(
            f"/notebooks/{created_note['notebook_id']}/notes/{created_note['id']}/tags/{tag_id}",
            headers=auth_headers,
        )

        # 3. Criar um template para testar os templates recentes
        template_response = client.post(
            "/templates/",
            json={"name": "Template Recente", "content": "Conteúdo"},
            headers=auth_headers,
        )
        template_id = template_response.json()["id"]

        # --- Ação ---
        response = client.get("/dashboard/", headers=auth_headers)
        data = response.json()

        # --- Verificação ---
        assert response.status_code == 200
        assert "recent_notes" in data
        assert "popular_tags" in data
        assert "favorite_notes" in data
        assert "favorite_notebooks" in data
        assert "recent_templates" in data

        assert len(data["recent_notes"]) > 0
        assert data["recent_notes"][0]["id"] == created_note["id"]

        assert len(data["favorite_notes"]) > 0
        assert data["favorite_notes"][0]["id"] == created_note["id"]

        assert len(data["favorite_notebooks"]) > 0
        assert data["favorite_notebooks"][0]["id"] == created_notebook["id"]

        assert len(data["popular_tags"]) > 0
        assert data["popular_tags"][0]["name"] == "Tag Popular"
        assert data["popular_tags"][0]["note_count"] == 1

        assert len(data["recent_templates"]) > 0
        assert data["recent_templates"][0]["id"] == template_id
