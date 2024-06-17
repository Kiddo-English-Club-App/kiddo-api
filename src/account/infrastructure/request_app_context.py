from flask import request

from shared.id import Id
from shared.account_type import AccountType
from shared.app_context import AppContext
from shared.exceptions import Unauthenticated
from ..application.token_service import TokenService


class RequestAppContext(AppContext):
    """
    RequestAppContext is an implementation of the AppContext interface that provides
    access to the current user identity and account type based on the request context.

    It uses the token service to read and validate the token from the request headers.

    The identity and account type are loaded lazily when requested for the first time.
    and cached for subsequent calls.
    """

    _identity: Id = None
    _account_type: AccountType = None

    def __init__(self, token_service: TokenService):
        self.token_service = token_service

    def _load_token(self):
        """
        Load the token from the request headers and extract the identity and account type.
        If the token is not found or invalid, an Unauthenticated exception is raised to
        indicate that the user is not authenticated.

        :raises Unauthenticated: If the token is not found or invalid.
        """
        authorization = request.authorization
        if not authorization:
            raise Unauthenticated("Token not found")

        if not authorization.token:
            raise Unauthenticated("Token not found")

        payload = self.token_service.read_token(authorization.token)
        self._identity = Id(payload["sub"])
        self._account_type = AccountType(payload["account_type"])

    def identity(self) -> Id:
        if not self._identity:
            self._load_token()
        return self._identity

    def account_type(self) -> AccountType:
        if not self._account_type:
            self._load_token()
        return self._account_type

    def authenticated(self) -> bool:
        try:
            self._load_token()
            return True
        except Unauthenticated:
            return False
