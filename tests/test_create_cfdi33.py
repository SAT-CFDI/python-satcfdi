import os
from datetime import datetime, date
from decimal import Decimal
from unittest import mock

import pytest

from satcfdi import render
from satcfdi.cfdi import CFDI
from satcfdi.create.cfd import cfdi33, nomina12
from satcfdi.create.cfd.catalogos import Impuesto, TipoFactor
from satcfdi.create.cfd.cfdi40 import PagoComprobante
from satcfdi.pacs.sat import SAT
from tests.utils import get_signer, verify_result, _uuid, stamp_v11, SAT_Certificate_Store_Pruebas, XElementPrettyPrinter

module = 'satcfdi'
current_dir = os.path.dirname(__file__)
current_filename = os.path.splitext(os.path.basename(__file__))[0]
sat = SAT()

invoices = [
    ('xiqb891116qe4', "xiqb891116qe4_ingreso_noobjeto", None, [cfdi33.Traslado(impuesto=Impuesto.ISR, tipo_factor=TipoFactor.TASA, tasa_o_cuota=Decimal('0.100000'))], '13851.27', False),
    # ('xiqb891116qe4', "xiqb891116qe4_ingreso_exento", cfdi33.Traslado.IVA_EXENTO, [cfdi33.Retencion.ISR10], '13851.27', False),
    ('xiqb891116qe4', "xiqb891116qe4_ingreso_iva16", cfdi33.Traslado(impuesto=Impuesto.IVA, tipo_factor=TipoFactor.TASA, tasa_o_cuota=Decimal('0.160000')),
     [cfdi33.Traslado(impuesto=Impuesto.ISR, tipo_factor=TipoFactor.TASA, tasa_o_cuota=Decimal('0.100000')), cfdi33.Traslado(impuesto=Impuesto.IVA, tipo_factor=TipoFactor.TASA, tasa_o_cuota=Decimal('0.106667'))], '14672.08', False),
    ('h&e951128469', "h&e951128469_ingreso_noobjeto", None, None, '15390.30', False),
    # ('h&e951128469', "h&e951128469_ingreso_exento", cfdi33.Traslado.IVA_EXENTO, None, '15390.30', False),
    ('h&e951128469', "h&e951128469_ingreso_iva16", cfdi33.Traslado(impuesto=Impuesto.IVA, tipo_factor=TipoFactor.TASA, tasa_o_cuota=Decimal('0.160000')), None, '17852.75', False),
    # ('h&e951128469', "h&e951128469_ingreso_ieps_exento", cfdi33.Traslado.IEPS_EXENTO, None, '15390.30', False)
]


def verify_invoice(invoice, path, include_metadata=False):
    if include_metadata:
        verify = verify_result(data=invoice.metadata, filename=f"{path}.txt")
        assert verify

    pp = XElementPrettyPrinter()
    verify = verify_result(data=pp.pformat(invoice), filename=f"{path}.pretty.py")
    assert verify

    verify = verify_result(data=invoice.xml_bytes(pretty_print=True), filename=f"{path}.xml")
    assert verify

    verify = verify_result(data=render.html_str(invoice), filename=f"{path}.html")
    assert verify


