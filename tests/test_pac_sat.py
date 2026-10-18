import os.path
import sqlite3
import types
from datetime import date, datetime, timedelta, timezone
from decimal import Decimal
from uuid import UUID
from pprint import PrettyPrinter
from unittest import mock

import requests

from satcfdi.utils import StrEnum

from satcfdi.create.catalogos import EstadoComprobante

from satcfdi.create.cfd.catalogos import TipoDeComprobante

from satcfdi import __version__
from satcfdi.cfdi import CFDI
from satcfdi.exceptions import ResponseError
from satcfdi.models import Code
from satcfdi.pacs import Environment
from satcfdi.pacs import TaxpayerStatus
from satcfdi.pacs import TaxpayerStatusList69
from satcfdi.pacs.sat import _CFDISolicitaDescargaEmitidos, _CFDIAutenticacion, EstadoSolicitud, \
    TipoDescargaMasivaTerceros, _init_and_load_listado_69
from satcfdi.pacs.sat import SAT
from satcfdi.pacs.sat import _get_listado_69b
from satcfdi.pacs.sat import _get_listado_69, _refresh_listado_69, _init_listado_69_db, _parse_listado_69_csv
from satcfdi.pacs.sat import _set_arguments

from .utils import get_signer, verify_result

UTC = timezone.utc

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


def test_listado69b_checks_expiration_on_each_call(tmp_path):
    cache_path = tmp_path / 'listado.json'
    cache_path.write_text('{"AAA191919HHH":"Desvirtuado"}', encoding='utf-8')
    os.utime(cache_path, (100, 100))
    with open(os.path.join(current_dir, 'pac_sat_responses', 'listado_69b.txt'), 'rb') as f:
        response = types.SimpleNamespace(status_code=200, content=f.read())

    with mock.patch(f'{module}.pacs.sat.LISTADO_COMPLETO_69B_JSON', str(cache_path)), \
         mock.patch(f'{module}.pacs.sat.time.time', return_value=110) as clock, \
         mock.patch('requests.get', return_value=response) as request:
        assert _get_listado_69b(refresh_time=10) == {'AAA191919HHH': 'Desvirtuado'}
        request.assert_not_called()

        clock.return_value = 111
        assert len(_get_listado_69b(refresh_time=10)) == 3
        request.assert_called_once()


def test_listado69b_missing_file_downloads(tmp_path):
    with open(os.path.join(current_dir, 'pac_sat_responses', 'listado_69b.txt'), 'rb') as f:
        response = types.SimpleNamespace(status_code=200, content=f.read())
    cache_path = tmp_path / 'missing.json'
    with mock.patch(f'{module}.pacs.sat.LISTADO_COMPLETO_69B_JSON', str(cache_path)), \
         mock.patch('requests.get', return_value=response) as request:
        assert len(_get_listado_69b()) == 3
        assert cache_path.exists()
        request.assert_called_once()


def test_listado69b_failed_download_preserves_file(tmp_path):
    import pytest

    cache_path = tmp_path / 'listado.json'
    original = '{"AAA191919HHH":"Desvirtuado"}'
    cache_path.write_text(original, encoding='utf-8')
    response = types.SimpleNamespace(status_code=503)
    with mock.patch(f'{module}.pacs.sat.LISTADO_COMPLETO_69B_JSON', str(cache_path)), \
         mock.patch('requests.get', return_value=response):
        with pytest.raises(ResponseError, match='503'):
            _get_listado_69b(refresh_time=-100000)
    assert cache_path.read_text(encoding='utf-8') == original


def _listado_69_request(url, **kwargs):
    path = os.path.join(current_dir, 'pac_sat_responses', 'listado_69', os.path.basename(url))
    if not os.path.exists(path):
        path = os.path.join(current_dir, 'pac_sat_responses', 'listado_69', 'default.csv')

    with open(path, 'rb') as f:
        data = f.read()

    a = types.SimpleNamespace()
    a.status_code = 200
    a.content = data
    return a


def test_listado69():
    with mock.patch(f'requests.get', _listado_69_request) as mk:
        connection = _get_listado_69(refresh_time=-100000)

        meta = dict(connection.execute("SELECT lista, updated_at FROM listado_69_meta"))
        assert set(meta) == {e.value for e in TaxpayerStatusList69}

        rows = connection.execute("SELECT lista, supuesto FROM listado_69 WHERE rfc = 'CCC030303CCC'").fetchall()
        assert rows == [('cancelados', 'CANCELADOS')]

        rows = connection.execute("SELECT lista, supuesto FROM listado_69 WHERE rfc = 'DDD040404DDD'").fetchall()
        assert rows == [('csd_sin_efectos', 'SUPUESTO CSD')]

        rows = connection.execute("SELECT count(*) FROM listado_69 WHERE rfc = ''").fetchone()
        assert rows == (0,)


