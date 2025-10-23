import uuid
from unittest.mock import MagicMock, patch

import pytest
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

from src.core.models import Tag
from src.modules.tags.schemas import TagCreate, TagUpdate
from src.modules.tags.service import TagService

TEST_USER_ID = uuid.uuid4()


@pytest.fixture
def mock_tag_repo():
    with patch(
        "src.modules.tags.service.tag_repository", new_callable=MagicMock
    ) as mock:
        yield mock


class TestUnitTagService:
    """Agrupa todos os testes unitários para o TagService."""

    def test_create_tag_success(self, mock_tag_repo: MagicMock):
        tag_data = TagCreate(name="Nova Tag")
        mock_db_session = MagicMock()

        mock_tag_repo.create_tag.return_value = Tag(
            id=uuid.uuid4(), name=tag_data.name, user_id=TEST_USER_ID
        )

        result = TagService.create_tag(mock_db_session, tag_data, TEST_USER_ID)

        mock_tag_repo.create_tag.assert_called_once_with(
            mock_db_session, tag_data, TEST_USER_ID
        )
        assert result.name == tag_data.name

    def test_create_tag_duplicate_raises_409(self, mock_tag_repo: MagicMock):
        tag_data = TagCreate(name="Tag Duplicada")
        mock_db_session = MagicMock()
        mock_db_session.rollback = MagicMock()

        mock_tag_repo.create_tag.side_effect = IntegrityError(
            "mocked error", params=None, orig=None
        )

        with pytest.raises(HTTPException) as exc_info:
            TagService.create_tag(mock_db_session, tag_data, TEST_USER_ID)

        assert exc_info.value.status_code == 409
        assert "Uma tag com esse nome já existe" in exc_info.value.detail
        mock_db_session.rollback.assert_called_once()

    def test_get_tag_by_id_success(self, mock_tag_repo: MagicMock):
        tag_id = uuid.uuid4()
        mock_db_session = MagicMock()
        mock_tag_repo.get_tag_by_id.return_value = Tag(
            id=tag_id, name="Tag Encontrada", user_id=TEST_USER_ID
        )

        result = TagService.get_tag_by_id(mock_db_session, tag_id, TEST_USER_ID)

        mock_tag_repo.get_tag_by_id.assert_called_once_with(
            mock_db_session, tag_id, TEST_USER_ID
        )
        assert result.id == tag_id

    def test_get_tag_by_id_not_found_raises_404(self, mock_tag_repo: MagicMock):
        tag_id = uuid.uuid4()
        mock_db_session = MagicMock()
        mock_tag_repo.get_tag_by_id.return_value = None

        with pytest.raises(HTTPException) as exc_info:
            TagService.get_tag_by_id(mock_db_session, tag_id, TEST_USER_ID)

        assert exc_info.value.status_code == 404
        assert "A tag não foi encontrada" in exc_info.value.detail

    def test_update_tag(self, mock_tag_repo: MagicMock):
        tag_id = uuid.uuid4()
        update_data = TagUpdate(name="Nome Atualizado")
        mock_db_session = MagicMock()

        tag_to_update = Tag(id=tag_id, name="Nome Antigo", user_id=TEST_USER_ID)
        mock_tag_repo.get_tag_by_id.return_value = tag_to_update

        mock_tag_repo.update_tag.return_value = Tag(
            id=tag_id, name=update_data.name, user_id=TEST_USER_ID
        )

        result = TagService.update_tag(
            mock_db_session, tag_id, update_data, TEST_USER_ID
        )

        mock_tag_repo.get_tag_by_id.assert_called_once_with(
            mock_db_session, tag_id, TEST_USER_ID
        )
        mock_tag_repo.update_tag.assert_called_once_with(
            mock_db_session, tag_to_update, update_data
        )
        assert result.name == "Nome Atualizado"

    def test_delete_tag(self, mock_tag_repo: MagicMock):
        tag_id = uuid.uuid4()
        mock_db_session = MagicMock()
        tag_to_delete = Tag(id=tag_id, name="Para Deletar", user_id=TEST_USER_ID)

        mock_tag_repo.get_tag_by_id.return_value = tag_to_delete

        TagService.delete_tag(mock_db_session, tag_id, TEST_USER_ID)

        mock_tag_repo.get_tag_by_id.assert_called_once_with(
            mock_db_session, tag_id, TEST_USER_ID
        )
        mock_tag_repo.delete_tag.assert_called_once_with(mock_db_session, tag_to_delete)
