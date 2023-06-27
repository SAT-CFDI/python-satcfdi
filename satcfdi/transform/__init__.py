import os
from datetime import datetime
from functools import cache
import pytz
from lxml import etree

from .helpers import SchemaCollector
from .objectify import cfdi_objectify
from .schemas import cfdi_schemas
from .xmlify import cfdi_xmlify
from .xslt import TRANSFORMS
from ..exceptions import SchemaValidationError, CFDIError
from ..models import CertificateStore, Certificate
from ..utils import parser
from ..catalogs import codigo_postal_uso_horario

__all__ = [
    'SchemaCollector',
    'cfdi_xmlify',
    'cfdi_schemas',
    'cfdi_objectify',
    'MEXICO_TZ',
    'get_timezone',
    'validate_xsd',
    'xslt_transform',
    'verify_certificate'
]

current_dir = os.path.dirname(__file__)
SCHEMA_ROOT = os.path.join(current_dir, "schemas")
SAT_Certificate_Store = None

HUSO_HORARIOS = {
    'Tiempo del Centro': "America/Mexico_City",
    'Tiempo del Centro en Frontera': "America/Monterrey",
    'Tiempo del Noroeste': "America/Matamoros",
    'Tiempo del Pacífico': "America/La_Paz",
    'Tiempo del Sureste': "America/Cancun"
}


@cache
def _pytz_timezone(tz):
    return pytz.timezone(tz)


def get_timezone(codigo_postal):
    tz = HUSO_HORARIOS[
        codigo_postal_uso_horario(codigo_postal)
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
