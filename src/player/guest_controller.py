from uuid import UUID
from flask import Blueprint, request
from dependify import inject


from shared.id import Id
from player.application.guest_service import GuestService, dto
from .dto import GuestDto, CreateGuestDto, AchievementDto


controller = Blueprint('guest', __name__, url_prefix='/guests')

@controller.get('/')
@inject
def get_guests(service: GuestService):
    host_id = service.app_context.identity()
    return [GuestDto.load(guest).model_dump() 
            for guest in service.get_guests(host_id)]
    

@controller.get('/<uuid:guest_id>')
@inject
def get_guest(service: GuestService, guest_id: UUID):
    guest_id = Id(guest_id)
    guest = service.get_guest(guest_id)
    return GuestDto.load(guest).model_dump()


@controller.post('/')
@inject
def create_guest(service: GuestService):
    data = CreateGuestDto(**request.json, host=service.app_context.identity())
    guest = service.create_guest(data)
    return GuestDto.load(guest).model_dump(), 201
    


@controller.get('/<uuid:guest_id>/achievements')
@inject
def get_guest_achievements(service: GuestService, guest_id: UUID):
    achievements = service.get_guest_achievements(Id(guest_id))
    return [AchievementDto.load(achievement).model_dump() 
            for achievement in achievements]


@controller.delete('/<uuid:guest_id>')
@inject
def delete_guest(service: GuestService, guest_id: UUID):
    service.delete_guest(Id(guest_id))
    return {
        'message': 'Guest deleted'
    }