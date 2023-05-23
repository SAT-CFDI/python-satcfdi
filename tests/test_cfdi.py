import logging
import os

import pytest

from satcfdi.cfdi import CFDI
from satcfdi.transform import HUSO_HORARIOS
from satcfdi.catalogs import catalog_code, select_all
from tests.constants import CFDI_FILES
from tests.utils import verify_result, XElementPrettyPrinter

module = 'satcfdi'
current_dir = os.path.dirname(__file__)

logging.basicConfig(level=logging.INFO)


def verify_invoice(invoice, path):
    pp = XElementPrettyPrinter()
    verify = verify_result(data=pp.pformat(invoice), filename=f"{path}.pretty.py")
    assert verify

    # verify = verify_result(data=invoice.xml_bytes(pretty_print=True), filename=f"{path}.xml")
    # assert verify

    verify = verify_result(data=invoice.html_str(), filename=f"{path}.html")
    assert verify

    invoice.pdf_write(os.path.join(current_dir, "test_cfdi", f"{path}.pdf"))


@pytest.mark.parametrize('xml_file', CFDI_FILES)
def test_generate_pdf(caplog, xml_file):
    cfdi = CFDI.from_file(
        os.path.join(current_dir, 'cfdi_ejemplos', xml_file)
    )

    verify_invoice(cfdi, xml_file)





