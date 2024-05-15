def init():
    print("guest initialized")
    from . import application
    from . import infrastructure

    infrastructure.init()
    application.init()