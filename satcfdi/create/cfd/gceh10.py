"""gceh http://www.sat.gob.mx/GastosHidrocarburos10"""
from decimal import Decimal
from datetime import datetime, date, time
from collections.abc import Sequence
from ...cfdi import CFDI
from ...xelement import XElement
from ...utils import ScalarMap


class Pozos(ScalarMap):
    """
    Nodo opcional para registrar el centro de costos del Pozo al cual se encuentra relacionado el Yacimiento.
    
    :param pozo: Atributo opcional para especificar el centro de costos del pozo al cual se encuentra relacionado el costo, gasto o inversión, conforme a los “Lineamientos para la elaboración y presentación de los costos, gastos e inversiones; la procura de bienes y servicios en los contratos y asignaciones; la verificación contable y financiera de los contratos, y la actualización de regalías en contratos y del derecho de extracción de hidrocarburos”, emitidos por la Secretaria de Hacienda y Crédito Público.
    """
    
    def __init__(
            self,
            pozo: str = None,
    ): 
        super().__init__({
            'Pozo': pozo,
        })
        

class Yacimientos(ScalarMap):
    """
    Nodo opcional para registrar el centro de costos del yacimiento al cual se encuentra relacionado el campo.
    
    :param yacimiento: Atributo opcional para especificar el centro de costos del yacimiento al cual se encuentra relacionado el costo, gasto o inversión, conforme a los “Lineamientos para la elaboración y presentación de los costos, gastos e inversiones; la procura de bienes y servicios en los contratos y asignaciones; la verificación contable y financiera de los contratos, y la actualización de regalías en contratos y del derecho de extracción de hidrocarburos”, emitidos por la Secretaria de Hacienda y Crédito Público.
    :param pozos: Nodo opcional para registrar el centro de costos del Pozo al cual se encuentra relacionado el Yacimiento.
    """
    
    def __init__(
            self,
            yacimiento: str = None,
            pozos: Pozos | dict | Sequence[Pozos | dict] = None,
    ): 
        super().__init__({
            'Yacimiento': yacimiento,
            'Pozos': pozos,
        })
        

class CentroCostos(ScalarMap):
    """
    Nodo opcional para capturar los datos complementarios del centro de costos al cual se encuentra relacionado el costo, gasto o inversión, especificando el pozo, yacimiento, campo y área contractual correspondiente.
    
    :param campo: Atributo opcional para especificar el centro de costos del campo al cual se encuentra relacionado el costo, gasto o inversión, conforme a los “Lineamientos para la elaboración y presentación de los costos, gastos e inversiones; la procura de bienes y servicios en los contratos y asignaciones; la verificación contable y financiera de los contratos, y la actualización de regalías en contratos y del derecho de extracción de hidrocarburos”, emitidos por la Secretaria de Hacienda y Crédito Público.
    :param yacimientos: Nodo opcional para registrar el centro de costos del yacimiento al cual se encuentra relacionado el campo.
    """
    
    def __init__(
            self,
            campo: str = None,
            yacimientos: Yacimientos | dict | Sequence[Yacimientos | dict] = None,
    ): 
        super().__init__({
            'Campo': campo,
            'Yacimientos': yacimientos,
        })
        

class Tareas(ScalarMap):
    """
    Nodo opcional para registrar las tareas relacionadas a cada sub actividad petrolera.
    
    :param tarea_relacionada: Atributo opcional para expresar la tarea con la cual se encuentra relacionado el costo, gasto o inversión de que se trata, conforme a los “Lineamientos para la elaboración y presentación de los costos, gastos e inversiones; la procura de bienes y servicios en los contratos y asignaciones; la verificación contable y financiera de los contratos, y la actualización de regalías en contratos y del derecho de extracción de hidrocarburos”, emitidos por la Secretaria de Hacienda y Crédito Público.
    """
    
    def __init__(
            self,
            tarea_relacionada: str = None,
    ): 
        super().__init__({
            'TareaRelacionada': tarea_relacionada,
        })
        

class SubActividades(ScalarMap):
    """
    Nodo opcional para registrar las sub actividades relacionadas a cada actividad petrolera.
    
    :param sub_actividad_relacionada: Atributo opcional para expresar la subactividad con la cual se encuentra relacionado el costo, gasto o inversión de que se trata, conforme a los “Lineamientos para la elaboración y presentación de los costos, gastos e inversiones; la procura de bienes y servicios en los contratos y asignaciones; la verificación contable y financiera de los contratos, y la actualización de regalías en contratos y del derecho de extracción de hidrocarburos”, emitidos por la Secretaria de Hacienda y Crédito Público.
    :param tareas: Nodo opcional para registrar las tareas relacionadas a cada sub actividad petrolera.
    """
    
    def __init__(
            self,
            sub_actividad_relacionada: str = None,
            tareas: Tareas | dict | Sequence[Tareas | dict] = None,
    ): 
        super().__init__({
            'SubActividadRelacionada': sub_actividad_relacionada,
            'Tareas': tareas,
        })
        

