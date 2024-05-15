# Guest service
from shared.app_context import AppContext
from shared.permissions import AdminOrSameUserPermission, validate
from shared.exceptions import Forbidden, NotFound
from account.domain.account_type import AccountType

from ..domain.guest import Guest
from ..domain.guest_repository import IGuestRepository
from . import dto


class GuestService:

    def __init__(self, guest_repository: IGuestRepository, app_context: AppContext) -> None:
        self.guest_repository = guest_repository
        self.app_context = app_context
    
    def create_guest(self, data: dto.CreateGuestDto) -> dto.GuestDto:
        validate(
            AdminOrSameUserPermission(
                AccountType.ADMIN, self.app_context, data.host
            )
        )

        guest = Guest(data.host, data.name, data.image)
        
        self.guest_repository.save(guest)

        return dto.GuestDto.from_entity(guest)

    def get_guest(self, guest_id: str) -> dto.GuestDto:
        guest = self.guest_repository.find_by_id(guest_id)

        if not guest:
            raise NotFound("Guest not found")
        
        if self.app_context.identity() != guest.host:
            raise Forbidden("You are not allowed to access this guest")
        
        return dto.GuestDto.from_entity(guest)

    def get_guests(self, host_id: str) -> list[dto.GuestDto]:
        if self.app_context.identity() != host_id:
            raise Forbidden("You are not allowed to access this guest")
        
        guests = self.guest_repository.find_all(host_id)
        return [dto.GuestDto.from_entity(guest) for guest in guests]