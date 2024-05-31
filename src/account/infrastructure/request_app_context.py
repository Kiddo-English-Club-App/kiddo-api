from uuid import UUID
from flask import request

from shared.id import Id
from shared.account_type import AccountType
from shared.app_context import AppContext
from shared.exceptions import Unauthenticated
from ..application.token_service import TokenService


class RequestAppContext(AppContext):
    _identity: Id = None
    _account_type: AccountType = None

    def __init__(self, token_service: TokenService):
        self.token_service = token_service

    def _load_token(self):
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
