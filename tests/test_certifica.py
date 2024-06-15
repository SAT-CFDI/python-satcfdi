from datetime import datetime, timezone
import io
import os
from unittest import mock
from zipfile import ZipInfo

import pytest
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.serialization import load_der_private_key

from satcfdi.certifica import _create_certificate_signing_request, _create_certificate_signing_request_zip, Certifica, _calculate_code, \
    _create_renovation_certificate_signing_request, _calculate_code_random, _create_generacion_certificate_signing_request, _create_renovation_moral_certificate_signing_request
from satcfdi.certifica.pkcs7 import create_pkcs7
from tests.utils import get_signer

current_dir = os.path.dirname(__file__)
current_filename = os.path.splitext(os.path.basename(__file__))[0]
test_dir = os.path.join(current_dir, current_filename)
module = 'satcfdi'


def test_certificate_csd():
    signer = get_signer("cacx7605101p8")
    sucursal = 'TestSucursal'

    with mock.patch(f'{module}.certifica.datetime') as d:
        d.now = mock.Mock(return_value=datetime(2022, 11, 18, 11, 7, 10))

        certifica = Certifica(signer=signer)
        certifica.solicitud_certificado(
            sucursal=sucursal,
            password="TestIt1234",
            dirname=os.path.join(test_dir, 'test_csd')
        )

    private_key = load_der_private_key(
        data=open(os.path.join(test_dir, 'test_csd', 'CSD_TestSucursal_CACX7605101P8_20221118_110710.key'), 'rb').read(),
        password=b'TestIt1234'
    )

    print(private_key)


def test_calculate_code():
    signer = get_signer("HAÑ930228SM9")
    assert _calculate_code(signer) == b'+HcCMz3yWNA/QxB/l2flfHZ1slU='
    signer = get_signer("cacx7605101p8")
    assert _calculate_code(signer) == b'g3dhTGuMM+KZoCQ37nuuG9IUzKk='
    signer = get_signer("IAÑL750210963")
    assert len(_calculate_code(signer)) == len(_calculate_code_random())


generacion = [
    ('generacion_1', 'Test1234', "IAÑL750210963", datetime(2022, 11, 20, 0, 44, 33), 'micorreo@pruebas.gob.mx',
     b'T/pD4GwyUGB9QOzYpWKLikLuP6U=', 'IANL750210HSRNZS09', "IAÑL750210963"),
    ('generacion_2', 'Test1234', "HAÑ930228SM9", datetime(2022, 11, 20, 21, 18, 37), 'super@correo.com',
     b'gyUkJAqQytfSsWrQSeC/ZOvgz6o=', ' / ', 'HAÑ930228SM9 / IAÑL750210963'),
]


@pytest.mark.parametrize('folder, password, rfc, file_name_date, correo, code, curp, rfc_rep', generacion)
def test_generacion_request(folder, password, rfc, file_name_date, correo, code, curp, rfc_rep):
    tmf = file_name_date.strftime('%Y%m%d_%H%M%S')

    private_key = load_der_private_key(
        data=open(os.path.join(test_dir, folder, f'Claveprivada_FIEL_{rfc}_{tmf}.key'), 'rb').read(),
        password=password.encode('windows-1252')
    )

    assert private_key.key_size == 2048
    assert private_key.public_key().public_numbers().e == 65537

    with mock.patch(f"{module}.certifica._calculate_code_random", lambda: code):
        res = _create_generacion_certificate_signing_request(private_key=private_key, rfc=rfc_rep, curp=curp, correo=correo)

    cer_req = open(os.path.join(test_dir, folder, f"Requerimiento_FIEL_{rfc}_{tmf}.req"), 'rb').read()
    assert res == cer_req


renovaciones = [
    ('renovacion_1', 'Test_iañl750210963!', "IAÑL750210963", datetime(2022, 11, 19, 21, 2, 18), 'micorreo@pruebas.gob.mx',
     b'vNJ4zp78Y7z75+lq99ltUJQPkjw='),
]


@pytest.mark.parametrize('folder, password, rfc, file_name_date, correo, code', renovaciones)
def test_create_renovacion_request(folder, password, rfc, file_name_date, correo, code):
    signer = get_signer(rfc)
    tmf = file_name_date.strftime('%Y%m%d_%H%M%S')

    private_key = load_der_private_key(
        data=open(os.path.join(test_dir, folder, f'Claveprivada_FIEL_{rfc}_{tmf}.key'), 'rb').read(),
        password=password.encode('windows-1252')
    )

    assert private_key.key_size == 2048
    assert private_key.public_key().public_numbers().e == 65537

    with mock.patch(f"{module}.certifica._calculate_code_random", lambda: code):
        res = _create_renovation_certificate_signing_request(signer=signer, private_key=private_key, correo=correo)

    cer_req = open(os.path.join(test_dir, folder, f"Renovacion_FIEL_{rfc}_{tmf}.req"), 'rb').read()
    assert res == cer_req


