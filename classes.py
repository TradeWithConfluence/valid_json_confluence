from enum import Enum


class CandleSize(Enum):
    MINUTE_1 = ("1m", 60)
    MINUTE_2 = ("2m", 120)
    MINUTE_3 = ("3m", 180)
    MINUTE_5 = ("5m", 300)
    MINUTE_10 = ("10m", 600)
    MINUTE_15 = ("15m", 900)
    MINUTE_20 = ("20m", 1200)
    MINUTE_30 = ("30m", 1800)
    HOUR_1 = ("1h", 3600)
    HOUR_2 = ("2h", 7200)
    HOUR_3 = ("3h", 10800)
    HOUR_4 = ("4h", 14400)
    HOUR_5 = ("5h", 18000)
    HOUR_6 = ("6h", 21600)
    HOUR_12 = ("12h", 43200)
    DAY_1 = ("1d", 86400)
    DAY_2 = ("2d", 172800)
    DAY_3 = ("3d", 259200)
    DAY_5 = ("5d", 432000)
    WEEK_1 = ("1w", 604800)
    WEEK_2 = ("2w", 1209600)
    WEEK_3 = ("3w", 1814400)
    MONTH_1 = ("1mo", 2592000)
    MONTH_2 = ("2mo", 5184000)
    MONTH_3 = ("3mo", 7776000)
    MONTH_6 = ("6mo", 15552000)
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
