# Domain model

from shared.reference import Ref
from shared.range import Range
from theme.domain.theme import Theme


class Score:
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
        _points = self.points.current
        _time = self.time.current
        _points = (_points * self.elements + points) / (self.elements + 1)
        _time = (_time * self.elements + time) / (self.elements + 1)
        
        self.points.current = _points
        self.time.current = _time
        self.elements += 1

    @property
    def total_points(self) -> float:
        return self.points.current * self.elements
    
    @property
    def total_time(self) -> float:
        return self.time.current * self.elements