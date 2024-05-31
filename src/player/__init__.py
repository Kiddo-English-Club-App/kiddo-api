def init():
    from settings.logs import logger
    from dependify import register

    from .application import guest_service, score_service, achievement_service
    from .domain import guest_repository, achievement_repository
    from .infrastructure import mongo_achievement_repository, mongo_guest_repository

    register(guest_service.GuestService)
    register(score_service.ScoreService)
    register(guest_repository.IGuestRepository, mongo_guest_repository.MongoDBGuestRepository)
    register(achievement_repository.IAchievementRepository, mongo_achievement_repository.MongoDBAchievementRepository)
    register(achievement_service.AchievementService)


    logger().debug("Player module initialized")