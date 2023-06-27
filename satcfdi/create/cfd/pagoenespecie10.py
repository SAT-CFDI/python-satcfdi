"""pagoenespecie http://www.sat.gob.mx/pagoenespecie"""
from decimal import Decimal
from datetime import datetime, date, time
from collections.abc import Sequence
from ...cfdi import CFDI
from ...xelement import XElement
from ...utils import ScalarMap


class PagoEnEspecie(CFDI):
    """
    Complemento para la expedición de comprobantes fiscales por la donación en la facilidad fiscal de Pago en Especie
    
    :param cve_pic: Clave de inscripción al Padrón de Instituciones Culturales adheridas al Programa de Pago en Especie
    :param folio_sol_don: Número de folio de la solicitud de donación
    :param pza_art_nombre: Nombre de la pieza de arte
    :param pza_art_tecn: Técnica de producción de la pieza de arte
    :param pza_art_aprod: Año de producción de la pieza de arte
    :param pza_art_dim: Dimensiones de la pieza de arte
    """
    
    tag = '{http://www.sat.gob.mx/pagoenespecie}PagoEnEspecie'
    version = '1.0'
    
    def __init__(
            self,
            cve_pic: str,
            folio_sol_don: str,
            pza_art_nombre: str,
            pza_art_tecn: str,
            pza_art_aprod: str,
            pza_art_dim: str,
    ): 
        super().__init__({
            'Version': self.version,
            'CvePIC': cve_pic,
            'FolioSolDon': folio_sol_don,
            'PzaArtNombre': pza_art_nombre,
            'PzaArtTecn': pza_art_tecn,
            'PzaArtAProd': pza_art_aprod,
            'PzaArtDim': pza_art_dim,
        })
        

