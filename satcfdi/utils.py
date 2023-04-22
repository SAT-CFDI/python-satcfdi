import enum
from collections.abc import Sequence, Mapping

from lxml import etree

parser = etree.XMLParser(no_network=True, remove_comments=True, remove_blank_text=True, huge_tree=True, collect_ids=False, remove_pis=True)


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
        return self.value


class CodeEnum(str, enum.Enum):
    def __str__(self):
        return str(self.value) + ' - ' + self.name
