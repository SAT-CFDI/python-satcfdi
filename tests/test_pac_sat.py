import os.path
import types
from datetime import datetime, timedelta, UTC
from decimal import Decimal
from pprint import PrettyPrinter
from unittest import mock

from satcfdi.create.catalogos import EstadoComprobante

from satcfdi.create.cfd.catalogos import TipoDeComprobante

from satcfdi import __version__
from satcfdi.cfdi import CFDI
from satcfdi.models import Code
from satcfdi.pacs import Environment
from satcfdi.pacs import TaxpayerStatus
from satcfdi.pacs.sat import _CFDISolicitaDescargaEmitidos, _CFDIAutenticacion, EstadoSolicitud, TipoDescargaMasivaTerceros
from satcfdi.pacs.sat import SAT
from satcfdi.pacs.sat import _get_listado_69b

from tests.utils import get_signer, verify_result

module = 'satcfdi'
current_dir = os.path.dirname(__file__)
pp = PrettyPrinter()


def test_pac_sat_cfdi():
    sat_service = SAT(environment=Environment.TEST)

    with mock.patch(f'requests.post') as mk:
        mk.return_value.ok = True
        mk.return_value.content = (
            b'<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"><s:Body><ConsultaResponse xmlns="http://tempuri.org/"><ConsultaResult '
            b'xmlns:a="http://schemas.datacontract.org/2004/07/Sat.Cfdi.Negocio.ConsultaCfdi.Servicio" xmlns:i="http://www.w3.org/2001/XMLSchema-instance"><a:CodigoEstatus>S - '
            b'Comprobante obtenido satisfactoriamente.</a:CodigoEstatus><a:EsCancelable>No '
            b'cancelable</a:EsCancelable><a:Estado>Vigente</a:Estado><a:EstatusCancelacion/><a:ValidacionEFOS>200</a:ValidacionEFOS></ConsultaResult></ConsultaResponse></s:Body'
            b'></s:Envelope> '
        )

        cfdi = CFDI({
            "Emisor": {
                "Rfc": 'RFC_EMISOR'
            },
            "Receptor": {
                "Rfc": 'RFC_RECEPTOR'
            },
            "Total": Decimal('123456.00'),
            "Complemento": {
                "TimbreFiscalDigital": {
                    "UUID": "6114cfd0-87d2-45b8-99b1-7c19475c9cda"
                }
            }
        })
        # res = sat_service.consulta(
        #     rfc_emisor='RFC_EMISOR',
        #     rfc_receptor='RFC_RECEPTOR',
        #     total='123,456.00',
        #     uuid="6114cfd0-87d2-45b8-99b1-7c19475c9cda"
        # )
        res = sat_service.status(
            cfdi
        )

        assert mk.called
        print(mk.call_args.kwargs)
        assert mk.call_args.kwargs == {
            'url': 'https://pruebacfdiconsultaqr.cloudapp.net/ConsultaCFDIService.svc',
            'data': '<Envelope xmlns="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tem="http://tempuri.org/"><Body><tem:Consulta><tem:expresionImpresa><![CDATA[?re=RFC_EMISOR&rr=RFC_RECEPTOR&tt=123456.00&id=6114cfd0-87d2-45b8-99b1-7c19475c9cda]]></tem:expresionImpresa></tem:Consulta></Body></Envelope>',
            'headers': {
                'Content-type': 'text/xml;charset="utf-8"',
                'Accept': 'text/xml',
                'Cache-Control': 'no-cache',
                'SOAPAction': 'http://tempuri.org/IConsultaCFDIService/Consulta',
                'User-Agent': __version__.__user_agent__,
            },
            'verify': False
        }

    assert res == {'CodigoEstatus': 'S - Comprobante obtenido satisfactoriamente.', 'EsCancelable': 'No cancelable', 'Estado': 'Vigente', 'EstatusCancelacion': None,
                   'ValidacionEFOS': '200'}


def test_listado69b():
    with open(os.path.join(current_dir, 'pac_sat_responses', 'listado_69b.txt'), 'rb') as f:
        data = f.read()

    def req(*args, **kwargs):
        a = types.SimpleNamespace()
        a.status_code = 200
        a.content = data
        return a

    with mock.patch(f'requests.get', req) as mk:

        listado = _get_listado_69b(refresh_time=-100000)
        assert "SAT970701NN3" not in listado
        assert len(listado) == 3
        values = [e.value for e in TaxpayerStatus]

        assert all(x in values for x in listado.values())
        assert listado['AAA090909HHH'] == TaxpayerStatus.SENTENCIA_FAVORABLE.value


