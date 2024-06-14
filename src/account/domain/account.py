# Domain model
from shared.id import Id
from .password import PasswordStr
from shared.name import NameStr
from shared.account_type import AccountType


class Account:
    """
    Account domain model. Represents a user account in the system. It contains basic information
    about the user such as name, email, password, and account type. The account type determines 
    the level of access and permissions the user has within the system.
    """
    id: Id
    first_name: NameStr
    last_name: NameStr
    email: str
    password: PasswordStr
    account_type: AccountType

    def __init__(
            self,
            first_name: str,
            last_name: str,
            email: str,
            password: PasswordStr | str,
            id: Id = None,
            account_type: AccountType = AccountType.USER
            ):
        """
        Initializes an Account object with the provided data. The ID is optional as it will be
        generated automatically if not provided.

        :param first_name: The first name of the account holder.
        :param last_name: The last name of the account holder.
        :param email: The email address of the account holder.
        :param password: The password for the account. It should be a PasswordStr object or a string.
        :param id: The unique identifier of the account (optional).
        :param account_type: The type of account (default is USER).
        """

        self.id = id if isinstance(id, Id) else Id(id)
        self.first_name = NameStr(first_name)
        self.last_name = NameStr(last_name)
        self.email = email.strip()
        self.account_type = account_type
        self.password = PasswordStr(password)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Account):
            return False

        return self.id == other.id    
