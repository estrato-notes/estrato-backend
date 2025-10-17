from typing import Annotated

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from src.core.database import get_db

from .schemas import SearchResponse
from .service import SearchService as search_service

router = APIRouter(prefix="/search", tags=["Search"])


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=SearchResponse,
    summary="Executa a busca unificada",
)
def search(
    q: Annotated[
        str,
        Query(
            description="Termo a ser buscado em notas, cadernos, tags e templates",
            min_length=1,
        ),
    ],
    db: Annotated[Session, Depends(get_db)],
) -> SearchResponse:
    return search_service.search(db, q)
