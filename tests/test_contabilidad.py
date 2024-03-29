import logging
import os

import pytest

from satcfdi import render
from satcfdi.cfdi import CFDI
from tests.constants import CFDI_FILES, CONTABILIDAD_FILES, SPEI_FILES
from tests.utils import verify_result, XElementPrettyPrinter

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
