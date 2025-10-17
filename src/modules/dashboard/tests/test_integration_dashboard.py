from fastapi.testclient import TestClient


class TestDashboardRoutes:
    """
    Agrupa todos os testes de integração para as rotas do módulo Dashboard.
    """

    def test_get_dashboard_data_returns_200(
        self, client: TestClient, created_note: dict, created_notebook: dict
    ):
        """
        Testa a rota GET /dashboard/ e verifica a estrutura da resposta.
        """
        # --- Cenário ---
        # 1. Marcar o caderno e a nota criados como favoritos
        client.patch(f"/notebooks/{created_notebook['id']}", json={"is_favorite": True})
        client.patch(
            f"/notebooks/{created_note['notebook_id']}/notes/{created_note['id']}",
            json={"is_favorite": True},
        )

        # 2. Criar uma tag e associá-la à nota para testar as tags populares
        tag_response = client.post("/tags/", json={"name": "Tag Popular"})
        tag_id = tag_response.json()["id"]
        client.post(
            f"/notebooks/{created_note['notebook_id']}/notes/{created_note['id']}/tags/{tag_id}"
        )

        # 3. Criar um template para testar os templates recentes
        template_response = client.post(
            "/templates/", json={"name": "Template Recente", "content": "Conteúdo"}
        )
        template_id = template_response.json()["id"]

        # --- Ação ---
        response = client.get("/dashboard/")
        data = response.json()

        # --- Verificação ---
        assert response.status_code == 200

        # Verifica a estrutura principal da resposta
        assert "recent_notes" in data
        assert "popular_tags" in data
        assert "favorite_notes" in data
        assert "favorite_notebooks" in data
        assert "recent_templates" in data  # <-- Nova verificação

        # Verifica se as listas não estão vazias e contêm os itens corretos
        assert len(data["recent_notes"]) > 0
        assert data["recent_notes"][0]["id"] == created_note["id"]

        assert len(data["favorite_notes"]) > 0
        assert data["favorite_notes"][0]["id"] == created_note["id"]

        assert len(data["favorite_notebooks"]) > 0
        assert data["favorite_notebooks"][0]["id"] == created_notebook["id"]

        assert len(data["popular_tags"]) > 0
        assert data["popular_tags"][0]["name"] == "Tag Popular"
        assert data["popular_tags"][0]["note_count"] == 1

        # Verifica o conteúdo dos templates recentes
        assert len(data["recent_templates"]) > 0
        assert data["recent_templates"][0]["id"] == template_id
        assert data["recent_templates"][0]["name"] == "Template Recente"
