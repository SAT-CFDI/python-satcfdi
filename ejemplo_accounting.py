#!/usr/bin/env python3
"""
EJEMPLO COMPLETO DEL MÓDULO ACCOUNTING
=======================================

Este ejemplo muestra cómo usar el módulo accounting de satcfdi para:
1. Cargar y procesar facturas
2. Filtrar facturas por diferentes criterios
3. Complementar datos con relaciones y pagos
4. Exportar a Excel
5. Imprimir en consola con formato tabular
"""

import os
from datetime import datetime, date
from decimal import Decimal
from uuid import UUID
from pathlib import Path
import xlsxwriter

# Importar módulos de satcfdi
from satcfdi.accounting import (
    SatCFDI,
    filter_invoices_iter,
    filter_payments_iter,
    complement_invoices_data,
    invoices_export,
    payments_export,
    invoices_print,
    payments_print
)
from satcfdi.create.catalogos import EstadoComprobante
from satcfdi.create.cfd.catalogos import TipoDeComprobante, MetodoPago

# ==============================================================================
# PASO 1: CREAR FACTURAS DE EJEMPLO
# ==============================================================================

print("=" * 80)
print("EJEMPLO COMPLETO DEL MÓDULO ACCOUNTING")
print("=" * 80)
print()

# Simular facturas cargadas (normalmente serían cargadas desde archivos XML)
# En este ejemplo las creamos manualmente para demostración

class SatCFDIDemo(SatCFDI):
    """Versión demo de SatCFDI para el ejemplo"""

    def __init__(self, data):
        super().__init__(data)
        self._estado = EstadoComprobante.VIGENTE
        self._consulta_estado = None

    def estatus(self):
        return self._estado

    def consulta_estado(self):
        return self._consulta_estado or {
            'CodigoEstatus': '1',
            'Estado': 'Vigente',
            'EsCancelable': 'Cancelable sin aceptación'
        }

    @property
    def fecha_cancelacion(self):
        return None


# Crear diccionario de facturas indexadas por UUID
invoices_dict = {}

# ==============================================================================
# FACTURA 1: Ingreso con pago en parcialidades
# ==============================================================================
uuid_1 = UUID("11111111-1111-1111-1111-111111111111")
factura_1 = SatCFDIDemo({
    'Version': '4.0',
    'TipoDeComprobante': TipoDeComprobante.INGRESO,
    'Serie': 'A',
    'Folio': '001',
    'Fecha': datetime(2024, 1, 15, 10, 30, 0),
    'LugarExpedicion': '06000',
    'Moneda': 'MXN',
    'MetodoPago': MetodoPago.PAGO_EN_PARCIALIDADES_O_DIFERIDO,
    'FormaPago': '99',  # Por definir
    'SubTotal': Decimal('10000.00'),
    'Descuento': Decimal('0.00'),
    'Total': Decimal('11600.00'),
    'Emisor': {
        'Rfc': 'AAA010101AAA',
        'Nombre': 'EMPRESA EMISORA SA DE CV',
        'RegimenFiscal': '601'
    },
    'Receptor': {
        'Rfc': 'XAXX010101000',
        'Nombre': 'CLIENTE RECEPTOR SA DE CV',
        'UsoCFDI': 'G03',
        'DomicilioFiscalReceptor': '64000',
        'RegimenFiscalReceptor': '601'
    },
    'Conceptos': [
        {
            'ClaveProdServ': '84111506',
            'Cantidad': Decimal('1'),
            'ClaveUnidad': 'E48',
            'Descripcion': 'SERVICIOS DE CONSULTORIA',
            'ValorUnitario': Decimal('10000.00'),
            'Importe': Decimal('10000.00')
        }
    ],
    'Impuestos': {
        'Traslados': {
            '002|Tasa|0.160000': {
                'Base': Decimal('10000.00'),
                'Impuesto': '002',
                'TipoFactor': 'Tasa',
                'TasaOCuota': Decimal('0.160000'),
                'Importe': Decimal('1600.00')
            }
        }
    },
    'Complemento': {
        'TimbreFiscalDigital': {
            'UUID': str(uuid_1),
            'FechaTimbrado': datetime(2024, 1, 15, 10, 35, 0),
            'RfcProvCertif': 'SAT970701NN3',
            'SelloCFD': 'ABC123...',
            'NoCertificadoSAT': '00001000000123456789',
            'SelloSAT': 'XYZ789...'
        }
    }
})
invoices_dict[uuid_1] = factura_1

