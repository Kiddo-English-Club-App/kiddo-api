# Domain model
from shared.id import Id
from .password import Password
from shared.account_type import AccountType


class Account:
    id: Id
    first_name: str
    last_name: str
    email: str
    password: Password
    account_type: AccountType

    def __init__(
            self,
            first_name: str,
            last_name: str,
            email: str,
            password: Password | str,
            id: Id = None,
            account_type: AccountType = AccountType.USER
            ):

        self.id = id if isinstance(id, Id) else Id(id)
        self.first_name = first_name.strip()
        self.last_name = last_name.strip()
        self.email = email.strip()
        self.account_type = account_type
        
        if isinstance(password, str):
            password = Password(password)
        
        self.password = password

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Account):
            return False

        return self.id == other.id    
