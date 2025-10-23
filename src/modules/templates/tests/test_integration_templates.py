from fastapi.testclient import TestClient


class TestTemplateRoutes:
    """Agrupa todos os testes de integração para as rotas do módulo Templates."""

    def test_create_template(self, client: TestClient, auth_headers: dict):
        """Testa a criação de um novo template (POST /templates/)."""
        response = client.post(
            "/templates/",
            json={"name": "Template de Teste", "content": "Conteúdo inicial"},
            headers=auth_headers,
        )
        data = response.json()

        assert response.status_code == 201
        assert data["name"] == "Template de Teste"
        assert data["content"] == "Conteúdo inicial"
        assert "id" in data

    def test_create_duplicate_template_fails(
        self, client: TestClient, auth_headers: dict
    ):
        """Testa que a criação de um template com nome duplicado falha (409)."""
        client.post(
            "/templates/", json={"name": "Template Duplicado"}, headers=auth_headers
        )
        response = client.post(
            "/templates/", json={"name": "Template Duplicado"}, headers=auth_headers
        )
        assert response.status_code == 409
        assert "Um template com esse nome já existe" in response.json()["detail"]

    def test_get_all_templates(
        self, client: TestClient, created_template: dict, auth_headers: dict
    ):
        """Testa a listagem de todos os templates (GET /templates/)."""
        response = client.get("/templates/", headers=auth_headers)
        data = response.json()

        assert response.status_code == 200
        assert isinstance(data, list)
        assert len(data) >= 1
        assert created_template["id"] in [t["id"] for t in data]

    def test_get_template_by_id(
        self, client: TestClient, created_template: dict, auth_headers: dict
    ):
        """Testa a busca de um template específico por ID."""
        template_id = created_template["id"]
        response = client.get(f"/templates/{template_id}", headers=auth_headers)
        data = response.json()

        assert response.status_code == 200
        assert data["id"] == template_id
        assert data["name"] == created_template["name"]

    def test_update_template(
        self, client: TestClient, created_template: dict, auth_headers: dict
    ):
        """Testa a atualização de um template."""
        template_id = created_template["id"]
        update_payload = {"name": "Nome Novo", "content": "Conteúdo Novo"}
        response = client.patch(
            f"/templates/{template_id}", json=update_payload, headers=auth_headers
        )
        data = response.json()

        assert response.status_code == 200
        assert data["name"] == "Nome Novo"
        assert data["content"] == "Conteúdo Novo"

    def test_delete_template(
        self, client: TestClient, created_template: dict, auth_headers: dict
    ):
        """Testa a exclusão de um template."""
        template_id = created_template["id"]
        delete_response = client.delete(
            f"/templates/{template_id}", headers=auth_headers
        )
        assert delete_response.status_code == 204

        get_response = client.get(f"/templates/{template_id}", headers=auth_headers)
        assert get_response.status_code == 404
