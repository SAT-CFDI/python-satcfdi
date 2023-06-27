import os

from satcfdi.accounting import SatCFDI

from satcfdi.cfdi import CFDI

current_dir = os.path.dirname(__file__)


def test_satcfdi():
    file = os.path.join(current_dir, 'cfdi_ejemplos', 'comprobante40/cfdv40-aerolineas.xml')
    c = CFDI.from_file(file)
    d = SatCFDI(c)

    assert d.payments == []
    assert d.relations == []

    assert d["Emisor"]["Rfc"] == "AAA010101AAA"
