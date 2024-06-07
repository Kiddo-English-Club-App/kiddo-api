# Domain model
from shared.id import Id
from .password import PasswordStr
from shared.name import NameStr
from shared.account_type import AccountType


class Account:
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
