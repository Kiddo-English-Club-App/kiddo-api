from player.domain.score import Score
from player.domain.achievement import Achievement
from player.domain.guest import Guest
from shared.id import Id
from shared.reference import Ref
from theme.domain.theme import Theme

class DummyRef[T](Ref[T]):
    _val: T
    def __init__(self, id: Id, val: T):
        super().__init__(id)
        self._val = val

    def fetch(self) -> Theme:
        return self._val

def mock_guest(achievements: list[Achievement] = [], host: Id = None, scores: list[int] = []):
    host = host if host else Id()
    return Guest(
        name="John Doe",
        image="image.jpg",
        achievements=achievements,
        host=host,
        scores=scores
    )


def mock_score(points: float = -1, time: float = -1, elements: int = 1):
    import random
    from shared.reference import Ref
    from theme.domain.theme import Theme
    from tests.theme.mocks import mock_theme

    theme = mock_theme()
        
    return Score(
        points=random.random() * 100 if points == -1 else points,
        time=random.random() * 500 if time == -1 else time,
        elements=elements,
        theme=DummyRef[Theme](theme.id, theme)
    )


def mock_achievement(theme):
    import random

    class AnyAchievement(Achievement):

        def key() -> str:
            return "any"

        def check(self, score: Score) -> bool:
            return True

    return AnyAchievement(theme, random.random() * 100, Id())


def mock_achievements(num: int = 5, theme: Theme = None):
    from tests.theme.mocks import mock_theme
    if not theme:
        theme = mock_theme()
    return [mock_achievement(theme) for _ in range(num)]