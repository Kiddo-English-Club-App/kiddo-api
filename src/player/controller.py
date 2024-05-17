from flask import Blueprint
from .guest_controller import controller as guest_controller
from .score_controller import controller as score_controller

controller = Blueprint('player', __name__)

controller.register_blueprint(guest_controller)
controller.register_blueprint(score_controller)