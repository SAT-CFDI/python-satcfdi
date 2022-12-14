import glob
import os
from unittest import mock
from unittest.mock import patch

import xlsxwriter
from satcfdi import DatePeriod
from xlsxwriter.exceptions import FileCreateError

from satcfdi.accounting._ansi_colors import *
from satcfdi.accounting.process import filter_invoices_by, InvoiceType, invoices_export, invoices_print, payments_print, \
    complement_invoices_data, payments_export, retentions_export, num2col, filter_payments_by, payments_retentions_export, filter_retenciones_by, retenciones_print
from satcfdi.accounting.formatters import SatCFDI

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
        ingresos_pendientes = filter_invoices_by(invoices=all_invoices, fecha=dp, rfc_emisor=rfc, invoice_type=InvoiceType.PAYMENT_PENDING)
        invoices_print(ingresos_pendientes)

        pagos_pendientes = filter_invoices_by(invoices=all_invoices, fecha=dp, rfc_receptor=rfc, invoice_type=InvoiceType.PAYMENT_PENDING)
        invoices_print(pagos_pendientes)

        emitidas = filter_invoices_by(invoices=all_invoices, fecha=dp, rfc_emisor=rfc)
        invoices_print(emitidas)

        pagos = filter_payments_by(invoices=all_invoices, fecha=dp, rfc_emisor=rfc)
        payments_print(pagos)

        recibidas = filter_invoices_by(invoices=all_invoices, fecha=dp, rfc_receptor=rfc)
        invoices_print(recibidas)

        pagos_hechos = filter_payments_by(invoices=all_invoices, fecha=dp, rfc_receptor=rfc)
        payments_print(pagos_hechos)

        path = os.path.join(current_dir, "test_accounting", "invoices.xlsx")

        workbook = xlsxwriter.Workbook(path)
        invoices_export(workbook, "EMITIDAS", emitidas)
        payments_export(workbook, "EMITIDAS PAGOS", pagos)
        invoices_export(workbook, "RECIBIDAS", recibidas)
        payments_export(workbook, "PAGOS EMITIDOS", pagos_hechos)
        workbook.close()

        pagos = filter_payments_by(invoices=all_invoices, fecha=dp, rfc_emisor=rfc)
        payments_retentions_export(os.path.join(current_dir, "test_accounting", "retenciones.txt"), pagos)


def test_retenciones():
    year = 2020
    all_invoices = {}

    for f in glob.iglob(os.path.join(current_dir, "test_accounting", "*.xml")):
        c = myCFDI.from_file(f)
        all_invoices[c.uuid] = c

    retenciones = filter_retenciones_by(all_invoices, ejerc=year)
    retenciones_print(retenciones)