# ==============================================================================
# FACTURA 2: Ingreso con pago en una exhibición
# ==============================================================================
uuid_2 = UUID("22222222-2222-2222-2222-222222222222")
factura_2 = SatCFDIDemo({
    'Version': '4.0',
    'TipoDeComprobante': TipoDeComprobante.INGRESO,
    'Serie': 'A',
    'Folio': '002',
    'Fecha': datetime(2024, 1, 20, 14, 15, 0),
    'LugarExpedicion': '06000',
    'Moneda': 'MXN',
    'MetodoPago': MetodoPago.PAGO_EN_UNA_SOLA_EXHIBICION,
    'FormaPago': '03',  # Transferencia
    'SubTotal': Decimal('5000.00'),
    'Total': Decimal('5800.00'),
    'Emisor': {
        'Rfc': 'AAA010101AAA',
        'Nombre': 'EMPRESA EMISORA SA DE CV',
        'RegimenFiscal': '601'
    },
    'Receptor': {
        'Rfc': 'BBB010101BBB',
        'Nombre': 'OTRO CLIENTE SA DE CV',
        'UsoCFDI': 'G03',
        'DomicilioFiscalReceptor': '64000',
        'RegimenFiscalReceptor': '601'
    },
    'Conceptos': [
        {
            'ClaveProdServ': '84111506',
            'Cantidad': Decimal('1'),
            'ClaveUnidad': 'E48',
            'Descripcion': 'SERVICIOS PROFESIONALES',
            'ValorUnitario': Decimal('5000.00'),
            'Importe': Decimal('5000.00')
        }
    ],
    'Impuestos': {
        'Traslados': {
            '002|Tasa|0.160000': {
                'Base': Decimal('5000.00'),
                'Impuesto': '002',
                'TipoFactor': 'Tasa',
                'TasaOCuota': Decimal('0.160000'),
                'Importe': Decimal('800.00')
            }
        }
    },
    'Complemento': {
        'TimbreFiscalDigital': {
            'UUID': str(uuid_2),
            'FechaTimbrado': datetime(2024, 1, 20, 14, 20, 0),
            'RfcProvCertif': 'SAT970701NN3',
            'SelloCFD': 'ABC456...',
            'NoCertificadoSAT': '00001000000123456789',
            'SelloSAT': 'XYZ012...'
        }
    }
})
invoices_dict[uuid_2] = factura_2