class Actividades(ScalarMap):
    """
    Nodo opcional para registrar las actividades petroleras.
    
    :param actividad_relacionada: Atributo opcional para expresar la actividad con la cual se encuentra relacionado el costo, gasto o inversión de que se trata, conforme a los “Lineamientos para la elaboración y presentación de los costos, gastos e inversiones; la procura de bienes y servicios en los contratos y asignaciones; la verificación contable y financiera de los contratos, y la actualización de regalías en contratos y del derecho de extracción de hidrocarburos”, emitidos por la Secretaria de Hacienda y Crédito Público.
    :param sub_actividades: Nodo opcional para registrar las sub actividades relacionadas a cada actividad petrolera.
    """
    
    def __init__(
            self,
            actividad_relacionada: str = None,
            sub_actividades: SubActividades | dict | Sequence[SubActividades | dict] = None,
    ): 
        super().__init__({
            'ActividadRelacionada': actividad_relacionada,
            'SubActividades': sub_actividades,
        })
        

class DocumentoRelacionado(ScalarMap):
    """
    Nodo requerido para expresar la información del documento relacionado a la erogación.
    
    :param origen_erogacion: Atributo requerido para expresar el origen de la operación nacional o extranjera, por lo que cuando sea nacional, deberá señalarse el FolioFiscalVinculado y cuando sea extranjera, deberá señalarse el NumeroPedimentoVinculado.
    :param mes: Atributo requerido para expresar el mes al que corresponden los costos, gastos o inversiones efectuadas.
    :param monto_total_erogaciones: Atributo requerido para expresar el monto total del costo, gasto o inversión, según corresponda, que conste en el CFDI o en el comprobante fiscal que cumpla con lo dispuesto en la regla 2.7.1.16. (o la regla que corresponda en la RMF del ejercicio que se trate), emitido a favor del operador del consorcio, el cual se encuentra vinculado con el CFDI emitido al integrante del consorcio.
    :param folio_fiscal_vinculado: Atributo condicional para expresar el folio fiscal del CFDI emitido al operador del consorcio con motivo de los costos, gastos o inversiones.
    :param rfc_proveedor: Atributo condicional para expresar el RFC del proveedor que expidió el CFDI a favor del operador del consorcio, con el que se encuentra vinculado el costo, gasto o inversión.
    :param monto_total_iva: Atributo condicional para expresar el monto total del IVA del CFDI expedido al operador del consorcio, el cual se encuentra vinculado con el CFDI emitido al integrante del consorcio.
    :param monto_retencion_isr: Atributo condicional para expresar el monto de retención del ISR que conste en el CFDI expedido al operador del consorcio.
    :param monto_retencion_iva: Atributo condicional para expresar el monto de retención del IVA que conste en el CFDI expedido al operador del consorcio.
    :param monto_retencion_otros_impuestos: Atributo condicional para expresar el monto de retención de otros impuestos que conste en el CFDI expedido al operador del consorcio.
    :param numero_pedimento_vinculado: Atributo condicional para expresar el número del pedimento de importación tramitado por el operador del consorcio con motivo de los costos, gastos o inversiones realizados en el extranjero, se expresa en el siguiente formato: últimos 2 dígitos del año de validación seguidos por dos espacios, 2 dígitos de la aduana de despacho seguidos por dos espacios, 4 dígitos del número de la patente seguidos por dos espacios, 1 dígito que corresponde al último dígito del año en curso, salvo que se trate de un pedimento consolidado iniciado en el año inmediato anterior o del pedimento original de una rectificación, seguido de 6 dígitos de la numeración progresiva por aduana.
    :param clave_pedimento_vinculado: Atributo condicional para expresar la clave del pedimento de importación tramitado por el operador del consorcio con motivo de los costos, gastos o inversiones, realizadas en el extranjero.
    :param clave_pago_pedimento_vinculado: Atributo condicional para expresar la clave de pago del pedimento tramitado por el operador del consorcio con motivo de los costos, gastos o inversiones, realizadas en el extranjero.
    :param monto_iva_pedimento: Atributo condicional para expresar el IVA pagado del pedimento de importación tramitado por el operador del consorcio con motivo de los costos, gastos o inversiones, realizadas en el extranjero.
    :param otros_impuestos_pagados_pedimento: Atributo condicional para expresar el monto total de otros impuestos pagados en el pedimento de importación, diferente de IVA, tramitado por el operador del consorcio con motivo de los costos, gastos o inversiones, realizadas en el extranjero.
    :param fecha_folio_fiscal_vinculado: Atributo condicional para expresar la fecha del comprobante fiscal, emitido al operador del consorcio con motivo de los costos, gastos o inversiones. Se expresa en la forma aaaa-mm-dd, de acuerdo con la especificación ISO 8601.
    """
    
    def __init__(
            self,
            origen_erogacion: str,
            mes: str,
            monto_total_erogaciones: Decimal | int,
            folio_fiscal_vinculado: str = None,
            rfc_proveedor: str = None,
            monto_total_iva: Decimal | int = None,
            monto_retencion_isr: Decimal | int = None,
            monto_retencion_iva: Decimal | int = None,
            monto_retencion_otros_impuestos: Decimal | int = None,
            numero_pedimento_vinculado: str = None,
            clave_pedimento_vinculado: str = None,
            clave_pago_pedimento_vinculado: str = None,
            monto_iva_pedimento: Decimal | int = None,
            otros_impuestos_pagados_pedimento: Decimal | int = None,
            fecha_folio_fiscal_vinculado: date = None,
    ): 
        super().__init__({
            'OrigenErogacion': origen_erogacion,
            'Mes': mes,
            'MontoTotalErogaciones': monto_total_erogaciones,
            'FolioFiscalVinculado': folio_fiscal_vinculado,
            'RFCProveedor': rfc_proveedor,
            'MontoTotalIVA': monto_total_iva,
            'MontoRetencionISR': monto_retencion_isr,
            'MontoRetencionIVA': monto_retencion_iva,
            'MontoRetencionOtrosImpuestos': monto_retencion_otros_impuestos,
            'NumeroPedimentoVinculado': numero_pedimento_vinculado,
            'ClavePedimentoVinculado': clave_pedimento_vinculado,
            'ClavePagoPedimentoVinculado': clave_pago_pedimento_vinculado,
            'MontoIVAPedimento': monto_iva_pedimento,
            'OtrosImpuestosPagadosPedimento': otros_impuestos_pagados_pedimento,
            'FechaFolioFiscalVinculado': fecha_folio_fiscal_vinculado,
        })
        

