import logging
import os

import pytest
import yaml
from satdigitalinvoice.file_data_managers import DuplicateKeySafeLoader

from satcfdi.models import DatePeriod

from satcfdi import render
from satcfdi.accounting.contabilidad import generar_contabilidad
from satcfdi.cfdi import CFDI
from tests.constants import CFDI_FILES, CONTABILIDAD_FILES, SPEI_FILES
from tests.utils import verify_result, XElementPrettyPrinter, compare_directories

module = 'satcfdi'
current_dir = os.path.dirname(__file__)

logging.basicConfig(level=logging.INFO)


def verify_invoice(invoice, path):
    pp = XElementPrettyPrinter()
    verify = verify_result(data=pp.pformat(invoice), filename=f"{path}.pretty.py")
    assert verify

    verify = verify_result(data=invoice.xml_bytes(pretty_print=True), filename=f"{path}.xml")
    assert verify

    verify = verify_result(data=render.html_str(invoice), filename=f"{path}.html")
    assert verify

    render.pdf_write(invoice, target=os.path.join(current_dir, "test_contabilidad", f"{path}.pdf"))


@pytest.mark.parametrize('xml_file', CONTABILIDAD_FILES)
def test_generate_pdf(caplog, xml_file):
    cfdi = CFDI.from_file(
        os.path.join(current_dir, 'contabilidad_ejemplos', xml_file)
    )

    verify_invoice(cfdi, xml_file)


@pytest.mark.parametrize('xml_file', SPEI_FILES)
def test_generate_spei_pdf(caplog, xml_file):
    cfdi = CFDI.from_file(
        os.path.join(current_dir, 'spei_ejemplos', xml_file)
    )

    verify_invoice(cfdi, xml_file)


def test_generate_contabilidad_empty():
    os.makedirs(os.path.join(current_dir, 'test_contabilidad_electronica/out/empty'), exist_ok=True)

    generar_contabilidad(
        dp=DatePeriod(2024, 2),
        rfc_emisor="CACX7605101P8",
        cuentas={},
        polizas=[],
        folder=os.path.join(current_dir, 'test_contabilidad_electronica/out/empty'),
    )

    assert compare_directories(
        os.path.join(current_dir, 'test_contabilidad_electronica/ref/empty'),
        os.path.join(current_dir, 'test_contabilidad_electronica/out/empty')
    )


def test_generate_contabilidad_simple():
    os.makedirs(os.path.join(current_dir, 'test_contabilidad_electronica/out/simple'), exist_ok=True)

    with open(os.path.join(current_dir, 'contabilidad_electronica', 'cuentas.yaml'), 'r', encoding='utf-8') as f:
        cuentas = yaml.load(f, Loader=DuplicateKeySafeLoader)

    generar_contabilidad(
        dp=DatePeriod(2024, 2),
        rfc_emisor="CACX7605101P8",
        cuentas=cuentas,
        polizas=[],
        folder=os.path.join(current_dir, 'test_contabilidad_electronica/out/simple'),
    )

    assert compare_directories(
        os.path.join(current_dir, 'test_contabilidad_electronica/ref/simple'),
        os.path.join(current_dir, 'test_contabilidad_electronica/out/simple')
    )
