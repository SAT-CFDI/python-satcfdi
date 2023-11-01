import json
import os
from datetime import datetime
from decimal import Decimal
from unittest import mock
from satcfdi.cfdi import CFDI
from satcfdi.create.cancela import cancelacionretencion
from satcfdi.create.cancela.aceptacionrechazo import SolicitudAceptacionRechazo, Folios
from satcfdi.create.cancela.cancelacion import Cancelacion, Folio
from satcfdi.create.cfd import cfdi40
from satcfdi.create.cfd.catalogos import Impuesto, TipoFactor
from satcfdi.pacs import Environment, Accept, CancelReason
from satcfdi.pacs.swsapien import SWSapien
from utils import get_signer, verify_result

current_dir = os.path.dirname(__file__)

swsapien = SWSapien(
    token="token",
    user="user",
    password="password",
    environment=Environment.TEST
)


def test_swsapien_test():
    signer = get_signer('xia190128j61', get_csd=True)
    emisor = cfdi40.Emisor(
        rfc=signer.rfc,
        nombre=signer.legal_name,
        regimen_fiscal="601"
    )
    assert emisor["Nombre"] == "XENON INDUSTRIAL ARTICLES"

    invoice = cfdi40.Comprobante(
        emisor=emisor,
        lugar_expedicion="27200",
        fecha=datetime.fromisoformat("2022-09-28T22:40:38"),
        receptor=cfdi40.Receptor(
            rfc="URE180429TM6",
            nombre="UNIVERSIDAD ROBOTICA ESPAÑOLA",
            uso_cfdi="G03",
            domicilio_fiscal_receptor="65000",
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
        mk.return_value.ok = True
        mk.return_value.json = mock.Mock(return_value={
            "status": "success",
            "data": {
                "uuid": '66ea0f5a-4f00-4406-a573-87eb1a34f1fa',
                "cfdi": "dGhpcyBpcyBhIHRlc3QgeG1s"
            }
        })

        res = swsapien.stamp(
            cfdi=invoice,
            accept=Accept.XML
        )

        assert mk.called
        mk.call_args.kwargs["headers"]["User-Agent"] = 'this is a test'

        args = json.dumps(mk.call_args.kwargs, indent=2, default=str, ensure_ascii=False)
        verify = verify_result(data=args, filename="test_stamp.json")
        assert verify


# @pytest.mark.skip(reason="skiping for now")
def test_connectia_cancel():
    cfdi = CFDI(
        {
            "Emisor": {
                "Rfc": "EKU9003173C9"
            },
            "Complemento": {
                "TimbreFiscalDigital": {
                    "UUID": "FE4E71B0-8959-4FB9-8091-F5AC4FB0FEF8"
                }
            }
        }
    )
    cfdi.tag = '{http://www.sat.gob.mx/cfd/3}Comprobante',

    with mock.patch(f'requests.request') as mk:
        mk.return_value.ok = True
        mk.return_value.json = mock.Mock(return_value={
            "data": {
                "acuse": "<?xml version=\"1.0\" encoding=\"utf-8\"?><Acuse xmlns:xsd=\"http://www.w3.org/2001/XMLSchema\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" Fecha=\"2022-10-27T11:02:56.2475804\" RfcEmisor=\"EKU9003173C9\"><Folios xmlns=\"http://cancelacfd.sat.gob.mx\"><UUID>FE4E71B0-8959-4FB9-8091-F5AC4FB0FEF8</UUID><EstatusUUID>202</EstatusUUID></Folios><Signature Id=\"SelloSAT\" xmlns=\"http://www.w3.org/2000/09/xmldsig#\"><SignedInfo><CanonicalizationMethod Algorithm=\"http://www.w3.org/TR/2001/REC-xml-c14n-20010315\" /><SignatureMethod Algorithm=\"http://www.w3.org/2001/04/xmldsig-more#hmac-sha512\" /><Reference URI=\"\"><Transforms><Transform Algorithm=\"http://www.w3.org/TR/1999/REC-xpath-19991116\"><XPath>not(ancestor-or-self::*[local-name()='Signature'])</XPath></Transform></Transforms><DigestMethod Algorithm=\"http://www.w3.org/2001/04/xmlenc#sha512\" /><DigestValue>rGaqXD3bdRxOv6PBbIi/Oe9JFTJF6hoYtyx63sVTyxByLo0A9+43SNOpyxMYQqGvPowqkiccPDbF1nel2ABSSQ==</DigestValue></Reference></SignedInfo><SignatureValue>LLZEDLTYoSlTJGJRCxkSlS1zqXDNu4kqQoVimYisqQWT9M+uedJYT5PeV2o0an0gcVphqvco7oQb38vz5gykLQ==</SignatureValue><KeyInfo><KeyName>BF66E582888CC845</KeyName><KeyValue><RSAKeyValue><Modulus>n5YsGT0w5Z70ONPbqszhExfJU+KY3Bscftc2jxUn4wxpSjEUhnCuTd88OK5QbDW3Mupoc61jr83lRhUCjchFAmCigpC10rEntTfEU+7qtX8ud/jJJDB1a9lTIB6bhBN//X8IQDjhmHrfKvfen3p7RxLrFoxzWgpwKriuGI5wUlU=</Modulus><Exponent>AQAB</Exponent></RSAKeyValue></KeyValue></KeyInfo></Signature></Acuse>",
                "uuid": {
                    "FE4E71B0-8959-4FB9-8091-F5AC4FB0FEF8": "202"
                }
            },
            "status": "success"
        })

        res = swsapien.cancel(
            cfdi=cfdi,
            reason=CancelReason.COMPROBANTE_EMITIDO_CON_ERRORES_SIN_RELACION
        )

        assert mk.called
        mk.call_args.kwargs["headers"]["User-Agent"] = 'this is a test'

        args = json.dumps(mk.call_args.kwargs, indent=2, default=str, ensure_ascii=False)
        verify = verify_result(data=args, filename="test_cancelation.json")
        assert verify

        assert res.code == "202"


def test_connectia_mass_cancel():
    signer = get_signer('EKU9003173C9', get_csd=True)

    cancelacion = Cancelacion(
        emisor=signer,
        fecha=datetime.fromisoformat("2021-12-26T18:15:28"),
        folios=[
            Folio(
                uuid="fe4e71b0-8959-4fb9-8091-f5ac4fb0fef8",
                motivo="02",
                folio_sustitucion=""
            )
        ]
    )

    with mock.patch(f'requests.request') as mk:
        mk.return_value.ok = True
        mk.return_value.json = mock.Mock(return_value={
            'data': {
                'acuse': '<?xml version="1.0" encoding="utf-8"?><Acuse xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" Fecha="2022-10-27T21:50:49.4572913" RfcEmisor="EKU9003173C9"><Folios xmlns="http://cancelacfd.sat.gob.mx"><UUID>FE4E71B0-8959-4FB9-8091-F5AC4FB0FEF8</UUID><EstatusUUID>202</EstatusUUID></Folios><Signature Id="SelloSAT" xmlns="http://www.w3.org/2000/09/xmldsig#"><SignedInfo><CanonicalizationMethod Algorithm="http://www.w3.org/TR/2001/REC-xml-c14n-20010315" /><SignatureMethod Algorithm="http://www.w3.org/2001/04/xmldsig-more#hmac-sha512" /><Reference URI=""><Transforms><Transform Algorithm="http://www.w3.org/TR/1999/REC-xpath-19991116"><XPath>not(ancestor-or-self::*[local-name()=\'Signature\'])</XPath></Transform></Transforms><DigestMethod Algorithm="http://www.w3.org/2001/04/xmlenc#sha512" /><DigestValue>9z9FlY3o/qJdn62GlDkQYCxD3xQQ/1GQDVpnvJz7/pvJ5hiOkhfY3LGyLfDqbJ7e0u+yOYMJfkYIb/jgwxdPjw==</DigestValue></Reference></SignedInfo><SignatureValue>AvHF37ni19Z889M7YGi2mw94VbT6doP1l4G5c//cGEspaqeuh/0JW2HHGLWbNUgRKPE+GO3OjzWSjt6hEfv61Q==</SignatureValue><KeyInfo><KeyName>BF66E582888CC845</KeyName><KeyValue><RSAKeyValue><Modulus>n5YsGT0w5Z70ONPbqszhExfJU+KY3Bscftc2jxUn4wxpSjEUhnCuTd88OK5QbDW3Mupoc61jr83lRhUCjchFAmCigpC10rEntTfEU+7qtX8ud/jJJDB1a9lTIB6bhBN//X8IQDjhmHrfKvfen3p7RxLrFoxzWgpwKriuGI5wUlU=</Modulus><Exponent>AQAB</Exponent></RSAKeyValue></KeyValue></KeyInfo></Signature></Acuse>',
                'uuid': {'FE4E71B0-8959-4FB9-8091-F5AC4FB0FEF8': '202'}
            },
            'status': 'success'
        })

        res = swsapien.cancel_comprobante(
            cancelacion
        )

        assert mk.called
        mk.call_args.kwargs["headers"]["User-Agent"] = 'this is a test'

        args = json.dumps(mk.call_args.kwargs, indent=2, default=str, ensure_ascii=False)
        verify = verify_result(data=args, filename="test_cancel_xml.json")
        assert verify

        assert res.code == {'FE4E71B0-8959-4FB9-8091-F5AC4FB0FEF8': '202'}


def test_connectia_mass_retencion_cancel():
    signer = get_signer('EKU9003173C9', get_csd=True)

    cancelacion = cancelacionretencion.Cancelacion(
        emisor=signer,
        fecha=datetime.fromisoformat("2021-12-26T18:15:28"),
        folios=[
            Folio(
                uuid="fe4e71b0-8959-4fb9-8091-f5ac4fb0fef8",
                motivo="02",
                folio_sustitucion=""
            )
        ]
    )

    # print(
    #     etree.tostring(cancelacion.to_xml(), pretty_print=True).decode()
    # )

    with mock.patch(f'requests.request') as mk:
        mk.return_value.ok = True
        mk.return_value.json = mock.Mock(return_value={
            'data': {
                'acuse': '<?xml version="1.0" encoding="utf-8"?><Acuse xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" Fecha="2022-10-27T21:50:49.4572913" RfcEmisor="EKU9003173C9"><Folios xmlns="http://cancelacfd.sat.gob.mx"><UUID>FE4E71B0-8959-4FB9-8091-F5AC4FB0FEF8</UUID><EstatusUUID>202</EstatusUUID></Folios><Signature Id="SelloSAT" xmlns="http://www.w3.org/2000/09/xmldsig#"><SignedInfo><CanonicalizationMethod Algorithm="http://www.w3.org/TR/2001/REC-xml-c14n-20010315" /><SignatureMethod Algorithm="http://www.w3.org/2001/04/xmldsig-more#hmac-sha512" /><Reference URI=""><Transforms><Transform Algorithm="http://www.w3.org/TR/1999/REC-xpath-19991116"><XPath>not(ancestor-or-self::*[local-name()=\'Signature\'])</XPath></Transform></Transforms><DigestMethod Algorithm="http://www.w3.org/2001/04/xmlenc#sha512" /><DigestValue>9z9FlY3o/qJdn62GlDkQYCxD3xQQ/1GQDVpnvJz7/pvJ5hiOkhfY3LGyLfDqbJ7e0u+yOYMJfkYIb/jgwxdPjw==</DigestValue></Reference></SignedInfo><SignatureValue>AvHF37ni19Z889M7YGi2mw94VbT6doP1l4G5c//cGEspaqeuh/0JW2HHGLWbNUgRKPE+GO3OjzWSjt6hEfv61Q==</SignatureValue><KeyInfo><KeyName>BF66E582888CC845</KeyName><KeyValue><RSAKeyValue><Modulus>n5YsGT0w5Z70ONPbqszhExfJU+KY3Bscftc2jxUn4wxpSjEUhnCuTd88OK5QbDW3Mupoc61jr83lRhUCjchFAmCigpC10rEntTfEU+7qtX8ud/jJJDB1a9lTIB6bhBN//X8IQDjhmHrfKvfen3p7RxLrFoxzWgpwKriuGI5wUlU=</Modulus><Exponent>AQAB</Exponent></RSAKeyValue></KeyValue></KeyInfo></Signature></Acuse>',
                'uuid': {'FE4E71B0-8959-4FB9-8091-F5AC4FB0FEF8': '202'}
            },
            'status': 'success'
        })

        res = swsapien.cancel_comprobante(
            cancelacion
        )

        assert mk.called
        mk.call_args.kwargs["headers"]["User-Agent"] = 'this is a test'

        args = json.dumps(mk.call_args.kwargs, indent=2, default=str, ensure_ascii=False)
        verify = verify_result(data=args, filename="test_cancel_retencion.json")
        assert verify

        assert res.code == {'FE4E71B0-8959-4FB9-8091-F5AC4FB0FEF8': '202'}


def test_swsapien_relacionados():
    cfdi = CFDI(
        {
            "Emisor": {
                "Rfc": "EKU9003173C9"
            },
            "Complemento": {
                "TimbreFiscalDigital": {
                    "UUID": "362efe1f-c0b4-47dd-9979-91d068a2bc75"
                }
            }
        }
    )
    cfdi.tag = '{http://www.sat.gob.mx/cfd/3}Comprobante',

    with mock.patch(f'requests.request') as mk:
        mk.return_value.ok = True
        mk.return_value.json = mock.Mock(return_value={'codStatus': '2001', 'data': None, 'message': 'No se encontraron CFDI relacionados. ', 'status': 'success'})

        res = swsapien.relations(
            cfdi
        )

        assert mk.called
        mk.call_args.kwargs["headers"]["User-Agent"] = 'this is a test'

        args = json.dumps(mk.call_args.kwargs, indent=2, default=str, ensure_ascii=False)
        verify = verify_result(data=args, filename="test_relacionados.json")
        assert verify

        assert res['codStatus'] == '2001'


def test_swsapien_accept_reject():
    signer = get_signer('EKU9003173C9', get_csd=True)

    request = SolicitudAceptacionRechazo(
        rfc_receptor=signer,
        rfc_pac_envia_solicitud=swsapien.RFC,
        fecha=datetime.fromisoformat("2018-09-20T14:48:09"),
        folios=[
            Folios(
                uuid="FD74D156-B9B0-44A5-9906-E08182E8363E",
                respuesta="Aceptacion"
            )
        ]
    )

    with mock.patch(f'requests.request') as mk:
        mk.return_value.ok = True
        mk.return_value.json = mock.Mock(return_value={
            'data': {
                'acuse': '<?xml version="1.0" encoding="utf-8"?><AcuseAceptacionRechazo xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" RfcReceptor="EKU9003173C9" RfcPac="SPR190613I52" CodEstatus="1000" Fecha="2022-10-28T12:20:33.885126"><Folios Respuesta="Aceptacion" xmlns="http://cancelacfd.sat.gob.mx"><UUID>FD74D156-B9B0-44A5-9906-E08182E8363E</UUID><EstatusUUID>1001</EstatusUUID></Folios><Signature Id="SelloSAT" xmlns="http://www.w3.org/2000/09/xmldsig#"><SignedInfo><CanonicalizationMethod Algorithm="http://www.w3.org/TR/2001/REC-xml-c14n-20010315" /><SignatureMethod Algorithm="http://www.w3.org/2001/04/xmldsig-more#hmac-sha512" /><Reference URI=""><Transforms><Transform Algorithm="http://www.w3.org/TR/1999/REC-xpath-19991116"><XPath>not(ancestor-or-self::*[local-name()=\'Signature\'])</XPath></Transform></Transforms><DigestMethod Algorithm="http://www.w3.org/2001/04/xmlenc#sha512" /><DigestValue>dFlQ/PTBmAAX0I8CBmmU04cr1EJhP6CTbRGuYXeE/4NI6iGi/PRKGDCaM1lxoDihRU8Kcy770QQ+hLNrmWIAmw==</DigestValue></Reference></SignedInfo><SignatureValue>FVpIur/3IyXObIxoit1kc3+/Em2hY9OTStJAxBD8aF+qIplTxOKTJ8fTL6fCjkf9lHGTvshkwPzJUXtYLu6fGw==</SignatureValue><KeyInfo><KeyName>BF66E582888CC845</KeyName><KeyValue><RSAKeyValue><Modulus>n5YsGT0w5Z70ONPbqszhExfJU+KY3Bscftc2jxUn4wxpSjEUhnCuTd88OK5QbDW3Mupoc61jr83lRhUCjchFAmCigpC10rEntTfEU+7qtX8ud/jJJDB1a9lTIB6bhBN//X8IQDjhmHrfKvfen3p7RxLrFoxzWgpwKriuGI5wUlU=</Modulus><Exponent>AQAB</Exponent></RSAKeyValue></KeyValue></KeyInfo></Signature></AcuseAceptacionRechazo>',
                'folios': [{'uuid': 'FD74D156-B9B0-44A5-9906-E08182E8363E', 'estatusUUID': '1001', 'respuesta': 'Aceptacion'}]
            },
            'status': 'success'
        })

        res = swsapien.accept_reject(
            request
        )

        assert mk.called
        mk.call_args.kwargs["headers"]["User-Agent"] = 'this is a test'

        args = json.dumps(mk.call_args.kwargs, indent=2, default=str, ensure_ascii=False)
        verify = verify_result(data=args, filename="test_accept_reject.json")
        assert verify

        assert res.folios == {'FD74D156-B9B0-44A5-9906-E08182E8363E': {'estatusUUID': '1001', 'respuesta': 'Aceptacion'}}


def test_swsapien_pending():
    with mock.patch(f'requests.request') as mk:
        mk.return_value.ok = True
        mk.return_value.json = mock.Mock(return_value={
            'codStatus': '1100',
            'message': 'CA1100 - Se recibío la respuesta de la petición de forma exitosa.',
            'data': {'uuid': ['C8F4B71E-2B2F-439B-8118-D044D8B5F444', '0EC7251E-7CB9-4CFB-A05E-88C0074A89D7', '7FDA7D8C-1B1A-4E24-9AF6-7F7CB3950D51'], 'codEstatus': '1100'},
            'status': 'success'
        })

        res = swsapien.pending("EKU9003173C9")

        assert mk.called
        mk.call_args.kwargs["headers"]["User-Agent"] = 'this is a test'

        args = json.dumps(mk.call_args.kwargs, indent=2, default=str, ensure_ascii=False)
        verify = verify_result(data=args, filename="test_pending.json")
        assert verify

        assert res == ['C8F4B71E-2B2F-439B-8118-D044D8B5F444', '0EC7251E-7CB9-4CFB-A05E-88C0074A89D7', '7FDA7D8C-1B1A-4E24-9AF6-7F7CB3950D51']


def test_swsapien_recover():
    with mock.patch(f'requests.request') as mk:
        mk.return_value.ok = True
        mk.return_value.json = mock.Mock(return_value={
            'data': {'metaData': {'page': 1, 'perPage': 10, 'pageCount': 0, 'totalCount': 0, 'links': {'current': '?page=1&perPage=10'}}, 'records': []}, 'status': 'success'
        })

        res = swsapien.recover(
            document_id="ab21a13a-7385-4493-bec1-52cfb53ec9a7"
        )

        assert mk.called
        mk.call_args.kwargs["headers"]["User-Agent"] = 'this is a test'

        args = json.dumps(mk.call_args.kwargs, indent=2, default=str, ensure_ascii=False)
        verify = verify_result(data=args, filename="recover.json")
        assert verify


def test_swsapien_list_69b():
    pass
    # unable to test
