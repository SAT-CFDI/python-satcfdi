import enum
from collections.abc import Sequence, Mapping


class ScalarMap(dict):
    pass


def iterate(item):
    if isinstance(item, str | bytes | ScalarMap):
        return [item]
    if isinstance(item, Mapping):
        return item.values()
    if isinstance(item, Sequence):
        return item
    if item is None:
        return []
    return [item]


class StrEnum(str, enum.Enum):
    def __str__(self):
        return str(self.value)

