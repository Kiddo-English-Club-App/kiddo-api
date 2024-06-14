from abc import ABC, abstractmethod
from . import dto


class TokenService(ABC):
    """
    Interface for token services. Token services are responsible for creating, verifying, and reading
    access and refresh tokens used for authentication and authorization in the application.

    The token service provides an abstraction over the token generation and verification process, allowing
    for different implementations to be used interchangeably in the application.
    """

    @abstractmethod
    def create_access_token(self, account: dto.AccountDto) -> str:
        """
        Creates an access token for the provided account.

        :param account: An AccountDto object representing the account to create the token for.
        :return: A string containing the generated access token.
        """
        pass

    @abstractmethod
    def create_refresh_token(self, account: dto.AccountDto) -> str:
        """
        Creates a refresh token for the provided account.

        :param account: An AccountDto object representing the account to create the token for.
        :return: A string containing the generated refresh token.
        """
        pass
    
    @abstractmethod
    def verify_token(self, token: str) -> bool:
        """
        Checks if the provided token is valid and not expired.

        :param token: A string containing the token to verify.
        :return: A boolean value indicating whether the token is valid or not.
        """
        pass

    @abstractmethod
    def read_token(self, token: str) -> dict:
        """
        Reads the contents of the provided token.

        :param token: A string containing the token to read.
        :return: A dictionary containing the token payload.
        """
        pass



