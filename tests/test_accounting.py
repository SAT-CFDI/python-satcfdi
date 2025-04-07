import glob
import os
from unittest import mock
from uuid import UUID
from datetime import datetime
import xlsxwriter

from satcfdi.accounting._ansi_colors import *
from satcfdi.accounting.formatters import SatCFDI
from satcfdi.create.catalogos import EstadoComprobante
from satcfdi.accounting.process import filter_invoices_iter, invoices_export, invoices_print, payments_print, \
    complement_invoices_data, payments_export, num2col, filter_payments_iter, payments_retentions_export, filter_retenciones_iter, retenciones_print, payments_groupby_receptor
from satcfdi.models import DatePeriod

current_dir = os.path.abspath(os.path.dirname(__file__))


def test_excel_utils():
    assert num2col(0) == "A"
    assert num2col(1) == "B"
    assert num2col(28) == "AC"


def test_ansi():
    assert paint("HOla", COLOR_BACKGROUND_BLACK) == '\x1b[40mHOla\x1b[39m'


class myCFDI(SatCFDI):
    def estatus(self) -> EstadoComprobante:
        return EstadoComprobante.VIGENTE

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

    cfdi_pagado = all_invoices[UUID("6d7434a6-e3f2-47ad-9e4c-08849946afa0")]

    assert cfdi_pagado.ultima_num_parcialidad == 1
    assert cfdi_pagado.saldo_pendiente() == 0
    assert cfdi_pagado.saldo_pendiente(datetime(2020, 1, 2)) == cfdi_pagado['Total']
    assert cfdi_pagado.saldo_pendiente(datetime(2020, 1, 3)) == 0

    cfdi_pagado.payments[0].comprobante.estatus = lambda: EstadoComprobante.CANCELADO

    assert cfdi_pagado.ultima_num_parcialidad == 0
    assert cfdi_pagado.saldo_pendiente() == cfdi_pagado['Total']

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

        os.makedirs(os.path.join(current_dir, "test_accounting"), exist_ok=True)
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

    retenciones = filter_retenciones_iter(all_invoices, ejerc=year, complemento="Intereses")
    retenciones_print(retenciones)