# ==============================================================================
# FACTURA 3: Complemento de Pago (Pago Parcial 1)
# ==============================================================================
uuid_3 = UUID("33333333-3333-3333-3333-333333333333")
pago_1 = SatCFDIDemo({
    'Version': '4.0',
    'TipoDeComprobante': TipoDeComprobante.PAGO,
    'Serie': 'P',
    'Folio': '001',
    'Fecha': datetime(2024, 2, 1, 9, 0, 0),
    'LugarExpedicion': '06000',
    'Moneda': 'XXX',
    'SubTotal': Decimal('0.00'),
    'Total': Decimal('0.00'),
    'Emisor': {
        'Rfc': 'AAA010101AAA',
        'Nombre': 'EMPRESA EMISORA SA DE CV',
        'RegimenFiscal': '601'
    },
    'Receptor': {
        'Rfc': 'XAXX010101000',
        'Nombre': 'CLIENTE RECEPTOR SA DE CV',
        'UsoCFDI': 'CP01',
        'DomicilioFiscalReceptor': '64000',
        'RegimenFiscalReceptor': '601'
    },
    'Conceptos': [
        {
            'ClaveProdServ': '84111506',
            'Cantidad': Decimal('1'),
            'ClaveUnidad': 'ACT',
            'Descripcion': 'Pago',
            'ValorUnitario': Decimal('0.00'),
            'Importe': Decimal('0.00'),
            'ObjetoImp': '01'
        }
    ],
    'Complemento': {
        'TimbreFiscalDigital': {
            'UUID': str(uuid_3),
            'FechaTimbrado': datetime(2024, 2, 1, 9, 5, 0),
            'RfcProvCertif': 'SAT970701NN3',
            'SelloCFD': 'DEF123...',
            'NoCertificadoSAT': '00001000000123456789',
            'SelloSAT': 'GHI456...'
        },
        'Pagos': {
            'Pago': [
                {
                    'FechaPago': datetime(2024, 2, 1, 9, 0, 0),
                    'FormaDePagoP': '03',  # Transferencia
                    'MonedaP': 'MXN',
                    'Monto': Decimal('5800.00'),
                    'DoctoRelacionado': [
                        {
                            'IdDocumento': str(uuid_1),
                            'Serie': 'A',
                            'Folio': '001',
                            'MonedaDR': 'MXN',
                            'NumParcialidad': 1,
                            'ImpSaldoAnt': Decimal('11600.00'),
                            'ImpPagado': Decimal('5800.00'),
                            'ImpSaldoInsoluto': Decimal('5800.00'),
                            'ObjetoImpDR': '02',
                            'ImpuestosDR': {
                                'TrasladosDR': [
                                    {
                                        'BaseDR': Decimal('5000.00'),
                                        'ImpuestoDR': '002',
                                        'TipoFactorDR': 'Tasa',
                                        'TasaOCuotaDR': Decimal('0.160000'),
                                        'ImporteDR': Decimal('800.00')
                                    }
                                ]
                            }
                        }
                    ]
                }
            ]
        }
    }
})
invoices_dict[uuid_3] = pago_1

# ==============================================================================
# FACTURA 4: Complemento de Pago (Pago Parcial 2 - Finiquito)
# ==============================================================================
uuid_4 = UUID("44444444-4444-4444-4444-444444444444")
pago_2 = SatCFDIDemo({
    'Version': '4.0',
    'TipoDeComprobante': TipoDeComprobante.PAGO,
    'Serie': 'P',
    'Folio': '002',
    'Fecha': datetime(2024, 3, 1, 10, 30, 0),
    'LugarExpedicion': '06000',
    'Moneda': 'XXX',
    'SubTotal': Decimal('0.00'),
    'Total': Decimal('0.00'),
    'Emisor': {
        'Rfc': 'AAA010101AAA',
        'Nombre': 'EMPRESA EMISORA SA DE CV',
        'RegimenFiscal': '601'
    },
    'Receptor': {
        'Rfc': 'XAXX010101000',
        'Nombre': 'CLIENTE RECEPTOR SA DE CV',
        'UsoCFDI': 'CP01',
        'DomicilioFiscalReceptor': '64000',
        'RegimenFiscalReceptor': '601'
    },
    'Conceptos': [
        {
            'ClaveProdServ': '84111506',
            'Cantidad': Decimal('1'),
            'ClaveUnidad': 'ACT',
            'Descripcion': 'Pago',
            'ValorUnitario': Decimal('0.00'),
            'Importe': Decimal('0.00'),
            'ObjetoImp': '01'
        }
    ],
    'Complemento': {
        'TimbreFiscalDigital': {
            'UUID': str(uuid_4),
            'FechaTimbrado': datetime(2024, 3, 1, 10, 35, 0),
            'RfcProvCertif': 'SAT970701NN3',
            'SelloCFD': 'JKL123...',
            'NoCertificadoSAT': '00001000000123456789',
            'SelloSAT': 'MNO456...'
        },
        'Pagos': {
            'Pago': [
                {
                    'FechaPago': datetime(2024, 3, 1, 10, 30, 0),
                    'FormaDePagoP': '03',  # Transferencia
                    'MonedaP': 'MXN',
                    'Monto': Decimal('5800.00'),
                    'DoctoRelacionado': [
                        {
                            'IdDocumento': str(uuid_1),
                            'Serie': 'A',
                            'Folio': '001',
                            'MonedaDR': 'MXN',
                            'NumParcialidad': 2,
                            'ImpSaldoAnt': Decimal('5800.00'),
                            'ImpPagado': Decimal('5800.00'),
                            'ImpSaldoInsoluto': Decimal('0.00'),
                            'ObjetoImpDR': '02',
                            'ImpuestosDR': {
                                'TrasladosDR': [
                                    {
                                        'BaseDR': Decimal('5000.00'),
                                        'ImpuestoDR': '002',
                                        'TipoFactorDR': 'Tasa',
                                        'TasaOCuotaDR': Decimal('0.160000'),
                                        'ImporteDR': Decimal('800.00')
                                    }
                                ]
                            }
                        }
                    ]
                }
            ]
        }
    }
})
invoices_dict[uuid_4] = pago_2

