import pytest
from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)


@pytest.mark.skip(reason="Testes de integração ainda não foram implementados")
class TestFolderRoutes:
    def test_create_folder(self):
        """Testa a criação de uma nova pasta (POST /folders/)."""
        pass

    def test_get_all_folders(self):
        """Testa a listagem de todas as pastas (GET /folders/)."""
        pass

    def test_get_folder_by_id(self):
        """Testa a busca de uma pasta específica por ID (GET /folders/{id})."""
        pass

    def test_update_folder(self):
        """Testa a atualização parcial de uma pasta (PATCH /folders/{id})."""
        pass

    def test_delete_folder(self):
        """Testa a exclusão de uma pasta (DELETE /folders/{id})."""
        pass

    def test_create_duplicate_folder_fails(self):
        """Testa que a criação de uma pasta com nome duplicado falha (POST /folders/)."""
        pass
