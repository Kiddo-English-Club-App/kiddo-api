def init():
    from dependify import register
    from .guest_service import GuestService

    register(GuestService)