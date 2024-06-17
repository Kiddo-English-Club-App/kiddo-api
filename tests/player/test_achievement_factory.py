import unittest
from player.domain.achievement import AchievementFactory


class TestAchievementFactory(unittest.TestCase):

    def test_singleton(self):
        factory1 = AchievementFactory()
        factory2 = AchievementFactory()
        self.assertIs(factory1, factory2)