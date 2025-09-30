import pytest
from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)


@pytest.mark.skip(reason="Testes de integração ainda não foram implementados")
class TestNotebookRoutes:
    def test_create_notebook(self):
        """Testa a criação de um novo notebook (POST /notebooks/)."""
        pass

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
