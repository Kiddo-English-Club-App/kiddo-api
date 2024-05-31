import jwt
from datetime import datetime, timedelta

from settings.environment import env
from account.application.dto import AccountDto
from shared.exceptions import InvalidToken

from ..application.token_service import TokenService


class JwtTokenService(TokenService):

    def create_access_token(self, account: AccountDto) -> str:
        payload = {
            "sub": str(account.id),
            "email": account.email,
            "account_type": account.account_type,
            "exp": (datetime.now() + timedelta(minutes=env.ACCESS_TOKEN_EXPIRATION)).timestamp()
        }
        print(env.ACCESS_TOKEN_SECRET)
        return jwt.encode(payload, env.ACCESS_TOKEN_SECRET, algorithm="HS256")
    
    def create_refresh_token(self, account: AccountDto) -> str:
        payload = {
            "sub": str(account.id),
            "email": account.email,
            "account_type": account.account_type.value,
            "exp": datetime.now() + timedelta(minutes=env.REFRESH_TOKEN_EXPIRATION)
        }
        return jwt.encode(payload, env.REFRESH_TOKEN_SECRET, algorithm="HS256")

    def verify_token(self, token: str) -> bool:
        try:
            jwt.decode(token, env.ACCESS_TOKEN_SECRET, algorithms=["HS256"])
            return True
        except jwt.ExpiredSignatureError:
            return False
        except jwt.InvalidTokenError:
            return False
        
    def read_token(self, token: str) -> dict:
        try:
            return jwt.decode(token, env.ACCESS_TOKEN_SECRET, algorithms=["HS256"])
        except jwt.PyJWTError as e:
            raise InvalidToken from e
        
