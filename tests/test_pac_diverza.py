import json
import os
from datetime import datetime
from decimal import Decimal
from unittest import mock

from satcfdi.create.cfd.catalogos import Impuesto, TipoFactor
from satcfdi.pacs import Environment
from satcfdi.pacs.diverza import Diverza
from satcfdi.create.cfd import cfdi33, cfdi40, pago20
from tests.utils import get_signer, verify_result

current_dir = os.path.dirname(__file__)
module = 'satcfdi'


def test_diverza_validate_rfc():
    diverza = Diverza(
        rfc="AAA010101AAA",
        id="3935",
        token="ABCD1234"
    )

    with mock.patch(f'requests.request') as mk:
        mk.return_value.json = mock.Mock(return_value={'identifiers': [{'rfc': 'AAA010101AAA', 'active': 'Y'}]})
        
        r = diverza.rfc_valid("AAA010101AAA")
        assert r

    with mock.patch(f'requests.request') as mk:
        mk.return_value.json = mock.Mock(return_value={'identifiers': [{'rfc': 'AAA010101AAA', 'active': 'Y'}, {'rfc': 'ABC010101DAS', 'active': 'N'}]})
        
        r = diverza.rfc_valid(["AAA010101AAA", "ABC010101DAS"])

        assert r[0]
        assert not r[1]


def test_diverza_stamp():
    signer = get_signer('xiqb891116qe4')
    emisor = cfdi40.Emisor(
        rfc=signer.rfc,
        nombre=signer.legal_name,
        regimen_fiscal="601"
    )

    diverza = Diverza(
        rfc="AAA010101AAA",
        id="3935",
        token="ABCD1234",
        environment=Environment.TEST
    )

    cfdi = cfdi33.Comprobante(
        emisor=emisor,
        lugar_expedicion="56820",
        fecha=datetime.fromisoformat("2022-09-28T22:40:38"),
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
                    traslados=cfdi33.Traslado(
                        impuesto=Impuesto.IVA,
                        tipo_factor=TipoFactor.TASA,
                        tasa_o_cuota=Decimal('0.160000'),
                    ),
                    retenciones=[
                        cfdi33.Retencion(
                            impuesto=Impuesto.ISR,
                            tipo_factor=TipoFactor.TASA,
                            tasa_o_cuota=Decimal('0.100000'),
                        ),
                        cfdi33.Retencion(
                            impuesto=Impuesto.IVA,
                            tipo_factor=TipoFactor.TASA,
                            tasa_o_cuota=Decimal('0.106667'),
                        )
                    ],
                )
            )
        ]
    )
    cfdi.sign(signer)

    with mock.patch(f'requests.request') as mk:
        mk.return_value.json = mock.Mock(return_value={
            "uuid": "3d94d0c5-9d4d-4c73-a61b-d083c553b7cc",
            "content": "dGhpcyBpcyBhIHRlc3QgeG1s"
        })
        diverza.stamp(cfdi=cfdi)

        assert mk.called
        mk.call_args.kwargs["headers"]["User-Agent"] = 'this is a test'

        args = json.dumps(mk.call_args.kwargs, indent=2)
        verify = verify_result(data=args, filename="test_diverza_stamp.json")
        assert verify

    with mock.patch(f'requests.request') as mk:
        mk.return_value.json = mock.Mock(return_value={
            "uuid": "3d94d0c5-9d4d-4c73-a61b-d083c553b7cc",
            "content": "dGhpcyBpcyBhIHRlc3QgeG1s"
        })
        diverza.issue(
            cfdi=cfdi,
            # certificate_number=signer.certificate_number()
        )

        assert mk.called
        mk.call_args.kwargs["headers"]["User-Agent"] = 'this is a test'

        args = json.dumps(mk.call_args.kwargs, indent=2)
        verify = verify_result(data=args, filename="test_diverza_issue.json")
        assert verify


