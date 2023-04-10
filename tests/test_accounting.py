import filecmp
import glob
import json
import os
from unittest import mock

import xlsxwriter
from lxml.etree import QName
from satcfdi.printer import Representable

from satcfdi.transform.pdf_environment import PDFEnvironment

from satcfdi import DatePeriod
from satcfdi.accounting._ansi_colors import *
from satcfdi.accounting.formatters import SatCFDI
from satcfdi.accounting.process import filter_invoices_iter, invoices_export, invoices_print, payments_print, \
    complement_invoices_data, payments_export, num2col, filter_payments_iter, payments_retentions_export, filter_retenciones_iter, retenciones_print, payments_groupby_receptor
from tests.utils import verify_result

current_dir = os.path.abspath(os.path.dirname(__file__))


def test_excel_utils():
    assert num2col(0) == "A"
    assert num2col(1) == "B"
    assert num2col(28) == "AC"


def test_ansi():
    assert paint("HOla", COLOR_BACKGROUND_BLACK) == '\x1b[40mHOla\x1b[39m'


class myCFDI(SatCFDI):
    @SatCFDI.estatus.getter
    def estatus(self) -> str:
        return '1'

    def consulta_estado(self):
        return {}


def test_cfdi():
    rfc = "H&E951128469"
    dp = DatePeriod(2020)

    all_invoices = {}

    for f in glob.iglob(os.path.join(current_dir, "invoices", "*.xml")):
        c = myCFDI.from_file(f)
        all_invoices[c.uuid] = c

    complement_invoices_data(all_invoices)

    for c in all_invoices.values():
        d = c.ultima_num_parcialidad
        assert d >= 0

    with mock.patch('builtins.print') as p:
        ingresos_pendientes = list(filter_invoices_iter(invoices=all_invoices.values(), fecha=dp, rfc_emisor=rfc, invoice_type="I", pending_balance=lambda x: x > 0))
        invoices_print(ingresos_pendientes)

        pagos_pendientes = list(filter_invoices_iter(invoices=all_invoices.values(), fecha=dp, rfc_receptor=rfc, invoice_type="I", pending_balance=lambda x: x > 0))
        invoices_print(pagos_pendientes)

        emitidas = list(filter_invoices_iter(invoices=all_invoices.values(), fecha=dp, rfc_emisor=rfc))
        invoices_print(emitidas)

        pagos = list(filter_payments_iter(invoices=all_invoices, fecha=dp, rfc_emisor=rfc))
        payments_print(pagos)

        recibidas = list(filter_invoices_iter(invoices=all_invoices.values(), fecha=dp, rfc_receptor=rfc))
        invoices_print(recibidas)

        pagos_hechos = list(filter_payments_iter(invoices=all_invoices, fecha=dp, rfc_receptor=rfc))
        payments_print(pagos_hechos)

        path = os.path.join(current_dir, "test_accounting", "invoices.xlsx")

        workbook = xlsxwriter.Workbook(path)
        invoices_export(workbook, "EMITIDAS", emitidas)
        payments_export(workbook, "EMITIDAS PAGOS", pagos)
        invoices_export(workbook, "RECIBIDAS", recibidas)
        payments_export(workbook, "PAGOS EMITIDOS", pagos_hechos)
        workbook.close()

        pagos = list(filter_payments_iter(invoices=all_invoices, fecha=dp, rfc_emisor=rfc))
        pagos_agrupados = payments_groupby_receptor(pagos)
        payments_retentions_export(os.path.join(current_dir, "test_accounting", "retenciones.txt"), pagos_agrupados)


def test_retenciones():
    year = 2020
    all_invoices = {}

    for f in glob.iglob(os.path.join(current_dir, "test_accounting", "*.xml")):
        c = myCFDI.from_file(f)
        all_invoices[c.uuid] = c

    retenciones = filter_retenciones_iter(all_invoices, ejerc=year)
    retenciones_print(retenciones)


def test_single_html_file():
    all_invoices = []
    for f in glob.iglob(os.path.join(current_dir, "invoices", "*.xml")):
        c = myCFDI.from_file(f)
        all_invoices.append(c)

    res = Representable.html_str_all(all_invoices)
    verify_result(res, "multiple_invoices.html")

    Representable.html_write_all(
        objs=all_invoices,
        target=os.path.join(current_dir, "test_accounting", "multiple_invoices2.html"),
    )

    with open(os.path.join(current_dir, "test_accounting", "multiple_invoices2.html"), "r", encoding='utf-8') as f:
        assert f.read() == res

    # assert filecmp.cmp(
    #     os.path.join(current_dir, "test_accounting", "multiple_invoices.html"),
    #     os.path.join(current_dir, "test_accounting", "multiple_invoices2.html")
    # )
