import os

from satcfdi.cfdi import CFDI
from tests.utils import verify_result

module = 'satcfdi'
current_dir = os.path.dirname(__file__)


def verify_invoice(invoice, path):
    verify = verify_result(
        data=invoice.html_str(
            templates_path=os.path.join(current_dir, 'templates')
        ),
        filename=f"{path}.html"
    )
    assert verify


def test_custom_template():
    xml_file = "cfdv40-ejemplo.xml"
    cfdi = CFDI.from_file(
        os.path.join(current_dir, 'cfdi_ejemplos/comprobante40', xml_file)
    )

    verify_invoice(cfdi, xml_file)
