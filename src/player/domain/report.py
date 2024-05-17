from .score import Score


class Report:
    avg_time: float
    avg_points: float
    top_scores: list[Score]
    bottom_scores: list[Score]

    def __init__(self, avg_time: float, avg_points: float, top_scores: list[Score], bottom_scores: list[Score]) -> None:
        self.avg_time = avg_time
        self.avg_points = avg_points
        self.top_scores = top_scores
        self.bottom_scores = bottom_scores