import uuid
from unittest.mock import MagicMock, patch

import pytest
from fastapi import HTTPException

from src.core.constants import QUICK_CAPTURE_NOTEBOOK_NAME
from src.core.models import Note, Notebook
from src.modules.notes.schemas import NoteCreate, NoteUpdate, QuickNoteCreate
from src.modules.notes.service import NoteService

TEST_USER_ID = uuid.uuid4()


@pytest.fixture
def mock_note_repo():
    with patch(
        "src.modules.notes.service.note_repository", new_callable=MagicMock
    ) as mock:
        yield mock


@pytest.fixture
def mock_notebook_service():
    with patch(
        "src.modules.notes.service.notebook_service", new_callable=MagicMock
    ) as mock:
        mock.get_notebook_by_id.return_value = Notebook(
            id=uuid.uuid4(), name="Mocked Notebook", user_id=TEST_USER_ID
        )
        yield mock


class TestUnitNoteService:
    """Agrupa todos os testes unitários para o NoteService."""

    def test_create_note_success(
        self, mock_note_repo: MagicMock, mock_notebook_service: MagicMock
    ):
        notebook_id = uuid.uuid4()
        note_data = NoteCreate(title="Nota de Teste")
        mock_db_session = MagicMock()

        mock_note_repo.create_note.return_value = Note(
            id=uuid.uuid4,
            title=note_data.title,
            notebook_id=notebook_id,
            user_id=TEST_USER_ID,
        )
        result = NoteService.create_note(
            mock_db_session, note_data, notebook_id, TEST_USER_ID
        )

        mock_notebook_service.get_notebook_by_id.assert_called_once_with(
            mock_db_session, notebook_id, TEST_USER_ID
        )
        mock_note_repo.create_note.assert_called_once_with(
            mock_db_session, note_data, notebook_id, TEST_USER_ID
        )

        assert result.title == note_data.title
        assert result.notebook_id == notebook_id

    def test_create_note_for_nonexistent_notebook_raises_404(
        self, mock_note_repo: MagicMock, mock_notebook_service: MagicMock
    ):
        notebook_id = uuid.uuid4()
        note_data = NoteCreate(title="Nota de Teste")
        mock_db_session = MagicMock()

        mock_notebook_service.get_notebook_by_id.side_effect = HTTPException(
            status_code=404, detail="O caderno não foi encontrado"
        )

        with pytest.raises(HTTPException) as exc_info:
            NoteService.create_note(
                mock_db_session, note_data, notebook_id, TEST_USER_ID
            )
        assert exc_info.value.status_code == 404
        mock_note_repo.create_note.assert_not_called()

    def test_get_note_by_id_success(self, mock_note_repo: MagicMock):
        notebook_id = uuid.uuid4()
        note_id = uuid.uuid4()
        mock_db_session = MagicMock()

        mock_note_repo.get_note_by_id.return_value = Note(
            id=note_id,
            title="Nota Encontrada",
            notebook_id=notebook_id,
            user_id=TEST_USER_ID,
        )

        result = NoteService.get_note_by_id(
            mock_db_session, note_id, notebook_id, TEST_USER_ID
        )

        mock_note_repo.get_note_by_id.assert_called_once_with(
            mock_db_session, note_id, notebook_id, TEST_USER_ID
        )
        assert result.id == note_id

    def test_get_note_by_id_not_found_raises_404(self, mock_note_repo: MagicMock):
        notebook_id = uuid.uuid4()
        note_id = uuid.uuid4()
        mock_db_session = MagicMock()

        mock_note_repo.get_note_by_id.return_value = None

        with pytest.raises(HTTPException) as exc_info:
            NoteService.get_note_by_id(
                mock_db_session, note_id, notebook_id, TEST_USER_ID
            )

        assert exc_info.value.status_code == 404
        assert "A nota não foi encontrada" in exc_info.value.detail

    @pytest.mark.parametrize(
        "update_data, expected_title, expected_content",
        [
            (NoteUpdate(title="Titulo Novo"), "Titulo Novo", "Conteudo Antigo"),
            (NoteUpdate(content="Conteudo Novo"), "Titulo Antigo", "Conteudo Novo"),
            (
                NoteUpdate(title="Titulo Final", content="Conteudo Final"),
                "Titulo Final",
                "Conteudo Final",
            ),
        ],
    )
    def test_update_note_data_by_id(
        self,
        mock_note_repo: MagicMock,
        update_data: NoteUpdate,
        expected_title: str,
        expected_content: str,
    ):
        notebook_id = uuid.uuid4()
        note_id = uuid.uuid4()
        mock_db_session = MagicMock()

        note_to_update = Note(
            id=note_id,
            title="Titulo Antigo",
            content="Conteudo Antigo",
            notebook_id=notebook_id,
            user_id=TEST_USER_ID,
        )

        mock_note_repo.get_note_by_id.return_value = note_to_update

        def update_side_effect(db, note, data):
            note.title = data.title if data.title is not None else note.title
            note.content = data.content if data.content is not None else note.content
            return note

        mock_note_repo.update_note.side_effect = update_side_effect
        result = NoteService.update_note_data_by_id(
            mock_db_session, note_id, notebook_id, update_data, TEST_USER_ID
        )
        mock_note_repo.get_note_by_id.assert_called_once_with(
            mock_db_session, note_id, notebook_id, TEST_USER_ID
        )
        mock_note_repo.update_note.assert_called_once_with(
            mock_db_session, note_to_update, update_data
        )
        assert result.title == expected_title
        assert result.content == expected_content

    def test_delete_note_by_id(self, mock_note_repo: MagicMock):
        notebook_id = uuid.uuid4()
        note_id = uuid.uuid4()
        mock_db_session = MagicMock()

        note_to_delete = Note(
            id=note_id,
            title="Nota para Deletar",
            notebook_id=notebook_id,
            user_id=TEST_USER_ID,
        )

        mock_note_repo.get_note_by_id.return_value = note_to_delete

        NoteService.delete_note_by_id(
            mock_db_session, note_id, notebook_id, TEST_USER_ID
        )

        mock_note_repo.get_note_by_id.assert_called_once_with(
            mock_db_session, note_id, notebook_id, TEST_USER_ID
        )

        mock_note_repo.delete_note.assert_called_once_with(
            mock_db_session, note_to_delete
        )

    @pytest.mark.parametrize(
        "content, expected_title",
        [
            ("Conteúdo curto", "Conteúdo curto"),
            (
                "Este conteúdo é deliberadamente muito longo para testar a lógica de truncagem do título.",
                "Este conteúdo é deliberadament...",
            ),
        ],
    )
    def test_create_quick_note(
        self,
        mock_note_repo: MagicMock,
        mock_notebook_service: MagicMock,
        content: str,
        expected_title: str,
    ):
        mock_db_session = MagicMock()
        quick_note_data = QuickNoteCreate(content=content)
        mock_quick_capture_notebook = Notebook(
            id=uuid.uuid4(), name=QUICK_CAPTURE_NOTEBOOK_NAME, user_id=TEST_USER_ID
        )

        mock_notebook_service.get_or_create_quick_capture_notebook.return_value = (
            mock_quick_capture_notebook
        )
        mock_note_repo.create_note.return_value = Note(
            id=uuid.uuid4(),
            title=expected_title,
            content=content,
            notebook_id=mock_quick_capture_notebook.id,
            user_id=TEST_USER_ID,
        )

        result = NoteService.create_quick_note(
            mock_db_session, quick_note_data, TEST_USER_ID
        )

        mock_notebook_service.get_or_create_quick_capture_notebook.assert_called_once_with(
            mock_db_session, TEST_USER_ID
        )

        assert len(mock_note_repo.create_note.call_args_list) == 1
        call_args = mock_note_repo.create_note.call_args[0]
        assert call_args[1].title == expected_title
        assert call_args[1].content == content
        assert call_args[2] == mock_quick_capture_notebook.id
        assert call_args[3] == TEST_USER_ID

        assert result.title == expected_title
        assert result.notebook_id == mock_quick_capture_notebook.id