def test_diverza_stamp_v40():
    signer = get_signer('xiqb891116qe4')
    emisor = cfdi40.Emisor(
        rfc=signer.rfc,
        nombre=signer.legal_name,
        regimen_fiscal="601"
    )

    diverza = Diverza(
        rfc="AAA010101AAA",
        id="3935",
        token="ABCD1234",
        environment=Environment.TEST
    )

    cfdi = cfdi40.Comprobante(
        emisor=emisor,
        lugar_expedicion="56820",
        fecha=datetime.fromisoformat("2022-09-28T22:40:38"),
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
                    retenciones=[cfdi40.Traslado(impuesto=Impuesto.ISR, tipo_factor=TipoFactor.TASA, tasa_o_cuota=Decimal('0.100000')), cfdi40.Traslado(impuesto=Impuesto.IVA, tipo_factor=TipoFactor.TASA, tasa_o_cuota=Decimal('0.106667'))],
                )
            )
        ]
    )
    cfdi.sign(signer)

    with mock.patch(f'requests.request') as mk:
        mk.return_value.json = mock.Mock(return_value={
            "uuid": "3d94d0c5-9d4d-4c73-a61b-d083c553b7cc",
            "content": "dGhpcyBpcyBhIHRlc3QgeG1s"
        })
        diverza.stamp(cfdi=cfdi)

        assert mk.called
        mk.call_args.kwargs["headers"]["User-Agent"] = 'this is a test'

        args = json.dumps(mk.call_args.kwargs, indent=2)
        verify = verify_result(data=args, filename="test_diverza_stamp_v40.json")
        assert verify

    with mock.patch(f'requests.request') as mk:
        mk.return_value.json = mock.Mock(return_value={
            "uuid": "3d94d0c5-9d4d-4c73-a61b-d083c553b7cc",
            "content": "dGhpcyBpcyBhIHRlc3QgeG1s"
        })
        diverza.issue(
            cfdi=cfdi,
            # certificate_number=signer.certificate_number()
        )

        assert mk.called
        mk.call_args.kwargs["headers"]["User-Agent"] = 'this is a test'

        args = json.dumps(mk.call_args.kwargs, indent=2)
        verify = verify_result(data=args, filename="test_diverza_issue_v40.json")
        assert verify


def test_diverza_stamp_pago_v40():
    signer = get_signer('xiqb891116qe4')
    emisor = cfdi40.Emisor(
        rfc=signer.rfc,
        nombre=signer.legal_name,
        regimen_fiscal="601"
    )

    diverza = Diverza(
        rfc="AAA010101AAA",
        id="3935",
        token="ABCD1234",
        environment=Environment.TEST
    )

    cfdi = cfdi40.Comprobante.pago(
        emisor=emisor,
        fecha=datetime.fromisoformat("2022-09-28T22:40:38"),
        receptor=cfdi40.Receptor(
            rfc='KIJ0906199R1',
            nombre='KIJ, S.A DE C.V.',
            uso_cfdi='G03',
            domicilio_fiscal_receptor="59820",
            regimen_fiscal_receptor="601"
        ),
        lugar_expedicion="56820",
        complemento_pago=pago20.Pagos(
            pago=pago20.Pago(
                fecha_pago=datetime(2020, 1, 1),
                forma_de_pago_p='03',
                moneda_p='MXN',
                tipo_cambio_p=1,
                docto_relacionado=pago20.DoctoRelacionado(
                    id_documento='d6042dc8-d525-4e78-8d1b-092c878bd518',
                    imp_pagado=Decimal("100.3"),
                    imp_saldo_ant=Decimal("203.45"),
                    num_parcialidad=3,
                    moneda_dr="MXN",
                    objeto_imp_dr="01"
                )
            )
        ),
        serie="A",
        folio="123456"
    )
    cfdi.sign(signer)

    with mock.patch(f'requests.request') as mk:
        mk.return_value.json = mock.Mock(return_value={
            "uuid": "3d94d0c5-9d4d-4c73-a61b-d083c553b7cc",
            "content": "dGhpcyBpcyBhIHRlc3QgeG1s"
        })
        diverza.stamp(cfdi=cfdi)

        assert mk.called
        mk.call_args.kwargs["headers"]["User-Agent"] = 'this is a test'

        args = json.dumps(mk.call_args.kwargs, indent=2)
        verify = verify_result(data=args, filename="test_diverza_stamp_pago_v40.json")
        assert verify

    with mock.patch(f'requests.request') as mk:
        mk.return_value.json = mock.Mock(return_value={
            "uuid": "3d94d0c5-9d4d-4c73-a61b-d083c553b7cc",
            "content": "dGhpcyBpcyBhIHRlc3QgeG1s"
        })
        diverza.issue(
            cfdi=cfdi,
            # certificate_number=signer.certificate_number()
        )

        assert mk.called
        mk.call_args.kwargs["headers"]["User-Agent"] = 'this is a test'

        args = json.dumps(mk.call_args.kwargs, indent=2)
        verify = verify_result(data=args, filename="test_diverza_issue_pago_v40.json")
        assert verify

