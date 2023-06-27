import os

from satcfdi.create.cfd.catalogos import Impuesto
from satcfdi.transform import HUSO_HORARIOS
from satcfdi.catalogs import moneda_decimales, catalog_code, select_all, codigo_postal_uso_horario

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
    code = catalog_code('C756_c_FormaPago', "24")
    assert code.code == "24"
    assert code.description == 'Confusión'

    code = catalog_code('C756_c_FormaPago', "-1")
    assert code.code == "-1"
    assert code.description is None


def test_huso_horario():
    c = select_all("C756_c_CodigoPostal")

    s = set( i[4] for i in c.values())
    print(sorted(s))

    for i in c.values():
        assert i[4] in HUSO_HORARIOS


def test_codigo_postal():
    cp = codigo_postal_uso_horario("50200")
    assert cp == "Tiempo del Centro"
