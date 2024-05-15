def init(app):
    from . import environment, dependencies, error_handlers
    """
    Initialize the module
    """
    environment.init(app)
    dependencies.init(app)
    error_handlers.init(app)
    
    from account import init as account_init
    from score import init as score_init
    from theme import init as theme_init
    from achievement import init as achievement_init
    from guest import init as guest_init
    
    account_init()
    score_init()
    theme_init()
    achievement_init()
    guest_init()
    pass