print(f"✓ Se crearon {len(invoices_dict)} facturas de ejemplo")
print()

# ==============================================================================
# PASO 2: COMPLEMENTAR DATOS (RELACIONES Y PAGOS)
# ==============================================================================
print("-" * 80)
print("PASO 2: Complementar datos de facturas con relaciones y pagos")
print("-" * 80)

complement_invoices_data(invoices_dict)

# Verificar complementos
print(f"✓ Factura A001 tiene {len(factura_1.payments)} pagos registrados")
print(f"  - Saldo pendiente: ${factura_1.saldo_pendiente()}")
print(f"  - Última parcialidad: {factura_1.ultima_num_parcialidad}")

print(f"✓ Factura A002 tiene {len(factura_2.payments)} pagos registrados")
print(f"  - Saldo pendiente: ${factura_2.saldo_pendiente()}")
print()

# ==============================================================================
# PASO 3: FILTRAR FACTURAS
# ==============================================================================
print("-" * 80)
print("PASO 3: Filtrar facturas por diferentes criterios")
print("-" * 80)

# Filtro 1: Todas las facturas de ingreso
print("\n3.1. Filtrar facturas de INGRESO:")
facturas_ingreso = list(filter_invoices_iter(
    invoices_dict.values(),
    invoice_type=TipoDeComprobante.INGRESO
))
print(f"    → Encontradas: {len(facturas_ingreso)} facturas")
for inv in facturas_ingreso:
    print(f"      - {inv['Serie']}{inv['Folio']}: ${inv['Total']}")

# Filtro 2: Facturas con saldo pendiente
print("\n3.2. Filtrar facturas con SALDO PENDIENTE:")
facturas_pendientes = list(filter_invoices_iter(
    invoices_dict.values(),
    invoice_type=TipoDeComprobante.INGRESO,
    pending_balance=lambda x: x is not None and x > 0
))
print(f"    → Encontradas: {len(facturas_pendientes)} facturas")
for inv in facturas_pendientes:
    print(f"      - {inv['Serie']}{inv['Folio']}: Saldo ${inv.saldo_pendiente()}")

# Filtro 3: Facturas por RFC emisor
print("\n3.3. Filtrar por RFC EMISOR (AAA010101AAA):")
facturas_emisor = list(filter_invoices_iter(
    invoices_dict.values(),
    rfc_emisor='AAA010101AAA'
))
print(f"    → Encontradas: {len(facturas_emisor)} facturas")

# Filtro 4: Facturas por método de pago
print("\n3.4. Filtrar por MÉTODO DE PAGO (Parcialidades):")
facturas_parcialidades = list(filter_invoices_iter(
    invoices_dict.values(),
    payment_method=MetodoPago.PAGO_EN_PARCIALIDADES_O_DIFERIDO
))
print(f"    → Encontradas: {len(facturas_parcialidades)} facturas")
for inv in facturas_parcialidades:
    print(f"      - {inv['Serie']}{inv['Folio']}: {inv.get('MetodoPago')}")

print()

# ==============================================================================
# PASO 4: FILTRAR PAGOS
# ==============================================================================
print("-" * 80)
print("PASO 4: Filtrar pagos realizados")
print("-" * 80)