renovaciones_moral = [
    ('renovacion_moral_1', 'Test1234', "HAÑ930228SM9", "KAHO641101B39", datetime(2022, 11, 20, 22, 16, 25), 'pruebas.sat@pruebas.gob.mx',
     b'BMwmgQnOpww0B3x7EhvlPsrywFw='),
]


@pytest.mark.parametrize('folder, password, rfc, rfc_rep, file_name_date, correo, code', renovaciones_moral)
def test_create_renovacion_moral_request(folder, password, rfc, rfc_rep, file_name_date, correo, code):
    signer = get_signer(rfc_rep)
    tmf = file_name_date.strftime('%Y%m%d_%H%M%S')

    private_key = load_der_private_key(
        data=open(os.path.join(test_dir, folder, f'Claveprivada_FIEL_{rfc}_{tmf}.key'), 'rb').read(),
        password=password.encode('windows-1252')
    )

    assert private_key.key_size == 2048
    assert private_key.public_key().public_numbers().e == 65537

    with mock.patch(f"{module}.certifica._calculate_code_random", lambda: code):
        res = _create_renovation_moral_certificate_signing_request(signer=signer, private_key=private_key, rfc=rfc, correo=correo)

    cer_req = open(os.path.join(test_dir, folder, f"Renovacion_FIEL_{rfc}_{tmf}.req"), 'rb').read()
    assert res == cer_req


solicitudes = [
    ('solicitud_1', 'Test1234', (2022, 11, 18, 11, 7, 22), 'MiSucursal', "CACX7605101P8", datetime(2022, 11, 18, 11, 7, 10)),
    ('solicitud_2', 'Test&ñ200!', (2022, 11, 18, 15, 32, 44), 'ABC& hañ 200!', "HAÑ930228SM9", datetime(2022, 11, 18, 15, 32, 25)),
]


@pytest.mark.parametrize('folder, password, zip_date, sucursal, rfc, file_name_date', solicitudes)
def test_create_signing_request(folder, password, zip_date, sucursal, rfc, file_name_date):
    signer = get_signer(rfc)
    tmf = file_name_date.strftime('%Y%m%d_%H%M%S')
    sucursal_f = sucursal.replace(" ", "_")

    private_key = load_der_private_key(
        data=open(os.path.join(test_dir, folder, f'CSD_{sucursal_f}_{rfc}_{tmf}.key'), 'rb').read(),
        password=password.encode('windows-1252')
    )

    assert private_key.key_size == 2048
    assert private_key.public_key().public_numbers().e == 65537

    res = _create_certificate_signing_request(signer=signer, private_key=private_key, sucursal=sucursal)

    cer_req = open(os.path.join(test_dir, folder, f"CSD_{sucursal_f}_{rfc}_{tmf}s.req"), 'rb').read()
    assert res == cer_req


@pytest.mark.parametrize('folder, password, zip_date, sucursal, rfc, file_name_date', solicitudes)
def test_create_signing_request_zip(folder, password, zip_date, sucursal, rfc, file_name_date):
    signer = get_signer(rfc)
    tmf = file_name_date.strftime('%Y%m%d_%H%M%S')
    sucursal_f = sucursal.replace(" ", "_")

    private_key = load_der_private_key(
        data=open(os.path.join(test_dir, folder, f'CSD_{sucursal_f}_{rfc}_{tmf}.key'), 'rb').read(),
        password=password.encode('windows-1252')
    )

    # Verify ZIP
    def zi(filename):
        return ZipInfo(
            filename=filename,
            date_time=zip_date  # time.localtime(time.time())[:6]
        )

    with mock.patch(f'{module}.zip.ZipInfo', zi) as m, mock.patch(f'{module}.certifica.datetime') as d:
        d.now = mock.Mock(return_value=file_name_date)

        res = _create_certificate_signing_request_zip(signer=signer, private_key=private_key, sucursal=sucursal)

    zip = open(os.path.join(test_dir, folder, f"CSD_{sucursal_f}_{rfc}_{tmf}s.zip"), 'rb').read()
    assert res == zip

    certifica = Certifica(signer)
    res = certifica._pkcs7_package(zip)

    assert len(res) > 3200
    # check something?


def test_pkcs7():
    with open(os.path.join(current_dir, 'certifica', 'test_create.pkcs7'), 'rb') as f:
        data = f.read()

    zip_data = b'123'
    signer = get_signer('cacx7605101p8')

    with mock.patch(f'{module}.certifica.pkcs7.datetime') as d:
        d.now = mock.Mock(return_value=datetime(2023, 6, 28, 19, 28, 1, tzinfo=timezone.utc))

        assert data == create_pkcs7(zip_data, signer, hash_algorithm=hashes.SHA1())

    # cert = self.signer.certificate.to_cryptography()
    # key = self.signer.key
    # options = [pkcs7.PKCS7Options.NoCapabilities, pkcs7.PKCS7Options.Binary]
    #
    # return pkcs7.PKCS7SignatureBuilder().set_data(data) \
    #     .add_signer(cert, key, hashes.SHA1()) \
    #     .sign(serialization.Encoding.DER, options)
