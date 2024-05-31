import unittest
from unittest.mock import Mock

from .mocks import mock_guest, mock_achievements, mock_score
from player.application.achievement_service import AchievementService



class TestValidateGuestAchievements(unittest.TestCase):

    def test_validate_guest_achievements_with_no_achievements(self):
        mock = Mock()
        # Given a guest with no achievements
        guest = mock_guest()
        # And a list of achievements
        achievements = mock_achievements()
        mock.find_not_in.return_value = achievements
        # When the guest achievements are validated
        achievement_service = AchievementService(mock)
        score = mock_score()

        result = achievement_service.validate_guest_achievements(guest, score)
        # Then the achievements are returned
        self.assertEqual(result, achievements)

    def test_validate_guest_achievements_with_achievements(self):
        mock = Mock()
        # Given a guest with achievements
        guest = mock_guest(mock_achievements(5))
        # And a list of achievements
        achievements = mock_achievements(2)
        mock.find_not_in.return_value = achievements
        # When the guest achievements are validated
        achievement_service = AchievementService(mock)
        score = mock_score()

        result = achievement_service.validate_guest_achievements(guest, score)
        self.assertEqual(result, achievements)
    



        