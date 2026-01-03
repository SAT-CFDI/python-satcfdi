# EJEMPLO COMPLETO DEL MÓDULO ACCOUNTING

## 📋 DESCRIPCIÓN

Este ejemplo demuestra el uso completo del módulo `satcfdi.accounting` para:

1. ✅ Cargar y procesar facturas (CFDIs)
2. ✅ Complementar datos con relaciones y pagos
3. ✅ Filtrar facturas por múltiples criterios
4. ✅ Filtrar pagos realizados
5. ✅ Imprimir en consola con formato tabular
6. ✅ Exportar a Excel

---

## 🚀 EJECUCIÓN

```bash
python ejemplo_accounting.py
```

---

## 📊 DATOS DE EJEMPLO

El ejemplo crea 4 comprobantes fiscales:

### Factura 1: Ingreso con Pago en Parcialidades
- **Serie/Folio:** A001
- **Tipo:** Ingreso (I)
- **Fecha:** 2024-01-15
- **Total:** $11,600.00
- **Método de Pago:** PPD (Pago en Parcialidades o Diferido)
- **Concepto:** Servicios de consultoría
- **IVA:** $1,600.00 (16%)

### Factura 2: Ingreso con Pago en Una Exhibición
- **Serie/Folio:** A002
- **Tipo:** Ingreso (I)
- **Fecha:** 2024-01-20
- **Total:** $5,800.00
- **Método de Pago:** PUE (Pago en Una Sola Exhibición)
- **Concepto:** Servicios profesionales
- **IVA:** $800.00 (16%)

### Complemento de Pago 1: Primera Parcialidad
- **Serie/Folio:** P001
- **Tipo:** Pago (P)
- **Fecha:** 2024-02-01
- **Monto Pagado:** $5,800.00
- **Factura Relacionada:** A001 (Parcialidad 1 de 2)
- **Saldo Anterior:** $11,600.00
- **Saldo Insoluto:** $5,800.00

### Complemento de Pago 2: Finiquito
- **Serie/Folio:** P002
- **Tipo:** Pago (P)
- **Fecha:** 2024-03-01
- **Monto Pagado:** $5,800.00
- **Factura Relacionada:** A001 (Parcialidad 2 de 2)
- **Saldo Anterior:** $5,800.00
- **Saldo Insoluto:** $0.00

---

## 📝 CÓDIGO PASO A PASO

### 1. Importaciones

```python
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
```

### 2. Crear Clase Extendida de SatCFDI

```python
class SatCFDIDemo(SatCFDI):
    """Versión demo de SatCFDI para el ejemplo"""

    def __init__(self, data):
        super().__init__(data)
        self._estado = EstadoComprobante.VIGENTE

    def estatus(self):
        return self._estado

    def consulta_estado(self):
        return {
            'CodigoEstatus': '1',
            'Estado': 'Vigente',
            'EsCancelable': 'Cancelable sin aceptación'
        }

    @property
    def fecha_cancelacion(self):
        return None
```

**Nota:** En producción, estos métodos consultarían el estado real del SAT.

### 3. Complementar Datos de Facturas

```python
# Diccionario indexado por UUID
invoices_dict = {
    uuid_1: factura_1,
    uuid_2: factura_2,
    uuid_3: pago_1,
    uuid_4: pago_2
}

# Complementar relaciones y pagos
complement_invoices_data(invoices_dict)
```

**Resultado:**
- Cada factura ahora tiene sus pagos relacionados en `factura.payments`
- Cada factura tiene sus relaciones en `factura.relations`
- Se puede consultar saldo pendiente: `factura.saldo_pendiente()`

### 4. Filtrar Facturas

#### Filtrar por Tipo de Comprobante

```python
facturas_ingreso = list(filter_invoices_iter(
    invoices_dict.values(),
    invoice_type=TipoDeComprobante.INGRESO
))
# Resultado: 2 facturas (A001, A002)
```

#### Filtrar por Saldo Pendiente

```python
facturas_pendientes = list(filter_invoices_iter(
    invoices_dict.values(),
    invoice_type=TipoDeComprobante.INGRESO,
    pending_balance=lambda x: x is not None and x > 0
))
# Resultado: 0 facturas (todas están pagadas)
```

#### Filtrar por RFC Emisor

```python
facturas_emisor = list(filter_invoices_iter(
    invoices_dict.values(),
    rfc_emisor='AAA010101AAA'
))
# Resultado: 4 facturas (todas del mismo emisor)
```

#### Filtrar por Método de Pago

```python
facturas_parcialidades = list(filter_invoices_iter(
    invoices_dict.values(),
    payment_method=MetodoPago.PAGO_EN_PARCIALIDADES_O_DIFERIDO
))
# Resultado: 1 factura (A001)
```