def test_sat_list_69():
    with mock.patch(f'requests.get', _listado_69_request) as mk:
        sat_service = SAT(environment=Environment.TEST)

        res = sat_service.list_69('AAA010101AAA')
        assert res == {
            TaxpayerStatusList69.FIRMES: 'FIRMES',
            TaxpayerStatusList69.CANCELADOS: 'CANCELADOS POR INSOLVENCIA',
            TaxpayerStatusList69.CONDONADOS_07_15: None,
        }

        res = sat_service.list_69(' bbb020202bbb ')
        assert res == {TaxpayerStatusList69.FIRMES: 'FIRMES'}


def test_sat_list_69_notfound():
    with mock.patch(f'requests.get', _listado_69_request) as mk:
        sat_service = SAT(environment=Environment.TEST)
        res = sat_service.list_69('xxxx')
        assert res == {}


def test_listado69_csv_windows_1252():
    data = 'RFC,Razón Social,Supuesto de Cancelación\r\nEEE050505EEE,CAMIÓN SA DE CV,ARTÍCULO 17-H\r\n'.encode('windows-1252')
    data += b'FFF060606FFF,EMPRESA \x81 SA DE CV,X\r\n'

    rows = list(_parse_listado_69_csv(data, 'RFC', 'SUPUESTO DE CANCELACION'))
    assert rows == [('EEE050505EEE', 'ARTÍCULO 17-H'), ('FFF060606FFF', 'X')]


def test_listado69_refresh_failure_keeps_data():
    connection = sqlite3.connect(':memory:')
    _init_listado_69_db(connection)

    with mock.patch(f'requests.get', _listado_69_request) as mk:
        _refresh_listado_69(connection, TaxpayerStatusList69.FIRMES)

    failures = [
        types.SimpleNamespace(status_code=500, content=b''),
        types.SimpleNamespace(status_code=200, content=b''),
        types.SimpleNamespace(status_code=200, content=b'<html></html>'),
        types.SimpleNamespace(status_code=200, content=b'RFC,SUPUESTO\r\n'),
    ]
    for response in failures:
        with mock.patch(f'requests.get', return_value=response) as mk:
            try:
                _refresh_listado_69(connection, TaxpayerStatusList69.FIRMES)
            except ResponseError:
                pass

    with mock.patch(f'requests.get', side_effect=requests.ConnectionError) as mk:
        try:
            _refresh_listado_69(connection, TaxpayerStatusList69.FIRMES)
        except ResponseError:
            pass

    rows = connection.execute("SELECT rfc FROM listado_69 WHERE lista = 'firmes' ORDER BY rfc").fetchall()
    assert rows == [('AAA010101AAA',), ('BBB020202BBB',)]


def test_listado69_never_loaded():
    import pytest

    response = types.SimpleNamespace(status_code=500, content=b'')
    _init_and_load_listado_69.cache_clear()
    with mock.patch(f'{module}.pacs.sat.LISTADO_69_DB', ':memory:'), mock.patch(f'requests.get', return_value=response):
        with pytest.raises(ResponseError):
            _get_listado_69(refresh_time=-100000)


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

        res = sat_service.recover_comprobante_emitted_request(
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


def test_set_arguments():
    from lxml import etree

    nsmap = {'des': 'http://example.com/test'}
    element = etree.Element(etree.QName(nsmap['des'], 'Root'), nsmap=nsmap)
    element.prefix  # force prefix resolution

    class MyEnum(StrEnum):
        VALUE_A = "enum_value_a"

    arguments = {
        'StringArg': 'hello',
        'EnumArg': MyEnum.VALUE_A,
        'UUIDArg': UUID('6114cfd0-87d2-45b8-99b1-7c19475c9cda'),
        'DateTimeArg': datetime(2022, 6, 15, 10, 30, 0),
        'DateArg': date(2022, 6, 15),
        'NoneArg': None,
        'ListArg': [('ItemA', 'val1'), ('ItemB', 'val2')],
    }

    _set_arguments(element, arguments)

    assert etree.tostring(element).decode() == (
        '<des:Root xmlns:des="http://example.com/test" StringArg="hello" EnumArg="enum_value_a" '
        'UUIDArg="6114cfd0-87d2-45b8-99b1-7c19475c9cda" DateTimeArg="2022-06-15T10:30:00" DateArg="2022-06-15">'
        '<des:ListArg><des:ItemA>val1</des:ItemA><des:ItemB>val2</des:ItemB></des:ListArg></des:Root>'
    )


def test_set_arguments_invalid_type():
    from lxml import etree
    import pytest

    nsmap = {'des': 'http://example.com/test'}
    element = etree.Element(etree.QName(nsmap['des'], 'Root'), nsmap=nsmap)

    with pytest.raises(ValueError, match="Invalid Arguments"):
        _set_arguments(element, {'BadArg': 12345})
