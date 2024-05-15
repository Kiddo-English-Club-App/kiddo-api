from enum import StrEnum
from types import MappingProxyType

class AccountType(StrEnum):
    USER = "user"
    ADMIN = "admin"

class Permission:
    scope: str
    action: str

    def __init__(self, scope: str, action: str):
        self.scope = scope
        self.action = action

    @staticmethod
    def from_string(permission: str):
        print(permission)
        scope, action = permission.split(":")
        return Permission(scope, action)

    def __eq__(self, other):
        if isinstance(other, str):
            other = Permission.from_string(other)

        if isinstance(other, Permission):
            same_scope = self.scope == other.scope or self.scope == "*" or other.scope == "*"
            same_action = self.action == other.action or self.action == "*" or other.action == "*"
            return same_scope and same_action

        return False


def create_permissions(permissions: list[str]):
    return [Permission.from_string(permission) for permission in permissions]


AccountPermissionsMapping = MappingProxyType( {
        "user": create_permissions([
                    "theme:read",
                    "theme:list",
                    "guest:read",
                    "guest:list",
                    "guest:update",
                    "guest:create",
                    "guest:delete",
                    "achievement:read",
                    "achievement:list",
                    "score:post",
                    "report:create",
                    "report:read",
                    "self:read",
                    "self:update"
                ]),
        "admin": [
            Permission("*", "*")
        ]
    })

