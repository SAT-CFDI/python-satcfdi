from datetime import date


class DatePeriod:
    # A class from defining a data range to then do date comparisons

    def __init__(self, year: int | None, month: int = None, day: int = None):
        self.year = year
        if year is None and month is not None:
            raise ValueError("Month can't have value if Year doesn't")
        self.month = month
        if month is None and day is not None:
            raise ValueError("Day can't have value if Month doesn't")
        self.day = day

    def __eq__(self, other):
        if isinstance(other, date | DatePeriod):
            for s, o in ((self.year, other.year), (self.month, other.month), (self.day, other.day)):
                if s is not None and s != o:
                    return False
            return True

        return NotImplemented

    def __ne__(self, other):
        if isinstance(other, date | DatePeriod):
            return not self.__eq__(other)

        return NotImplemented

    def __gt__(self, other):
        if isinstance(other, date | DatePeriod):
            for s, o in ((self.year, other.year), (self.month, other.month), (self.day, other.day)):
                if s is not None and s != o:
                    return s > o
            return False

        return NotImplemented

    def __ge__(self, other):
        if isinstance(other, date | DatePeriod):
            return self > other or self == other

        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, date | DatePeriod):
            for s, o in ((self.year, other.year), (self.month, other.month), (self.day, other.day)):
                if s is not None and s != o:
                    return s < o
            return False

        return NotImplemented

    def __le__(self, other):
        if isinstance(other, date | DatePeriod):
            return self < other or self == other

        return NotImplemented

    def __str__(self):
        res = ""
        for n, f in ((self.year, "{:04d}"), (self.month, "-{:02d}"), (self.day, "-{:02d}")):
            if n:
                res += f.format(n)

        return res

    def __hash__(self):
        return (self.year or 0) * 1000 + (self.month or 0) * 100 + (self.day or 0)

    def strftime(self, fmt):
        return (fmt
                .replace("%Y", str(self.year))
                .replace("%m", str(self.month))
                .replace("%d", str(self.day))
                )
