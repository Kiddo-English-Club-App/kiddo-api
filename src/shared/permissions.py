import logging
from abc import ABC, abstractmethod

from shared.id import Id

from .exceptions import Unauthorized
from .account_type import AccountType
from .app_context import AppContext


class Permission(ABC):
    """
    Permission is an interface that defines the contract for verifying if a user has permission to perform
    a specific operation based on the application context.
    """

    @abstractmethod
    def verify(self, app_context: AppContext):
        """
        Verify if the user has permission to perform the operation based on the application context.

        :param app_context: The application context that provides access to the current user identity and account type.
        :return: True if the user has permission, False otherwise.
        """
        pass

    def __str__(self):
        return "Permission denied"


class AdminOrSameUserPermission(Permission):
    """
    Permission that requires the user to be an admin or the same user as the one being accessed.

    This permission is used to restrict access to resources that can only be accessed by an admin or the same user.
    """

    def __init__(self, identity: Id):
        """ """
        self.identity = identity

    def verify(self, app_context: AppContext):
        logger = logging.getLogger("kiddo")
        logger.debug(f"Id: {app_context.identity()} passed:  {self.identity}")
        logger.debug(f"Is admin: {app_context.account_type() == AccountType.ADMIN}")

        return (
            app_context.account_type() == AccountType.ADMIN
            or app_context.identity() == self.identity
        )

    def __str__(self):
        return "Permission denied: Admin or same user required"


class SameUserPermission(Permission):
    def __init__(self, identity: Id):
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
    """
    Validate if the user has permission to perform the operation based on the application context.
    If any of the permissions fail, an Unauthorized exception is raised.
    """

    for permission in permissions:
        if not permission.verify(app_context):
            raise Unauthorized(str(permission))