@pytest.mark.parametrize('rfc, xml_file, traslados, retenciones, total, traslado_incluido', invoices)
def test_create_invoice(rfc, xml_file, traslados, retenciones, total, traslado_incluido):
    signer = get_signer(rfc)
    emisor = cfdi33.Emisor(
        rfc=signer.rfc,
        nombre=signer.legal_name,
        regimen_fiscal="601"
    )

    invoice = cfdi33.Comprobante(
        emisor=emisor,
        lugar_expedicion="56820",
        fecha=datetime.fromisoformat("2020-01-01T22:40:38"),
        receptor=cfdi33.Receptor(
            rfc='KIJ0906199R1',
            nombre='KIJ, S.A DE C.V.',
            uso_cfdi='G03'
        ),
        metodo_pago='PPD',
        serie="A",
        folio="123456",
        conceptos=[
            cfdi33.Concepto(
                cuenta_predial='1234567890',
                clave_prod_serv='10101702',
                cantidad=Decimal('1.00'),
                clave_unidad='E48',
                descripcion='SERVICIOS DE FACTURACION',
                valor_unitario=Decimal('15390.30'),
                impuestos=cfdi33.Impuestos(
                    traslados=traslados,
                    retenciones=retenciones
                )
            )
        ]
    )
    invoice.sign(signer)
    invoice.to_xml(validate=True)
    assert invoice["Total"] == Decimal(total)

    verify_invoice(invoice, f"{xml_file}")

    # Stamping
    with mock.patch('uuid.uuid4', _uuid), \
            mock.patch(f'{module}.models.Certificate.rfc_pac', "SAT970701NN3"):
        stamp_v11(invoice, signer=signer, date=datetime(year=2020, month=1, day=11))

    verify_invoice(invoice, f"{xml_file}_stamped")

    def from_no_certificado(_, no_certificado):
        return signer

    # Verify Signature
    with mock.patch(f'{module}.transform.SAT_Certificate_Store', SAT_Certificate_Store_Pruebas), \
            mock.patch(f'{module}.pacs.sat.SAT.recover_certificate', from_no_certificado), \
            mock.patch(f'{module}.models.Certificate.rfc_pac', "SAT970701NN3"):
        ver = sat.validate(invoice)
        assert ver


@pytest.mark.parametrize('rfc, xml_file, traslados, retenciones, total, traslado_incluido', invoices)
def test_create_pago(rfc, xml_file, traslados, retenciones, total, traslado_incluido):
    signer = get_signer(rfc)
    emisor = cfdi33.Emisor(
        rfc=signer.rfc,
        nombre=signer.legal_name,
        regimen_fiscal="601"
    )

    ingreso_invoice = CFDI.from_file(os.path.join(current_dir, f"{current_filename}/{xml_file}_stamped.xml"))

    invoice = cfdi33.Comprobante.pago_comprobantes(
        emisor=emisor,
        lugar_expedicion="56820",
        fecha=datetime.fromisoformat("2020-01-01T22:40:38"),
        comprobantes=[ingreso_invoice],
        fecha_pago=datetime.fromisoformat("2020-01-02T22:40:38"),
        forma_pago="03",
        serie="A",
        folio="123456",
    )
    invoice.sign(signer)

    assert invoice['Complemento']['Pago'][0]['Monto'] == Decimal(total)

    verify_invoice(invoice, f"pago_{xml_file}")


@pytest.mark.parametrize('rfc, xml_file, traslados, retenciones, total, traslado_incluido', invoices)
def test_create_pago_parcial(rfc, xml_file, traslados, retenciones, total, traslado_incluido):
    signer = get_signer(rfc)
    emisor = cfdi33.Emisor(
        rfc=signer.rfc,
        nombre=signer.legal_name,
        regimen_fiscal="601"
    )

    ingreso_invoice = CFDI.from_file(os.path.join(current_dir, f"{current_filename}/{xml_file}_stamped.xml"))

    invoice = cfdi33.Comprobante.pago_comprobantes(
        emisor=emisor,
        lugar_expedicion="56820",
        fecha=datetime.fromisoformat("2020-01-01T22:40:38"),
        comprobantes=PagoComprobante(
            comprobante=ingreso_invoice,
            num_parcialidad=2,
            imp_saldo_ant=Decimal("5000.43"),
            imp_pagado=Decimal("3245.12"),
        ),
        fecha_pago=datetime.fromisoformat("2020-01-02T22:40:38"),
        forma_pago="03",
        serie="A",
        folio="123456",
    )
    invoice.sign(signer)

    assert invoice['Complemento']['Pago'][0]['Monto'] == Decimal("3245.12")

    verify_invoice(invoice, f"pago_p_{xml_file}")


