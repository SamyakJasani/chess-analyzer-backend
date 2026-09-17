from dataclasses import dataclass
from typing import Any

import requests


class ExternalAPIError(Exception):
    """Raised when an external API request cannot be completed."""


@dataclass
class ExternalAPIClient:
    base_url: str
    timeout: float = 10

    @classmethod
    def from_app_config(cls, config):
        return cls(
            base_url=config["EXTERNAL_API_BASE_URL"],
            timeout=config["EXTERNAL_API_TIMEOUT"],
        )

    def get(self, path: str, **params) -> Any:
        return self.get_url(f"{self.base_url}/{path.lstrip('/')}", **params)

    def get_url(self, url: str, **params) -> Any:
        headers = {"Accept": "application/json"}
        headers["User-Agent"] = "chess-analyzer/0.1"

        try:
            response = requests.get(
                url,
                headers=headers,
                params=params,
                timeout=self.timeout,
            )
            response.raise_for_status()
        except requests.RequestException as error:
            raise ExternalAPIError(f"External API request failed: {error}") from error

        try:
            return response.json()
        except ValueError as error:
            raise ExternalAPIError("External API returned invalid JSON") from error
