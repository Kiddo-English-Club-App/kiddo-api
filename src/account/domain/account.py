# Domain model
from uuid import UUID, uuid4

from .password import Password
from .account_type import AccountType


class Account:
    id: UUID
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
            id: UUID = uuid4(),
            account_type: AccountType = AccountType.USER
            ):

        self.id = id
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
