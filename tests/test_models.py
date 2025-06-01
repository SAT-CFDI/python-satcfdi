import logging
import os
import types
from datetime import date, datetime
from enum import StrEnum
from itertools import chain
from unittest import mock

import pytest
from OpenSSL import crypto

from satcfdi.models import Code
from satcfdi.models.certificate import CertificateType
from satcfdi.models.certificate_request import CertificateSigningRequest
from satcfdi.exceptions import CFDIError
from satcfdi.models.curp import CURP
from satcfdi.models.date_period import DatePeriod
from satcfdi.models.rfc import RFC, RFCType, RFC_Generico_Nacional, RFC_Generico_Extranjero
from satcfdi.models.signer import Signer
from satcfdi.pacs.sat import SAT
from satcfdi.transform import verify_certificate
from tests.constants import PERSONAS_FISICAS, PERSONAS_MORALES
from tests.utils import get_signer, SAT_Certificate_Store_Pruebas

module = 'satcfdi'
current_dir = os.path.dirname(__file__)

logging.basicConfig(level=logging.INFO)

sat = SAT()


def test_descarga_certificado_sat_pac():
    with open(os.path.join(current_dir, 'pac_sat_responses', '00001000000504465028.cer'), 'rb') as f:
        data = f.read()

    def req(*args, **kwargs):
        a = types.SimpleNamespace()
        a.status_code = 200
        a.content = data
        return a

    with mock.patch(f'requests.get', req) as mk:
        cert = sat.recover_certificate("00001000000504465028")

    # assert cert.issuer().startswith("1.2.840.113549.1.9.2=responsable: ADMINISTRACION CENTRAL DE SERVICIOS TRIBUTARIOS AL CONTRIBUYE")
    # assert cert.subject().startswith(r"OU=MEGAPACSAT970701NN301,2.5.4.5=\ / GARJ750416HDFRVR09,2.5.4.45=SAT970701NN3 / GARJ7504168N4,O=SERVIC")
    # assert cert.issuer().startswith("CN=AUTORIDAD CERTIFICADORA,O=SERVICIO DE ADMINISTRACION TRIBUTARIA,OU=SAT-IES Authority,emailAddress=contacto.tecnic")
    # assert cert.subject().startswith("CN=SERVICIO DE ADMINISTRACION TRIBUTARIA,name=SERVICIO DE ADMINISTRACION TRIBUTARIA,O=SERVICIO DE ADMINISTRACION TRIBUTARIA,x500Unique")
    assert cert.certificate_base64().startswith("MIIGKTCCBBGgAwIBAgIUMDAwMDEwMDAwMDA1MDQ0NjUwM")
    assert str(cert.serial_number) == '275106190557734483187066766829380167334928331320'
    assert cert.certificate_number == "00001000000504465028"
    assert cert.branch_name == "MEGAPACSAT970701NN301"
    assert cert.rfc_pac == "SAT970701NN3"
    assert cert.rfc_representante == "GARJ7504168N4"
    assert cert.curp is None
    assert cert.curp_representante == "GARJ750416HDFRVR09"
    assert str(cert.serial_number) == "275106190557734483187066766829380167334928331320"
    assert cert.rfc_pac == "SAT970701NN3"
    assert cert.rfc_representante == "GARJ7504168N4"
    assert cert.legal_name == 'SERVICIO DE ADMINISTRACION TRIBUTARIA'
    assert cert.email is None


