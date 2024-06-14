def init():
    """
    Initializes the account module by registering dependencies and initializing infrastructure.
    """
    from dependify import register
    from settings.logs import logger
    from .application.account_service import AccountService
    from . import infrastructure

    register(AccountService)
    infrastructure.init()
    
    logger().debug("Account module initialized")