import base64
import csv
import json
import logging
import os
import time
from abc import abstractmethod
from collections.abc import Sequence
from datetime import date, datetime, timedelta, UTC
from enum import IntEnum, Enum, StrEnum
from functools import cache
from itertools import islice
from uuid import UUID

import requests
from bs4 import BeautifulSoup
from lxml import etree
from lxml.etree import QName
from packaging import version

from satcfdi.create.cfd.catalogos import TipoDeComprobante
from . import PAC, Environment, TaxpayerStatus
from .. import __version__
from ..cfdi import CFDI
from ..create.w3.signature import signature_c14n_sha1, _digest, _tobytes
from ..exceptions import ResponseError
from ..models import Signer, Certificate
from ..transform import MEXICO_TZ, get_timezone, verify_certificate
from ..utils import iterate, parser

logger = logging.getLogger(__name__)
current_dir = os.path.dirname(__file__)

LISTADO_COMPLETO_69B_JSON = os.path.join(current_dir, 'Listado_Completo_69-B.json')
REFRESH_TIME = (15 * 86400)  # 15 Days


class EstadoSolicitud(IntEnum):
    ACEPTADA = 1
    EN_PROCESO = 2
    TERMINADA = 3
    ERROR = 4
    RECHAZADA = 5
    VENCIDA = 6


class EstadoComprobante(StrEnum):
    CANCELADO = 'Cancelado'
    VIGENTE = 'Vigente'
    TODOS = 'Todos'


class CodigoEstadoSolicitud(StrEnum):
    # 5000 Solicitud recibida con éxito
    # Indica que la solicitud de descarga que se está
    # verificando fue aceptada.
    EXITO = "5000"

    # 5002 Se agotó las solicitudes
    # de por vida
    # Para el caso de descarga de tipo CFDI, se tiene un
    # límite máximo para solicitudes con los mismos
    # parámetros (Fecha Inicial, Fecha Final, RfcEmisor,
    # RfcReceptor).
    AGOTADO = "5002"

    # 5003 Tope máximo Indica que en base a los parámetros de consulta
    # se está superando el tope máximo de CFDI o
    # Metadata, por solicitud de descarga masiva.
    TOPE_MAXIMO = "5003"

    # 5004 No se encontró la información
    # Indica que la solicitud de descarga que se está
    # verificando no generó paquetes por falta de
    # información.
    NO_ENCONTRADO = "5004"

    # 5005 Solicitud duplicada En caso de que exista una solicitud vigente con
    # los mismos parámetros (Fecha Inicial, Fecha Final,
    # RfcEmisor, RfcReceptor, TipoSolicitud), no se
    # permitirá generar una nueva solicitud.
    DUPLICADO = "5005"

    # 404 Error no Controlado Error genérico, en caso de presentarse realizar
    # nuevamente la petición y si persiste el error
    # levantar un RMA.
    ERROR_NO_CONTROLADO = "404"


class TipoDescargaMasivaTerceros(StrEnum):
    CFDI = 'CFDI'
    METADATA = 'Metadata'
    PDF = 'PDF'
    PDFCOCEMA = 'PDFCOCEMA'
    TXTUUIDMASIVA = 'TXTUUIDMASIVA'


def _service_logger(response_type, response):
    if response["CodEstatus"] == "5000":
        logger.info("%s: %s", response_type, response)
        return
    raise ResponseError(response)


def _certificate_path(certificate_no):
    return f"{certificate_no[0:6]}/{certificate_no[6:12]}/{certificate_no[12:14]}/{certificate_no[14:16]}/{certificate_no[16:18]}/{certificate_no}"


@cache
def _get_listado_69b(refresh_time=REFRESH_TIME):
    try:
        t = os.path.getmtime(LISTADO_COMPLETO_69B_JSON)
    except FileNotFoundError:
        t = -refresh_time

    if time.time() > t + refresh_time:
        r = requests.get(
            url="http://omawww.sat.gob.mx/cifras_sat/Documents/Listado_Completo_69-B.csv",
            headers={
                "User-Agent": __version__.__user_agent__
            }
        )

        if r.status_code == 200:
            lines = str(r.content, 'windows-1250').splitlines(keepends=True)
            cvs_reader = csv.reader(islice(lines, 3, None), delimiter=',', quotechar='"')
            res = {row[1]: row[3] for row in cvs_reader}
            _save_listado_69b(res)
            return res

        logger.error("Unable to get latest Listado 69B, status code: %s", r.status_code)

    if t > 0:
        return _load_listado_69b()
    else:
        raise ResponseError("Unable to load Listado Completo 69B")


