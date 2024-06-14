import jwt
from datetime import datetime, timedelta

from settings.environment import env
from settings.logs import logger
from account.application.dto import AccountDto
from shared.exceptions import InvalidToken

from ..application.token_service import TokenService


class JwtTokenService(TokenService):
    """
    JwtTokenService is an implementation of the TokenService interface that provides methods
    for creating, verifying, and reading access and refresh tokens using JSON Web Tokens (JWT).

    It uses the configured secret keys and expiration times from the environment settings.
    """

    def create_access_token(self, account: AccountDto) -> str:
        """
        Creates an access token for the provided account. The token contains the following claims:
        - sub: Subject (account ID)
        - email: Email address of the account
        - account_type: Type of account (user or admin)
        - exp: Expiration time (current time + expiration time from settings)

        :param account: An AccountDto object representing the account to create the token for.
        :return: A string containing the generated access token.
        """
        payload = {
            "sub": str(account.id),
            "email": account.email,
            "account_type": account.account_type,
            "exp": (datetime.now() + timedelta(minutes=env.ACCESS_TOKEN_EXPIRATION)).timestamp()
        }
        
        return jwt.encode(payload, env.ACCESS_TOKEN_SECRET, algorithm="HS256")
    
    def create_refresh_token(self, account: AccountDto) -> str:
        """
        Creates a refresh token for the provided account. The token contains the following claims:
        - sub: Subject (account ID)
        - email: Email address of the account
        - account_type: Type of account (user or admin)
        - exp: Expiration time (current time + expiration time from settings)

        :param account: An AccountDto object representing the account to create the token for.
        :return: A string containing the generated refresh token.
        """
        payload = {
            "sub": str(account.id),
            "email": account.email,
            "account_type": account.account_type.value,
            "exp": datetime.now() + timedelta(minutes=env.REFRESH_TOKEN_EXPIRATION)
        }
        return jwt.encode(payload, env.REFRESH_TOKEN_SECRET, algorithm="HS256")

    def verify_token(self, token: str) -> bool:
        """
        Checks if the provided token is valid and not expired. It uses the access token secret key 
        to verify the token signature and expiration time. If the token is valid, it returns True;
        otherwise, it returns False.

        :param token: A string containing the token to verify.
        :return: A boolean value indicating whether the token is valid or not.
        """
        try:
            if env.is_development():
                logger().debug(f"Token: {token}")

            jwt.decode(token, env.ACCESS_TOKEN_SECRET, algorithms=["HS256"])
            return True
        except jwt.ExpiredSignatureError:
            return False
        except jwt.InvalidTokenError:
            return False
        
    def read_token(self, token: str) -> dict:
        """
        Reads the contents of the provided token. It decodes the token using the access token secret key
        and returns the payload as a dictionary.

        :param token: A string containing the token to read.
        :return: A dictionary containing the token payload.
        :raises InvalidToken: If the token is invalid or expired.
        """
        try:
            return jwt.decode(token, env.ACCESS_TOKEN_SECRET, algorithms=["HS256"])
        except jwt.PyJWTError as e:
            raise InvalidToken from e
        
