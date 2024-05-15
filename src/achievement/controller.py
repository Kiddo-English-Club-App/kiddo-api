from flask import Blueprint
from dependify import inject

from achievement.application.achievement_service import AchievementService, dto

controller = Blueprint('achievement', __name__, url_prefix='/achievements')