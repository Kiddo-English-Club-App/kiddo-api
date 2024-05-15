from uuid import UUID
from pydantic import BaseModel

from ..domain.guest import Guest


class GuestDto(BaseModel):
    id: UUID
    host: UUID
    name: str
    image: str

    @staticmethod
    def from_entity(guest: Guest):
        return GuestDto(
            id=guest.id,
            name=guest.name,
            host=guest.host,
            image=guest.image
        )


class CreateGuestDto(BaseModel):
    host: UUID
    name: str
    image: str