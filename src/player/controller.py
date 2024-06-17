"""
This module is responsible for the player controller. It registers the guest and score controllers with the player controller
blueprint to manage the player-related routes in one place.
"""

from flask import Blueprint
from .guest_controller import controller as guest_controller
from .score_controller import controller as score_controller

controller = Blueprint("player", __name__)

controller.register_blueprint(guest_controller)
controller.register_blueprint(score_controller)
