import unittest
from unittest.mock import Mock

from player.application.guest_service import GuestService
from shared.account_type import AccountType
from shared import exceptions
from shared.id import Id
from tests.mocks import mock_app_context
from tests.player.mocks import mock_guest


class TestCreateGuest(unittest.TestCase):
    def test_create_guest(self):
        class CreateGuest:
            host: Id
            name: str
            image: str

        mock = Mock()
        mock.save.return_value = mock_guest()

        host = Id()
        mock = mock_app_context(mock, host, ac_type=AccountType.USER)
        
        data = CreateGuest()
        data.host = host
        data.name = "John Doe"
        data.image = "image"

        service = GuestService(mock, mock, mock)
        guest = service.create_guest(data)

        self.assertEqual(guest.name, data.name)
        self.assertEqual(guest.host, data.host)
        self.assertEqual(guest.image, data.image)
    
    def test_create_guest_unauthorized(self):
        class CreateGuest:
            host: Id
            name: str
            image: str

        mock = Mock()
        mock.save.return_value = mock_guest()

        host = Id()
        mock = mock_app_context(mock, Id(), ac_type=AccountType.USER, authorized=False)
        
        data = CreateGuest()
        data.host = host
        data.name = "John Doe"
        data.image = "image"

        service = GuestService(mock, mock, mock)
        with self.assertRaises(exceptions.Unauthorized):
            service.create_guest(data)

        
class TestGetGuest(unittest.TestCase):

    def test_get_guest(self):
        # Given a guest
        mocked_guest = mock_guest()
        mock = Mock()
        mock.find_by_id.return_value = mocked_guest
        # And a logged in user
        mock = mock_app_context(mock, mocked_guest.host, ac_type=AccountType.USER)
        # When the guest is retrieved
        service = GuestService(mock, mock, mock)
        guest = service.get_guest(mocked_guest.id)
        # Then the guest is returned
        self.assertEqual(mocked_guest.id, guest.id)
        self.assertEqual(mocked_guest.name, guest.name)
        self.assertEqual(mocked_guest.host, guest.host)
        self.assertEqual(mocked_guest.image, guest.image)

    def test_get_guest_not_found(self):
        mock = Mock()
        mock.find_by_id.return_value = None

        mock = mock_app_context(mock, Id(), ac_type=AccountType.USER)
        
        service = GuestService(mock, mock, mock)
        with self.assertRaises(exceptions.NotFound):
            service.get_guest(Id())


class TestGetGuests(unittest.TestCase):

    def test_get_guests(self):
        mocked_guest = mock_guest()
        mock = Mock()
        mock.find_all.return_value = [mocked_guest]

        mock = mock_app_context(mock, mocked_guest.host, ac_type=AccountType.USER)
        
        service = GuestService(mock, mock, mock)
        guests = service.get_guests(mocked_guest.host)

        self.assertEqual(len(guests), 1)
        self.assertEqual(mocked_guest.id, guests[0].id)
        self.assertEqual(mocked_guest.name, guests[0].name)
        self.assertEqual(mocked_guest.host, guests[0].host)
        self.assertEqual(mocked_guest.image, guests[0].image)
    
    def test_get_guests_with_admin(self):
        mocked_guest = mock_guest()
        mock = Mock()
        mock.find_all.return_value = [mocked_guest]

        mock = mock_app_context(mock, Id(), ac_type=AccountType.ADMIN)
        
        service = GuestService(mock, mock, mock)
        guests = service.get_guests(Id())

        self.assertEqual(len(guests), 1)
        self.assertEqual(mocked_guest.id, guests[0].id)
        self.assertEqual(mocked_guest.name, guests[0].name)
        self.assertEqual(mocked_guest.host, guests[0].host)
        self.assertEqual(mocked_guest.image, guests[0].image)
    
    def test_get_guests_unauthorized_with_user(self):
        mocked_guest = mock_guest()
        mock = Mock()
        mock.find_all.return_value = [mocked_guest]

        mock = mock_app_context(mock, Id(), ac_type=AccountType.USER, authorized=False)
        
        service = GuestService(mock, mock, mock)
        with self.assertRaises(exceptions.Unauthorized):
            service.get_guests(Id())