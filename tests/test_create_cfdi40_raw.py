import json
import os
from datetime import datetime
from decimal import Decimal

from satcfdi import render
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


def test_create_raw():
    signer = get_signer('xiqb891116qe4')

    raw_cfdi = {
        "Fecha": datetime.fromisoformat("2020-01-01T22:40:38"),
        "Version": "4.0",
        "Emisor": {
            'Rfc': signer.rfc,
            'Nombre': signer.legal_name,
            'RegimenFiscal': "601",
        },
        "Receptor": {
            "Rfc": "KIJ0906199R1",
            "Nombre": "KIJ, S.A DE C.V.",
            "DomicilioFiscalReceptor": "59820",
            "RegimenFiscalReceptor": "601",
            "UsoCFDI": "G03"
        },
        "Conceptos": [
            {
                "ClaveProdServ": "10101702",
                "Cantidad": 1,
                "ClaveUnidad": "E48",
                "Descripcion": "SERVICIOS DE FACTURACION",
                "ValorUnitario": Decimal(15390.30),
                "Impuestos": {
                    "Traslados": cfdi40.Traslado(impuesto=Impuesto.IVA, tipo_factor=TipoFactor.TASA, tasa_o_cuota=Decimal('0.160000')),
                    "Retenciones": [
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
                    ]
                },
                "CuentaPredial": "1234567890",
                "_traslados_incluidos": False
            }
        ],
        "LugarExpedicion": "56820",
        "Serie": "A",
        "Folio": "123456",
        "Moneda": "MXN",
        "Sello": "",
        'TipoDeComprobante': 'I',
        'Exportacion': "01"
    }

    a = cfdi40.Comprobante.__new__(cfdi40.Comprobante)
    a.update(raw_cfdi)
    a.compute()
    a.sign(signer)

    verify_invoice(a, "manual.xml")


def test_create_raw_no_signature():
    signer = get_signer('xiqb891116qe4')

    raw_cfdi = {
        "Fecha": datetime.fromisoformat("2020-01-01T22:40:38"),
        "Version": "4.0",
        "Emisor": {
            'Rfc': signer.rfc,
            'Nombre': signer.legal_name,
            'RegimenFiscal': "601",
        },
        "Receptor": {
            "Rfc": "KIJ0906199R1",
            "Nombre": "KIJ, S.A DE C.V.",
            "DomicilioFiscalReceptor": "59820",
            "RegimenFiscalReceptor": "601",
            "UsoCFDI": "G03"
        },
        "Conceptos": [
            {
                "ClaveProdServ": "10101702",
                "Cantidad": 1,
                "ClaveUnidad": "E48",
                "Descripcion": "SERVICIOS DE FACTURACION",
                "ValorUnitario": Decimal(15390.30),
                "Impuestos": {
                    "Traslados": cfdi40.Traslado(impuesto=Impuesto.IVA, tipo_factor=TipoFactor.TASA, tasa_o_cuota=Decimal('0.160000')),
                    "Retenciones": [
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
                    ]
                },
                "CuentaPredial": "1234567890",
                "_traslados_incluidos": False
            }
        ],
        "LugarExpedicion": "56820",
        "Serie": "A",
        "Folio": "123456",
        "Moneda": "MXN",
        'NoCertificado': '',
        'Certificado': '',
        "Sello": "",
        'TipoDeComprobante': 'I',
        'Exportacion': "01"
    }

    a = cfdi40.Comprobante.__new__(cfdi40.Comprobante)
    a.update(raw_cfdi)
    a.compute()
    # a.sign(signer)

    verify_invoice(a, "manual_no_signature.xml")


def test_create_no_signature():
    signer = get_signer('xiqb891116qe4')

    invoice = cfdi40.Comprobante(
        emisor=cfdi40.Emisor(
            rfc=signer.rfc,
            nombre=signer.legal_name,
            regimen_fiscal="601",
        ),
        lugar_expedicion="56820",
        fecha=datetime.fromisoformat("2020-01-01T22:40:38"),
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
                    traslados=cfdi40.Traslado(impuesto=Impuesto.IVA, tipo_factor=TipoFactor.TASA, tasa_o_cuota=Decimal('0.160000')),
                    retenciones=[
                        cfdi40.Traslado(impuesto=Impuesto.ISR, tipo_factor=TipoFactor.TASA, tasa_o_cuota=Decimal('0.100000')),
                        cfdi40.Traslado(impuesto=Impuesto.IVA, tipo_factor=TipoFactor.TASA, tasa_o_cuota=Decimal('0.106667')),
                    ],
                ),
                _traslados_incluidos=False
            )
        ]
    )

    verify_invoice(invoice, "no_signature.xml")

