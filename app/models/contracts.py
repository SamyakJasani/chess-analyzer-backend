from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class APIModel(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        extra="allow",
    )


class UserProfile(APIModel):
    chess_id: str = Field(alias="@id")
    url: str
    username: str
    player_id: int
    title: str | None = None
    status: str
    name: str | None = None
    avatar: str | None = None
    location: str | None = None
    country: str | None = None
    joined: int
    last_online: int
    followers: int
    is_streamer: bool = False
    twitch_url: str | None = None
    fide: int | None = None
    verified: bool | None = None
    league: str | None = None
    streaming_platforms: list[Any] = Field(default_factory=list)


class GamePlayer(APIModel):
    rating: int | None = None
    result: str | None = None
    chess_id: str | None = Field(default=None, alias="@id")
    username: str
    uuid: str | None = None


class Game(APIModel):
    url: str
    pgn: str
    time_control: str | None = None
    end_time: int | None = None
    rated: bool | None = None
    tcn: str | None = None
    uuid: str | None = None
    initial_setup: str | None = None
    fen: str | None = None
    time_class: str | None = None
    rules: str | None = None
    white: GamePlayer
    black: GamePlayer
    eco: str | None = None


class GamesResponse(APIModel):
    username: str
    archive: str | None = None
    games: list[Game]


class HealthResponse(BaseModel):
    status: str


class ErrorResponse(BaseModel):
    error: str