### 5. Filtrar Pagos

```python
pagos_realizados = list(filter_payments_iter(
    invoices_dict,
    rfc_emisor='AAA010101AAA'
))
# Resultado: 3 pagos
#   1. A002 (PUE - pago automático al ser una exhibición)
#   2. P001 (Parcialidad 1 de A001)
#   3. P002 (Parcialidad 2 de A001)
```

**Estructura de PaymentsDetails:**

```python
pago_detail = pagos_realizados[1]  # P001

pago_detail.comprobante          # CFDI del complemento de pago (P001)
pago_detail.comprobante_pagado   # CFDI de la factura pagada (A001)
pago_detail.pago                 # Elemento <Pago> del complemento
pago_detail.docto_relacionado    # Elemento <DoctoRelacionado>
pago_detail.total                # Monto pagado: $5,800.00
pago_detail.sub_total_desc       # Subtotal - Descuento: $5,000.00
pago_detail.impuestos            # Impuestos del pago
```

### 6. Imprimir en Consola

```python
# Imprimir facturas de ingreso
invoices_print(facturas_ingreso)

# Imprimir pagos
payments_print(pagos_realizados)
```

**Resultado: Tabla con formato**

```
   Factura                               Fecha                Total    Pendiente
-- ------------------------------------ ------------------- -------- -----------
01 I 4.0                                2024-01-15 10:30:00 11600.00         0.00
   11111111-1111-1111-1111-111111111111 06000
   - A001                               G03

02 I 4.0                                2024-01-20 14:15:00  5800.00         0.00
   22222222-2222-2222-2222-222222222222 06000
   - A002                               G03

Total                                                       17400.00         0.00
```

### 7. Exportar a Excel

```python
import xlsxwriter

excel_file = 'facturas_ejemplo.xlsx'
workbook = xlsxwriter.Workbook(excel_file)

# Exportar facturas
invoices_export(workbook, 'Facturas', facturas_ingreso)

# Exportar pagos
payments_export(workbook, 'Pagos', pagos_realizados)

workbook.close()
```

**Resultado: Archivo Excel con 2 hojas**

#### Hoja "Facturas"
- Columnas: Factura, Fecha, Emisor, Receptor, Forma Pago, SubTotal, Descuento, IVA16 Base, IVA16 Tras, IVA Ret, ISR Ret, Total, Pendiente, Pagos, Relaciones, Estado CFDI, Conceptos
- 2 filas de datos + 1 fila de totales
- Formato con ajuste de texto y altura de filas
- Fórmulas SUM automáticas para totales

#### Hoja "Pagos"
- Columnas: Factura, Fecha, Emisor, Receptor, Forma Pago, Factura Pagada, Fecha de Pago, Pagado, Saldo Ant, Saldo Insoluto, Parcialidad, SubtotalDesc, IVA16 Base, IVA16 Tras, IVA Ret, ISR Ret, Estatus SAT
- 3 filas de datos + 1 fila de totales
- Incluye información detallada de parcialidades

---

## 📈 RESULTADO ESPERADO COMPLETO

```
================================================================================
EJEMPLO COMPLETO DEL MÓDULO ACCOUNTING
================================================================================

✓ Se crearon 4 facturas de ejemplo

--------------------------------------------------------------------------------
PASO 2: Complementar datos de facturas con relaciones y pagos
--------------------------------------------------------------------------------
✓ Factura A001 tiene 2 pagos registrados
  - Saldo pendiente: $0.00
  - Última parcialidad: 2
✓ Factura A002 tiene 0 pagos registrados
  - Saldo pendiente: $0

--------------------------------------------------------------------------------
PASO 3: Filtrar facturas por diferentes criterios
--------------------------------------------------------------------------------

3.1. Filtrar facturas de INGRESO:
    → Encontradas: 2 facturas
      - A001: $11600.00
      - A002: $5800.00

3.2. Filtrar facturas con SALDO PENDIENTE:
    → Encontradas: 0 facturas

3.3. Filtrar por RFC EMISOR (AAA010101AAA):
    → Encontradas: 4 facturas

3.4. Filtrar por MÉTODO DE PAGO (Parcialidades):
    → Encontradas: 1 facturas
      - A001: PPD

--------------------------------------------------------------------------------
PASO 4: Filtrar pagos realizados
--------------------------------------------------------------------------------

✓ Total de pagos procesados: 3

Detalle de pagos:

  Pago #1:
    - Comprobante de pago: A002
    - Factura pagada: A002
    - Monto pagado: $5800.00
    - SubTotal-Desc: $5000.00

  Pago #2:
    - Comprobante de pago: P001
    - Factura pagada: A001
    - Monto pagado: $5800.00
    - SubTotal-Desc: $5000.00
    - Parcialidad: 1
    - Saldo anterior: $11600.00
    - Saldo insoluto: $5800.00

  Pago #3:
    - Comprobante de pago: P002
    - Factura pagada: A001
    - Monto pagado: $5800.00
    - SubTotal-Desc: $5000.00
    - Parcialidad: 2
    - Saldo anterior: $5800.00
    - Saldo insoluto: $0.00

--------------------------------------------------------------------------------
PASO 5: Imprimir facturas en consola (formato tabular)
--------------------------------------------------------------------------------

[TABLAS FORMATEADAS CON DATOS COMPLETOS]

--------------------------------------------------------------------------------
PASO 6: Exportar a Excel
--------------------------------------------------------------------------------

✓ Exportadas 2 facturas a hoja 'Facturas'
✓ Exportados 3 pagos a hoja 'Pagos'

✓ Archivo Excel generado: /tmp/facturas_ejemplo.xlsx
  Tamaño: 7,346 bytes

================================================================================
RESUMEN FINAL
================================================================================

📊 ESTADÍSTICAS:
   • Total de facturas de ingreso: 2
   • Total de complementos de pago: 2
   • Total facturado: $17,400.00
   • Total cobrado: $17,400.00
   • Saldo pendiente: $0.00

✅ EJEMPLO COMPLETADO EXITOSAMENTE
================================================================================
```

