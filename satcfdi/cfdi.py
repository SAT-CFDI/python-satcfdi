import logging
import os
import lxml.etree
from satcfdi.models import Signer

from .exceptions import CFDIError
from .transform import *
from .transform.helpers import fmt_decimal
from .xelement import XElement

current_dir = os.path.dirname(__file__)
logger = logging.getLogger(__name__)

VERIFICA_CFDI = "https://verificacfdi.facturaelectronica.sat.gob.mx/default.aspx"
VERIFICA_RETENCION = "https://prodretencionverificacion.clouda.sat.gob.mx/"


class CFDI(XElement):
    def to_xml(self, validate=False, include_schema_location=True) -> lxml.etree.Element:
        return super().to_xml(validate, include_schema_location)

    def xml_write(self, target, pretty_print=False, xml_declaration=True, validate=False, include_schema_location=True) -> bytes:
        return super().xml_write(target, pretty_print=pretty_print, xml_declaration=xml_declaration, validate=validate, include_schema_location=include_schema_location)

    def xml_bytes(self, pretty_print=False, xml_declaration=True, validate=False, include_schema_location=True) -> bytes:
        return super().xml_bytes(pretty_print=pretty_print, xml_declaration=xml_declaration, validate=validate, include_schema_location=include_schema_location)

    def process(self, validate=False) -> 'CFDI':
        return CFDI.from_xml(self.to_xml(validate=validate))

    def copy(self) -> 'CFDI':
        cfdi = CFDI(super().copy())
        cfdi.tag = self.tag
        return cfdi

    @property
    def verifica_url(self) -> str:
        match self.tag:
            case '{http://www.sat.gob.mx/cfd/3}Comprobante' | '{http://www.sat.gob.mx/cfd/4}Comprobante':
                base_url = VERIFICA_CFDI
                q = {
                    "id": self['Complemento']['TimbreFiscalDigital']["UUID"],
                    "re": self['Emisor']["Rfc"],
                    "rr": self['Receptor']["Rfc"],
                    "tt": fmt_decimal(self["Total"]),
                    "fe": self["Sello"][-8:]
                }

            case '{http://www.sat.gob.mx/esquemas/retencionpago/1}Retenciones':
                base_url = VERIFICA_RETENCION
                q = {
                    "id": self["Complemento"]["TimbreFiscalDigital"]["UUID"],
                    "re": self['Emisor']["RFCEmisor"],
                    "tt": fmt_decimal(self['Totales']["MontoTotOperacion"]),
                    "fe": self["Sello"][-8:]
                }
                match self['Receptor']['Nacionalidad']:
                    case "Nacional":
                        q["rr"] = self['Receptor']['Nacional']["RFCRecep"]
                    case "Extranjero":
                        if nr := self['Receptor']['Extranjero'].get("NumRegIdTrib"):
                            q["nr"] = nr

            case '{http://www.sat.gob.mx/esquemas/retencionpago/2}Retenciones':
                base_url = VERIFICA_RETENCION
                q = {
                    "id": self["Complemento"]["TimbreFiscalDigital"]["UUID"],
                    "re": self['Emisor']["RfcE"],
                    "tt": fmt_decimal(self['Totales']["MontoTotOperacion"]),
                    "fe": self["Sello"][-8:]
                }
                match self['Receptor']['NacionalidadR']:
                    case "Nacional":
                        q["rr"] = self['Receptor']['Nacional']["RfcR"]
                    case "Extranjero":
                        if nr := self['Receptor']['Extranjero'].get("NumRegIdTribR"):
                            q["nr"] = nr

            case _:
                raise CFDIError("No Verification URL found")

        if base_url:
            return base_url + "?" + "&".join(f"{k}={v}" for k, v in q.items())

    def cadena_original(self):
        transform = xslt_transform(self.tag, self['Version'])
        xml = super().to_xml()
        return str(transform(xml))

    def sign(self, signer: Signer):
        self['NoCertificado'] = signer.certificate_number
        self['Certificado'] = signer.certificate_base64()
        self['Sello'] = signer.sign_sha256(
            self.cadena_original().encode()
        )
