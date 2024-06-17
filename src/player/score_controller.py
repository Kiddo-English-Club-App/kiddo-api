"""
This module contains the score controller. It defines the routes for managing scores.
"""

from uuid import UUID
from flask import Blueprint, request
from dependify import inject

from player.application.score_service import ScoreService
from shared.id import Id
from .dto import ReportDto, AddScoreDto, ScoreDto


controller = Blueprint("score", __name__, url_prefix="/scores")


@controller.post("/")
@inject
def add_score(score_service: ScoreService):
    data = AddScoreDto(**request.json)
    score = score_service.add_score(data)
    return ScoreDto.load(score).model_dump()


@controller.get("/report/<uuid:guest_id>")
@inject
def create_report(score_service: ScoreService, guest_id: UUID):
    report = score_service.create_report(Id(guest_id))
    return ReportDto.load(report).model_dump()
