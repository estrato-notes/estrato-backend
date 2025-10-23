import uuid
from unittest.mock import MagicMock, patch

import pytest

from src.modules.search.schemas import SearchResultType
from src.modules.search.service import SearchService

TEST_USER_ID = uuid.uuid4()


@pytest.fixture
def mock_search_repo():
    with patch(
        "src.modules.search.service.search_repository",
        new_callable=MagicMock,
    ) as mock:
        yield mock


class TestUnitSearchService:
    """Agrupa todos os testes unitários para o SearchService."""

    def test_search_calls_repository_and_formats_response(
        self, mock_search_repo: MagicMock
    ):
        mock_db_session = MagicMock()
        search_term = "teste"

        mock_row = MagicMock()
        mock_row.id = uuid.uuid4()
        mock_row.name = "Resultado do Teste"
        mock_row.type = SearchResultType.NOTE
        mock_row.snippet = "Conteúdo do resultado"

        mock_search_repo.search_query.return_value = [mock_row]

        # --- Ação ---
        result = SearchService.search(mock_db_session, search_term, TEST_USER_ID)

        # --- Verificação ---
        mock_search_repo.search_query.assert_called_once_with(
            mock_db_session, search_term, TEST_USER_ID
        )

        assert len(result.results) == 1
        search_item = result.results[0]
        assert search_item.id == mock_row.id

    def test_search_with_empty_result_from_repository(
        self, mock_search_repo: MagicMock
    ):
        mock_db_session = MagicMock()
        search_term = "termo_inexistente"

        mock_search_repo.search_query.return_value = []

        result = SearchService.search(mock_db_session, search_term, TEST_USER_ID)

        mock_search_repo.search_query.assert_called_once_with(
            mock_db_session, search_term, TEST_USER_ID
        )
        assert result.results == []