def test_signer_razon_social():
    res = {
        'CACX7605101P8': 'XOCHILT CASAS CHAVEZ',
        'FUNK671228PH6': 'KARLA FUENTE NOLASCO',
        'IAÑL750210963': 'LUIS IAN ÑUZCO',
        'JUFA7608212V6': 'ADRIANA JUAREZ FERNANDEZ',
        'KAHO641101B39': 'OSCAR KALA HAAK',
        'KICR630120NX3': 'RODRIGO KITIA CASTRO',
        'MISC491214B86': 'CECILIA MIRANDA SANCHEZ',
        'RAQÑ7701212M3': 'ÑEVES RAMIREZ QUEZADA',
        'WATM640917J45': 'MARIA WATEMBER TORRES',
        'WERX631016S30': 'XAIME WEIR ROJO',
        'XAMA620210DQ5': 'ALBA XKARAJAM MENDEZ',
        'XIQB891116QE4': 'BERENICE XIMO QUEZADA',
        'XOJI740919U48': 'INGRID XODAR JIMENEZ',
        'EKU9003173C9': 'ESCUELA KEMPER URGATE',
        'EWE1709045U0': 'ESCUELA WILSON ESQUIVEL',
        'H&E951128469': 'HERRERIA & ELECTRICOS',
        'HAÑ930228SM9': 'HERMANOS ANZURES ÑARVAEZ',
        'IIA040805DZ4': 'INDISTRIA ILUMINADORA DE ALMACENES',
        'IVD920810GU2': 'INNOVACION VALOR Y DESARROLLO',
        'IXS7607092R5': 'INTERNACIONAL XIMBO Y SABORES',
        'JES900109Q90': 'JIMENEZ ESTRADA SALAS A A',
        'KIJ0906199R1': 'KERNEL INDUSTIA JUGUETERA',
        'L&O950913MSA': 'LUCES & OBRAS',
        'OÑO120726RX3': 'ORGANICOS ÑAVEZ OSORIO S.A DE C.V',
        'S&S051221SE2': 'S & SOFTWARE',
        'URE180429TM6': 'UNIVERSIDAD ROBOTICA ESPAÑOLA',
        'XIA190128J61': 'XENON INDUSTRIAL ARTICLES',
        'ZUÑ920208KL4': 'ZAPATERIA URTADO ÑERI'
    }

    for rfc in chain(PERSONAS_FISICAS, PERSONAS_MORALES):
        try:
            signer = get_signer(rfc, get_csd=True)
            rs = signer.legal_name
            assert res[rfc] == rs
            assert rfc == signer.rfc
        except FileNotFoundError as ex:
            pass


def test_curp():
    curp = CURP("FEPM890204HASRRN08")
    assert curp.is_valid()
    assert curp.estado == "AS"

    # for rfc in PERSONAS_FISICAS:
    #     signer = get_signer(rfc)
    #     assert not signer.curp.is_valid()


def test_crypto_razon_social():
    for rfc in chain(PERSONAS_FISICAS, PERSONAS_MORALES):
        try:
            signer = get_signer(rfc, get_csd=True)

            cer = crypto.load_certificate(crypto.FILETYPE_ASN1, signer.certificate_bytes())
            subj = cer.get_subject()
            for k, v in subj.get_components():
                k.decode("latin_1")
                v.decode("latin_1")

        except (FileNotFoundError, ValueError) as ex:
            pass


def test_verify_certificates():
    for rfc in chain(PERSONAS_FISICAS, PERSONAS_MORALES):
        with mock.patch(f'{module}.transform.SAT_Certificate_Store', SAT_Certificate_Store_Pruebas):
            try:
                signer = get_signer(rfc)
                verify_certificate(signer, at=datetime(2021, 6, 12))
                assert signer.type == CertificateType.Fiel

                signer_csd = get_signer(rfc, get_csd=True)
                verify_certificate(signer_csd, at=datetime(2021, 6, 12))
                assert signer_csd.type == CertificateType.CSD

            except FileNotFoundError as ex:
                pass


def test_requirement():
    for rfc in PERSONAS_FISICAS:
        res = CertificateSigningRequest.load2(
            request=open(os.path.join(current_dir, "csd", "Personas Fisicas", f'{rfc.lower()}.req'), 'rb').read()
        )
    for rfc in PERSONAS_MORALES:
        res = CertificateSigningRequest.load2(
            request=open(os.path.join(current_dir, "csd", "Personas Morales", f'{rfc.lower()}.req'), 'rb').read()
        )


