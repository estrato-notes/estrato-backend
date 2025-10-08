import pytest  # noqa
import uuid
from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)


class TestNoteRoutes:
    """Agrupa todos os testes para as rotas do módulo Notas."""

    @pytest.fixture
    def created_note(self, client: TestClient, created_notebook: dict) -> dict:
        notebook_id = created_notebook["id"]
        note_payload = {"title": "Titulo da nota inicial"}
        response = client.post(f"/notebooks/{notebook_id}/notes/", json=note_payload)
        assert response.status_code == 201
        return response.json()

    # Testes pro POST (/notebooks/{notebook_id}/notes/)
    def test_create_note_for_existing_notebook_returns_201(
        self, client: TestClient, created_notebook: dict
    ):
        """Testa se uma nota é criada com sucesso em um caderno existente"""
        notebook_id = created_notebook["id"]
        note_payload = {"title": "Titulo da Nota"}
        response = client.post(f"/notebooks/{notebook_id}/notes/", json=note_payload)
        data = response.json()

        assert response.status_code == 201
        assert data["title"] == "Titulo da Nota"
        assert data["notebook_id"] == notebook_id
        assert "id" in data

    def test_create_note_for_nonexisting_notebook_returns_404(self, client: TestClient):
        """Testa se a criação de uma nota falha se o caderno não existir"""
        nonexisting_id = uuid.uuid4()
        response = client.post(
            f"/notebooks/{nonexisting_id}/notes/", json={"title": "Nota"}
        )
        assert response.status_code == 404
        assert "O caderno não foi encontrado" in response.json()["detail"]

    # Testes pro GET (/notebooks/{notebook_id}/notes/)
    def test_list_notes_from_existing_notebook_returns_200(
        self, client: TestClient, created_notebook: dict, created_note: dict
    ):
        """Testa se a listagem de notas de um caderno funciona"""
        notebook_id = created_notebook["id"]

        response = client.get(f"/notebooks/{notebook_id}/notes/")
        data = response.json()

        assert response.status_code == 200
        assert isinstance(data, list)
        assert len(data) >= 1
        assert created_note["id"] in [note["id"] for note in data]

    # Testes pro GET (/notebooks/{notebook_id}/notes/{note_id})
    def test_get_note_by_id_returns_200(
        self, client: TestClient, created_notebook: dict, created_note: dict
    ):
        """Testa a busca de uma nota específica pelo seu ID."""
        notebook_id = created_notebook["id"]
        note_id = created_note["id"]

        response = client.get(f"/notebooks/{notebook_id}/notes/{note_id}")
        data = response.json()

        assert response.status_code == 200
        assert data["id"] == note_id

    def test_get_note_from_wrong_notebook_returns_404(
        self, client: TestClient, created_note: dict
    ):
        """Testa se a busca falha ao usar o ID de caderno incorreto na URL."""
        wrong_notebook_id = uuid.uuid4()
        note_id = created_note["id"]

        response = client.get(f"/notebooks/{wrong_notebook_id}/notes/{note_id}")
        assert response.status_code == 404

    # Testes pro PATCH (/notebooks/{notebook_id}/notes/{note_id})
    @pytest.mark.parametrize(
        "update_payload, expected_title, expected_content, expected_favorite",
        [
            ({"title": "Titulo Atualizado"}, "Titulo Atualizado", None, False),
            (
                {"content": "Conteudo Adicionado"},
                "Nota Inicial para Update",
                "Conteudo Adicionado",
                False,
            ),
            ({"is_favorite": True}, "Nota Inicial para Update", None, True),
            (
                {"title": "Final", "content": "Completo", "is_favorite": True},
                "Final",
                "Completo",
                True,
            ),
        ],
    )
    def test_update_note_returns_200(
        self,
        client: TestClient,
        created_notebook: dict,
        update_payload: dict,
        expected_title: str,
        expected_content: str,
        expected_favorite: bool,
    ):
        """Testa a atualização bem-sucedida de uma nota."""
        notebook_id = created_notebook["id"]
        note_response = client.post(
            f"/notebooks/{notebook_id}/notes",
            json={"title": "Nota Inicial para Update"},
        )
        note_id = note_response.json()["id"]

        response = client.patch(
            f"/notebooks/{notebook_id}/notes/{note_id}", json=update_payload
        )
        data = response.json()

        assert response.status_code == 200
        assert data["title"] == expected_title
        assert data["content"] == expected_content
        assert data["is_favorite"] == expected_favorite

    # Testes pro DELETE (/notebooks/{notebook_id}/notes/{note_id})
    def test_delete_note_returns_204(
        self, client: TestClient, created_note: dict, created_notebook: dict
    ):
        """Testa a deleção bem-sucedida de uma nota."""
        notebook_id = created_notebook["id"]
        note_id = created_note["id"]

        delete_response = client.delete(f"/notebooks/{notebook_id}/notes/{note_id}")
        assert delete_response.status_code == 204

        get_response = client.get(f"/notebooks/{notebook_id}/notes/{note_id}")
        assert get_response.status_code == 404
