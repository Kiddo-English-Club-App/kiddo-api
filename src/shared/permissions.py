from abc import ABC, abstractmethod
from uuid import UUID

from .exceptions import Forbidden
from .app_context import AppContext


class Permission(ABC):

    @abstractmethod
    def verify(self):
        pass
        
    def __str__(self):
        return "Permission denied"
    

class AdminOrSameUserPermission(Permission):

    def __init__(self, admin: str, context: AppContext, identity: UUID):
        self.context = context
        self.admin = admin
        self.identity = identity

    def verify(self):
        return self.context.account_type() == self.admin \
            or self.context.identity() == self.identity

    def __str__(self):
        return "Permission denied: Admin or same user required"
    

def validate(*permissions: Permission):
    for permission in permissions:
        if not permission.verify():
            raise Forbidden(str(permission))