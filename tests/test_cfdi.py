import logging
import os

import pytest

from satcfdi.cfdi import CFDI
from satcfdi.transform import HUSO_HORARIOS
# noinspection PyUnresolvedReferences
from satcfdi.transform.catalog import CATALOGS
from satcfdi.transform.helpers import catalog_code
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


def test_catalog(caplog):
    code = catalog_code('{http://www.sat.gob.mx/sitio_internet/cfd/catalogos}c_FormaPago', "24")
    assert code.code == "24"
    assert code.description == 'Confusión'

    code = catalog_code('{http://www.sat.gob.mx/sitio_internet/cfd/catalogos}c_FormaPago', "-1")
    assert code.code == "-1"
    assert code.description is None
    for record in caplog.records:
        assert record.args == ('{http://www.sat.gob.mx/sitio_internet/cfd/catalogos}c_FormaPago -1',)


def test_huso_horario():
    c = CATALOGS['{http://www.sat.gob.mx/sitio_internet/cfd/catalogos}c_CodigoPostal']
    for i in c.values():
        assert i[4] in HUSO_HORARIOS


