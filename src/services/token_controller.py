"""
This module contains the token controller, which is responsible for handling the token validation endpoint.
"""

from flask import Blueprint, request
from dependify import inject

from account.application.token_service import TokenService
from .dto import TokenValidation


controller = Blueprint("services", __name__)


@controller.post("/validation/token")
@inject
def validate_token(service: TokenService):
    is_valid = service.verify_token(TokenValidation(**request.json).token)
    return {"is_valid": is_valid}, 200 if is_valid else 401
