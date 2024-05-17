# Guest service
from shared.app_context import AppContext
from shared.permissions import (
    AdminOrSameUserPermission, SameUserPermission, AuthenticatedPermission, validate)
from shared.exceptions import Forbidden, NotFound
from account.domain.account_type import AccountType

from ..domain.guest import Guest
from ..domain.guest_repository import IGuestRepository
from ..domain.achievement_repository import IAchievementRepository
from . import dto


class GuestService:

    def __init__(
            self, 
            guest_repository: IGuestRepository,
            achievement_repository: IAchievementRepository, 
            app_context: AppContext) -> None:
        self.guest_repository = guest_repository
        self.app_context = app_context
        self.achievement_repository = achievement_repository
    
    def create_guest(self, data: dto.CreateGuestDto) -> dto.GuestDto:
        validate(self.app_context, SameUserPermission(AccountType.ADMIN, data.host))

        guest = Guest(data.host, data.name, data.image)
        
        self.guest_repository.save(guest)

        return dto.GuestDto.from_entity(guest)

    def get_guest(self, guest_id: str) -> dto.GuestDto:
        validate(self.app_context, AuthenticatedPermission())
        guest = self.guest_repository.find_by_id(guest_id)

        if not guest:
            raise NotFound("Guest not found")
        
        if self.app_context.identity() != guest.host:
            raise Forbidden("You are not allowed to access this guest")
        
        return dto.GuestDto.from_entity(guest)

    def get_guests(self, host_id: str) -> list[dto.GuestDto]:
        validate(self.app_context, AdminOrSameUserPermission(AccountType.ADMIN, host_id))
        if self.app_context.identity() != host_id:
            raise Forbidden("You are not allowed to access this guest")
        
        guests = self.guest_repository.find_all(host_id)
        return [dto.GuestDto.from_entity(guest) for guest in guests]
    
    def get_guest_achievements(self, guest_id: str, compute: bool = False) -> list[dto.AchievementDto]:
        guest = self.guest_repository.find_by_id(guest_id)

        if not guest:
            raise NotFound("Guest not found")
        
        validate(self.app_context, SameUserPermission(guest.host))

        if self.app_context.identity() != guest.host:
            raise Forbidden("You are not allowed to access this guest")
        
        if compute:
            achievements = self.achievement_repository.find_not_in([achievement.id for achievement in guest.achievements])
            guest.update_achievements(achievements)
            self.guest_repository.save(guest)
        
        return [dto.AchievementDto.from_entity(achievement) for achievement in guest.achievements]