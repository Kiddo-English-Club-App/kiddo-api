# Domain model

from abc import ABC, abstractmethod
from uuid import UUID
from typing import Callable, Protocol

from shared.id import Id
from shared.reference import Ref
from shared.range import Range


class Theme(Protocol):
    """
    Theme is a protocol that defines the contract for a theme in the game.

    It's used to represent only the necessary information about a theme and avoing
    the need to import the entire Theme class.
    """

    id: UUID
    name: str


class Score(Protocol):
    """
    Score is a protocol that defines the contract for a score in the game.

    It's used to represent only the necessary information about a score and avoing
    the need to import the entire Score class.
    """

    points: Range
    time: Range
    elements: int
    theme: Ref[Theme]
    total_points: float
    total_time: float


class Achievement(ABC):
    """
    Achievement class that defines the contract for an achievement in the game.

    An achievement is a goal that the player can achieve by playing the game.
    """

    id: Id
    theme: Ref[Theme]
    value: float

    def __init__(self, theme: Ref[Theme], value: float, id: Id = None):
        self.id = id if isinstance(id, Id) else Id(id)
        self.theme = theme
        self.value = value

    @abstractmethod
    def key() -> str:
        """
        Key to identify the type of achievement in the factory

        :return: A string with the key of the achievement
        """
        pass

    @abstractmethod
    def check(self, score: Score) -> bool:
        """
        Check if the score meets the requirements of the achievement.

        :param score: The score of the player
        :return: True if the score meets the requirements, False otherwise
        """
        pass

    def __eq__(self, value: object) -> bool:
        return isinstance(value, Achievement) and value.id == self.id


class PointsAchievement(Achievement):
    """
    Achievement class that checks if the player has achieved a certain number of points in a theme.
    """

    def key() -> str:
        return "points"

    def check(self, score: Score) -> bool:
        value = score.points.current * score.elements
        return value >= self.value and score.theme.id == self.theme.id

    def __str__(self) -> str:
        return f"Complete {self.theme.value.name} with at least {self.value} points"


class TimeAchievement(Achievement):
    """
    Achievement class that checks if the player has completed a theme in a certain amount of time.
    """

    def key() -> str:
        return "min_time"

    def check(self, score: Score) -> bool:
        in_range = score.time.min <= self.value and score.time.min > 0
        is_theme = score.theme.id == self.theme.id
        return in_range and is_theme

    def __str__(self) -> str:
        return f"Complete {self.theme.value.name} in less than {self.value} seconds"


class NGamesOfThemeAchievement(Achievement):
    """
    Achievement class that checks if the player has played a theme a determined number of times.
    """

    def key() -> str:
        return "n_games"

    def check(self, score: Score) -> bool:
        return score.elements >= self.value and score.theme.id == self.theme.id

    def __str__(self) -> str:
        return f"Complete {self.theme.value.name} {self.value} times"


class AchievementFactory:
    """
    AchievementFactory class that creates achievements based on a key.
    A key is a string that identifies the type of achievement to create.

    The factory uses a dictionary to store the creators of each type of achievement.

    The factory is a singleton, so it can be accessed from anywhere in the code.

    The registration of new creators can be done by setting a new item in the factory as
    follows:

    ```python
    factory = AchievementFactory() # Get the factory instance (singleton)

    def create_new_achievement(theme: Ref[Theme], value: float, id: Id = None) -> Achievement:
        # Create a new achievement
        return PointsAchievement(theme=theme, value=value, id=id)

    factory["new_achievement"] = create_new_achievement # Register the new creator
    ```
    """

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(AchievementFactory, cls).__new__(cls)
        return cls._instance

    __creators: dict = {
        PointsAchievement.key(): PointsAchievement,
        TimeAchievement.key(): TimeAchievement,
        NGamesOfThemeAchievement.key(): NGamesOfThemeAchievement,
    }

    def __setitem__(self, key: str, creator: Callable[..., Achievement]):
        self.__creators[key] = creator

    def __getitem__(self, key: str) -> Callable[..., Achievement]:
        return self.__creators[key]

    def create(
        self, key: str, theme: Ref[Theme], value: float, id: Id = None
    ) -> Achievement:
        return self.__creators[key](theme=theme, value=value, id=id)
