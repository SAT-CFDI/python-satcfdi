import json
from lxml import etree

from .printer import Representable
from .transform import SchemaCollector, cfdi_schemas, validate_xsd
from .utils import ScalarMap
from .transform.objectify import cfdi_objectify
from .transform.xmlify import cfdi_xmlify

parser = etree.XMLParser(no_network=True, remove_comments=True, remove_blank_text=True)


class XElement(ScalarMap, Representable):
    def to_xml(self, validate=False, include_schema_location=False) -> etree.Element:
        xml = cfdi_xmlify[self.tag](self)

        if validate or include_schema_location:
            col = SchemaCollector()
            cfdi_schemas[self.tag](col, self)
            if validate:
                validate_xsd(xml, col.base)
            if include_schema_location:
                xml.attrib['{http://www.w3.org/2001/XMLSchema-instance}schemaLocation'] = " ".join(col.schemas)

        return xml

    def process(self, validate=False) -> 'XElement':
        return XElement.from_xml(self.to_xml(validate=validate))

    @classmethod
    def from_xml(cls, xml_root) -> 'XElement':
        obj = cfdi_objectify[xml_root.tag](cls, xml_root)
        if not isinstance(obj, XElement):
            obj = XElement(obj)
            obj.tag = xml_root.tag
        return obj

    @classmethod
    def from_file(cls, filename) -> 'XElement':
        return cls.from_xml(etree.parse(filename, parser=parser).getroot())

    @classmethod
    def from_string(cls, string) -> 'XElement':
        return cls.from_xml(etree.fromstring(string, parser=parser))

    def xml_write(self, target, pretty_print=False, xml_declaration=True):
        xml = self.to_xml()
        et = etree.ElementTree(xml)
        et.write(
            target,
            xml_declaration=xml_declaration,
            encoding="UTF-8",
            pretty_print=pretty_print
        )

    def xml_bytes(self, pretty_print=False, xml_declaration=True, validate=False, include_schema_location=False) -> bytes:
        xml = self.to_xml(validate=validate, include_schema_location=include_schema_location)
        return etree.tostring(xml, xml_declaration=xml_declaration, encoding="UTF-8", pretty_print=pretty_print)

    def json_write(self, target, pretty_print=False):
        if isinstance(target, str):
            with open(target, 'w') as f:
                json.dump(self, f, ensure_ascii=False, default=str, indent=2 if pretty_print else None)
                return

        json.dump(self, target, ensure_ascii=False, default=str, indent=2 if pretty_print else None)

    def json_str(self, pretty_print=False) -> str:
        return json.dumps(self, ensure_ascii=False, default=str, indent=2 if pretty_print else None)

    def __repr__(self):
        # return '%s.%s(%s)' % (self.__class__.__module__,
        #                       self.__class__.__qualname__,
        #                       f'{repr(self.tag)}, {super().__repr__()}')
        return '%s(%s)' % (
            self.__class__.__qualname__,
            f'{dict.__repr__(self)}'
        )
