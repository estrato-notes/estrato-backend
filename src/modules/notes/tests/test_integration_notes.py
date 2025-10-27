import uuid

import pytest
from fastapi.testclient import TestClient

from src.core.constants import QUICK_CAPTURE_NOTEBOOK_NAME


class TestNoteRoutes:
    """Agrupa todos os testes para as rotas do módulo Notas."""

    def test_create_note_for_existing_notebook_returns_201(
        self, client: TestClient, created_notebook: dict, auth_headers: dict
    ):
        """Testa se uma nota é criada com sucesso em um caderno existente"""
        notebook_id = created_notebook["id"]
        note_payload = {"title": "Titulo da Nota"}
        response = client.post(
            f"/notebooks/{notebook_id}/notes/", json=note_payload, headers=auth_headers
        )
        data = response.json()

        assert response.status_code == 201
        assert data["title"] == "Titulo da Nota"
        assert data["notebook_id"] == notebook_id
        assert "id" in data

    def test_create_note_for_nonexisting_notebook_returns_404(
        self, client: TestClient, auth_headers: dict
    ):
        """Testa se a criação de uma nota falha se o caderno não existir"""
        nonexisting_id = uuid.uuid4()
        response = client.post(
            f"/notebooks/{nonexisting_id}/notes/",
            json={"title": "Nota"},
            headers=auth_headers,
        )
        assert response.status_code == 404
        assert "O caderno não foi encontrado" in response.json()["detail"]

    def test_list_notes_from_existing_notebook_returns_200(
        self,
        client: TestClient,
        created_notebook: dict,
        created_note: dict,
        auth_headers: dict,
    ):
        """Testa se a listagem de notas de um caderno funciona"""
        notebook_id = created_notebook["id"]

        response = client.get(f"/notebooks/{notebook_id}/notes/", headers=auth_headers)
        data = response.json()

        assert response.status_code == 200
        assert isinstance(data, list)
        assert len(data) >= 1
        assert created_note["id"] in [note["id"] for note in data]

    def test_get_note_by_id_returns_200(
        self,
        client: TestClient,
        created_notebook: dict,
        created_note: dict,
        auth_headers: dict,
    ):
        """Testa a busca de uma nota específica pelo seu ID."""
        notebook_id = created_notebook["id"]
        note_id = created_note["id"]

        response = client.get(
            f"/notebooks/{notebook_id}/notes/{note_id}", headers=auth_headers
        )
        data = response.json()

        assert response.status_code == 200
        assert data["id"] == note_id

    def test_get_note_from_wrong_notebook_returns_404(
        self, client: TestClient, created_note: dict, auth_headers: dict
    ):
        """Testa se a busca falha ao usar o ID de caderno incorreto na URL."""
        wrong_notebook_id = uuid.uuid4()
        note_id = created_note["id"]

        response = client.get(
            f"/notebooks/{wrong_notebook_id}/notes/{note_id}", headers=auth_headers
        )
        assert response.status_code == 404

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
        auth_headers: dict,
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
            headers=auth_headers,
        )
        note_id = note_response.json()["id"]

        response = client.patch(
            f"/notebooks/{notebook_id}/notes/{note_id}",
            json=update_payload,
            headers=auth_headers,
        )
        data = response.json()

        assert response.status_code == 200
        assert data["title"] == expected_title
        assert data["content"] == expected_content
        assert data["is_favorite"] == expected_favorite

    def test_delete_note_returns_204(
        self,
        client: TestClient,
        created_note: dict,
        created_notebook: dict,
        auth_headers: dict,
    ):
        """Testa a deleção bem-sucedida de uma nota."""
        notebook_id = created_notebook["id"]
        note_id = created_note["id"]

        delete_response = client.delete(
            f"/notebooks/{notebook_id}/notes/{note_id}", headers=auth_headers
        )
        assert delete_response.status_code == 204

        get_response = client.get(
            f"/notebooks/{notebook_id}/notes/{note_id}", headers=auth_headers
        )
        assert get_response.status_code == 404

    def test_add_tag_to_note_returns_201(
        self,
        client: TestClient,
        created_note: dict,
        created_notebook: dict,
        auth_headers: dict,
    ):
        """Testa a associação bem-sucedida de uma tag a uma nota."""
        notebook_id = created_notebook["id"]
        note_id = created_note["id"]

        # Cria uma tag para associar
        tag_response = client.post(
            "/tags/", json={"name": "Tag Associada"}, headers=auth_headers
        )
        assert tag_response.status_code == 201
        tag_id = tag_response.json()["id"]

        # Associa a tag à nota
        response = client.post(
            f"/notebooks/{notebook_id}/notes/{note_id}/tags/{tag_id}",
            headers=auth_headers,
        )
        data = response.json()

        assert response.status_code == 201
        assert data["note_title"] == created_note["title"]
        assert data["tag_name"] == "Tag Associada"

    def test_remove_tag_from_note_returns_204(
        self,
        client: TestClient,
        created_note: dict,
        created_notebook: dict,
        auth_headers: dict,
    ):
        """Testa a remoção bem-sucedida de uma tag de uma nota."""
        notebook_id = created_notebook["id"]
        note_id = created_note["id"]

        # Cria e associa uma tag
        tag_response = client.post(
            "/tags/", json={"name": "Tag para Remover"}, headers=auth_headers
        )
        tag_id = tag_response.json()["id"]
        add_response = client.post(
            f"/notebooks/{notebook_id}/notes/{note_id}/tags/{tag_id}",
            headers=auth_headers,
        )
        assert add_response.status_code == 201

        # Remove a associação
        response = client.delete(
            f"/notebooks/{notebook_id}/notes/{note_id}/tags/{tag_id}",
            headers=auth_headers,
        )
        assert response.status_code == 204

    def test_move_note_to_another_notebook(
        self, client: TestClient, created_note: dict, auth_headers: dict
    ):
        """Testa se uma nota é movida com sucesso para um novo caderno."""
        origin_notebook_id = created_note["notebook_id"]
        note_id = created_note["id"]

        destination_notebook_response = client.post(
            "/notebooks/", json={"name": "Caderno de Destino"}, headers=auth_headers
        )
        assert destination_notebook_response.status_code == 201
        destination_notebook_id = destination_notebook_response.json()["id"]

        assert origin_notebook_id != destination_notebook_id

        update_payload = {"notebook_id": destination_notebook_id}
        response = client.patch(
            f"/notebooks/{origin_notebook_id}/notes/{note_id}",
            json=update_payload,
            headers=auth_headers,
        )

        assert response.status_code == 200
        assert response.json()["notebook_id"] == destination_notebook_id

        get_old_response = client.get(
            f"/notebooks/{origin_notebook_id}/notes/{note_id}", headers=auth_headers
        )
        assert get_old_response.status_code == 404

        get_new_response = client.get(
            f"/notebooks/{destination_notebook_id}/notes/{note_id}",
            headers=auth_headers,
        )
        assert get_new_response.status_code == 200
        assert get_new_response.json()["id"] == note_id

    @pytest.mark.parametrize(
        "content, expected_title",
        [
            ("Nota rápida com título curto.", "Nota rápida com título curto."),
            (
                "Este é um conteúdo muito longo para uma nota de captura rápida e deve ser truncado.",
                "Este é um conteúdo muito longo...",
            ),
        ],
    )
    def test_create_quick_note_returns_201(
        self,
        client: TestClient,
        auth_headers: dict,
        content: str,
        expected_title: str,
    ):
        """Testa a criação de uma nota de captura rápida."""
        quick_note_payload = {"content": content}

        response = client.post(
            "/notes/quick-capture",
            json=quick_note_payload,
            headers=auth_headers,
        )
        data = response.json()

        assert response.status_code == 201
        assert data["content"] == content
        assert data["title"] == expected_title

        quick_capture_notebook_id = data["notebook_id"]
        notebook_response = client.get(
            f"/notebooks/{quick_capture_notebook_id}", headers=auth_headers
        )
        assert notebook_response.status_code == 200
        assert notebook_response.json()["name"] == QUICK_CAPTURE_NOTEBOOK_NAME
