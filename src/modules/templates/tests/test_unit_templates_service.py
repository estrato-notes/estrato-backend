import uuid
from unittest.mock import MagicMock, patch

import pytest
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

from src.core.models import Template
from src.modules.templates.schemas import TemplateCreate
from src.modules.templates.service import TemplateService

TEST_USER_ID = uuid.uuid4()


@pytest.fixture
def mock_template_repo():
    with patch(
        "src.modules.templates.service.template_repository", new_callable=MagicMock
    ) as mock:
        yield mock


class TestUnitTemplateService:
    """Agrupa todos os testes unitários para o TemplateService."""

    def test_create_template_success(self, mock_template_repo: MagicMock):
        template_data = TemplateCreate(name="Novo Template")
        mock_db_session = MagicMock()

        mock_template_repo.create_template.return_value = Template(
            id=uuid.uuid4(), name=template_data.name, user_id=TEST_USER_ID
        )

        result = TemplateService.create_template(
            mock_db_session, template_data, TEST_USER_ID
        )

        mock_template_repo.create_template.assert_called_once_with(
            mock_db_session, template_data, TEST_USER_ID
        )
        assert result.name == template_data.name

    def test_create_template_duplicate_raises_409(self, mock_template_repo: MagicMock):
        template_data = TemplateCreate(name="Template Duplicado")
        mock_db_session = MagicMock()
        mock_db_session.rollback = MagicMock()

        mock_template_repo.create_template.side_effect = IntegrityError(
            "mocked error", params=None, orig=None
        )

        with pytest.raises(HTTPException) as exc_info:
            TemplateService.create_template(
                mock_db_session, template_data, TEST_USER_ID
            )

        assert exc_info.value.status_code == 409
        assert "Um template com esse nome já existe" in exc_info.value.detail
        mock_db_session.rollback.assert_called_once()

    def test_get_template_by_id_not_found_raises_404(
        self, mock_template_repo: MagicMock
    ):
        template_id = uuid.uuid4()
        mock_db_session = MagicMock()
        mock_template_repo.get_template_by_id.return_value = None

        with pytest.raises(HTTPException) as exc_info:
            TemplateService.get_template_by_id(
                mock_db_session, template_id, TEST_USER_ID
            )

        assert exc_info.value.status_code == 404

    def test_delete_template(self, mock_template_repo: MagicMock):
        template_id = uuid.uuid4()
        mock_db_session = MagicMock()
        template_to_delete = Template(
            id=template_id, name="Para Deletar", user_id=TEST_USER_ID
        )

        mock_template_repo.get_template_by_id.return_value = template_to_delete

        TemplateService.delete_template_by_id(
            mock_db_session, template_id, TEST_USER_ID
        )

        mock_template_repo.get_template_by_id.assert_called_once_with(
            mock_db_session, template_id, TEST_USER_ID
        )
        mock_template_repo.delete_template.assert_called_once_with(
            mock_db_session, template_to_delete
        )