# Todos los pagos
pagos_realizados = list(filter_payments_iter(
    invoices_dict,
    rfc_emisor='AAA010101AAA'
))

print(f"\n✓ Total de pagos procesados: {len(pagos_realizados)}")
print("\nDetalle de pagos:")
for i, pago_detail in enumerate(pagos_realizados, 1):
    print(f"\n  Pago #{i}:")
    print(f"    - Comprobante de pago: {pago_detail.comprobante['Serie']}{pago_detail.comprobante['Folio']}")
    print(f"    - Factura pagada: {pago_detail.comprobante_pagado['Serie']}{pago_detail.comprobante_pagado['Folio']}")
    print(f"    - Monto pagado: ${pago_detail.total}")
    print(f"    - SubTotal-Desc: ${pago_detail.sub_total_desc}")
    if pago_detail.docto_relacionado:
        print(f"    - Parcialidad: {pago_detail.docto_relacionado.get('NumParcialidad', 'N/A')}")
        print(f"    - Saldo anterior: ${pago_detail.docto_relacionado['ImpSaldoAnt']}")
        print(f"    - Saldo insoluto: ${pago_detail.docto_relacionado['ImpSaldoInsoluto']}")

print()

# ==============================================================================
# PASO 5: IMPRIMIR EN CONSOLA
# ==============================================================================
print("-" * 80)
print("PASO 5: Imprimir facturas en consola (formato tabular)")
print("-" * 80)
print()

print("5.1. FACTURAS DE INGRESO:")
print()
invoices_print(facturas_ingreso)

print()
print("-" * 80)
print("5.2. PAGOS REALIZADOS:")
print()
payments_print(pagos_realizados)

print()

# ==============================================================================
# PASO 6: EXPORTAR A EXCEL
# ==============================================================================
print("-" * 80)
print("PASO 6: Exportar a Excel")
print("-" * 80)
print()

excel_file = '/tmp/facturas_ejemplo.xlsx'
workbook = xlsxwriter.Workbook(excel_file)

# Exportar facturas
invoices_export(workbook, 'Facturas', facturas_ingreso)
print(f"✓ Exportadas {len(facturas_ingreso)} facturas a hoja 'Facturas'")

# Exportar pagos
payments_export(workbook, 'Pagos', pagos_realizados)
print(f"✓ Exportados {len(pagos_realizados)} pagos a hoja 'Pagos'")

workbook.close()
print(f"\n✓ Archivo Excel generado: {excel_file}")

# Verificar tamaño del archivo
if os.path.exists(excel_file):
    size = os.path.getsize(excel_file)
    print(f"  Tamaño: {size:,} bytes")

print()

# ==============================================================================
# PASO 7: RESUMEN Y ESTADÍSTICAS
# ==============================================================================
print("=" * 80)
print("RESUMEN FINAL")
print("=" * 80)
print()

total_facturas = len([i for i in invoices_dict.values() if i['TipoDeComprobante'] == TipoDeComprobante.INGRESO])
total_pagos_comp = len([i for i in invoices_dict.values() if i['TipoDeComprobante'] == TipoDeComprobante.PAGO])
total_facturado = sum(i['Total'] for i in invoices_dict.values() if i['TipoDeComprobante'] == TipoDeComprobante.INGRESO)
total_cobrado = sum(p.total for p in pagos_realizados)
saldo_pendiente_total = sum(i.saldo_pendiente() or 0 for i in invoices_dict.values() if i['TipoDeComprobante'] == TipoDeComprobante.INGRESO)

print(f"📊 ESTADÍSTICAS:")
print(f"   • Total de facturas de ingreso: {total_facturas}")
print(f"   • Total de complementos de pago: {total_pagos_comp}")
print(f"   • Total facturado: ${total_facturado:,.2f}")
print(f"   • Total cobrado: ${total_cobrado:,.2f}")
print(f"   • Saldo pendiente: ${saldo_pendiente_total:,.2f}")
print()

print("✅ EJEMPLO COMPLETADO EXITOSAMENTE")
print("=" * 80)
