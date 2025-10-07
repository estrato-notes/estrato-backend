from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)


class TestNotebookRoutes:
    """Agrupa todos os testes de integração para as rotas do módulo Cadernos."""

    def test_create_notebook(self, client: TestClient):
        """Testa a criação de um novo notebook (POST /notebooks/)."""
        response = client.post("/notebooks/", json={"name": "Caderno de Testes"})
        data = response.json
        assert response.status_code == 201
        assert data["name"] == "Caderno de Testes"
        assert "id" in data

    def test_get_all_notebooks(self):
        """Testa a listagem de todos os notebooks (GET /notebooks/)."""
        pass

    def test_get_notebook_by_id(self):
        """Testa a busca de um notebook específico por ID (GET /notebooks/{id})."""
        pass

    def test_update_notebook(self):
        """Testa a atualização parcial de um notebook (PATCH /notebooks/{id})."""
        pass

    def test_delete_notebook(self):
        """Testa a exclusão de um notebook (DELETE /notebooks/{id})."""
        pass

    def test_create_duplicate_notebook_fails(self):
        """Testa que a criação de um notebook com nome duplicado falha (POST /notebooks/)."""
        pass
