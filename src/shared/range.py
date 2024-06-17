class Range:
    """
    A class to represent a range of values. It keeps track of the minimum and maximum values
    that have been set, and updates them as the current value changes.
    """

    __current: float = 0
    __min: float = 0
    __max: float = 0

    def __init__(self, value: float = 0.0, _min: float = None, _max: float = None):
        self.__current = value
        self.__min = _min if _min is not None else value
        self.__max = _max if _max is not None else value

    @property
    def max(self):
        return self.__max

    @property
    def min(self):
        return self.__min

    @property
    def current(self):
        return self.__current

    @current.setter
    def current(self, value):
        self.__current = value
        self.__min = min(self.__min, value)
        self.__max = max(self.__max, value)