def _save_listado_69b(data):
    with open(LISTADO_COMPLETO_69B_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, separators=(',', ':'), check_circular=False)


def _load_listado_69b():
    with open(LISTADO_COMPLETO_69B_JSON, "r", encoding="utf-8") as f:
        return json.load(f)


# SAT REQUESTS #
def _set_arguments(element, arguments: dict) -> etree.Element:
    for key, value in arguments.items():
        if value is None:
            continue
        elif isinstance(value, str):
            element.set(key, value)
        elif isinstance(value, UUID):
            element.set(key, str(value))
        elif isinstance(value, datetime):
            element.set(key, value.isoformat(timespec="seconds"))
        elif isinstance(value, date):
            element.set(key, value.isoformat())
        elif isinstance(value, Enum):
            element.set(key, value.value)
        elif isinstance(value, list):
            sub_elem = etree.SubElement(element, etree.QName(element.nsmap[element.prefix], key))
            for (k, v) in value:
                etree.SubElement(sub_elem, etree.QName(element.nsmap[element.prefix], k)).text = v
        else:
            raise ValueError("Invalid Arguments", key, value)


def _get_template(template_name: str) -> etree.Element:
    return etree.parse(
        source=os.path.join(current_dir, "sat_templates", template_name),
        parser=parser
    ).getroot()


class _SATRequest:
    xml_name = None
    soap_url = None
    soap_action = None
    solicitud_xpath = None
    sign_payload = True
    https_verify = True

    def __init__(self, signer: Signer = None, arguments: dict = None):
        self.signer = signer
        self.arguments = arguments or {}

    def get_payload(self):
        template = _get_template(self.xml_name)
        self._prepare_payload(template)
        # return _tobytes(template)
        return etree.tostring(template, encoding="UTF-8")

    @abstractmethod
    def process_response(self, response: etree.Element):
        pass

    def _prepare_payload(self, root: etree.Element):
        sol = root.find(self.solicitud_xpath)
        _set_arguments(sol, self.arguments)
        if self.sign_payload:
            sol.append(
                signature_c14n_sha1(
                    signer=self.signer,
                    element=sol.getparent()
                ).to_xml()
            )


class _CFDIAutenticacion(_SATRequest):
    xml_name = 'autentica.xml'
    soap_url = 'https://cfdidescargamasivasolicitud.clouda.sat.gob.mx/Autenticacion/Autenticacion.svc'
    wsdl_url = 'https://cfdidescargamasivasolicitud.clouda.sat.gob.mx/Autenticacion/Autenticacion.svc?wsdl'
    soap_action = 'http://DescargaMasivaTerceros.gob.mx/IAutenticacion/Autentica'

    DATE_TIME_FORMAT: str = '%Y-%m-%dT%H:%M:%S.%fZ'

    def _prepare_payload(self, root):
        date_created = datetime.now(UTC).replace(tzinfo=None)
        date_expires = date_created + timedelta(seconds=self.arguments.get("seconds", 300))
        security = root.find('{*}Header/{*}Security')

        security.find('{*}Timestamp/{*}Created').text = date_created.strftime(
            self.DATE_TIME_FORMAT)
        security.find('{*}Timestamp/{*}Expires').text = date_expires.strftime(
            self.DATE_TIME_FORMAT)
        security.find('{*}BinarySecurityToken').text = self.signer.certificate_base64()

        security.find('{*}Signature/{*}SignedInfo/{*}Reference/{*}DigestValue').text = _digest(
            security.find('{*}Timestamp')
        )
        security.find('{*}Signature/{*}SignatureValue').text = \
            self.signer.sign_sha1(
                _tobytes(security.find('{*}Signature/{*}SignedInfo'))
            )

    def process_response(self, response):
        authres = response.find('{*}Body/{*}AutenticaResponse/{*}AutenticaResult')
        timestamps = response.find('{*}Header/{*}Security/{*}Timestamp')

        def todatetime(name):
            return datetime.fromisoformat(timestamps.find(name).text[:-1])

        return {
            "Created": todatetime('{*}Created'),
            "Expires": todatetime('{*}Expires'),
            "AutenticaResult": authres.text
        }


class _CFDISolicitaDescargaEmitidos(_SATRequest):
    xml_name = 'solicitaEmitidos.xml'
    soap_url = 'https://cfdidescargamasivasolicitud.clouda.sat.gob.mx/SolicitaDescargaService.svc'
    soap_action = "http://DescargaMasivaTerceros.sat.gob.mx/ISolicitaDescargaService/SolicitaDescargaEmitidos"
    solicitud_xpath = '{*}Body/{*}SolicitaDescargaEmitidos/{*}solicitud'

    def process_response(self, response: etree.Element):
        res = response.find('{*}Body/{*}SolicitaDescargaEmitidosResponse/{*}SolicitaDescargaEmitidosResult')
        return {
            **res.attrib
        }


