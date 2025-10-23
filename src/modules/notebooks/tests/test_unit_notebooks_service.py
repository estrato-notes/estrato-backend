import uuid
from unittest.mock import MagicMock, patch

import pytest
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

from src.core.models import Notebook
from src.modules.notebooks.schemas import NotebookCreate, NotebookUpdate
from src.modules.notebooks.service import NotebookService

TEST_USER_ID = uuid.uuid4()


@pytest.fixture
def mock_notebook_repo():
    with patch(
        "src.modules.notebooks.service.notebook_repository", new_callable=MagicMock
    ) as mock:
        yield mock


class TestUnitNotebookService:
    """Agrupa os testes unitários do NotebookService"""

    def test_create_notebook_success(self, mock_notebook_repo: MagicMock):
        notebook_data = NotebookCreate(name="Caderno A")
        mock_db_session = MagicMock()

        mock_notebook_repo.create_notebook.return_value = Notebook(
            id=uuid.uuid4(), name=notebook_data.name, user_id=TEST_USER_ID
        )

        result = NotebookService.create_notebook(
            mock_db_session, notebook_data, TEST_USER_ID
        )

        mock_notebook_repo.create_notebook.assert_called_once_with(
            mock_db_session, notebook_data, TEST_USER_ID
        )
        assert result.name == notebook_data.name
        assert result.user_id == TEST_USER_ID

    def test_create_notebook_duplicate_raises_409(self, mock_notebook_repo: MagicMock):
        notebook_data = NotebookCreate(name="Caderno Duplicado")
        mock_db_session = MagicMock()
        mock_db_session.rollback = MagicMock()

        mock_notebook_repo.create_notebook.side_effect = IntegrityError(
            "mocked error", params=None, orig=None
        )

        with pytest.raises(HTTPException) as exc_info:
            NotebookService.create_notebook(
                mock_db_session, notebook_data, TEST_USER_ID
            )

        assert exc_info.value.status_code == 409
        assert "Um caderno com esse nome já existe" in exc_info.value.detail
        mock_db_session.rollback.assert_called_once()

    def test_get_notebook_by_id_success(self, mock_notebook_repo: MagicMock):
        notebook_id = uuid.uuid4()
        mock_db_session = MagicMock()
        mock_notebook_repo.get_notebook_by_id.return_value = Notebook(
            id=notebook_id, name="Caderno Encontrado", user_id=TEST_USER_ID
        )
        result = NotebookService.get_notebook_by_id(
            mock_db_session, notebook_id, TEST_USER_ID
        )

        mock_notebook_repo.get_notebook_by_id.assert_called_once_with(
            mock_db_session, notebook_id, TEST_USER_ID
        )
        assert result.id == notebook_id

    def test_get_notebook_by_id_not_found_raises_404(
        self, mock_notebook_repo: MagicMock
    ):
        notebook_id = uuid.uuid4()
        mock_db_session = MagicMock()
        mock_notebook_repo.get_notebook_by_id.return_value = None
        with pytest.raises(HTTPException) as exc_info:
            NotebookService.get_notebook_by_id(
                mock_db_session, notebook_id, TEST_USER_ID
            )

        assert exc_info.value.status_code == 404
        assert "O caderno não foi encontrado" in exc_info.value.detail

    @pytest.mark.parametrize(
        "update_data, initial_name, expected_name, expected_favorite",
        [
            (NotebookUpdate(name="Nome Novo"), "Nome Antigo", "Nome Novo", False),
            (NotebookUpdate(is_favorite=True), "Nome Antigo", "Nome Antigo", True),
        ],
    )
    def test_udpate_notebook_data_by_id(
        self,
        mock_notebook_repo: MagicMock,
        update_data: NotebookUpdate,
        initial_name: str,
        expected_name: str,
        expected_favorite: bool,
    ):
        notebook_id = uuid.uuid4()
        mock_db_session = MagicMock()
        notebook_to_update = Notebook(
            id=notebook_id, name=initial_name, is_favorite=False, user_id=TEST_USER_ID
        )
        mock_notebook_repo.get_notebook_by_id.return_value = notebook_to_update

        def update_side_effect(db, notebook, data):
            notebook.name = data.name if data.name is not None else notebook.name
            notebook.is_favorite = (
                data.is_favorite
                if data.is_favorite is not None
                else notebook.is_favorite
            )
            return notebook

        mock_notebook_repo.update_notebook.side_effect = update_side_effect
        result = NotebookService.update_notebook_data_by_id(
            mock_db_session, notebook_id, update_data, TEST_USER_ID
        )
        assert result.name == expected_name
        assert result.is_favorite == expected_favorite

    def test_delete_notebook_by_id(self, mock_notebook_repo: MagicMock):
        notebook_id = uuid.uuid4()
        mock_db_session = MagicMock()
        notebook_to_delete = Notebook(
            id=notebook_id, name="Para Deletar", user_id=TEST_USER_ID
        )

        mock_notebook_repo.get_notebook_by_id.return_value = notebook_to_delete
        NotebookService.delete_notebook_by_id(
            mock_db_session, notebook_id, TEST_USER_ID
        )

        mock_notebook_repo.get_notebook_by_id.assert_called_once_with(
            mock_db_session, notebook_id, TEST_USER_ID
        )
        mock_notebook_repo.delete_notebook.assert_called_once_with(
            mock_db_session, notebook_to_delete
        )
