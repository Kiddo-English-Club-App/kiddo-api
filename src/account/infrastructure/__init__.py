def init():
    from dependify import register
    
    from .jwt_token_service import JwtTokenService, TokenService
    from .mongo_repository import MongoDBAccountRepository, IAccountRepository
    from .request_app_context import RequestAppContext, AppContext

    register(TokenService, JwtTokenService)
    register(IAccountRepository, MongoDBAccountRepository)
    register(AppContext, RequestAppContext)
