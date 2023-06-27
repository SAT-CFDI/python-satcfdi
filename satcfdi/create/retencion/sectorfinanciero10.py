"""sectorfinanciero http://www.sat.gob.mx/esquemas/retencionpago/1/sectorfinanciero"""
from decimal import Decimal
from datetime import datetime, date, time
from collections.abc import Sequence
from ...cfdi import CFDI
from ...xelement import XElement
from ...utils import ScalarMap


class SectorFinanciero(CFDI):
    """
    Complemento requerido para uso exclusivo de las entidades integrantes del sistema financiero que actúen en su carácter de fiduciarias
    
    :param id_fideicom: Atributo requerido para expresar el Identificador o Número del Fideicomiso
    :param descrip_fideicom: Atributo requerido para expresar el objeto o fin del Fideicomiso
    :param nom_fideicom: Atributo opcional para expresar el Nombre del Fideicomiso
    """
    
    tag = '{http://www.sat.gob.mx/esquemas/retencionpago/1/sectorfinanciero}SectorFinanciero'
    version = '1.0'
    
    def __init__(
            self,
            id_fideicom: str,
            descrip_fideicom: str,
            nom_fideicom: str = None,
    ): 
        super().__init__({
            'Version': self.version,
            'IdFideicom': id_fideicom,
            'DescripFideicom': descrip_fideicom,
            'NomFideicom': nom_fideicom,
        })
        

