import uuid
from unittest.mock import MagicMock, patch

import pytest

from src.modules.search.schemas import SearchResultType
from src.modules.search.service import SearchService


@pytest.fixture
def mock_search_repo():
    """Cria um mock para o search_repository."""
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
        """
        Testa se o serviço chama o método de busca do repositório e formata
        a resposta corretamente para o schema SearchResponse.
        """
        # --- Cenário ---
        mock_db_session = MagicMock()
        search_term = "teste"

        # Mock do resultado que o repositório retornaria.
        # Usamos um objeto MagicMock que simula a estrutura de um resultado de linha do SQLAlchemy.
        mock_row = MagicMock()
        mock_row.id = uuid.uuid4()
        mock_row.name = "Resultado do Teste"
        mock_row.type = SearchResultType.NOTE
        mock_row.snippet = "Conteúdo do resultado"

        mock_search_repo.search_query.return_value = [mock_row]

        # --- Ação ---
        result = SearchService.search(mock_db_session, search_term)

        # --- Verificação ---
        # 1. Garante que o repositório foi chamado com os parâmetros corretos.
        mock_search_repo.search_query.assert_called_once_with(
            mock_db_session, search_term
        )

        # 2. Verifica se o resultado foi formatado corretamente.
        assert len(result.results) == 1
        search_item = result.results[0]
        assert search_item.id == mock_row.id
        assert search_item.name == "Resultado do Teste"
        assert search_item.type == SearchResultType.NOTE
        assert search_item.snippet == "Conteúdo do resultado"

    def test_search_with_empty_result_from_repository(
        self, mock_search_repo: MagicMock
    ):
        """
        Testa se o serviço retorna uma lista vazia quando o repositório não
        encontra resultados.
        """
        mock_db_session = MagicMock()
        search_term = "termo_inexistente"

        mock_search_repo.search_query.return_value = []

        result = SearchService.search(mock_db_session, search_term)

        mock_search_repo.search_query.assert_called_once_with(
            mock_db_session, search_term
        )
        assert result.results == []
