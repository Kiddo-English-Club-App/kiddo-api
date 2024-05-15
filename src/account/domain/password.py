import bcrypt

class Password:
    hashed: str

    def __init__(self, password: str, hashed: bool = False):
        if hashed:
            self.hashed = password
        else:
            self.hashed = self._hash(password)
    
    def _hash(self, password: str) -> str:
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    
    def __eq__(self, other: object) -> bool:
        if isinstance(other, Password):
            return self.hashed == other.hashed
        
        if isinstance(other, str):
            return bcrypt.checkpw(other.encode(), self.hashed.encode())
        
        return False