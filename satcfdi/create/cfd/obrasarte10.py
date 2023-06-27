"""obrasarte http://www.sat.gob.mx/arteantiguedades"""
from decimal import Decimal
from datetime import datetime, date, time
from collections.abc import Sequence
from ...cfdi import CFDI
from ...xelement import XElement
from ...utils import ScalarMap


class Obrasarteantiguedades(CFDI):
    """
    Complemento al Comprobante Fiscal Digital por Internet (CFDI) para el manejo de la enajenación de obras de artes plásticas y antigüedades.
    
    :param tipo_bien: Atributo requerido para expresar el tipo de bien enajenado de conformidad con el Catálogo publicado en el portal del SAT en Internet.
    :param titulo_adquirido: Atributo requerido para expresar el titulo o forma por el que se adquirió la obra de arte plástica o antigüedades de conformidad con el Catálogo publicado en el portal del SAT en Internet.
    :param fecha_adquisicion: Atributo requerido que indica la fecha en que se adquirió originalmente la obra de arte plástica o antigüedades.
    :param caracteristicas_de_obra_o_pieza: Atributo requerido para expresar las características de la obra o pieza de arte plástica o antigüedades de conformidad con el Catálogo publicado en el portal del SAT en Internet.
    :param otros_tipo_bien: Atributo opcional que sólo debe incluirse en caso de haber elegido “Otros” en el atributo TipoBien.
    :param otros_titulo_adquirido: Atributo opcional que sólo debe incluirse en caso de haber elegido “Otros” en el atributo TituloAdquirido.
    :param subtotal: Atributo opcional para expresar el monto o valor original de adquisición, en su caso.
    :param iva: Atributo opcional para expresar el IVA del monto o valor original de adquisición, en su caso.
    """
    
    tag = '{http://www.sat.gob.mx/arteantiguedades}obrasarteantiguedades'
    version = '1.0'
    
    def __init__(
            self,
            tipo_bien: str,
            titulo_adquirido: str,
            fecha_adquisicion: date,
            caracteristicas_de_obra_o_pieza: str,
            otros_tipo_bien: str = None,
            otros_titulo_adquirido: str = None,
            subtotal: Decimal | int = None,
            iva: Decimal | int = None,
    ): 
        super().__init__({
            'Version': self.version,
            'TipoBien': tipo_bien,
            'TituloAdquirido': titulo_adquirido,
            'FechaAdquisicion': fecha_adquisicion,
            'CaracterísticasDeObraoPieza': caracteristicas_de_obra_o_pieza,
            'OtrosTipoBien': otros_tipo_bien,
            'OtrosTituloAdquirido': otros_titulo_adquirido,
            'Subtotal': subtotal,
            'IVA': iva,
        })
        

