def init():
    from dependify import register

    from .score_service import ScoreService

    register(ScoreService)