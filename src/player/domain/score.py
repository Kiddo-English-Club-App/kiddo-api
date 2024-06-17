# Domain model

from shared.reference import Ref
from shared.range import Range
from theme.domain.theme import Theme


class Score:
    """
    Score class that represents the score of a player in the game. It contains the points and time
    of the player's performance in a theme.

    The points and time are represented as a range, which allows the score to be updated with new
    points and time and calculate the average of all the scores, which is useful for the report and
    achievements.

    The elements attribute is used to keep track of the number of scores that were added to the score,
    so the average can be calculated correctly and avoid the need to iterate over all scores every time
    the average is needed.

    The theme attribute is a reference to the theme that the score is related to. It's used to identify
    the theme of the score and avoid the need to import the entire Theme class.
    """

    points: Range
    time: Range
    elements: int
    theme: Ref[Theme]

    def __init__(
        self,
        theme: Ref[Theme],
        points: float | int | Range = Range(0),
        time: float | int | Range = Range(0),
        elements: int = 1,
    ):
        if isinstance(points, (float, int)):
            points = Range(points)

        if isinstance(time, (float, int)):
            time = Range(time)

        self.points = points
        self.time = time
        self.elements = elements
        self.theme = theme

    def update(self, points: int, time: float) -> None:
        """
        Update the score with new points and time. It calculates the average points and time
        based on the new values and the number of elements. It also increments the number of
        elements.

        :param points: The new points to add to the score.
        :param time: The new time to add to the score.
        """
        _points = self.points.current
        _time = self.time.current
        _points = (_points * self.elements + points) / (self.elements + 1)
        _time = (_time * self.elements + time) / (self.elements + 1)

        self.points.current = _points
        self.time.current = _time
        self.elements += 1

    @property
    def total_points(self) -> float:
        """
        Calculate the total points of the score by multiplying the average points by the number of elements.
        """
        return self.points.current * self.elements

    @property
    def total_time(self) -> float:
        """
        Calculate the total time of the score by multiplying the average time by the number of elements.
        """
        return self.time.current * self.elements
