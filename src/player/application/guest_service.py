# Guest service
from shared.app_context import AppContext
from shared.id import Id
from shared.permissions import AdminOrSameUserPermission, SameUserPermission, validate
from shared.exceptions import DomainException, NotFound, ValidationError

from ..domain.guest import Guest
from ..domain.guest_repository import IGuestRepository
from ..domain.achievement_repository import IAchievementRepository
from . import dto


class GuestService:
    """
    GuestService provides methods to manage guests in the game. It allows to create, get, delete
    and list guests. It also allows to get the achievements of a guest.

    There is a limit of 3 guests per host.
    """

    GUESTS_LIMIT = 3

    def __init__(
        self,
        guest_repository: IGuestRepository,
        achievement_repository: IAchievementRepository,
        app_context: AppContext,
    ) -> None:
        self.guest_repository = guest_repository
        self.app_context = app_context
        self.achievement_repository = achievement_repository

    def create_guest(self, data: dto.CreateGuestDto) -> dto.GuestDto:
        """
        Create a new guest in the system. It validates that the host is the same as the logged user
        and that the host has less than 3 guests.

        :param data: The data to create the guest.
        :return: The created guest.
        :raises ValidationError: If the host has more than 3 guests.
        :raises Unauthorized: If the host is not the same as the logged user.
        """
        validate(self.app_context, SameUserPermission(data.host))

        guest = Guest(name=data.name, host=data.host, image=data.image)

        guests = self.guest_repository.find_all(data.host)

        if len(guests) >= GuestService.GUESTS_LIMIT:
            raise ValidationError("You can't have more than 3 guests")

        self.guest_repository.save(guest)

        return dto.GuestDto.from_entity(guest)

    def get_guest(self, guest_id: str) -> dto.GuestDto:
        """
        Get a guest by its unique identifier. It validates that the host is the same as the logged user.

        :param guest_id: The unique identifier of the guest.
        :return: The guest if found.
        :raises NotFound: If the guest is not found.
        :raises Unauthorized: If the host is not the same as the logged user.
        """
        guest = self.guest_repository.find_by_id(guest_id)

        if not guest:
            raise NotFound("Guest not found")

        validate(self.app_context, AdminOrSameUserPermission(guest.host))

        return dto.GuestDto.from_entity(guest)

    def get_guests(self, host_id: Id) -> list[dto.GuestDto]:
        """
        Get all guests for a host. It validates that the host is the same as the logged user or an admin.

        :param host_id: The unique identifier of the host.
        :return: A list of guests.
        :raises Unauthorized: If the host is not the same as the logged user or an admin.
        """
        validate(self.app_context, AdminOrSameUserPermission(host_id))

        guests = self.guest_repository.find_all(host_id)
        return [dto.GuestDto.from_entity(guest) for guest in guests]

    def get_guest_achievements(self, guest_id: Id) -> list[dto.AchievementDto]:
        """
        Get all achievements of a guest by its unique identifier. It validates that the host is the same
        as the logged user or an admin.

        :param guest_id: The unique identifier of the guest.
        :return: A list of achievements.
        :raises NotFound: If the guest is not found.
        :raises Unauthorized: If the host is not the same as the logged user or an admin.
        """
        guest = self.guest_repository.find_by_id(guest_id)

        if not guest:
            raise NotFound("Guest not found")

        validate(self.app_context, AdminOrSameUserPermission(guest.host))

        return [
            dto.AchievementDto.from_entity(achievement)
            for achievement in guest.achievements
        ]

    def delete_guest(self, guest_id: Id) -> None:
        """
        Delete a guest by its unique identifier. It validates that the host is the same as the logged user.

        :param guest_id: The unique identifier of the guest.
        :raises NotFound: If the guest is not found.
        :raises Unauthorized: If the host is not the same as the logged user.
        """
        guest = self.guest_repository.find_by_id(guest_id)

        if not guest:
            raise NotFound("Guest not found")

        validate(self.app_context, SameUserPermission(guest.host))

        if not self.guest_repository.delete_by_id(guest_id):
            raise DomainException("Error deleting guest")
