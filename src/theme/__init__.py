def init():
    print("theme initialized")
    from . import application
    from . import infrastructure

    application.init()
    infrastructure.init()