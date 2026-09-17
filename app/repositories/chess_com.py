from typing import Any

from ..services.external_api import ExternalAPIClient


class ChessComRepository:
    def __init__(self, client: ExternalAPIClient):
        self.client = client

    def get_player(self, username: str) -> dict[str, Any]:
        return self.client.get(f"player/{username}")

    def get_archives(self, username: str) -> list[str]:
        response = self.client.get(f"player/{username}/games/archives")
        return response.get("archives", [])

    def get_games_from_archive(self, archive_url: str) -> list[dict[str, Any]]:
        response = self.client.get_url(archive_url)
        return response.get("games", [])