def test_sat_list_69b():
    sat_service = SAT(environment=Environment.TEST)
    res = sat_service.list_69b('AAA191919HHH')
    assert res == TaxpayerStatus.DESVIRTUADO


def test_sat_list_69b_notfound():
    sat_service = SAT(environment=Environment.TEST)
    res = sat_service.list_69b('xxxx')
    assert res is None


def test_sat_service_authentication():
    signer = get_signer('xiqb891116qe4')

    with mock.patch(f'{module}.pacs.sat.datetime') as m:
        m.now = mock.Mock(return_value=datetime(2022, 1, 1))

        req = _CFDIAutenticacion(signer=signer)
        res = req.get_payload()

        verify = verify_result(data=res, filename="test_sat_service_authentication.xml")
        assert verify


def test_sat_service_solicitud():
    signer = get_signer('xiqb891116qe4')

    with mock.patch(f'{module}.pacs.sat.datetime') as m:
        m.now = mock.Mock(return_value=datetime(2022, 1, 1))

        req = _CFDISolicitaDescargaEmitidos(
            signer=signer,
            arguments={
                'FechaFinal': 'FechaFinal',
                'FechaInicial': 'FechaInicial',
                'RfcEmisor': "RfcEmisor",
                'RfcSolicitante': "RfcSolicitante",
                'TipoSolicitud': "TipoSolicitud",
                'TipoComprobante': "TipoComprobante",
                'EstadoComprobante': "EstadoComprobante",
                'RfcACuentaTerceros': "RfcACuentaTerceros",
                'Complemento': "Complemento",
                'UUID': "UUID",
            }

        )
        res = req.get_payload()

        verify = verify_result(data=res, filename="test_sat_service_solicitud.xml")
        assert verify


def test_status_code():
    assert EstadoSolicitud(5).name == 'RECHAZADA'

    est_code = Code(5, EstadoSolicitud(5).name)
    alt_text = str(est_code)
    assert alt_text == "5 - RECHAZADA"
    assert EstadoSolicitud.RECHAZADA == est_code
    assert est_code == EstadoSolicitud.RECHAZADA


def test_pac_sat_uuid():
    signer = get_signer('xiqb891116qe4')
    sat_service = SAT(environment=Environment.TEST, signer=signer)

    sat_service.token_comprobante = {
        "Expires": datetime.now(UTC).replace(tzinfo=None) + timedelta(seconds=3600),
        "AutenticaResult": "token_comprobante"
    }

    with open(os.path.join(current_dir, 'pac_sat_responses', 'response-folio-with-id.xml'), 'rb') as f:
        content = f.read()

    with mock.patch(f'requests.post') as mk:
        mk.return_value.ok = True
        mk.return_value.content = content

        res = sat_service.recover_comprobante_uuid_request(
            folio="6114cfd0-87d2-45b8-99b1-7c19475c9cda",
        )

        mk.assert_called_once()
        del mk.call_args.kwargs['headers']['User-Agent']

        verify = verify_result(data=pp.pformat(mk.call_args.kwargs), filename=f"pac_sat_uuid.pretty.py")
        assert verify


def test_pac_sat_rfc():
    signer = get_signer('xiqb891116qe4')
    sat_service = SAT(environment=Environment.TEST, signer=signer)

    sat_service.token_comprobante = {
        "Expires": datetime.now(UTC).replace(tzinfo=None) + timedelta(seconds=3600),
        "AutenticaResult": "token_comprobante"
    }

    with open(os.path.join(current_dir, 'pac_sat_responses', 'response-emited-with-id.xml'), 'rb') as f:
        content = f.read()

    with mock.patch(f'requests.post') as mk:
        mk.return_value.ok = True
        mk.return_value.content = content

        res = sat_service.recover_comprobante_emited_request(
            tipo_solicitud=TipoDescargaMasivaTerceros.CFDI,
            rfc_emisor="ABC123456ABC",
            rfc_receptor="ABC123456ABC",
            fecha_inicial=datetime(2021, 1, 1),
            fecha_final=datetime(2021, 1, 1),
            tipo_comprobante=TipoDeComprobante.INGRESO,
            estado_comprobante=EstadoComprobante.VIGENTE,

        )

        mk.assert_called_once()
        del mk.call_args.kwargs['headers']['User-Agent']

        verify = verify_result(data=pp.pformat(mk.call_args.kwargs), filename=f"pac_sat_rfc.pretty.py")
        assert verify