def test_thumbprint():
    signer = get_signer("xiqb891116qe4")

    assert signer.fingerprint().hex() == 'cad8b0aa7940aec665d9db9755b995b8631409c4'

    signer2 = get_signer("h&e951128469")

    with pytest.raises(CFDIError) as ex:
        signer = Signer(
            key=signer.key,
            certificate=signer2.certificate,
            check=True
        )

    password = "IGUESSTHISISSECURE"
    p12 = signer.pcks12_bytes(password)
    with open(os.path.join(current_dir, "csd", f'xiqb891116qe4.pfx'), 'wb') as f:
        f.write(p12)

    pkcs12_signer = Signer.load_pkcs12(
        data=open(os.path.join(current_dir, "csd", f'xiqb891116qe4.pfx'), 'rb').read(),
        password=password
    )

    assert pkcs12_signer.legal_name == 'BERENICE XIMO QUEZADA'

    os.remove(os.path.join(current_dir, "csd", f'xiqb891116qe4.pfx'))


def test_signer_change_password():
    rfc = 'xiqb891116qe4'
    signer = get_signer(rfc)

    password = "THISISMORESCURE"
    key = signer.key_bytes(password)
    cer = signer.certificate_bytes()

    with open(os.path.join(current_dir, "csd", 'xiqb891116qe4.out.key'), 'wb') as f:
        f.write(key)
    with open(os.path.join(current_dir, "csd", 'xiqb891116qe4.out.cer'), 'wb') as f:
        f.write(cer)
    with open(os.path.join(current_dir, "csd", 'xiqb891116qe4.out.txt'), 'w') as f:
        f.write(password)

    signer = Signer.load(
        certificate=open(os.path.join(current_dir, f'csd/{rfc}.out.cer'), 'rb').read(),
        key=open(os.path.join(current_dir, f'csd/{rfc}.out.key'), 'rb').read(),
        password=open(os.path.join(current_dir, f'csd/{rfc}.out.txt'), 'rb').read()
    )

    os.remove(os.path.join(current_dir, "csd", 'xiqb891116qe4.out.key'))
    os.remove(os.path.join(current_dir, "csd", 'xiqb891116qe4.out.cer'))
    os.remove(os.path.join(current_dir, "csd", 'xiqb891116qe4.out.txt'))


def test_rfc():
    for rfc in PERSONAS_FISICAS:
        r = RFC(rfc, entity_type=RFCType.FISICA)
        assert r.is_valid()

    for rfc in PERSONAS_MORALES:
        r = RFC(rfc, entity_type=RFCType.MORAL)
        assert r.is_valid()

    r = RFC_Generico_Nacional
    assert r.is_valid()
    assert r.type == RFCType.FISICA

    r = RFC_Generico_Extranjero
    assert r.is_valid()
    assert r.type == RFCType.FISICA


def test_period():
    period = DatePeriod(year=2020, month=4)
    my_date = date(year=2021, month=3, day=20)
    assert my_date > period
    assert my_date >= period
    assert my_date != period
    assert not my_date == period
    assert not my_date <= period
    assert not my_date < period

    assert str(period) == '2020-04'

    period = DatePeriod(year=None)
    my_date = date(year=2021, month=3, day=20)
    assert my_date >= period
    assert my_date == period
    assert my_date <= period
    assert not my_date > period
    assert not my_date < period
    assert not my_date != period

    assert str(period) == ""

    assert not period == 1
    assert period != 1
    with pytest.raises(TypeError):
        assert not period < 1
    with pytest.raises(TypeError):
        assert not period > 1
    with pytest.raises(TypeError):
        assert not period >= 1
    with pytest.raises(TypeError):
        assert not period <= 1


def test_code():
    class Salutaciones(StrEnum):
        Hola = '01'
        Adios = '02'

    c = Code('01', 'Hola')

    assert Salutaciones.Hola == c
    assert c == Salutaciones.Hola
    assert c == '01'
    assert '01' == c
    assert c == Code('01', 'OtherHola')