---

## 🎯 CASOS DE USO REALES

### Caso 1: Sistema de Cuentas por Cobrar

```python
# Obtener todas las facturas con saldo pendiente
facturas_por_cobrar = list(filter_invoices_iter(
    invoices_dict.values(),
    invoice_type=TipoDeComprobante.INGRESO,
    pending_balance=lambda x: x is not None and x > 0
))

# Calcular total por cobrar
total_por_cobrar = sum(f.saldo_pendiente() for f in facturas_por_cobrar)
print(f"Total por cobrar: ${total_por_cobrar:,.2f}")
```

### Caso 2: Reporte de Pagos del Mes

```python
from datetime import date

# Filtrar pagos de un mes específico
def es_febrero_2024(fecha):
    return fecha.year == 2024 and fecha.month == 2

pagos_febrero = list(filter_payments_iter(
    invoices_dict,
    fecha=es_febrero_2024
))

# Exportar a Excel
workbook = xlsxwriter.Workbook('pagos_febrero_2024.xlsx')
payments_export(workbook, 'Febrero 2024', pagos_febrero)
workbook.close()
```

### Caso 3: Análisis de Cartera por Cliente

```python
from itertools import groupby

# Agrupar facturas por cliente (RFC Receptor)
facturas_sorted = sorted(
    filter_invoices_iter(invoices_dict.values(), invoice_type=TipoDeComprobante.INGRESO),
    key=lambda f: f['Receptor']['Rfc']
)

for rfc, facturas in groupby(facturas_sorted, key=lambda f: f['Receptor']['Rfc']):
    facturas_list = list(facturas)
    total = sum(f['Total'] for f in facturas_list)
    pendiente = sum(f.saldo_pendiente() or 0 for f in facturas_list)

    print(f"\nCliente: {rfc}")
    print(f"  Total facturado: ${total:,.2f}")
    print(f"  Saldo pendiente: ${pendiente:,.2f}")
```

### Caso 4: Exportación Mensual para Contabilidad

```python
# Filtrar facturas del mes
def es_enero_2024(fecha):
    return fecha.year == 2024 and fecha.month == 1

facturas_mes = list(filter_invoices_iter(
    invoices_dict.values(),
    invoice_type=TipoDeComprobante.INGRESO,
    fecha=es_enero_2024
))

pagos_mes = list(filter_payments_iter(
    invoices_dict,
    fecha=es_enero_2024
))

# Crear Excel con múltiples hojas
workbook = xlsxwriter.Workbook('contabilidad_enero_2024.xlsx')
invoices_export(workbook, 'Facturas Emitidas', facturas_mes)
payments_export(workbook, 'Pagos Recibidos', pagos_mes)
workbook.close()
```

---

## 🔧 FUNCIONES PRINCIPALES DEL MÓDULO

### `complement_invoices_data(invoices: Mapping[UUID, SatCFDI])`
**Propósito:** Complementar datos de facturas con relaciones y pagos.

**Entrada:**
- `invoices`: Diccionario con UUID como clave y SatCFDI como valor

**Efecto:**
- Agrega información de pagos a `invoice.payments`
- Agrega información de relaciones a `invoice.relations`
- Permite calcular saldos pendientes con `invoice.saldo_pendiente()`

---

### `filter_invoices_iter(invoices, **criterios)`
**Propósito:** Filtrar facturas por múltiples criterios.

