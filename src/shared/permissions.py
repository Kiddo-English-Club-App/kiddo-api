from abc import ABC, abstractmethod
from uuid import UUID

from .exceptions import Forbidden
from .app_context import AppContext


class Permission(ABC):

    @abstractmethod
    def verify(self, app_context: AppContext):
        pass
        
    def __str__(self):
        return "Permission denied"
    

class AdminOrSameUserPermission(Permission):

    def __init__(self, admin: str, identity: UUID):
        self.admin = admin
        self.identity = identity

    def verify(self, app_context: AppContext):
        return app_context.account_type() == self.admin \
            or app_context.identity() == self.identity

    def __str__(self):
        return "Permission denied: Admin or same user required"


class SameUserPermission(Permission):

    def __init__(self, identity: UUID):
        self.identity = identity

    def verify(self, app_context: AppContext):
        return app_context.identity() == self.identity

    def __str__(self):
        return "Permission denied: Same user required"


class AuthenticatedPermission(Permission):
    
    def verify(self, app_context: AppContext):
        return app_context.authenticated()
    
    def __str__(self):
        return "Permission denied: Authenticated user required"


def validate(app_context: AppContext, *permissions: Permission):
    for permission in permissions:
        if not permission.verify(app_context):
            raise Forbidden(str(permission))
