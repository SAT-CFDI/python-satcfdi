from satcfdi.create.cfd.catalogos import Impuesto


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

