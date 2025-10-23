import uuid

from sqlalchemy.orm import Session

from .repository import SearchRepository as search_repository
from .schemas import SearchResponse, SearchResultItem


class SearchService:
    @staticmethod
    def search(db: Session, query_term: str, user_id: uuid.UUID) -> SearchResponse:
        """Orquestra a busca no repositório e formata o resultado"""
        query_result = search_repository.search_query(db, query_term, user_id)
        items: list[SearchResultItem] = []

        for row in query_result:
            items.append(SearchResultItem.model_validate(row))

        return SearchResponse(results=items)
