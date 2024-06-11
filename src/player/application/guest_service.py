# Guest service
from shared.app_context import AppContext
from shared.id import Id
from shared.permissions import (
    AdminOrSameUserPermission, SameUserPermission, validate)
from shared.exceptions import  NotFound, ValidationError
from shared.account_type import AccountType

from ..domain.guest import Guest
from ..domain.guest_repository import IGuestRepository
from ..domain.achievement_repository import IAchievementRepository
from . import dto


class GuestService:

    GUESTS_LIMIT = 3

    def __init__(
            self, 
            guest_repository: IGuestRepository,
            achievement_repository: IAchievementRepository, 
            app_context: AppContext) -> None:
        self.guest_repository = guest_repository
        self.app_context = app_context
        self.achievement_repository = achievement_repository
    
    def create_guest(self, data: dto.CreateGuestDto) -> dto.GuestDto:
        validate(self.app_context, SameUserPermission(data.host))

        guest = Guest(
            name=data.name,
            host=data.host,
            image=data.image)
        
        guests = self.guest_repository.find_all(data.host)

        if len(guests) >= GuestService.GUESTS_LIMIT:
            raise ValidationError("You can't have more than 3 guests")
        
        self.guest_repository.save(guest)

        return dto.GuestDto.from_entity(guest)

    def get_guest(self, guest_id: str) -> dto.GuestDto:
        guest = self.guest_repository.find_by_id(guest_id)

        if not guest:
            raise NotFound("Guest not found")
        
        validate(self.app_context, AdminOrSameUserPermission(AccountType.ADMIN, guest.host))

        return dto.GuestDto.from_entity(guest)

    def get_guests(self, host_id: Id) -> list[dto.GuestDto]:
        validate(self.app_context, AdminOrSameUserPermission(AccountType.ADMIN, host_id))
        
        guests = self.guest_repository.find_all(host_id)
        return [dto.GuestDto.from_entity(guest) for guest in guests]
    
    def get_guest_achievements(self, guest_id: Id) -> list[dto.AchievementDto]:
        guest = self.guest_repository.find_by_id(guest_id)

        if not guest:
            raise NotFound("Guest not found")
        
        validate(self.app_context, AdminOrSameUserPermission(AccountType.ADMIN, guest.host))
        
        return [dto.AchievementDto.from_entity(achievement) for achievement in guest.achievements]