class _CFDISolicitaDescargaRecibidos(_SATRequest):
    xml_name = 'solicitaRecibidos.xml'
    soap_url = 'https://cfdidescargamasivasolicitud.clouda.sat.gob.mx/SolicitaDescargaService.svc'
    soap_action = "http://DescargaMasivaTerceros.sat.gob.mx/ISolicitaDescargaService/SolicitaDescargaRecibidos"
    solicitud_xpath = '{*}Body/{*}SolicitaDescargaRecibidos/{*}solicitud'

    def process_response(self, response: etree.Element):
        res = response.find('{*}Body/{*}SolicitaDescargaRecibidosResponse/{*}SolicitaDescargaRecibidosResult')
        return {
            **res.attrib
        }

class _CFDISolicitaDescargaFolio(_SATRequest):
    xml_name = 'solicitaFolio.xml'
    soap_url = 'https://cfdidescargamasivasolicitud.clouda.sat.gob.mx/SolicitaDescargaService.svc'
    soap_action = "http://DescargaMasivaTerceros.sat.gob.mx/ISolicitaDescargaService/SolicitaDescargaFolio"
    solicitud_xpath = '{*}Body/{*}SolicitaDescargaFolio/{*}solicitud'

    def process_response(self, response: etree.Element):
        res = response.find('{*}Body/{*}SolicitaDescargaFolioResponse/{*}SolicitaDescargaFolioResult')
        return {
            **res.attrib
        }

class _CFDIVerificaSolicitudDescarga(_SATRequest):
    xml_name = 'verifica.xml'
    soap_url = 'https://cfdidescargamasivasolicitud.clouda.sat.gob.mx/VerificaSolicitudDescargaService.svc'
    soap_action = 'http://DescargaMasivaTerceros.sat.gob.mx/IVerificaSolicitudDescargaService/VerificaSolicitudDescarga'
    solicitud_xpath = '{*}Body/{*}VerificaSolicitudDescarga/{*}solicitud'

    def process_response(self, response: etree.Element):
        res = response.find('{*}Body/{*}VerificaSolicitudDescargaResponse/{*}VerificaSolicitudDescargaResult')

        def descarga_result(node):
            result = dict()
            result['IdsPaquetes'] = [n.text for n in node.iterfind('{http://DescargaMasivaTerceros.sat.gob.mx}IdsPaquetes')]
            at = node.attrib.get('CodEstatus')
            if at is not None:
                result['CodEstatus'] = at
            result['EstadoSolicitud'] = int(node.attrib['EstadoSolicitud'])
            at = node.attrib.get('CodigoEstadoSolicitud')
            if at is not None:
                result['CodigoEstadoSolicitud'] = at
            result['NumeroCFDIs'] = int(node.attrib['NumeroCFDIs'])
            at = node.attrib.get('Mensaje')
            if at is not None:
                result['Mensaje'] = at
            return result

        return descarga_result(res)


class _CFDIDescargaMasiva(_SATRequest):
    xml_name = 'descarga.xml'
    soap_url = 'https://cfdidescargamasiva.clouda.sat.gob.mx/DescargaMasivaService.svc'
    soap_action = 'http://DescargaMasivaTerceros.sat.gob.mx/IDescargaMasivaTercerosService/Descargar'
    solicitud_xpath = '{*}Body/{*}PeticionDescargaMasivaTercerosEntrada/{*}peticionDescarga'

    def process_response(self, response: etree.Element):
        paquete = response.find('{*}Body/{*}RespuestaDescargaMasivaTercerosSalida/{*}Paquete')
        header = response.find('{*}Header/{*}respuesta')

        def respuesta(node):
            result = dict()
            at = node.attrib.get('CodEstatus')
            if at is not None:
                result['CodEstatus'] = at
            at = node.attrib.get('Mensaje')
            if at is not None:
                result['Mensaje'] = at
            return result

        return respuesta(header), paquete.text


class _RetenAutenticacion(_CFDIAutenticacion):
    soap_url = 'https://retendescargamasivasolicitud.clouda.sat.gob.mx/Autenticacion/Autenticacion.svc'

class _RetenSolicitaDescargaEmitidos(_CFDISolicitaDescargaEmitidos):
    soap_url = 'https://retendescargamasivasolicitud.clouda.sat.gob.mx/SolicitaDescargaService.svc'

class _RetenSolicitaDescargaRecibidos(_CFDISolicitaDescargaRecibidos):
    soap_url = 'https://retendescargamasivasolicitud.clouda.sat.gob.mx/SolicitaDescargaService.svc'