@pytest.mark.parametrize('rfc, xml_file, traslados, retenciones, total, traslado_incluido', invoices)
def test_create_pago_multiple(rfc, xml_file, traslados, retenciones, total, traslado_incluido):
    signer = get_signer(rfc)
    emisor = cfdi33.Emisor(
        rfc=signer.rfc,
        nombre=signer.legal_name,
        regimen_fiscal="601"
    )

    ingreso_invoice = CFDI.from_file(os.path.join(current_dir, f"{current_filename}/{xml_file}_stamped.xml"))

    invoice = cfdi33.Comprobante.pago_comprobantes(
        emisor=emisor,
        lugar_expedicion="56820",
        fecha=datetime.fromisoformat("2020-01-01T22:40:38"),
        comprobantes=[ingreso_invoice, ingreso_invoice],
        fecha_pago=datetime.fromisoformat("2020-01-02T22:40:38"),
        forma_pago="03",
        serie="A",
        folio="123456",
    )
    invoice.sign(signer)

    assert invoice['Complemento']['Pago'][0]['Monto'] == Decimal(total) * 2

    verify_invoice(invoice, f"mpago_{xml_file}")


def test_nomina():
    xml_file = "invoice_nomina"

    signer = get_signer('xiqb891116qe4')
    emisor = cfdi33.Emisor(
        rfc=signer.rfc,
        nombre=signer.legal_name,
        regimen_fiscal="601"
    )

    invoice = cfdi33.Comprobante.nomina(
        emisor=emisor,
        receptor=cfdi33.Receptor(
            rfc='KIJ0906199R1',
            nombre='KIJ, S.A DE C.V.',
            uso_cfdi='G03',
        ),
        lugar_expedicion="56820",
        complemento_nomina=nomina12.Nomina(
            emisor={
                'RegistroPatronal': 'Z1234567890'
            },
            receptor={
                'Curp': 'XIQB891116MCHZRL72',
                'NumSeguridadSocial': '987654321',
                'FechaInicioRelLaboral': date(2020, 1, 1),
                'Antigüedad': 'P96W',
                'TipoContrato': '01',
                'Sindicalizado': 'No',
                'TipoJornada': '01',
                'TipoRegimen': '02',
                'NumEmpleado': '12345678',
                'Departamento': 'Departamento del Trabajo',
                'Puesto': 'Trabajador',
                'RiesgoPuesto': '2',
                'PeriodicidadPago': '04',
                'CuentaBancaria': '0001000200030004',
                'SalarioDiarioIntegrado': Decimal('100.01'),
                'ClaveEntFed': 'MOR'
            },
            percepciones={
                'Percepcion': [
                    {
                        'TipoPercepcion': '001',
                        'Clave': '001',
                        'Concepto': 'SUELDO',
                        'ImporteGravado': Decimal('1200.00'),
                        'ImporteExento': Decimal('400.00')
                    }
                ]
            },
            deducciones={
                'Deduccion': [
                    {
                        'TipoDeduccion': '002',
                        'Clave': '300',
                        'Concepto': 'ISR A CARGO',
                        'Importe': Decimal('1234.73')
                    },
                    {
                        'TipoDeduccion': '004',
                        'Clave': '204',
                        'Concepto': 'FONDO DE AHORRO EMPLEADOS',
                        'Importe': Decimal('521.10')
                    },
                ]
            },
            otros_pagos=[
                {
                    'TipoOtroPago': '999',
                    'Clave': '046',
                    'Concepto': 'REEMBOLSO DE GASTOS',
                    'Importe': Decimal('456.00')
                },
                {
                    'SubsidioAlEmpleo': Decimal('0.00'),
                    'TipoOtroPago': '002',
                    'Clave': '002',
                    'Concepto': 'SUBSIDIO EMPLEO',
                    'Importe': Decimal('0.00')
                }
            ],
            incapacidades=[
                {
                    "DiasIncapacidad": 2,
                    'TipoIncapacidad': '02',
                    'ImporteMonetario': Decimal('1000.00'),
                }
            ],
            tipo_nomina='O',
            fecha_pago=date(2020, 1, 30),
            fecha_final_pago=date(2020, 1, 31),
            fecha_inicial_pago=date(2020, 1, 16),
            num_dias_pagados=Decimal('16.000')
        ),
        serie="A",
        folio="123456",
        fecha=datetime.fromisoformat("2020-09-29T22:40:38")
    )
    invoice.sign(signer)

    verify_invoice(invoice, f"{xml_file}")
