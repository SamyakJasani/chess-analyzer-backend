from flask import Blueprint, current_app, jsonify, request

from .openapi import get_openapi_document
from .models.contracts import HealthResponse
from .services.chess import ChessService
from .services.external_api import ExternalAPIError

api_bp = Blueprint("api", __name__)


@api_bp.get("/health")
def health_check():
    return jsonify(HealthResponse(status="ok").model_dump())


@api_bp.get("/openapi.json")
def openapi_document():
    return jsonify(get_openapi_document())


@api_bp.get("/users/<username>")
def get_user(username):
    service = ChessService.from_app_config(current_app.config)
    try:
        response = service.get_user(username)
    except ExternalAPIError as error:
        return jsonify({"error": str(error)}), 502

    return jsonify(response)


@api_bp.get("/users/<username>/games")
def get_games(username):
    service = ChessService.from_app_config(current_app.config)
    try:
        page = _get_positive_query_int("page", default=1)
        page_size = _get_positive_query_int("page_size", default=20)
        if page_size > 100:
            raise ValueError("page_size must be less than or equal to 100")
    except ValueError as error:
        return jsonify({"error": str(error)}), 400

    try:
        response = service.get_games(username, page=page, page_size=page_size)
    except ExternalAPIError as error:
        return jsonify({"error": str(error)}), 502

    return jsonify(response)


def _get_positive_query_int(name: str, default: int) -> int:
    value = request.args.get(name)
    if value is None:
        return default

    try:
        parsed_value = int(value)
    except ValueError as error:
        raise ValueError(f"{name} must be an integer") from error

    if parsed_value < 1:
        raise ValueError(f"{name} must be greater than or equal to 1")

    return parsed_value
