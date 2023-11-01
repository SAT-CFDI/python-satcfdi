import os
from datetime import datetime
from decimal import Decimal

from satcfdi import render
from satcfdi.create.addendas import dvz11
from satcfdi.create.cfd import cfdi40
from satcfdi.create.cfd.catalogos import Impuesto, TipoFactor
from satcfdi.pacs.sat import SAT
from tests.utils import get_signer, verify_result, XElementPrettyPrinter

module = 'satcfdi'
current_dir = os.path.dirname(__file__)
current_filename = os.path.splitext(os.path.basename(__file__))[0]
sat = SAT()


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


def test_create_addenda():
    xml_file = "cfdi_addenda"
    signer = get_signer('h&e951128469')
    emisor = cfdi40.Emisor(
        rfc=signer.rfc,
        nombre=signer.legal_name,
        regimen_fiscal="606",
    )

    invoice = cfdi40.Comprobante(
        emisor=emisor,
        fecha=datetime.fromisoformat("2020-09-29T22:40:38"),
        lugar_expedicion="56820",
        receptor=cfdi40.Receptor(
            rfc='KIJ0906199R1',
            nombre='KIJ, S.A DE C.V.',
            uso_cfdi='G03',
            domicilio_fiscal_receptor="59820",
            regimen_fiscal_receptor="601"
        ),
        metodo_pago='PPD',
        serie="A",
        folio="123456",
        conceptos=[
            cfdi40.Concepto(
                cuenta_predial='1234567890',
                clave_prod_serv='10101702',
                cantidad=Decimal('1.00'),
                clave_unidad='E48',
                descripcion='SERVICIOS DE FACTURACION',
                valor_unitario=Decimal('15390.30'),
                impuestos=cfdi40.Impuestos(
                    traslados=cfdi40.Traslado(
                        impuesto=Impuesto.IVA,
                        tipo_factor=TipoFactor.TASA,
                        tasa_o_cuota=Decimal('0.160000'),
                    ),
                    retenciones=[
                        cfdi40.Retencion(
                            impuesto=Impuesto.ISR,
                            tipo_factor=TipoFactor.TASA,
                            tasa_o_cuota=Decimal('0.100000'),
                        ),
                        cfdi40.Retencion(
                            impuesto=Impuesto.IVA,
                            tipo_factor=TipoFactor.TASA,
                            tasa_o_cuota=Decimal('0.106667'),
                        )
                    ],
                ),
                _traslados_incluidos=False
            )
        ],
        addenda=dvz11.Diverza(
            generales=dvz11.Generales(
                tipo_documento="Factura"
            )
        )
    )
    invoice.sign(signer=signer)

    verify_invoice(invoice, f"{xml_file}")

    verify_invoice(invoice.process(), f"{xml_file}_process")


def test_copy_cfdi():
    xml_file = "cfdi_copy"
    signer = get_signer('h&e951128469')
    emisor = cfdi40.Emisor(
        rfc=signer.rfc,
        nombre=signer.legal_name,
        regimen_fiscal="606",
    )

    invoice = cfdi40.Comprobante(
        emisor=emisor,
        fecha=datetime.fromisoformat("2020-09-29T22:40:38"),
        lugar_expedicion="56820",
        receptor=cfdi40.Receptor(
            rfc='KIJ0906199R1',
            nombre='KIJ, S.A DE C.V.',
            uso_cfdi='G03',
            domicilio_fiscal_receptor="59820",
            regimen_fiscal_receptor="601"
        ),
        metodo_pago='PPD',
        serie="A",
        folio="123456",
        conceptos=[
            cfdi40.Concepto(
                cuenta_predial='1234567890',
                clave_prod_serv='10101702',
                cantidad=Decimal('1.00'),
                clave_unidad='E48',
                descripcion='SERVICIOS DE FACTURACION',
                valor_unitario=Decimal('15390.30'),
                impuestos=cfdi40.Impuestos(
                    traslados=cfdi40.Traslado(
                        impuesto=Impuesto.IVA,
                        tipo_factor=TipoFactor.TASA,
                        tasa_o_cuota=Decimal('0.160000'),
                    ),
                    retenciones=[
                        cfdi40.Retencion(
                            impuesto=Impuesto.ISR,
                            tipo_factor=TipoFactor.TASA,
                            tasa_o_cuota=Decimal('0.100000'),
                        ),
                        cfdi40.Retencion(
                            impuesto=Impuesto.IVA,
                            tipo_factor=TipoFactor.TASA,
                            tasa_o_cuota=Decimal('0.106667'),
                        )
                    ],
                ),
                _traslados_incluidos=False
            )
        ]
    )
    invoice.sign(signer=signer)

    copy = invoice.copy()
    verify_invoice(copy, f"{xml_file}")

    render.json_str(copy, pretty_print=True)
