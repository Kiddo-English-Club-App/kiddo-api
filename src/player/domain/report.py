from .score import Score


class Report:
    avg_time: float = 0
    avg_points: float = 0
    top_scores: list[Score] = []
    bottom_scores: list[Score] = []

    def __init__(self, scores: list[Score], number: int = 3) -> None:
        if len(scores) == 0:
            return
        
        number = min(number, len(scores))
        
        scores.sort(key=lambda x: x.points.current, reverse=True)

        self.avg_time = sum([score.time.current for score in scores])/len(scores)
        self.avg_points = sum([score.points.current for score in scores])/len(scores)
        self.top_scores = scores[:number]
        self.bottom_scores = scores[-number:]