class _RetenSolicitaDescargaFolio(_CFDISolicitaDescargaFolio):
    soap_url = 'https://retendescargamasivasolicitud.clouda.sat.gob.mx/SolicitaDescargaService.svc'

class _RetenVerificaSolicitudDescarga(_CFDIVerificaSolicitudDescarga):
    soap_url = 'https://retendescargamasivasolicitud.clouda.sat.gob.mx/VerificaSolicitudDescargaService.svc'

class _RetenDescargaMasiva(_CFDIDescargaMasiva):
    soap_url = 'https://retendescargamasiva.clouda.sat.gob.mx/DescargaMasivaService.svc'


class SAT(PAC):
    RFC = "SAT970701NN3"

    def __init__(self, signer: Signer = None, environment=Environment.PRODUCTION):
        self.signer = signer
        super().__init__(environment)
        self.token_comprobante = None
        self.token_retencion = None
        self.wait_time = 60

    def _get_headers(self, soap_action, needs_token_fn) -> dict:
        headers = {
            'Content-type': 'text/xml;charset="utf-8"',
            'Accept': 'text/xml',
            'Cache-Control': 'no-cache',
            "User-Agent": __version__.__user_agent__,
            'SOAPAction': soap_action
        }
        if needs_token_fn:
            headers['Authorization'] = f'WRAP access_token="{needs_token_fn()}"'
        return headers

    def _request(self, soap_url, data, soap_action, needs_token_fn, verify=True):
        response = requests.post(
            url=soap_url,
            data=data,
            headers=self._get_headers(soap_action, needs_token_fn=needs_token_fn),
            verify=verify
        )

        if not response.ok:
            raise ResponseError(response)

        return etree.fromstring(
            response.content,
            parser=parser
        )

    def _get_token_comprobante(self):
        if self.token_comprobante is None or self.token_comprobante["Expires"] <= datetime.now(UTC).replace(tzinfo=None) + timedelta(seconds=30):
            self.token_comprobante = self._autentica_comprobante()
        return self.token_comprobante["AutenticaResult"]

    def _get_token_retencion(self):
        if self.token_retencion is None or self.token_retencion["Expires"] <= datetime.now(UTC).replace(tzinfo=None) + timedelta(seconds=30):
            self.token_retencion = self._autentica_retencion()
        return self.token_retencion["AutenticaResult"]

    def _autentica_comprobante(self):
        return self._execute_req(
            _CFDIAutenticacion(signer=self.signer),
            needs_token_fn=None
        )

    def _autentica_retencion(self):
        return self._execute_req(
            _RetenAutenticacion(signer=self.signer),
            needs_token_fn=None
        )

    def _execute_req(self, req: _SATRequest, needs_token_fn):
        payload = req.get_payload()

        xml = self._request(
            soap_url=req.soap_url,
            data=payload,
            soap_action=req.soap_action,
            verify=req.https_verify,
            needs_token_fn=needs_token_fn
        )

        return req.process_response(xml)

    def status(self, cfdi: CFDI) -> dict:
        rfc_emisor = cfdi["Emisor"]["Rfc"]
        rfc_receptor = cfdi["Receptor"]["Rfc"]
        total = cfdi["Total"]
        uuid = cfdi["Complemento"]["TimbreFiscalDigital"]["UUID"]

        template = f'<Envelope xmlns="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tem="http://tempuri.org/"><Body><tem:Consulta><tem:expresionImpresa>' \
                   f'<![CDATA[?re={rfc_emisor}&rr={rfc_receptor}&tt={total}&id={uuid}]]>' \
                   f'</tem:expresionImpresa></tem:Consulta></Body></Envelope>'

        match self.environment:
            case Environment.PRODUCTION:
                host = "https://consultaqr.facturaelectronica.sat.gob.mx"
                verify = True
            case Environment.TEST:
                host = "https://pruebacfdiconsultaqr.cloudapp.net"
                verify = False
            case _:
                raise NotImplementedError("Environment not Supported")

        res = self._request(
            soap_url=f'{host}/ConsultaCFDIService.svc',
            data=template,
            soap_action='http://tempuri.org/IConsultaCFDIService/Consulta',
            verify=verify,
            needs_token_fn=None
        )

        res = res.find('{*}Body/{*}ConsultaResponse/{*}ConsultaResult')
        return {
            QName(i.tag).localname: i.text
            for i in res
        }

    def status_retencion(self, cfdi: CFDI) -> dict:
        rfc_emisor = cfdi["Emisor"]["RfcE"]
        rfc_receptor = cfdi["Receptor"]["Nacional"]["RfcR"]
        uuid = cfdi["Complemento"]["TimbreFiscalDigital"]["UUID"]

        params = {
            'folio': uuid,
            'rfcEmisor': rfc_emisor,
            'rfcReceptor': rfc_receptor
        }

        res = requests.get('https://prodretencionverificacion.clouda.sat.gob.mx/Home/ConsultaRetencion', params)

        if res.status_code == 200:
            soup = BeautifulSoup(res.text, 'html.parser')
            status = soup.find('span', string='Cancelado').string
            date = soup.find('td', id='tdFechaCancelacion').get_text(strip=True)

        return {
            "estado": status, "fecha": date
        }

    def validate(self, cfdi: CFDI):
        """
                verify if the CFDI is valid based on its signatures and certificates
                this method might need improvements
                :return:
                True is all certificate and signatures verifications passed
                """
        match cfdi.tag:
            case '{http://www.sat.gob.mx/cfd/3}Comprobante' | '{http://www.sat.gob.mx/cfd/4}Comprobante':
                return self._validate(
                    cfdi,
                    certificate=cfdi["Certificado"],
                    num_certificate=cfdi['NoCertificado'],
                    rfc=cfdi["Emisor"]["Rfc"],
                    seal=cfdi["Sello"],
                    date=cfdi['Fecha'],
                    postal_code=cfdi['LugarExpedicion'],
                    stamp_version="1.0" if version.parse(cfdi["Version"]) <= version.parse("3.2") else "1.1"
                )

            case '{http://www.sat.gob.mx/esquemas/retencionpago/1}Retenciones':
                return self._validate(
                    cfdi,
                    certificate=cfdi["Cert"],
                    num_certificate=cfdi['NumCert'],
                    rfc=cfdi["Emisor"]["RFCEmisor"],
                    seal=cfdi["Sello"],
                    date=cfdi['FechaExp'],
                    postal_code=None,
                    stamp_version="1.0"
                )

            case '{http://www.sat.gob.mx/esquemas/retencionpago/2}Retenciones':
                return self._validate(
                    cfdi,
                    certificate=cfdi["Certificado"],
                    num_certificate=cfdi['NoCertificado'],
                    rfc=cfdi["Emisor"]["RfcE"],
                    seal=cfdi["Sello"],
                    date=cfdi['FechaExp'],
                    postal_code=cfdi['LugarExpRetenc'],
                    stamp_version="1.1"
                )

    def _validate(self, cfdi, certificate, num_certificate, rfc, seal, date: datetime, postal_code, stamp_version):
        if not date.tzinfo:
            # debe corresponder con la hora local donde se expide el comprobante
            date = date.replace(tzinfo=get_timezone(postal_code))

        if stamp_version == "1.0":
            verify_fn = Certificate.verify_sha1
        else:
            verify_fn = Certificate.verify_sha256

        cert = Certificate.load_certificate(
            base64.b64decode(certificate)
        )

        if not verify_certificate(cert, at=date):
            return False

        if not cert.certificate_number == num_certificate:
            return False

        if not cert.rfc == rfc:
            return False

        if not verify_fn(
                self=cert,
                data=cfdi.cadena_original().encode(),
                signature=base64.b64decode(seal)
        ):
            return False

        # Timbre
        timbre = cfdi["Complemento"]["TimbreFiscalDigital"]
        # debe corresponder con la hora de la Zona Centro del Sistema de Horario en México.
        stamp_date = timbre["FechaTimbrado"].replace(tzinfo=MEXICO_TZ)

        if not timbre["Version"] == stamp_version:
            return False

        if not timbre["SelloCFD"] == seal:
            return False

        cert_sat = self.recover_certificate(
            no_certificado=timbre["NoCertificadoSAT"]
        )

        if rfc_pac := timbre.get("RfcProvCertif"):
            if not rfc_pac == cert_sat.rfc_pac:
                return False

        if not verify_certificate(cert, at=stamp_date):
            return False

        if not verify_fn(
                self=cert_sat,
                data=timbre.cadena_original().encode(),
                signature=base64.b64decode(timbre["SelloSAT"])
        ):
            return False

        # El rango de la fecha de generación no debe de ser mayor a 72 horas para la emisión del timbre.
        if not date <= stamp_date + timedelta(hours=72):
            return False

        return True

    def list_69b(self, rfc: str) -> TaxpayerStatus | None:
        listado = _get_listado_69b()
        r = listado.get(rfc)
        if r:
            return TaxpayerStatus(r)
        return None

    def recover_comprobante_emited_request(
            self,
            fecha_inicial: date | datetime | None = None,
            fecha_final: date | datetime | None = None,
            rfc_receptor: str | Sequence[str] | None = None,
            rfc_emisor: str | None = None,
            tipo_solicitud: TipoDescargaMasivaTerceros | str = TipoDescargaMasivaTerceros.CFDI,
            tipo_comprobante: TipoDeComprobante | str | None = None,
            estado_comprobante: EstadoComprobante | str | None = None,
            rfc_a_cuenta_terceros: str | None = None,
            complemento: str | None = None) -> dict:
        """
        Esta operación permite solicitar la descarga de CFDIs o Metadata y como
        resultado devuelve un id de solicitud o estatus de la petición realizada.

        :param fecha_inicial: Solo se buscarán CFDI, cuya fecha de emisión sea igual o mayor a la fecha inicial indicada en este parámetro.
            Parámetro obligatorio. Este parámetro no debe declararse en caso de realizar una consulta por el folio fiscal (UUID).
        :param fecha_final: Solo se buscarán CFDI, cuya fecha de emisión sea igual o menor a la fecha final indicada en este parámetro.
            Parámetro obligatorio. Este parámetro no debe declararse en caso de realizar una consulta por el folio fiscal (UUID).
        :param rfc_receptor: Contiene el/los RFCs receptores de los cuales se quiere consultar los CFDIs
            Importante: El campo RfcReceptor, únicamente permite la captura de 5 registros como máximo
        :param rfc_emisor: Contiene el RFC del emisor del cual se quiere consultar los CFDI.
            Parámetro obligatorio. Este parámetro no debe declararse en caso de realizar una consulta por el folio fiscal (UUID).
        :param tipo_solicitud: Define el tipo de descarga
        :param tipo_comprobante: Define el tipo de comprobante
        :param estado_comprobante: Define el estado del comprobante
        :param rfc_a_cuenta_terceros: Contiene el RFC del a cuenta a tercero del cual se quiere consultar los CFDIs
        :param complemento: Define el complemento de CFDI a descargar
        :return: respuesta de solicitud de descarga
        """
        arguments = {
            'FechaFinal': fecha_final,
            'FechaInicial': fecha_inicial,
            'RfcEmisor': rfc_emisor,
            'RfcReceptores': [('RfcReceptor', r) for r in iterate(rfc_receptor)] if rfc_receptor else None,
            'RfcSolicitante': self.signer.rfc,
            'TipoSolicitud': tipo_solicitud,
            'TipoComprobante': tipo_comprobante,
            'EstadoComprobante': estado_comprobante,
            'RfcACuentaTerceros': rfc_a_cuenta_terceros,
            'Complemento': complemento,
        }

        return self._execute_req(
            _CFDISolicitaDescargaEmitidos(
                signer=self.signer,
                arguments=arguments
            ),
            needs_token_fn=self._get_token_comprobante
        )

    def recover_comprobante_received_request(
            self,
            fecha_inicial: date | datetime | None = None,
            fecha_final: date | datetime | None = None,
            rfc_receptor: str | None = None,
            rfc_emisor: str | None = None,
            tipo_solicitud: TipoDescargaMasivaTerceros | str = TipoDescargaMasivaTerceros.CFDI,
            tipo_comprobante: TipoDeComprobante | str | None = None,
            estado_comprobante: EstadoComprobante | str | None = None,
            rfc_a_cuenta_terceros: str | None = None,
            complemento: str | None = None) -> dict:
        """
        Esta operación permite solicitar la descarga de CFDIs o Metadata y como
        resultado devuelve un id de solicitud o estatus de la petición realizada.

        :param fecha_inicial: Solo se buscarán CFDI, cuya fecha de emisión sea igual o mayor a la fecha inicial indicada en este parámetro.
            Parámetro obligatorio. Este parámetro no debe declararse en caso de realizar una consulta por el folio fiscal (UUID).
        :param fecha_final: Solo se buscarán CFDI, cuya fecha de emisión sea igual o menor a la fecha final indicada en este parámetro.
            Parámetro obligatorio. Este parámetro no debe declararse en caso de realizar una consulta por el folio fiscal (UUID).
        :param rfc_receptor: Contiene el/los RFCs receptores de los cuales se quiere consultar los CFDIs
            Importante: El campo RfcReceptor, únicamente permite la captura de 5 registros como máximo
        :param rfc_emisor: Contiene el RFC del emisor del cual se quiere consultar los CFDI.
            Parámetro obligatorio. Este parámetro no debe declararse en caso de realizar una consulta por el folio fiscal (UUID).
        :param tipo_solicitud: Define el tipo de descarga
        :param tipo_comprobante: Define el tipo de comprobante
        :param estado_comprobante: Define el estado del comprobante
        :param rfc_a_cuenta_terceros: Contiene el RFC del a cuenta a tercero del cual se quiere consultar los CFDIs
        :param complemento: Define el complemento de CFDI a descargar
        :return: respuesta de solicitud de descarga
        """
        arguments = {
            'FechaFinal': fecha_final,
            'FechaInicial': fecha_inicial,
            'RfcEmisor': rfc_emisor,
            'RfcReceptor': rfc_receptor,
            'RfcSolicitante': self.signer.rfc,
            'TipoSolicitud': tipo_solicitud,
            'TipoComprobante': tipo_comprobante,
            'EstadoComprobante': estado_comprobante,
            'RfcACuentaTerceros': rfc_a_cuenta_terceros,
            'Complemento': complemento,
        }

        return self._execute_req(
            _CFDISolicitaDescargaRecibidos(
                signer=self.signer,
                arguments=arguments
            ),
            needs_token_fn=self._get_token_comprobante
        )

    def recover_comprobante_uuid_request(
            self,
            folio: str | UUID | None = None) -> dict:
        """
        Esta operación permite solicitar la descarga de CFDIs o Metadata y como
        resultado devuelve un id de solicitud o estatus de la petición realizada.

        :param folio: Folio Fiscal
        :return: respuesta de solicitud de descarga
        """
        arguments = {
            'RfcSolicitante': self.signer.rfc,
            'Folio': folio,
        }

        return self._execute_req(
            _CFDISolicitaDescargaFolio(
                signer=self.signer,
                arguments=arguments
            ),
            needs_token_fn=self._get_token_comprobante
        )

    def recover_comprobante_status(self, id_solicitud: str) -> dict:
        return self._execute_req(
            _CFDIVerificaSolicitudDescarga(
                signer=self.signer,
                arguments={
                    'RfcSolicitante': self.signer.rfc,
                    'IdSolicitud': id_solicitud,
                }
            ),
            needs_token_fn=self._get_token_comprobante
        )

    def recover_comprobante_download(self, id_paquete: str) -> (dict, str):
        return self._execute_req(
            _CFDIDescargaMasiva(
                signer=self.signer,
                arguments={
                    'RfcSolicitante': self.signer.rfc,
                    'IdPaquete': id_paquete,
                }
            ),
            needs_token_fn=self._get_token_comprobante
        )

    def recover_retencion_emited_request(
            self,
            fecha_inicial: date | datetime | None = None,
            fecha_final: date | datetime | None = None,
            rfc_receptor: str | Sequence[str] | None = None,
            rfc_emisor: str | None = None,
            tipo_solicitud: TipoDescargaMasivaTerceros | str = TipoDescargaMasivaTerceros.CFDI,
            estado_comprobante: EstadoComprobante | str | None = None,
            complemento: str | None = None) -> dict:
        """
        Esta operación permite solicitar la descarga de CFDIs o Metadata y como
        resultado devuelve un id de solicitud o estatus de la petición realizada.

        :param fecha_inicial: Solo se buscarán CFDI, cuya fecha de emisión sea igual o mayor a la fecha inicial indicada en este parámetro.
            Parámetro obligatorio. Este parámetro no debe declararse en caso de realizar una consulta por el folio fiscal (UUID).
        :param fecha_final: Solo se buscarán CFDI, cuya fecha de emisión sea igual o menor a la fecha final indicada en este parámetro.
            Parámetro obligatorio. Este parámetro no debe declararse en caso de realizar una consulta por el folio fiscal (UUID).
        :param rfc_receptor: Contiene el/los RFCs receptores de los cuales se quiere consultar los CFDIs
            Importante: El campo RfcReceptor, únicamente permite la captura de 5 registros como máximo
        :param rfc_emisor: Contiene el RFC del emisor del cual se quiere consultar los CFDI.
            Parámetro obligatorio. Este parámetro no debe declararse en caso de realizar una consulta por el folio fiscal (UUID).
        :param tipo_solicitud: Define el tipo de descarga
        :param estado_comprobante: Define el estado del comprobante
        :param complemento: Define el complemento de CFDI a descargar
        :return: respuesta de solicitud de descarga
        """
        arguments = {
            'FechaFinal': fecha_final,
            'FechaInicial': fecha_inicial,
            'RfcEmisor': rfc_emisor,
            'RfcReceptores': [('RfcReceptor', r) for r in iterate(rfc_receptor)] if rfc_receptor else None,
            'RfcSolicitante': self.signer.rfc,
            'TipoSolicitud': tipo_solicitud,
            'EstadoComprobante': estado_comprobante,
            'Complemento': complemento,
        }

        return self._execute_req(
            _RetenSolicitaDescargaEmitidos(
                signer=self.signer,
                arguments=arguments
            ),
            needs_token_fn=self._get_token_retencion
        )

    def recover_retencion_received_request(
            self,
            fecha_inicial: date | datetime | None = None,
            fecha_final: date | datetime | None = None,
            rfc_receptor: str | None = None,
            rfc_emisor: str | None = None,
            tipo_solicitud: TipoDescargaMasivaTerceros | str = TipoDescargaMasivaTerceros.CFDI,
            estado_comprobante: EstadoComprobante | str | None = None,
            complemento: str | None = None) -> dict:
        """
        Esta operación permite solicitar la descarga de CFDIs o Metadata y como
        resultado devuelve un id de solicitud o estatus de la petición realizada.

        :param fecha_inicial: Solo se buscarán CFDI, cuya fecha de emisión sea igual o mayor a la fecha inicial indicada en este parámetro.
            Parámetro obligatorio. Este parámetro no debe declararse en caso de realizar una consulta por el folio fiscal (UUID).
        :param fecha_final: Solo se buscarán CFDI, cuya fecha de emisión sea igual o menor a la fecha final indicada en este parámetro.
            Parámetro obligatorio. Este parámetro no debe declararse en caso de realizar una consulta por el folio fiscal (UUID).
        :param rfc_receptor: Contiene el/los RFCs receptores de los cuales se quiere consultar los CFDIs
            Importante: El campo RfcReceptor, únicamente permite la captura de 5 registros como máximo
        :param rfc_emisor: Contiene el RFC del emisor del cual se quiere consultar los CFDI.
            Parámetro obligatorio. Este parámetro no debe declararse en caso de realizar una consulta por el folio fiscal (UUID).
        :param tipo_solicitud: Define el tipo de descarga
        :param estado_comprobante: Define el estado del comprobante
        :param complemento: Define el complemento de CFDI a descargar
        :return: respuesta de solicitud de descarga
        """
        arguments = {
            'FechaFinal': fecha_final,
            'FechaInicial': fecha_inicial,
            'RfcEmisor': rfc_emisor,
            'RfcReceptor': rfc_receptor,
            'RfcSolicitante': self.signer.rfc,
            'TipoSolicitud': tipo_solicitud,
            'EstadoComprobante': estado_comprobante,
            'Complemento': complemento,
        }

        return self._execute_req(
            _RetenSolicitaDescargaRecibidos(
                signer=self.signer,
                arguments=arguments
            ),
            needs_token_fn=self._get_token_retencion
        )

    def recover_retencion_uuid_request(
            self,
            folio: str | UUID | None = None) -> dict:
        """
        Esta operación permite solicitar la descarga de CFDIs o Metadata y como
        resultado devuelve un id de solicitud o estatus de la petición realizada.

        :param folio: Folio Fiscal
        :return: respuesta de solicitud de descarga
        """
        arguments = {
            'RfcSolicitante': self.signer.rfc,
            'Folio': folio,
        }

        return self._execute_req(
            _RetenSolicitaDescargaFolio(
                signer=self.signer,
                arguments=arguments
            ),
            needs_token_fn=self._get_token_retencion
        )


    def recover_retencion_status(self, id_solicitud: str) -> dict:
        return self._execute_req(
            _RetenVerificaSolicitudDescarga(
                signer=self.signer,
                arguments={
                    'RfcSolicitante': self.signer.rfc,
                    'IdSolicitud': id_solicitud,
                }
            ),
            needs_token_fn=self._get_token_retencion
        )

    def recover_retencion_download(self, id_paquete: str) -> (dict, str):
        return self._execute_req(
            _RetenDescargaMasiva(
                signer=self.signer,
                arguments={
                    'RfcSolicitante': self.signer.rfc,
                    'IdPaquete': id_paquete,
                }
            ),
            needs_token_fn=self._get_token_retencion
        )

    def recover_certificate(self, no_certificado: str | int) -> Certificate:
        path = _certificate_path(no_certificado)
        file_name = os.path.join(current_dir, f"rdc.sat.gob.mx/rccf/{no_certificado}.cer")

        if os.path.exists(file_name):
            with open(file_name, "rb") as f:
                cert_data = f.read()
        else:
            r = requests.get(
                url=f"https://rdc.sat.gob.mx/rccf/{path}.cer",
                headers={
                    "User-Agent": __version__.__user_agent__
                }
            )
            if r.status_code == 200:
                cert_data = r.content

                os.makedirs(os.path.dirname(file_name), exist_ok=True)
                with open(file_name, 'wb') as f:
                    f.write(cert_data)
            else:
                raise ResponseError(r)

        return Certificate.load_certificate(cert_data)
