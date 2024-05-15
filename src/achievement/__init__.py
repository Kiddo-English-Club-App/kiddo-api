def init():
    print("achievement initialized")
    from . import infrastructure, application

    infrastructure.init()
    application.init()