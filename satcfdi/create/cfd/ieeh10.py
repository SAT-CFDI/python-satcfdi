"""ieeh http://www.sat.gob.mx/IngresosHidrocarburos10"""
from decimal import Decimal
from datetime import datetime, date, time
from collections.abc import Sequence
from ...cfdi import CFDI
from ...xelement import XElement
from ...utils import ScalarMap


class DocumentoRelacionado(ScalarMap):
    """
    Nodo requerido para expresar la información del documento relacionado al ingreso.
    
    :param folio_fiscal_vinculado: Atributo requerido para expresar el folio fiscal del CFDI expedido por el operador del consorcio al FMP.
    :param fecha_folio_fiscal_vinculado: Atributo requerido para expresar la fecha del CFDI expedido por el operador del consorcio al FMP. Se expresa en la forma aaaa-mm-dd, de acuerdo con la especificación ISO 8601.
    :param mes: Atributo requerido para expresar el mes que corresponda al CFDI expedido por el operador del consorcio al FMP.
    """
    
    def __init__(
            self,
            folio_fiscal_vinculado: str,
            fecha_folio_fiscal_vinculado: date,
            mes: str,
    ): 
        super().__init__({
            'FolioFiscalVinculado': folio_fiscal_vinculado,
            'FechaFolioFiscalVinculado': fecha_folio_fiscal_vinculado,
            'Mes': mes,
        })
        

class IngresosHidrocarburos(CFDI):
    """
    Complemento para incorporar la información sobre Ingresos atribuibles a los Integrantes de un consorcio derivados de la contraprestación de un contrato de exploración o extracción de hidrocarburos.
    
    :param numero_contrato: Atributo requerido para expresar el número de contrato asignado por la Comisión Nacional de Hidrocarburos con el cual se encuentra vinculado el ingreso.
    :param contraprestacion_pagada_operador: Atributo requerido para precisar el importe total de las contraprestaciones pagadas al operador del consorcio.
    :param porcentaje: Atributo requerido para expresar el porcentaje que ampara el CFDI que emite cada integrante del consorcio al operador, respecto del total de las contraprestaciones entregadas al operador del consorcio por el FMP.
    :param documento_relacionado: Nodo requerido para expresar la información del documento relacionado al ingreso.
    """
    
    tag = '{http://www.sat.gob.mx/IngresosHidrocarburos10}IngresosHidrocarburos'
    version = '1.0'
    
    def __init__(
            self,
            numero_contrato: str,
            contraprestacion_pagada_operador: Decimal | int,
            porcentaje: Decimal | int,
            documento_relacionado: DocumentoRelacionado | dict | Sequence[DocumentoRelacionado | dict],
    ): 
        super().__init__({
            'Version': self.version,
            'NumeroContrato': numero_contrato,
            'ContraprestacionPagadaOperador': contraprestacion_pagada_operador,
            'Porcentaje': porcentaje,
            'DocumentoRelacionado': documento_relacionado,
        })
        

