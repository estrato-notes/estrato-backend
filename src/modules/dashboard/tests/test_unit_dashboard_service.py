import uuid
from datetime import datetime, timezone
from unittest.mock import MagicMock, patch

import pytest

from src.core.models import Note, Notebook, Tag, Template
from src.modules.dashboard.service import DashboardService


@pytest.fixture
def mock_dashboard_repo():
    """Cria um mock para o dashboard_repository."""
    with patch(
        "src.modules.dashboard.service.dashboard_repository",
        new_callable=MagicMock,
    ) as mock:
        yield mock


class TestUnitDashboardService:
    """Agrupa todos os testes unitários para o DashboardService."""

    def test_get_dashboard_data(self, mock_dashboard_repo: MagicMock):
        """
        Testa se o serviço chama todos os métodos do repositório e formata
        os dados corretamente.
        """
        # --- Cenário de Mock ---
        mock_db_session = MagicMock()
        notebook_id = uuid.uuid4()
        now = datetime.now(timezone.utc)

        # Criando mocks com todos os campos necessários para a validação do Pydantic
        mock_recent_note = Note(
            id=uuid.uuid4(),
            title="Nota Recente",
            is_favorite=False,
            notebook_id=notebook_id,
            created_at=now,
            updated_at=now,
        )
        mock_fav_note = Note(
            id=uuid.uuid4(),
            title="Nota Favorita",
            is_favorite=True,
            notebook_id=notebook_id,
            created_at=now,
            updated_at=now,
        )
        mock_fav_notebook = Notebook(
            id=notebook_id,
            name="Caderno Favorito",
            is_favorite=True,
            created_at=now,
            updated_at=now,
        )
        mock_tag = Tag(id=uuid.uuid4(), name="Tag Popular")
        mock_recent_template = Template(
            id=uuid.uuid4(), name="Template Recente", content="Conteúdo", created_at=now
        )

        # Configura os retornos dos métodos mockados do repositório
        mock_dashboard_repo.get_recent_notes.return_value = [mock_recent_note]
        mock_dashboard_repo.get_recent_templates.return_value = [mock_recent_template]
        mock_dashboard_repo.get_favorite_notes.return_value = [mock_fav_note]
        mock_dashboard_repo.get_favorite_notebooks.return_value = [mock_fav_notebook]
        mock_dashboard_repo.get_popular_tags.return_value = [(mock_tag, 1)]

        # --- Ação ---
        result = DashboardService.get_dashboard_data(mock_db_session)

        # --- Verificação ---
        # Garante que todos os métodos do repositório foram chamados uma vez
        mock_dashboard_repo.get_recent_notes.assert_called_once_with(mock_db_session)
        mock_dashboard_repo.get_recent_templates.assert_called_once_with(
            mock_db_session
        )
        mock_dashboard_repo.get_favorite_notes.assert_called_once_with(mock_db_session)
        mock_dashboard_repo.get_favorite_notebooks.assert_called_once_with(
            mock_db_session
        )
        mock_dashboard_repo.get_popular_tags.assert_called_once_with(mock_db_session)

        # Verifica se os dados retornados estão corretos e bem formatados
        assert len(result.recent_notes) == 1
        assert result.recent_notes[0].title == "Nota Recente"

        assert len(result.recent_templates) == 1
        assert result.recent_templates[0].name == "Template Recente"

        assert len(result.favorite_notes) == 1
        assert result.favorite_notes[0].is_favorite is True

        assert len(result.favorite_notebooks) == 1
        assert result.favorite_notebooks[0].name == "Caderno Favorito"

        assert len(result.popular_tags) == 1
        assert result.popular_tags[0].name == "Tag Popular"
        assert result.popular_tags[0].note_count == 1