class Erogacion(ScalarMap):
    """
    Nodo requerido para capturar los datos de la erogación.
    
    :param tipo_erogacion: Atributo requerido para señalar el tipo de erogación realizada por el operador.
    :param montocu_erogacion: Atributo requerido para expresar el importe de cada uno de los costos, gastos o inversiones efectuados en el mes de que se trate y que integran el total del monto del CFDI emitido al integrante del consorcio y que se encuentran amparados en el CFDI o en el comprobante fiscal que cumpla con lo dispuesto en la regla 2.7.1.16. (o la regla que corresponda en la RMF del ejercicio de que se trate), expedido a favor del operador del consorcio.
    :param porcentaje: Atributo requerido para expresar el porcentaje que representa el importe total del CFDI que se expide al integrante del consorcio por los costos, gastos o inversiones efectuados en el mes de que se trate, en relación al importe total de los comprobantes expedidos al operador del consorcio.
    :param documento_relacionado: Nodo requerido para expresar la información del documento relacionado a la erogación.
    :param actividades: Nodo opcional para registrar las actividades petroleras.
    :param centro_costos: Nodo opcional para capturar los datos complementarios del centro de costos al cual se encuentra relacionado el costo, gasto o inversión, especificando el pozo, yacimiento, campo y área contractual correspondiente.
    """
    
    def __init__(
            self,
            tipo_erogacion: str,
            montocu_erogacion: Decimal | int,
            porcentaje: Decimal | int,
            documento_relacionado: DocumentoRelacionado | dict | Sequence[DocumentoRelacionado | dict],
            actividades: Actividades | dict | Sequence[Actividades | dict] = None,
            centro_costos: CentroCostos | dict | Sequence[CentroCostos | dict] = None,
    ): 
        super().__init__({
            'TipoErogacion': tipo_erogacion,
            'MontocuErogacion': montocu_erogacion,
            'Porcentaje': porcentaje,
            'DocumentoRelacionado': documento_relacionado,
            'Actividades': actividades,
            'CentroCostos': centro_costos,
        })
        

class GastosHidrocarburos(CFDI):
    """
    Complemento para incorporar la información sobre los gastos del consorcio derivados de la ejecución de un contrato de exploración o extracción de hidrocarburos.
    
    :param numero_contrato: Atributo requerido para expresar el número de contrato asignado por la Comisión Nacional de Hidrocarburos con el cual se encuentra vinculado el gasto.
    :param erogacion: Nodo requerido para capturar los datos de la erogación.
    :param area_contractual: Atributo opcional para especificar el centro de costos del área contractual al cual se encuentra relacionado el costo, gasto o inversión, conforme a los “Lineamientos para la elaboración y presentación de los costos, gastos e inversiones; la procura de bienes y servicios en los contratos y asignaciones; la verificación contable y financiera de los contratos, y la actualización de regalías en contratos y del derecho de extracción de hidrocarburos”, emitidos por la Secretaria de Hacienda y Crédito Público.
    """
    
    tag = '{http://www.sat.gob.mx/GastosHidrocarburos10}GastosHidrocarburos'
    version = '1.0'
    
    def __init__(
            self,
            numero_contrato: str,
            erogacion: Erogacion | dict | Sequence[Erogacion | dict],
            area_contractual: str = None,
    ): 
        super().__init__({
            'Version': self.version,
            'NumeroContrato': numero_contrato,
            'Erogacion': erogacion,
            'AreaContractual': area_contractual,
        })
        

