# Domain model
from shared.id import Id
from shared.name import NameStr
from .score import Score
from .achievement import Achievement


class Guest:
    """
    Guest class that represents a player in the game. It's called guests
    because they are not registered users, they are accounts created by a
    host inside of its own account, so they are guests in the system. They
    don't have an email or password, they are only accessible by the host.

    A guest can play the game, earn scores and achievements.

    A host can have multiple guests, but a guest can only belong to one host.

    It's not referenced by the Account class because not all accounts have guests,
    it will only be created if the host decides to create a guest account.
    """

    id: Id
    name: NameStr
    host: Id
    image: str
    scores: list[Score]
    achievements: list[Achievement]

    def __init__(
        self,
        name: str,
        image: str,
        host: Id,
        scores: list[Score] = [],
        achievements: list[Achievement] = [],
        id: Id = None,
    ) -> None:
        self.id = id if isinstance(id, Id) else Id()
        self.name = NameStr(name)
        self.image = image
        self.scores = scores
        self.host = host
        self.achievements = achievements

    def get_score_by_theme(self, theme_id: Id) -> Score:
        """
        Get the score for a specific theme by its unique identifier.

        :param theme_id: The unique identifier of the theme.
        :return: The score if found, None otherwise.
        """
        for score in self.scores:
            if score.theme.id == theme_id:
                return score
        return None
