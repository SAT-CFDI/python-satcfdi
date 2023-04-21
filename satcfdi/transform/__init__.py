import os
from datetime import datetime
from functools import cache
import pytz
from lxml import etree

# noinspection PyUnresolvedReferences
from .catalog import TRANSLATIONS, CATALOGS
from .helpers import SchemaCollector
from .objectify import cfdi_objectify
from .pdf_environment import DefaultPDFEnvironment
from .schemas import cfdi_schemas
from .xmlify import cfdi_xmlify
from .xslt import TRANSFORMS
from .. import SchemaValidationError, CFDIError, Certificate
from ..models import CertificateStore
from ..utils import parser

__all__ = [
    'TRANSLATIONS',
    'CATALOGS',
    'SchemaCollector',
    'cfdi_xmlify',
    'cfdi_schemas',
    'cfdi_objectify',
    'PDF_INIT_TEMPLATE',
    'MEXICO_TZ',
    'get_timezone',
    'validate_xsd',
    'xslt_transform',
    'verify_certificate',
    'moneda_decimales'
]

current_dir = os.path.dirname(__file__)
SCHEMA_ROOT = os.path.join(current_dir, "schemas")
PDF_INIT_TEMPLATE = DefaultPDFEnvironment.get_template("_init.html")
SAT_Certificate_Store = None


def moneda_decimales(moneda):
    return CATALOGS['{http://www.sat.gob.mx/sitio_internet/cfd/catalogos}c_Moneda'][moneda][1]


# America/Chihuahua, America/Mazatlan
HUSO_HORARIOS = {
    "Tiempo del Centro en Frontera": "America/Monterrey",
    "Tiempo del Centro": "America/Mexico_City",
    "Tiempo del Noroeste en Frontera": "America/Matamoros",
    "Tiempo del Pacífico Sonora": "America/Hermosillo",
    "Tiempo del Pacífico en Frontera": "America/Tijuana",
    "Tiempo del Pacífico": "America/La_Paz",
    "Tiempo del Sureste": "America/Cancun",
}


@cache
def _pytz_timezone(tz):
    return pytz.timezone(tz)


def get_timezone(codigo_postal):
    tz = HUSO_HORARIOS[
        CATALOGS['{http://www.sat.gob.mx/sitio_internet/cfd/catalogos}c_CodigoPostal'][codigo_postal][4]
    ]

    return _pytz_timezone(tz)


MEXICO_TZ = _pytz_timezone('America/Mexico_City')


def validate_xsd(xml, base):
    element = etree.fromstring(
        '<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema"/>',
        base_url=os.path.join(SCHEMA_ROOT, "schema.xsd"),
        parser=parser
    )

    for col_s in base:
        etree.SubElement(
            element,
            '{http://www.w3.org/2001/XMLSchema}import',
            attrib={
                "namespace": "",
                "schemaLocation": col_s
            }
        )

    schema = etree.XMLSchema(
        element
    )

    if not schema.validate(xml):
        raise SchemaValidationError(schema.error_log)


@cache
def _get_xslt_transform(path):
    return etree.XSLT(
        etree.parse(
            os.path.join(SCHEMA_ROOT, path)
        )
    )


def xslt_transform(tag, version):
    if trans := TRANSFORMS.get(tag):
        path = trans.format(
            v=version.replace(".", "_")
        )
    else:
        raise CFDIError("XSLT File Transform not found")

    return _get_xslt_transform(path)


def verify_certificate(cert: Certificate, at: datetime) -> bool:
    global SAT_Certificate_Store
    if SAT_Certificate_Store is None:
        SAT_Certificate_Store = CertificateStore.create(os.path.join(current_dir, "CertsProd.zip"))
    return SAT_Certificate_Store.verify_certificate(cert.certificate.to_cryptography(), at=at)
