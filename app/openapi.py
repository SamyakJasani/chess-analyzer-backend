from .models.contracts import (
    ErrorResponse,
    GamesResponse,
    HealthResponse,
    Pagination,
    UserProfile,
)


def _replace_definition_refs(value):
    if isinstance(value, dict):
        return {
            key: (
                value.replace("#/$defs/", "#/components/schemas/")
                if key == "$ref" and isinstance(value, str)
                else _replace_definition_refs(value)
            )
            for key, value in value.items()
        }
    if isinstance(value, list):
        return [_replace_definition_refs(item) for item in value]
    return value


def get_openapi_document() -> dict:
    schemas = {}
    for name, model in {
        "UserProfile": UserProfile,
        "GamesResponse": GamesResponse,
        "Pagination": Pagination,
        "HealthResponse": HealthResponse,
        "ErrorResponse": ErrorResponse,
    }.items():
        schema = model.model_json_schema()
        schemas.update(schema.pop("$defs", {}))
        schemas[name] = schema

    schemas = _replace_definition_refs(schemas)
    return {
        "openapi": "3.0.3",
        "info": {
            "title": "Chess Analyzer API",
            "version": "1.0.0",
            "description": "Read-only API for Chess.com player profiles and games.",
        },
        "servers": [{"url": "http://127.0.0.1:5000"}],
        "paths": {
            "/api/health": {
                "get": {
                    "operationId": "getHealth",
                    "responses": {
                        "200": {
                            "description": "Service is healthy.",
                            "content": {"application/json": {"schema": {"$ref": "#/components/schemas/HealthResponse"}}},
                        }
                    },
                }
            },
            "/api/users/{username}": {
                "get": {
                    "operationId": "getUser",
                    "parameters": [{"$ref": "#/components/parameters/Username"}],
                    "responses": {
                        "200": {
                            "description": "Chess.com player profile.",
                            "content": {"application/json": {"schema": {"$ref": "#/components/schemas/UserProfile"}}},
                        },
                        "502": {"$ref": "#/components/responses/ExternalAPIError"},
                    },
                }
            },
            "/api/users/{username}/games": {
                "get": {
                    "operationId": "getGames",
                    "parameters": [
                        {"$ref": "#/components/parameters/Username"},
                        {"$ref": "#/components/parameters/Page"},
                        {"$ref": "#/components/parameters/PageSize"},
                    ],
                    "responses": {
                        "200": {
                            "description": "Latest monthly games, newest first.",
                            "content": {"application/json": {"schema": {"$ref": "#/components/schemas/GamesResponse"}}},
                        },
                        "400": {"$ref": "#/components/responses/InvalidPagination"},
                        "502": {"$ref": "#/components/responses/ExternalAPIError"},
                    },
                }
            },
        },
        "components": {
            "schemas": schemas,
            "parameters": {
                "Username": {
                    "name": "username",
                    "in": "path",
                    "required": True,
                    "description": "Chess.com username.",
                    "schema": {"type": "string", "example": "Sam28062002"},
                },
                "Page": {
                    "name": "page",
                    "in": "query",
                    "required": False,
                    "description": "One-based page number.",
                    "schema": {"type": "integer", "minimum": 1, "default": 1},
                },
                "PageSize": {
                    "name": "page_size",
                    "in": "query",
                    "required": False,
                    "description": "Number of games per page. Maximum 100.",
                    "schema": {
                        "type": "integer",
                        "minimum": 1,
                        "maximum": 100,
                        "default": 20,
                    },
                },
            },
            "responses": {
                "InvalidPagination": {
                    "description": "The page or page_size query parameter is invalid.",
                    "content": {"application/json": {"schema": {"$ref": "#/components/schemas/ErrorResponse"}}},
                },
                "ExternalAPIError": {
                    "description": "Chess.com could not be reached or returned invalid data.",
                    "content": {"application/json": {"schema": {"$ref": "#/components/schemas/ErrorResponse"}}},
                }
            },
        },
    }