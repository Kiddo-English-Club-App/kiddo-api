from flask import Blueprint, request
from dependify import inject

from score.application.score_service import ScoreService, dto


controller = Blueprint('score', __name__, url_prefix='/scores')


@controller.post('/')
@inject
def add_score(score_service: ScoreService):
    data = dto.AddScoreDto(**request.json)
    return score_service.add_score(data).model_dump()


@controller.get('/report/<uuid:guest_id>')
@inject
def create_report(score_service: ScoreService, guest_id):
    return score_service.create_report(guest_id).model_dump()