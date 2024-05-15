from uuid import UUID
from flask import request

from shared.app_context import AppContext
from shared.exceptions import Unauthorized
from ..domain.account_type import AccountPermissionsMapping
from ..application.token_service import TokenService


class RequestAppContext(AppContext):
    _identity: UUID = None
    _account_type: str = None

    def __init__(self, token_service: TokenService):
        self.token_service = token_service

    def _load_token(self):
        authorization = request.authorization
        if not authorization:
            raise Unauthorized("Token not found")

        if not authorization.token:
            raise Unauthorized("Token not found")
        
        payload = self.token_service.read_token(authorization.token)
        self._identity = UUID(payload["sub"])
        self._account_type = payload["account_type"]

    def identity(self):
        if not self._identity:
            self._load_token()
        return self._identity
    
    def account_type(self):
        if not self._account_type:
            self._load_token()
        return self._account_type

    def authenticated(self):
        try:
            self._load_token()
            return True
        except Unauthorized:
            return False
        
    def authorized(self, all_: list[str] =  None, any_: list[str] = None) -> bool:
        if not self.authenticated():
            return False
        
        account_type = self.account_type()
        
        if all_ is None and any_ is None:
            return True
        
        all_permissions = all_ and all([permission in AccountPermissionsMapping[account_type] for permission in all_])
        any_permissions = any_ and any([permission in AccountPermissionsMapping[account_type] for permission in any_])

        return all_permissions and any_permissions