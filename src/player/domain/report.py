from .score import Score


class Report:
    """
    Report class that represents a summary of the scores of a player.

    It contains the average time, average points, and the top and bottom scores of the player.

    The top and bottom scores are determined by the number of scores to show, which is 3 by default.

    The average time is calculated by summing the time of all scores and dividing by the number of scores.

    The average points is calculated by summing the points of all scores and dividing by the number of scores.

    The top scores are the scores with the highest points, and the bottom scores are the scores with the lowest points.

    If there are fewer scores than the number of scores to show, all scores are included in the report.
    """

    avg_time: float = 0
    avg_points: float = 0
    top_scores: list[Score] = []
    bottom_scores: list[Score] = []

    def __init__(self, scores: list[Score], number: int = 3) -> None:
        if len(scores) == 0:
            return

        number = min(number, len(scores))

        scores.sort(key=lambda x: x.points.current, reverse=True)

        self.avg_time = sum([score.time.current for score in scores]) / len(scores)
        self.avg_points = sum([score.points.current for score in scores]) / len(scores)
        self.top_scores = scores[:number]
        self.bottom_scores = scores[-number:]
