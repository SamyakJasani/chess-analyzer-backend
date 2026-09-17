from flask import Blueprint, current_app, jsonify

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
        response = service.get_games(username)
    except ExternalAPIError as error:
        return jsonify({"error": str(error)}), 502

    return jsonify(response)
