import logging
from decimal import Decimal
from lxml import etree
from lxml.etree import QName

from .. import CFDIError
from ..models import Code
# noinspection PyUnresolvedReferences
from ..transform.catalog import TRANSLATIONS, CATALOGS
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
    tipo_factor = attrib.get('TipoFactor' + ext)
    if tipo_factor:
        impuesto += "|" + tipo_factor
        tasa_cuota = attrib.get('TasaOCuota' + ext)
        if tasa_cuota:
            impuesto += "|" + Decimal(tasa_cuota).__format__(".6f")

    return impuesto


def catalog_code(*args):
    desc = CATALOGS
    code = args[1]
    try:
        for arg in args:
            if arg is None:  # like Postal Code
                desc = None
                continue
            desc = desc[arg]
    except KeyError:
        logger.error("Key Not found: %s", " ".join(args))
        desc = None

    return Code(code, desc)


def strcode(data):
    if isinstance(data, Code):
        return data.code
    return data


def format_address_raw(calle, num_exterior, num_interior, referencia, colonia, municipio, localidad, estado, pais, codigo_postal):
    parts = []

    calle_num = None
    if calle or num_exterior or num_interior:
        if num_exterior:
            calle_num = f"{calle} #{num_exterior}"
        else:
            calle_num = f"{calle}"

        if num_interior:
            calle_num = f"{calle_num}, int. #{num_interior}"

    if colonia:
        if calle_num:
            parts.append(f"{calle_num}, {colonia}")
        else:
            parts.append(f"{colonia}")

    if referencia:
        parts.append(f"{referencia}")

    if localidad and localidad != municipio:
        parts.append(f"{localidad}")

    if municipio:
        parts.append(f"{municipio}, {estado} {codigo_postal}")
    else:
        parts.append(f"{estado} {codigo_postal}")

    parts.append(f"{pais}")
    return "\n".join(parts)


def format_address(k):
    return format_address_raw(
        calle=k["Calle"],
        num_exterior=k.get("NumeroExterior"),
        num_interior=k.get("NumeroInterior"),
        referencia=desc(k.get("Referencia")),
        colonia=desc(k.get("Colonia")),
        municipio=desc(k.get("Municipio")),
        localidad=desc(k.get("Localidad")),
        estado=desc(k["Estado"]),
        pais=desc(k["Pais"]),
        codigo_postal=k["CodigoPostal"]
    )


def split_at_upper(word: str):
    def split_at_upper_itr(word: str):
        piu = None
        for w in word:
            niu = w.isupper()
            if piu == False:
                if niu:
                    yield " "

            if piu is None:
                yield w.upper()
            else:
                yield w
            piu = niu

    return "".join(split_at_upper_itr(word))


def trans(k):
    res = TRANSLATIONS.get(k)
    if res is None:
        res = split_at_upper(k)
    return res


def desc(s):
    if isinstance(s, Code):
        return s.description
    return s
