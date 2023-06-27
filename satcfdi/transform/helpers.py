import logging
from decimal import Decimal

from lxml import etree
from lxml.etree import QName

from ..exceptions import CFDIError
from ..models import Code
from ..utils import iterate

logger = logging.getLogger(__name__)
TEXT_KEY = "_text"
_ = iterate


class SchemaCollector:
    def __init__(self):
        self.nsmap = {}
        self.schemas = []
        self.base = set()

    def add_schema(self, schema):
        if schema not in self.schemas:
            self.schemas.append(schema)

    def add_map(self, tns_alias, tns):
        if tns_alias in self.nsmap:
            if not self.nsmap[tns_alias] == tns:
                raise CFDIError("TNS Alias already registered with a different alias")
        else:
            self.nsmap[tns_alias] = tns

    def add_base(self, base):
        self.base.add(base)


class Xint(int):
    """
    An int class that knows the original value that was used to create it
    """

    def __new__(cls, value: str):
        self = int.__new__(cls, value)
        self.value = value
        return self

    def __str__(self):
        return self.value


def fmt_decimal(d):
    if isinstance(d, Decimal):
        return d.__format__("f")
    return str(d)


def simple_element(_tag, nsmap=None, text=None):
    el = etree.Element(_tag, nsmap=nsmap)
    el.text = text
    return el


def default_objectify(cls, node):
    self = cls()
    self.tag = node.tag

    def add_attributes(n, target):
        for k, v in n.attrib.items():
            target[k] = v

        text = n.text
        if text:
            text = n.text.strip()
            if text:
                target[TEXT_KEY] = text

    def add_elements(n, target):
        for el in n:
            new = cls()
            name = QName(el.tag).localname
            add_attributes(el, target=new)
            add_elements(el, target=new)

            current = target.get(name)
            if current is None:
                target[name] = new
            elif isinstance(current, cls):
                target[name] = [current, new]
            else:
                current.append(new)

    add_attributes(node, target=self)
    add_elements(node, target=self)

    return self


def impuesto_index(attrib, attribute_name):
    impuesto = attrib[attribute_name]
    ext = attribute_name[8:]
    if tipo_factor := attrib.get('TipoFactor' + ext):
        impuesto += "|" + tipo_factor
        if tasa_cuota := attrib.get('TasaOCuota' + ext):
            impuesto += "|" + Decimal(tasa_cuota).__format__(".6f")

    return impuesto


def strcode(data):
    if isinstance(data, Code):
        return data.code
    return data



