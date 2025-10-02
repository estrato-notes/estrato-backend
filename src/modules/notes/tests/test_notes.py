import pytest
from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)


@pytest.mark.skip(reason="Implementação dos testes de integração pendentes")
class TestNoteRoutes:
    """Agrupa todos os testes para as rotas do módulo Notas."""

    # Testes pro POST (/notebooks/{notebook_id}/notes/)
    def test_create_note_for_existing_notebook_returns_201(self):
        """Testa se uma nota é criada com sucesso em um caderno existente"""
        pass

    def test_create_note_for_nonexisting_notebook_returns_404(self):
        """Testa se a criação de uma nota falha se o caderno não existir"""
        pass

    # Testes pro GET (/notebooks/{notebook_id}/notes/)
    def test_list_notes_from_existing_notebook_returns_200(self):
        """Testa se a listagem de notas de um caderno funciona"""
        pass

    def test_list_notes_from_nonexisting_notebook_returns_404(self):
        """Testa se a listagem de notas de um caderno que não existe falha"""
        pass

    # Testes pro GET (/notebooks/{notebook_id}/notes/{note_id})
    def test_get_note_by_id_returns_200(self):
        """Testa a busca de uma nota específica pelo seu ID."""
        pass

    def test_get_nonexistent_note_returns_404(self):
        """Testa a busca por uma nota com ID que não existe."""
        pass

    def test_get_note_from_wrong_notebook_returns_404(self):
        """Testa se a busca falha ao usar o ID de caderno incorreto na URL."""
        pass

    # Testes pro PATCH (/notebooks/{notebook_id}/notes/{note_id})
    def test_update_note_returns_200(self):
        """Testa a atualização bem-sucedida de uma nota."""
        pass

    def test_update_nonexistent_note_returns_404(self):
        """Testa se a atualização falha para uma nota que não existe."""
        pass

    def test_update_note_from_wrong_notebook_returns_404(self):
        """Testa se a atualização falha ao usar o ID de caderno incorreto na URL."""
        pass

    # Testes pro DELETE (/notebooks/{notebook_id}/notes/{note_id})
    def test_delete_note_returns_204(self):
        """Testa a deleção bem-sucedida de uma nota."""
        pass

    def test_delete_nonexistent_note_returns_404(self):
        """Testa se a deleção falha para uma nota que não existe."""
        pass

    def test_delete_note_from_wrong_notebook_returns_404(self):
        """Testa se a deleção falha ao usar o ID de caderno incorreto na URL."""
        pass
