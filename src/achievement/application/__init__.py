def init():
    from dependify import register

    from .achievement_service import AchievementService

    register(AchievementService)