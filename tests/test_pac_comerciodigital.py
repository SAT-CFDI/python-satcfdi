import json
from datetime import datetime
from decimal import Decimal
from unittest import mock

from satcfdi.create.cfd import cfdi40
from satcfdi.create.cfd.catalogos import Impuesto, TipoFactor
from satcfdi.pacs import Environment
from satcfdi.pacs.comerciodigital import ComercioDigital
from utils import get_signer, verify_result


def test_comercio_digital_test():
    comercio_digital = ComercioDigital(
        user="AAA010101AAA",
        password="PWD",
        environment=Environment.TEST
    )

    signer = get_signer('xia190128j61')
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
            rfc="ARE100609JP4",
            nombre="ACE RENUEVA SA DE CV",
            uso_cfdi="G03",
            domicilio_fiscal_receptor="85000",
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
            _traslados_incluidos=True
        )
    )
    invoice.sign(signer)

    with mock.patch(f'requests.request') as mk:
        mk.return_value.ok = True
        mk.return_value.headers = {
            'codigo': '000',
            'uuid': '66ea0f5a-4f00-4406-a573-87eb1a34f1fa'
        }
        mk.return_value.content = b'Hello'

        comercio_digital.stamp(
            cfdi=invoice
        )

        assert mk.called
        mk.call_args.kwargs["headers"]["User-Agent"] = 'this is a test'
        mk.call_args.kwargs["data"] = b"".join(mk.call_args.kwargs["data"])

        args = json.dumps(mk.call_args.kwargs, indent=2, default=str, ensure_ascii=False)
        verify = verify_result(data=args, filename="test_stamp.json")
        assert verify

