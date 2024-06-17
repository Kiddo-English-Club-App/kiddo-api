"""
This module contains the error handlers for the application to handle exceptions and errors.
Provides a centralized location to handle exceptions and errors that occur in the application.
"""

from werkzeug.exceptions import HTTPException
from pydantic import ValidationError
from shared import exceptions as exc
from settings.environment import env


def handle_domain_exception(error: exc.DomainException):
    match error.title:
        case exc.NotFound.title:
            status_code = 404

        case exc.Unauthenticated.title:
            status_code = 401

        case exc.Unauthorized.title:
            status_code = 403
        case _:
            status_code = 400

    return {"error": error.title, "message": error.message}, status_code


def handle_exception(e: Exception):
    error_message = "An unexpected error occurred. Please try again later."
    if env.is_development() or env.is_testing():
        error_message = [error_message, str(e)]
    return {"error": "internal_server_error", "message": error_message}, 500


def handle_validation_error(e: ValidationError):
    return {"error": "validation_error", "message": e.errors(include_url=False)}, 400


def handle_http_exception(e: HTTPException):
    return {"error": e.name.lower().replace(" ", "_"), "message": e.description}, 404


def init(app):
    """
    Initialize the module
    """
    app.register_error_handler(exc.DomainException, handle_domain_exception)
    app.register_error_handler(ValidationError, handle_validation_error)
    app.register_error_handler(HTTPException, handle_http_exception)

    if not env.is_development():
        app.register_error_handler(Exception, handle_exception)
