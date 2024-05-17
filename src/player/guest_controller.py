from uuid import UUID
from flask import Blueprint, request
from dependify import inject

from player.application.guest_service import GuestService, dto

controller = Blueprint('guest', __name__, url_prefix='/guests')
# TODO: Add authentication middleware

@controller.get('/')
@inject
def get_guests(service: GuestService):
    # TODO: read host_id from token
    host_id = service.app_context.identity()
    return [guest.model_dump() for guest in service.get_guests(host_id)]


@controller.get('/<uuid:guest_id>')
@inject
def get_guest(service: GuestService, guest_id: UUID):
    return service.get_guest(guest_id).model_dump()


@controller.post('/')
@inject
def create_guest(service: GuestService):
    data = dto.CreateGuestDto(**request.json)
    return service.create_guest(data).model_dump()


@controller.get('/<uuid:guest_id>/achievements')
@inject
def get_guest_achievements(service: GuestService, guest_id: UUID):
    compute = request.args.get('compute', '0')
    compute = compute == '1'
    achievements = service.get_guest_achievements(guest_id, compute)
    return [achievement.model_dump() for achievement in achievements]