import json
from datetime import datetime
from decimal import Decimal
from unittest import mock

from requests.auth import HTTPBasicAuth

from satcfdi.create.cfd import cfdi40
from satcfdi.create.cfd.catalogos import Impuesto, TipoFactor
from satcfdi.pacs import Environment
from satcfdi.pacs.prodigia import Prodigia
from utils import get_signer, verify_result


def test_prodigia_test():
    prodigia = Prodigia(
        contrato="ccde5231-5bfe-4cba-b991-a59424336d4d",
        user="user",
        password="password",
        environment=Environment.TEST
    )

    signer = get_signer('xiqb891116qe4')
    emisor = cfdi40.Emisor(
        rfc=signer.rfc,
        nombre=signer.legal_name,
        regimen_fiscal="601"
    )

    invoice = cfdi40.Comprobante(
        emisor=emisor,
        lugar_expedicion="27200",
        fecha=datetime.fromisoformat("2022-09-28T22:40:38"),
        receptor=cfdi40.Receptor(
            rfc="H&E951128469",
            nombre="H & E",
            uso_cfdi="G03",
            domicilio_fiscal_receptor="34500",
            regimen_fiscal_receptor="601"
        ),
        metodo_pago="PPD",
        forma_pago="99",
        serie="T",
        folio="1000",
        conceptos=cfdi40.Concepto(
            cuenta_predial='1234567890',
            clave_prod_serv='10101702',
            cantidad=Decimal('.10'),
            clave_unidad='E48',
            descripcion='SERVICIOS DE RENTA',
            valor_unitario=Decimal("1.00"),
            impuestos=cfdi40.Impuestos(
                traslados=cfdi40.Traslado(impuesto=Impuesto.IVA, tipo_factor=TipoFactor.TASA, tasa_o_cuota=Decimal('0.160000')),
                retenciones=[cfdi40.Traslado(impuesto=Impuesto.ISR, tipo_factor=TipoFactor.TASA, tasa_o_cuota=Decimal('0.100000')), cfdi40.Traslado(impuesto=Impuesto.IVA, tipo_factor=TipoFactor.TASA, tasa_o_cuota=Decimal('0.106667'))],
            ),
            _traslados_incluidos=True
        )
    )
    invoice.sign(signer)

    with mock.patch(f'requests.request') as mk:
        mk.return_value.json = mock.Mock(return_value={
            'servicioTimbrado': {
                'codigo': 0,
                'selloSAT': 'dGhpcyBpcyBhIHNlYWwgdGVzdA==',
                'xmlBase64': 'PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiPz48Y2ZkaTpDb21wcm9iYW50ZSB4bWxuczpjZmRpPSJodHRwOi8vd3d3LnNhdC5nb2IubXgvY2ZkLzQiIA==',
                'contrato': '97353117-126d-4d72-93aa-1142496fbd81',
                'timbradoOk': True,
                'id': '21afd57c-20a3-4d48-a478-76de7b3fe4f4',
                'mensaje': '*** generado en modo de pruebas ***',
                'FechaTimbrado': '2020-01-01T112:20:00',
                'noCertificadoSAT': 12345678,
                'UUID': 'A6C30EF1-1967-4E4A-B4A0-EDAC0CF88541',
                'version': 1.1
            }
        })

        res = prodigia.stamp(
            cfdi=invoice
        )
        assert res.xml == b'<?xml version="1.0" encoding="UTF-8"?><cfdi:Comprobante xmlns:cfdi="http://www.sat.gob.mx/cfd/4" '
        assert not res.pdf

        assert mk.called
        mk.call_args.kwargs["headers"]["User-Agent"] = 'this is a test'
        assert mk.call_args.kwargs["auth"] == HTTPBasicAuth("user", "password")
        mk.call_args.kwargs["auth"] = "Basic abc"

        args = json.dumps(mk.call_args.kwargs, indent=2, default=str, ensure_ascii=False)
        verify = verify_result(data=args, filename="test_prodigia_stamp.json")
        assert verify
