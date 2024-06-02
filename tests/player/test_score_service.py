import unittest
from unittest.mock import Mock

from player.application.score_service import ScoreService
from shared.account_type import AccountType
from shared import exceptions
from shared.id import Id
from tests.mocks import mock_app_context
from tests.player.mocks import mock_guest, DummyRef, mock_score
from tests.theme.mocks import mock_theme
from theme.domain.theme import Theme


class TestAddScore(unittest.TestCase):

    def test_add_score(self):
        # Given a guest and an app context
        mock = Mock()
        id = Id()
        mock = mock_app_context(mock, id, AccountType.USER)
        guest = mock_guest(host=id)
        mock.find_by_id.return_value = guest
        mock.validate_guest_achievements.return_value = []
        theme = mock_theme()
        mock.ref.return_value = DummyRef[Theme](theme.id, theme)
        # And a score
        class AddScore:
            guest_id: Id = guest.id
            theme_id: Id = theme.id
            points: int = 10
            time: int = 100
        
        data = AddScore()

        # When the score is added
        service = ScoreService(mock, mock, mock, mock)

        # Then the score is returned
        score = service.add_score(data)

        self.assertEqual(score.guest_id, data.guest_id)
        self.assertEqual(score.theme_id, data.theme_id)
        self.assertEqual(score.points, data.points)
        self.assertEqual(score.time, data.time)
    
    def test_add_score_with_existing_score(self):
        # Given a guest and an app context
        mock = Mock()
        id = Id()
        mock = mock_app_context(mock, id, AccountType.USER)
        guest = mock_guest(host=id, scores=[mock_score()])
        mock.find_by_id.return_value = guest
        mock.validate_guest_achievements.return_value = []
        theme = mock_theme()
        mock.ref.return_value = DummyRef[Theme](theme.id, theme)
        # And a score
        class AddScore:
            guest_id: Id = guest.id
            theme_id: Id = theme.id
            points: int = 10
            time: int = 100
        
        data = AddScore()

        # When the score is added
        service = ScoreService(mock, mock, mock, mock)
        score = service.add_score(data)

        # Then the score is returned
        self.assertEqual(score.guest_id, data.guest_id)
        self.assertEqual(score.theme_id, data.theme_id)
        self.assertEqual(score.points, data.points)
        self.assertEqual(score.time, data.time)
        self.assertEqual(len(guest.scores), 2)
    
    def test_add_score_when_guest_not_found(self):
        # Given a guest and an app context
        mock = Mock()
        id = Id()
        mock = mock_app_context(mock, id, AccountType.USER)
        mock.find_by_id.return_value = None
        # And a score
        class AddScore:
            guest_id: Id = Id()
            theme_id: Id = Id()
            points: int = 10
            time: int = 100

        # When the score is added
        service = ScoreService(mock, mock, mock, mock)

        # Then an exception is raised
        with self.assertRaisesRegex(exceptions.NotFound, "Guest not found"):
            service.add_score(AddScore())

    def test_add_score_with_different_host(self):
        # Given a guest and an app context
        mock = Mock()
        id = Id()
        mock = mock_app_context(mock, id, AccountType.USER)
        guest = mock_guest(host=Id())
        mock.find_by_id.return_value = guest
        # And a score
        class AddScore:
            guest_id: Id = guest.id
            theme_id: Id = Id()
            points: int = 10
            time: int = 100

        # When the score is added
        service = ScoreService(mock, mock, mock, mock)

        # Then an exception is raised
        with self.assertRaises(exceptions.Unauthorized):
            service.add_score(AddScore())


class TestCreateReport(unittest.TestCase):

    def test_create_report(self):
        # Given a guest and an app context
        mock = Mock()
        id = Id()
        mock = mock_app_context(mock, id, AccountType.USER)
        scores = [mock_score(80.0, 300.0, 5) for _ in range(6)]
        average_points = 80.0
        average_time = 300.0
        guest = mock_guest(host=id, scores=scores)
        mock.find_by_id.return_value = guest
        # When the report is created
        service = ScoreService(mock, mock, mock, mock)
        report = service.create_report(guest.id)
        # Then the report contains the average points and time
        self.assertEqual(report.avg_points, average_points)
        self.assertEqual(report.avg_time, average_time)
    
    def test_create_report_when_guest_not_found(self):
        # Given a not existing guest and an app context
        mock = Mock()
        id = Id()
        mock = mock_app_context(mock, id, AccountType.USER)
        mock.find_by_id.return_value = None
        # When the report is created
        service = ScoreService(mock, mock, mock, mock)
        # Then a NotFound exception is raised
        with self.assertRaisesRegex(exceptions.NotFound, "Guest not found"):
            service.create_report(Id())
    
    def test_create_report_with_different_host(self):
        # Given a guest, an app context and a different host
        mock = Mock()
        id = Id()
        mock = mock_app_context(mock, id, AccountType.USER)
        guest = mock_guest(host=Id())
        mock.find_by_id.return_value = guest
        # When the report is created
        service = ScoreService(mock, mock, mock, mock)
        # Then an Unauthorized exception is raised
        with self.assertRaises(exceptions.Unauthorized):
            service.create_report(guest.id)


