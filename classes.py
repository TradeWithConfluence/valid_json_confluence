from enum import Enum


class CandleSize(Enum):
    MINUTE_1 = ("1m", 60)
    MINUTE_5 = ("5m", 300)
    MINUTE_15 = ("15m", 900)
    MINUTE_30 = ("30m", 1800)
    HOUR_1 = ("1h", 3600)
    HOUR_4 = ("4h", 14400)
    DAY_1 = ("1d", 86400)
    WEEK_1 = ("1w", 604800)
    MONTH_1 = ("1mo", 2592000)
    YEAR_1 = ("1y", 31536000)

    def __new__(cls, value, seconds):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.seconds = seconds
        return obj

    def __lt__(self, other):
        if isinstance(other, CandleSize):
            return self.seconds < other.seconds
        return NotImplemented

    def __le__(self, other):
        if isinstance(other, CandleSize):
            return self.seconds <= other.seconds
        return NotImplemented

    def __gt__(self, other):
        if isinstance(other, CandleSize):
            return self.seconds > other.seconds
        return NotImplemented

    def __ge__(self, other):
        if isinstance(other, CandleSize):
            return self.seconds >= other.seconds
        return NotImplemented
