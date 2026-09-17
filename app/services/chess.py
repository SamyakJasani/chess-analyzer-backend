from typing import Any

from pydantic import ValidationError

from ..models.contracts import GamesResponse, UserProfile
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

    def get_games(self, username: str) -> dict[str, Any]:
        archives = self.repository.get_archives(username)
        if not archives:
            return GamesResponse(
                username=username, archive=None, games=[]
            ).model_dump(exclude_none=True)

        latest_archive = archives[-1]
        games = self.repository.get_games_from_archive(latest_archive)
        try:
            response = GamesResponse(
                username=username,
                archive=latest_archive,
                games=list(reversed(games)),
            )
        except ValidationError as error:
            raise ExternalAPIError("Chess.com returned invalid game data") from error

        return response.model_dump(by_alias=True, exclude_none=True)