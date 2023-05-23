import os

from satcfdi.create.cfd.catalogos import Impuesto
from satcfdi.transform import HUSO_HORARIOS
from satcfdi.transform import moneda_decimales
from satcfdi.transform.helpers import catalog_code, select_all

module = 'satcfdi'
current_dir = os.path.dirname(__file__)


def test_catalog():
    _impuestos = {
        "ISR": "001",
        "IVA": "002",
        "IEPS": "003",
    }

    impuesto = "ISR"
    r = _impuestos.get(impuesto, impuesto)
    assert r == '001'

    # v = Impuesto(impuesto)
    # print(v)

    # search enum by name without throwing exception
    v = Impuesto['IVA']
    assert v == Impuesto.IVA
    assert v.value == '002'
    assert v == '002'

    v = Impuesto.get('002', '002')
    assert v == Impuesto.IVA


def test_moneda():
    res = moneda_decimales('MXN')
    assert res == 2


def test_catalog(caplog):
    # {http://www.sat.gob.mx/sitio_internet/cfd/catalogos}c_FormaPago Td5a9fdcc78ab4510aee9addb48db94cf47a91f1b
    code = catalog_code('Td5a9fdcc78ab4510aee9addb48db94cf47a91f1b', "24")
    assert code.code == "24"
    assert code.description == 'Confusión'

    code = catalog_code('Td5a9fdcc78ab4510aee9addb48db94cf47a91f1b', "-1")
    assert code.code == "-1"
    assert code.description is None
    for record in caplog.records:
        assert record.args == ('Td5a9fdcc78ab4510aee9addb48db94cf47a91f1b -1',)


def test_huso_horario():
    # {http://www.sat.gob.mx/sitio_internet/cfd/catalogos}c_CodigoPostal T1c22cc9094f6f89d8589f52d827f368d767db6b0
    c = select_all("T1c22cc9094f6f89d8589f52d827f368d767db6b0")
    for i in c.values():
        assert i[4] in HUSO_HORARIOS