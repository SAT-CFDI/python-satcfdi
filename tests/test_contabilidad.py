import datetime
import logging
import os
from unittest import mock
from uuid import UUID
from zipfile import ZipInfo

import pytest
import yaml
from satcfdi.create.contabilidad.PLZ13 import Poliza, Transaccion, CompNal

from satcfdi.models import DatePeriod
from satcfdi import render
from satcfdi.accounting.contabilidad import generar_contabilidad
from satcfdi.cfdi import CFDI
from tests.constants import CFDI_FILES, CONTABILIDAD_FILES, SPEI_FILES
from tests.utils import verify_result, XElementPrettyPrinter, compare_directories

module = 'satcfdi'
current_dir = os.path.dirname(__file__)

logging.basicConfig(level=logging.INFO)


def verify_invoice(invoice, path):
    pp = XElementPrettyPrinter()
    verify = verify_result(data=pp.pformat(invoice), filename=f"{path}.pretty.py")
    assert verify

    verify = verify_result(data=invoice.xml_bytes(pretty_print=True), filename=f"{path}.xml")
    assert verify

    verify = verify_result(data=render.html_str(invoice), filename=f"{path}.html")
    assert verify

    render.pdf_write(invoice, target=os.path.join(current_dir, "test_contabilidad", f"{path}.pdf"))


@pytest.mark.parametrize('xml_file', CONTABILIDAD_FILES)
def test_generate_pdf(caplog, xml_file):
    cfdi = CFDI.from_file(
        os.path.join(current_dir, 'contabilidad_ejemplos', xml_file)
    )

    verify_invoice(cfdi, xml_file)


@pytest.mark.parametrize('xml_file', SPEI_FILES)
def test_generate_spei_pdf(caplog, xml_file):
    cfdi = CFDI.from_file(
        os.path.join(current_dir, 'spei_ejemplos', xml_file)
    )

    verify_invoice(cfdi, xml_file)


def test_generate_contabilidad_empty():
    os.makedirs(os.path.join(current_dir, 'test_contabilidad_electronica/out/empty'), exist_ok=True)

    generar_contabilidad(
        dp=DatePeriod(2024, 2),
        rfc_emisor="CACX7605101P8",
        cuentas={},
        polizas=[],
        folder=os.path.join(current_dir, 'test_contabilidad_electronica/out/empty'),
    )

    assert compare_directories(
        os.path.join(current_dir, 'test_contabilidad_electronica/ref/empty'),
        os.path.join(current_dir, 'test_contabilidad_electronica/out/empty')
    )


polizas = [
    Poliza(
        num_un_iden_pol="1",
        fecha=datetime.date(2024, 2, 1),
        concepto="Compra de equipo de computo",
        transaccion=[
            Transaccion(
                num_cta="1020.01",
                des_cta='',
                concepto="Nal",
                debe=10000,
                haber=0,
                comp_nal=[
                    CompNal(
                        uuid_cfdi='a4f4fea5-e798-4ab3-a2e5-75f741f4ecca',
                        rfc="CACX7605101P8",
                        monto_total=10000
                    )
                ]
            ),
            Transaccion(
                num_cta="1020.02",
                des_cta='',
                concepto="Ext",
                debe=0,
                haber=10000,
                comp_nal=[
                    CompNal(
                        uuid_cfdi='a4f4fea5-e798-4ab3-a2e5-75f741f4ecca',
                        rfc="CACX7605101P8",
                        monto_total=10000
                    )
                ]
            )
        ]
    )
]


def test_generate_contabilidad_simple():
    path = 'simple'
    os.makedirs(os.path.join(current_dir, 'test_contabilidad_electronica/out', path), exist_ok=True)

    with open(os.path.join(current_dir, 'contabilidad_electronica', 'cuentas.yaml'), 'r', encoding='utf-8') as f:
        cuentas = yaml.load(f, Loader=yaml.SafeLoader)

    generar_contabilidad(
        dp=DatePeriod(2024, 2),
        rfc_emisor="CACX7605101P8",
        cuentas=cuentas,
        polizas=polizas,
        folder=os.path.join(current_dir, 'test_contabilidad_electronica/out', path),
        tipo_solicitud='AF',
        zip_xml=False
    )

    assert compare_directories(
        os.path.join(current_dir, 'test_contabilidad_electronica/ref', path),
        os.path.join(current_dir, 'test_contabilidad_electronica/out', path)
    )


def test_generate_contabilidad_zip():
    path = 'simple_zip'
    os.makedirs(os.path.join(current_dir, 'test_contabilidad_electronica/out', path), exist_ok=True)

    with open(os.path.join(current_dir, 'contabilidad_electronica', 'cuentas.yaml'), 'r', encoding='utf-8') as f:
        cuentas = yaml.load(f, Loader=yaml.SafeLoader)

    def zi(filename):
        return ZipInfo(
            filename=filename,
            date_time=(2022, 11, 8, 11, 41, 8)  # time.localtime(time.time())[:6]
        )

    with mock.patch(f'{module}.zip.ZipInfo', zi) as m:
        generar_contabilidad(
            dp=DatePeriod(2024, 2),
            rfc_emisor="CACX7605101P8",
            cuentas=cuentas,
            polizas=polizas,
            folder=os.path.join(current_dir, 'test_contabilidad_electronica/out', path),
            tipo_solicitud='AF',
            zip_xml=True
        )

    assert compare_directories(
        os.path.join(current_dir, 'test_contabilidad_electronica/ref', path),
        os.path.join(current_dir, 'test_contabilidad_electronica/out', path)
    )