**Parámetros:**
- `rfc_emisor`: RFC del emisor
- `rfc_receptor`: RFC del receptor
- `estatus`: Estado del comprobante
- `fecha`: Fecha (puede ser función lambda)
- `invoice_type`: Tipo de comprobante
- `payment_method`: Método de pago
- `pending_balance`: Saldo pendiente (puede ser función lambda)

**Retorna:** Iterator[SatCFDI]

---

### `filter_payments_iter(invoices, **criterios)`
**Propósito:** Filtrar pagos realizados.

**Parámetros:**
- `rfc_emisor`: RFC del emisor
- `rfc_receptor`: RFC del receptor
- `fecha`: Fecha de pago (puede ser función lambda)
- `invoice_type`: Tipo de comprobante

**Retorna:** Iterator[PaymentsDetails]

---

### `invoices_print(invoices: Sequence[SatCFDI])`
**Propósito:** Imprimir facturas en consola con formato tabular.

**Entrada:** Lista de facturas

**Resultado:** Tabla formateada en consola con:
- Información general (Factura, Fecha, Emisor, Receptor)
- Importes (SubTotal, Descuento, Impuestos, Total)
- Saldo pendiente
- Relaciones y pagos
- Conceptos

---

### `payments_print(payments: Sequence[PaymentsDetails])`
**Propósito:** Imprimir pagos en consola con formato tabular.

**Resultado:** Tabla con información de:
- Comprobante de pago
- Factura pagada
- Montos (Pagado, Saldo Anterior, Saldo Insoluto)
- Parcialidades
- Impuestos del pago

---

### `invoices_export(workbook, name, invoices)`
**Propósito:** Exportar facturas a hoja de Excel.

**Parámetros:**
- `workbook`: Objeto xlsxwriter.Workbook
- `name`: Nombre de la hoja
- `invoices`: Secuencia de facturas

**Resultado:** Hoja de Excel con:
- Formato profesional (encabezados negros con texto blanco)
- Columnas ajustadas automáticamente
- Fórmulas SUM en totales
- Ajuste de texto en celdas

---

### `payments_export(workbook, name, payments)`
**Propósito:** Exportar pagos a hoja de Excel.

**Resultado:** Similar a invoices_export pero con columnas específicas de pagos.

---

## 📦 ARCHIVOS GENERADOS

### ejemplo_accounting.py
Script completo ejecutable con todos los ejemplos.

### /tmp/facturas_ejemplo.xlsx
Archivo Excel generado con:
- **Hoja "Facturas":** 2 registros + totales
- **Hoja "Pagos":** 3 registros + totales
- **Tamaño:** ~7.3 KB

---

## 💡 TIPS Y MEJORES PRÁCTICAS

1. **Siempre complementar datos antes de filtrar pagos:**
   ```python
   complement_invoices_data(invoices_dict)
   pagos = list(filter_payments_iter(invoices_dict))
   ```

2. **Usar funciones lambda para filtros complejos:**
   ```python
   # Facturas del último trimestre con saldo > $1000
   facturas = list(filter_invoices_iter(
       invoices_dict.values(),
       fecha=lambda f: f >= date(2024, 10, 1),
       pending_balance=lambda s: s is not None and s > 1000
   ))
   ```

3. **Indexar por UUID para búsquedas rápidas:**
   ```python
   invoices_dict = {factura.uuid: factura for factura in facturas}
   ```

4. **Exportar múltiples reportes en un solo Excel:**
   ```python
   workbook = xlsxwriter.Workbook('reportes.xlsx')
   invoices_export(workbook, 'Enero', facturas_enero)
   invoices_export(workbook, 'Febrero', facturas_febrero)
   payments_export(workbook, 'Pagos', todos_pagos)
   workbook.close()
   ```

---

## ✅ VERIFICACIÓN

Para verificar que el ejemplo funciona correctamente:

1. El script debe completarse sin errores
2. Debe mostrar 3 pagos procesados
3. El saldo pendiente de A001 debe ser $0.00
4. El archivo Excel debe generarse con tamaño ~7.3 KB
5. Las tablas deben mostrar totales correctos

**Total facturado:** $17,400.00
**Total cobrado:** $17,400.00
**Saldo pendiente:** $0.00

---

## 🎓 APRENDIZAJES CLAVE

1. ✅ `complement_invoices_data()` es esencial para trabajar con pagos
2. ✅ `filter_invoices_iter()` soporta filtros múltiples y funciones lambda
3. ✅ `filter_payments_iter()` maneja automáticamente PUE y PPD
4. ✅ Las funciones de exportación incluyen totales automáticos
5. ✅ Las tablas en consola tienen formato profesional con colores

---

**Archivo de ejemplo:** `ejemplo_accounting.py`
**Documentación:** Este archivo
**Autor:** SAT-CFDI Python Library
**Fecha:** 2024
