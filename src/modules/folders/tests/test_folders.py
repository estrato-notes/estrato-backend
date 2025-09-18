import pytest
from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)


@pytest.mark.skip(reason="Testes de integração ainda não foram implementados")
class TestFolderRoutes:
    def test_create_folder(self):
        pass

    def test_get_all_folders(self):
        pass

    def test_get_folder_by_id(self):
        pass

    def test_update_folder(self):
        pass

    def test_delete_folder(self):
        pass

    def test_create_duplicate_folder_fails(self):
        pass
