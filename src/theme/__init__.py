def init():
    from . import application
    from . import infrastructure

    application.init()
    infrastructure.init()

    import logging
    logger = logging.getLogger("kiddo")
    logger.debug("Theme module initialized")