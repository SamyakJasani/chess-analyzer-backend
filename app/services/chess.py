from typing import Any

from pydantic import ValidationError

from ..models.contracts import GamesResponse, Pagination, UserProfile
from ..repositories.chess_com import ChessComRepository
from .external_api import ExternalAPIClient, ExternalAPIError


class ChessService:
    def __init__(self, repository: ChessComRepository):
        self.repository = repository

    @classmethod
    def from_app_config(cls, config):
        client = ExternalAPIClient.from_app_config(config)
        return cls(ChessComRepository(client))

    def get_user(self, username: str) -> dict[str, Any]:
        try:
            return UserProfile.model_validate(
                self.repository.get_player(username)
            ).model_dump(by_alias=True, exclude_none=True)
        except ValidationError as error:
            raise ExternalAPIError("Chess.com returned an invalid player profile") from error

    def get_games(
        self, username: str, page: int = 1, page_size: int = 20
    ) -> dict[str, Any]:
        archives = self.repository.get_archives(username)
        if not archives:
            return GamesResponse(
                username=username,
                archive=None,
                games=[],
                pagination=Pagination(
                    page=page,
                    page_size=page_size,
                    total_games=0,
                    total_pages=0,
                    has_next=False,
                    has_previous=page > 1,
                ),
            ).model_dump(exclude_none=True)

        latest_archive = archives[-1]
        games = list(reversed(self.repository.get_games_from_archive(latest_archive)))
        total_games = len(games)
        total_pages = (total_games + page_size - 1) // page_size
        start = (page - 1) * page_size
        paginated_games = games[start : start + page_size]
        try:
            response = GamesResponse(
                username=username,
                archive=latest_archive,
                games=paginated_games,
                pagination=Pagination(
                    page=page,
                    page_size=page_size,
                    total_games=total_games,
                    total_pages=total_pages,
                    has_next=page < total_pages,
                    has_previous=page > 1,
                ),
            )
        except ValidationError as error:
            raise ExternalAPIError("Chess.com returned invalid game data") from error

        return response.model_dump(by_alias=True, exclude_none=True)