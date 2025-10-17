from sqlalchemy.orm import Session

from .repository import DashboardRepository as dashboard_repository
from .schemas import DashboardResponse, TagPopularResponse


class DashboardService:
    @staticmethod
    def get_dashboard_data(db: Session) -> DashboardResponse:
        """Orquestra a busca de todos os dados necessários para o dashboard"""
        recent_notes = dashboard_repository.get_recent_notes(db)
        favorite_notes = dashboard_repository.get_favorite_notes(db)
        favorite_notebooks = dashboard_repository.get_favorite_notebooks(db)
        popular_tag_data = dashboard_repository.get_popular_tags(db)

        popular_tags = []
        for tag, count in popular_tag_data:
            popular_tags.append(
                TagPopularResponse(id=tag.id, name=tag.name, note_count=count)
            )

        return DashboardResponse(
            recent_notes=recent_notes,
            popular_tags=popular_tags,
            favorite_notes=favorite_notes,
            favorite_notebooks=favorite_notebooks,
        )
