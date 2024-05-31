def init(app):
    from . import environment, dependencies, error_handlers, logs
    """
    Initialize the module
    """
    environment.init(app)
    logs.init()
    dependencies.init(app)
    error_handlers.init(app)
    
    from account import init as account
    from player import init as player
    from theme import init as theme
    from services import init as services
    
    account()
    player()
    theme()
    services()