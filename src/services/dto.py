from pydantic import BaseModel


class TokenValidation(BaseModel):
    token: str
