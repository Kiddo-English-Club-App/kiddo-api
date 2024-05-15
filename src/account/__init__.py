def init():
    from dependify import register
    from .application.account_service import AccountService
    from . import infrastructure

    register(AccountService)
    infrastructure.init()
    
    print("account initialized")