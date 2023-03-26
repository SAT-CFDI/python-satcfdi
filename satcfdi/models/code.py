import logging


logger = logging.getLogger(__name__)


class Code:
    def __init__(self, code, description):
        self.code = code
        self.description = description

    def __str__(self):
        if self.description is None:
            return self.code
        if isinstance(self.description, list):
            return str(self.code) + " - " + "; ".join(self.description)
        return str(self.code) + " - " + str(self.description)

    def __repr__(self):
        # return '%s.%s(%s)' % (self.__class__.__module__,
        #                       self.__class__.__qualname__,
        #                       f'{repr(self.code)}, {repr(self.description)}')

        return '%s(%s)' % (
            self.__class__.__qualname__,
            f'{repr(self.code)}, {repr(self.description)}'
        )

    def __eq__(self, other):
        if isinstance(other, Code):
            return self.code == other.code
        if isinstance(other, str) or isinstance(other, int):
            return self.code == other
        return NotImplemented

    def __hash__(self):
        return self.code.__hash__()


