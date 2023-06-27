"""fep http://www.uif.shcp.gob.mx/recepcion/fep"""
from decimal import Decimal
from datetime import datetime, date, time
from collections.abc import Sequence
from ...cfdi import CFDI
from ...xelement import XElement
from ...utils import ScalarMap


class DatosComiteTecnicoType(ScalarMap):
    """
    
    :param comite_tecnico:
    :param modificacion_comite_tecnico:
    """
    
    def __init__(
            self,
            comite_tecnico: str,
            modificacion_comite_tecnico: str,
    ): 
        super().__init__({
            'ComiteTecnico': comite_tecnico,
            'ModificacionComiteTecnico': modificacion_comite_tecnico,
        })
        

class DatosPropietarioType(ScalarMap):
    """
    
    :param propietario_solicita:
    :param tipo_persona:
    """
    
    def __init__(
            self,
            propietario_solicita: str,
            tipo_persona: TipoPersonaSimpleType | dict = None,
    ): 
        super().__init__({
            'PropietarioSolicita': propietario_solicita,
            'TipoPersona': tipo_persona,
        })
        

class AvaluoType(ScalarMap):
    """
    
    :param tipo_bien:
    :param valor_avaluo:
    :param datos_propietario:
    :param descripcion:
    """
    
    def __init__(
            self,
            tipo_bien: str,
            valor_avaluo: str,
            datos_propietario: DatosPropietarioType | dict,
            descripcion: str = None,
    ): 
        super().__init__({
            'TipoBien': tipo_bien,
            'ValorAvaluo': valor_avaluo,
            'DatosPropietario': datos_propietario,
            'Descripcion': descripcion,
        })
        

class DatosLiquidacionSimpleType(ScalarMap):
    """
    
    :param moneda:
    :param monto_operacion:
    """
    
    def __init__(
            self,
            moneda: str,
            monto_operacion: str,
    ): 
        super().__init__({
            'Moneda': moneda,
            'MontoOperacion': monto_operacion,
        })
        

class PersonaMoralGaranteType(ScalarMap):
    """
    
    :param denominacion_razon:
    :param fecha_constitucion:
    :param rfc:
    """
    
    def __init__(
            self,
            denominacion_razon: str,
            fecha_constitucion: date = None,
            rfc: str = None,
    ): 
        super().__init__({
            'DenominacionRazon': denominacion_razon,
            'FechaConstitucion': fecha_constitucion,
            'Rfc': rfc,
        })
        

class PersonaFisicaGaranteType(ScalarMap):
    """
    
    :param nombre:
    :param apellido_paterno:
    :param apellido_materno:
    :param fecha_nacimiento:
    :param rfc:
    :param curp:
    """
    
    def __init__(
            self,
            nombre: str,
            apellido_paterno: str,
            apellido_materno: str,
            fecha_nacimiento: date = None,
            rfc: str = None,
            curp: str = None,
    ): 
        super().__init__({
            'Nombre': nombre,
            'ApellidoPaterno': apellido_paterno,
            'ApellidoMaterno': apellido_materno,
            'FechaNacimiento': fecha_nacimiento,
            'Rfc': rfc,
            'Curp': curp,
        })
        

class TipoPersonaGaranteType(ScalarMap):
    """
    
    :param persona_fisica:
    :param persona_moral:
    :param fideicomiso:
    """
    
    def __init__(
            self,
            persona_fisica: PersonaFisicaGaranteType | dict = None,
            persona_moral: PersonaMoralGaranteType | dict = None,
            fideicomiso: FideicomisoType | dict = None,
    ): 
        super().__init__({
            'PersonaFisica': persona_fisica,
            'PersonaMoral': persona_moral,
            'Fideicomiso': fideicomiso,
        })
        

class DatosOtroType(ScalarMap):
    """
    
    :param descripcion_garantia:
    """
    
    def __init__(
            self,
            descripcion_garantia: str,
    ): 
        super().__init__({
            'DescripcionGarantia': descripcion_garantia,
        })
        

class DatosInmuebleType(ScalarMap):
    """
    
    :param tipo_inmueble:
    :param valor_referencia:
    :param codigo_postal:
    :param folio_real:
    """
    
    def __init__(
            self,
            tipo_inmueble: str,
            valor_referencia: str,
            codigo_postal: str,
            folio_real: str,
    ): 
        super().__init__({
            'TipoInmueble': tipo_inmueble,
            'ValorReferencia': valor_referencia,
            'CodigoPostal': codigo_postal,
            'FolioReal': folio_real,
        })
        

class DatosBienMutuoType(ScalarMap):
    """
    
    :param datos_inmueble:
    :param datos_otro:
    """
    
    def __init__(
            self,
            datos_inmueble: DatosInmuebleType | dict = None,
            datos_otro: DatosOtroType | dict = None,
    ): 
        super().__init__({
            'DatosInmueble': datos_inmueble,
            'DatosOtro': datos_otro,
        })
        

class DatosGarantiaType(ScalarMap):
    """
    
    :param tipo_garantia:
    :param datos_bien_mutuo:
    :param tipo_persona:
    """
    
    def __init__(
            self,
            tipo_garantia: str,
            datos_bien_mutuo: DatosBienMutuoType | dict = None,
            tipo_persona: TipoPersonaGaranteType | dict = None,
    ): 
        super().__init__({
            'TipoGarantia': tipo_garantia,
            'DatosBienMutuo': datos_bien_mutuo,
            'TipoPersona': tipo_persona,
        })
        

class DatosDeudorType(ScalarMap):
    """
    
    :param tipo_persona:
    """
    
    def __init__(
            self,
            tipo_persona: TipoPersonaType | dict,
    ): 
        super().__init__({
            'TipoPersona': tipo_persona,
        })
        

class DatosAcreedorType(ScalarMap):
    """
    
    :param tipo_persona:
    """
    
    def __init__(
            self,
            tipo_persona: TipoPersonaType | dict,
    ): 
        super().__init__({
            'TipoPersona': tipo_persona,
        })
        

class ContratoMutuoCredType(ScalarMap):
    """
    
    :param tipo_otorgamiento:
    :param datos_acreedor:
    :param datos_deudor:
    :param datos_liquidacion:
    :param datos_garantia:
    """
    
    def __init__(
            self,
            tipo_otorgamiento: str,
            datos_acreedor: DatosAcreedorType | dict | Sequence[DatosAcreedorType | dict],
            datos_deudor: DatosDeudorType | dict | Sequence[DatosDeudorType | dict],
            datos_liquidacion: DatosLiquidacionSimpleType | dict | Sequence[DatosLiquidacionSimpleType | dict],
            datos_garantia: DatosGarantiaType | dict | Sequence[DatosGarantiaType | dict] = None,
    ): 
        super().__init__({
            'TipoOtorgamiento': tipo_otorgamiento,
            'DatosAcreedor': datos_acreedor,
            'DatosDeudor': datos_deudor,
            'DatosLiquidacion': datos_liquidacion,
            'DatosGarantia': datos_garantia,
        })
        

class DatosCesionType(ScalarMap):
    """
    
    :param monto_cesion:
    """
    
    def __init__(
            self,
            monto_cesion: str,
    ): 
        super().__init__({
            'MontoCesion': monto_cesion,
        })
        

class DatosCesionarioType(ScalarMap):
    """
    
    :param tipo_persona:
    """
    
    def __init__(
            self,
            tipo_persona: TipoPersonaType | dict,
    ): 
        super().__init__({
            'TipoPersona': tipo_persona,
        })
        

class DatosCedenteType(ScalarMap):
    """
    
    :param tipo_persona:
    """
    
    def __init__(
            self,
            tipo_persona: TipoPersonaType | dict,
    ): 
        super().__init__({
            'TipoPersona': tipo_persona,
        })
        

class CesionDerechosType(ScalarMap):
    """
    
    :param denominacion_razon:
    :param tipo_cesion:
    :param datos_cedente:
    :param datos_cesionario:
    :param datos_cesion:
    :param identificador_fideicomiso:
    :param rfc:
    """
    
    def __init__(
            self,
            denominacion_razon: str,
            tipo_cesion: str,
            datos_cedente: DatosCedenteType | dict,
            datos_cesionario: DatosCesionarioType | dict,
            datos_cesion: DatosCesionType | dict,
            identificador_fideicomiso: str = None,
            rfc: str = None,
    ): 
        super().__init__({
            'DenominacionRazon': denominacion_razon,
            'TipoCesion': tipo_cesion,
            'DatosCedente': datos_cedente,
            'DatosCesionario': datos_cesionario,
            'DatosCesion': datos_cesion,
            'IdentificadorFideicomiso': identificador_fideicomiso,
            'Rfc': rfc,
        })
        

class DatosFideicomisarioType(ScalarMap):
    """
    
    :param datos_fideicomisarios_determinados:
    :param tipo_persona:
    """
    
    def __init__(
            self,
            datos_fideicomisarios_determinados: str,
            tipo_persona: TipoPersona1Type | dict | Sequence[TipoPersona1Type | dict] = None,
    ): 
        super().__init__({
            'DatosFideicomisariosDeterminados': datos_fideicomisarios_determinados,
            'TipoPersona': tipo_persona,
        })
        

class PatrimonioOtroBienType(ScalarMap):
    """
    
    :param descripcion:
    :param valor_bien:
    """
    
    def __init__(
            self,
            descripcion: str,
            valor_bien: str,
    ): 
        super().__init__({
            'Descripcion': descripcion,
            'ValorBien': valor_bien,
        })
        

class PatrimonioInmuebleType(ScalarMap):
    """
    
    :param tipo_inmueble:
    :param codigo_postal:
    :param folio_real:
    :param importe_garantia:
    """
    
    def __init__(
            self,
            tipo_inmueble: str,
            codigo_postal: str,
            folio_real: str,
            importe_garantia: str,
    ): 
        super().__init__({
            'TipoInmueble': tipo_inmueble,
            'CodigoPostal': codigo_postal,
            'FolioReal': folio_real,
            'ImporteGarantia': importe_garantia,
        })
        

class PatrimonioMonetariaType(ScalarMap):
    """
    
    :param moneda:
    :param monto_operacion:
    """
    
    def __init__(
            self,
            moneda: str,
            monto_operacion: str,
    ): 
        super().__init__({
            'Moneda': moneda,
            'MontoOperacion': monto_operacion,
        })
        

class DatosTipoPatrimonioType(ScalarMap):
    """
    
    :param patrimonio_monetario:
    :param patrimonio_inmueble:
    :param patrimonio_otro_bien:
    """
    
    def __init__(
            self,
            patrimonio_monetario: PatrimonioMonetariaType | dict = None,
            patrimonio_inmueble: PatrimonioInmuebleType | dict = None,
            patrimonio_otro_bien: PatrimonioOtroBienType | dict = None,
    ): 
        super().__init__({
            'PatrimonioMonetario': patrimonio_monetario,
            'PatrimonioInmueble': patrimonio_inmueble,
            'PatrimonioOtroBien': patrimonio_otro_bien,
        })
        

class DatosFideicomitenteType(ScalarMap):
    """
    
    :param tipo_movimiento_fideicomitente:
    :param tipo_persona:
    :param datos_tipo_patrimonio:
    """
    
    def __init__(
            self,
            tipo_movimiento_fideicomitente: str,
            tipo_persona: TipoPersonaType | dict,
            datos_tipo_patrimonio: DatosTipoPatrimonioType | dict | Sequence[DatosTipoPatrimonioType | dict] = None,
    ): 
        super().__init__({
            'TipoMovimientoFideicomitente': tipo_movimiento_fideicomitente,
            'TipoPersona': tipo_persona,
            'DatosTipoPatrimonio': datos_tipo_patrimonio,
        })
        

class ConstModFideicomisoType(ScalarMap):
    """
    
    :param tipo_movimiento:
    :param tipo_fideicomiso:
    :param denominacion_razon:
    :param monto_patrimonio:
    :param datos_fideicomitente:
    :param descripcion:
    :param rfc:
    :param identificador_fideicomiso:
    :param datos_fideicomisarios:
    :param datos_miembro_comite_tecnico:
    """
    
    def __init__(
            self,
            tipo_movimiento: str,
            tipo_fideicomiso: str,
            denominacion_razon: str,
            monto_patrimonio: str,
            datos_fideicomitente: DatosFideicomitenteType | dict | Sequence[DatosFideicomitenteType | dict],
            descripcion: str = None,
            rfc: str = None,
            identificador_fideicomiso: str = None,
            datos_fideicomisarios: DatosFideicomisarioType | dict | Sequence[DatosFideicomisarioType | dict] = None,
            datos_miembro_comite_tecnico: DatosComiteTecnicoType | dict = None,
    ): 
        super().__init__({
            'TipoMovimiento': tipo_movimiento,
            'TipoFideicomiso': tipo_fideicomiso,
            'DenominacionRazon': denominacion_razon,
            'MontoPatrimonio': monto_patrimonio,
            'DatosFideicomitente': datos_fideicomitente,
            'Descripcion': descripcion,
            'Rfc': rfc,
            'IdentificadorFideicomiso': identificador_fideicomiso,
            'DatosFideicomisarios': datos_fideicomisarios,
            'DatosMiembroComiteTecnico': datos_miembro_comite_tecnico,
        })
        

class DatosLiquidacionType(ScalarMap):
    """
    
    :param fecha_pago:
    :param moneda:
    :param monto_operacion:
    :param instrumento_monetario:
    """
    
    def __init__(
            self,
            fecha_pago: date,
            moneda: str,
            monto_operacion: str,
            instrumento_monetario: str = None,
    ): 
        super().__init__({
            'FechaPago': fecha_pago,
            'Moneda': moneda,
            'MontoOperacion': monto_operacion,
            'InstrumentoMonetario': instrumento_monetario,
        })
        

class DatosCompradorType(ScalarMap):
    """
    
    :param numero_acciones_compradas:
    :param tipo_persona:
    """
    
    def __init__(
            self,
            numero_acciones_compradas: str,
            tipo_persona: TipoPersonaSimpleType | dict,
    ): 
        super().__init__({
            'NumeroAccionesCompradas': numero_acciones_compradas,
            'TipoPersona': tipo_persona,
        })
        

class DatosVendedorType(ScalarMap):
    """
    
    :param numero_acciones_vendidas:
    :param tipo_persona:
    """
    
    def __init__(
            self,
            numero_acciones_vendidas: str,
            tipo_persona: TipoPersonaSimpleType | dict,
    ): 
        super().__init__({
            'NumeroAccionesVendidas': numero_acciones_vendidas,
            'TipoPersona': tipo_persona,
        })
        

class PersonaMoralAccionesType(ScalarMap):
    """
    
    :param denominacion_razon:
    :param pais_nacionalidad:
    :param valor_nominal:
    :param numero_acciones:
    :param datos_vendedor:
    :param datos_comprador:
    :param fecha_constitucion:
    :param rfc:
    """
    
    def __init__(
            self,
            denominacion_razon: str,
            pais_nacionalidad: str,
            valor_nominal: str,
            numero_acciones: str,
            datos_vendedor: DatosVendedorType | dict | Sequence[DatosVendedorType | dict],
            datos_comprador: DatosCompradorType | dict | Sequence[DatosCompradorType | dict],
            fecha_constitucion: date = None,
            rfc: str = None,
    ): 
        super().__init__({
            'DenominacionRazon': denominacion_razon,
            'PaisNacionalidad': pais_nacionalidad,
            'ValorNominal': valor_nominal,
            'NumeroAcciones': numero_acciones,
            'DatosVendedor': datos_vendedor,
            'DatosComprador': datos_comprador,
            'FechaConstitucion': fecha_constitucion,
            'Rfc': rfc,
        })
        

class CompraVentaAccionesType(ScalarMap):
    """
    
    :param tipo_operacion:
    :param persona_moral_acciones:
    :param datos_liquidacion:
    """
    
    def __init__(
            self,
            tipo_operacion: str,
            persona_moral_acciones: PersonaMoralAccionesType | dict | Sequence[PersonaMoralAccionesType | dict],
            datos_liquidacion: DatosLiquidacionType | dict | Sequence[DatosLiquidacionType | dict],
    ): 
        super().__init__({
            'TipoOperacion': tipo_operacion,
            'PersonaMoralAcciones': persona_moral_acciones,
            'DatosLiquidacion': datos_liquidacion,
        })
        

class EscindidaType(ScalarMap):
    """
    
    :param denominacion_razon:
    :param pais_nacionalidad:
    :param giro_mercantil:
    :param capital_social_fijo:
    :param numero_total_acciones:
    :param datos_accionista:
    :param fecha_constitucion:
    :param rfc:
    :param capital_social_variable:
    :param folio_mercantil:
    """
    
    def __init__(
            self,
            denominacion_razon: str,
            pais_nacionalidad: str,
            giro_mercantil: str,
            capital_social_fijo: str,
            numero_total_acciones: str,
            datos_accionista: DatosAccionista1Type | dict | Sequence[DatosAccionista1Type | dict],
            fecha_constitucion: date = None,
            rfc: str = None,
            capital_social_variable: str = None,
            folio_mercantil: str = None,
    ): 
        super().__init__({
            'DenominacionRazon': denominacion_razon,
            'PaisNacionalidad': pais_nacionalidad,
            'GiroMercantil': giro_mercantil,
            'CapitalSocialFijo': capital_social_fijo,
            'NumeroTotalAcciones': numero_total_acciones,
            'DatosAccionista': datos_accionista,
            'FechaConstitucion': fecha_constitucion,
            'Rfc': rfc,
            'CapitalSocialVariable': capital_social_variable,
            'FolioMercantil': folio_mercantil,
        })
        

class DatosEscindidasType(ScalarMap):
    """
    
    :param escindidas_determinadas:
    :param dato_escindida:
    """
    
    def __init__(
            self,
            escindidas_determinadas: str,
            dato_escindida: EscindidaType | dict | Sequence[EscindidaType | dict] = None,
    ): 
        super().__init__({
            'EscindidasDeterminadas': escindidas_determinadas,
            'DatoEscindida': dato_escindida,
        })
        

class DatosEscindenteType(ScalarMap):
    """
    
    :param denominacion_razon:
    :param pais_nacionalidad:
    :param giro_mercantil:
    :param capital_social_fijo:
    :param escindente_subsiste:
    :param fecha_constitucion:
    :param rfc:
    :param capital_social_variable:
    :param folio_mercantil:
    :param datos_accionista_escindente:
    """
    
    def __init__(
            self,
            denominacion_razon: str,
            pais_nacionalidad: str,
            giro_mercantil: str,
            capital_social_fijo: str,
            escindente_subsiste: str,
            fecha_constitucion: date = None,
            rfc: str = None,
            capital_social_variable: str = None,
            folio_mercantil: str = None,
            datos_accionista_escindente: DatosAccionista1Type | dict | Sequence[DatosAccionista1Type | dict] = None,
    ): 
        super().__init__({
            'DenominacionRazon': denominacion_razon,
            'PaisNacionalidad': pais_nacionalidad,
            'GiroMercantil': giro_mercantil,
            'CapitalSocialFijo': capital_social_fijo,
            'EscindenteSubsiste': escindente_subsiste,
            'FechaConstitucion': fecha_constitucion,
            'Rfc': rfc,
            'CapitalSocialVariable': capital_social_variable,
            'FolioMercantil': folio_mercantil,
            'DatosAccionistaEscindente': datos_accionista_escindente,
        })
        

class EscisionType(ScalarMap):
    """
    
    :param datos_escindente:
    :param datos_escindidas:
    """
    
    def __init__(
            self,
            datos_escindente: DatosEscindenteType | dict,
            datos_escindidas: DatosEscindidasType | dict,
    ): 
        super().__init__({
            'DatosEscindente': datos_escindente,
            'DatosEscindidas': datos_escindidas,
        })
        

class FusionanteType(ScalarMap):
    """
    
    :param denominacion_razon:
    :param pais_nacionalidad:
    :param giro_mercantil:
    :param capital_social_fijo:
    :param numero_total_acciones:
    :param datos_accionista:
    :param fecha_constitucion:
    :param rfc:
    :param capital_social_variable:
    :param folio_mercantil:
    """
    
    def __init__(
            self,
            denominacion_razon: str,
            pais_nacionalidad: str,
            giro_mercantil: str,
            capital_social_fijo: str,
            numero_total_acciones: str,
            datos_accionista: DatosAccionista1Type | dict | Sequence[DatosAccionista1Type | dict],
            fecha_constitucion: date = None,
            rfc: str = None,
            capital_social_variable: str = None,
            folio_mercantil: str = None,
    ): 
        super().__init__({
            'DenominacionRazon': denominacion_razon,
            'PaisNacionalidad': pais_nacionalidad,
            'GiroMercantil': giro_mercantil,
            'CapitalSocialFijo': capital_social_fijo,
            'NumeroTotalAcciones': numero_total_acciones,
            'DatosAccionista': datos_accionista,
            'FechaConstitucion': fecha_constitucion,
            'Rfc': rfc,
            'CapitalSocialVariable': capital_social_variable,
            'FolioMercantil': folio_mercantil,
        })
        

class DatosFusionanteType(ScalarMap):
    """
    
    :param fusionante_determinadas:
    :param fusionante:
    """
    
    def __init__(
            self,
            fusionante_determinadas: str,
            fusionante: FusionanteType | dict = None,
    ): 
        super().__init__({
            'FusionanteDeterminadas': fusionante_determinadas,
            'Fusionante': fusionante,
        })
        

class DatosFusionadaType(ScalarMap):
    """
    
    :param denominacion_razon:
    :param pais_nacionalidad:
    :param giro_mercantil:
    :param capital_social_fijo:
    :param fecha_constitucion:
    :param rfc:
    :param capital_social_variable:
    :param folio_mercantil:
    """
    
    def __init__(
            self,
            denominacion_razon: str,
            pais_nacionalidad: str,
            giro_mercantil: str,
            capital_social_fijo: str,
            fecha_constitucion: date = None,
            rfc: str = None,
            capital_social_variable: str = None,
            folio_mercantil: str = None,
    ): 
        super().__init__({
            'DenominacionRazon': denominacion_razon,
            'PaisNacionalidad': pais_nacionalidad,
            'GiroMercantil': giro_mercantil,
            'CapitalSocialFijo': capital_social_fijo,
            'FechaConstitucion': fecha_constitucion,
            'Rfc': rfc,
            'CapitalSocialVariable': capital_social_variable,
            'FolioMercantil': folio_mercantil,
        })
        

class DatosFusionadasType(ScalarMap):
    """
    
    :param datos_fusionada:
    """
    
    def __init__(
            self,
            datos_fusionada: DatosFusionadaType | dict | Sequence[DatosFusionadaType | dict],
    ): 
        super().__init__({
            'DatosFusionada': datos_fusionada,
        })
        

class FusionType(ScalarMap):
    """
    
    :param tipo_fusion:
    :param datos_fusionadas:
    :param datos_fusionante:
    """
    
    def __init__(
            self,
            tipo_fusion: str,
            datos_fusionadas: DatosFusionadasType | dict,
            datos_fusionante: DatosFusionanteType | dict,
    ): 
        super().__init__({
            'TipoFusion': tipo_fusion,
            'DatosFusionadas': datos_fusionadas,
            'DatosFusionante': datos_fusionante,
        })
        

class DatosAccionista1Type(ScalarMap):
    """
    
    :param tipo_persona:
    :param numero_acciones:
    """
    
    def __init__(
            self,
            tipo_persona: TipoPersonaSimpleType | dict,
            numero_acciones: str,
    ): 
        super().__init__({
            'TipoPersona': tipo_persona,
            'NumeroAcciones': numero_acciones,
        })
        

class DatosModificacionType(ScalarMap):
    """
    
    :param tipo_modificacion_capital_fijo:
    :param inicial_capital_fijo:
    :param final_capital_fijo:
    :param tipo_modificacion_capital_variable:
    :param inicial_capital_variable:
    :param final_capital_variable:
    :param datos_accionista:
    """
    
    def __init__(
            self,
            tipo_modificacion_capital_fijo: str,
            inicial_capital_fijo: str,
            final_capital_fijo: str,
            tipo_modificacion_capital_variable: str,
            inicial_capital_variable: str,
            final_capital_variable: str,
            datos_accionista: DatosAccionista1Type | dict | Sequence[DatosAccionista1Type | dict],
    ): 
        super().__init__({
            'TipoModificacionCapitalFijo': tipo_modificacion_capital_fijo,
            'InicialCapitalFijo': inicial_capital_fijo,
            'FinalCapitalFijo': final_capital_fijo,
            'TipoModificacionCapitalVariable': tipo_modificacion_capital_variable,
            'InicialCapitalVariable': inicial_capital_variable,
            'FinalCapitalVariable': final_capital_variable,
            'DatosAccionista': datos_accionista,
        })
        

class PersonaMoralModificaType(ScalarMap):
    """
    
    :param denominacion_razon:
    :param pais_nacionalidad:
    :param giro_mercantil:
    :param numero_total_acciones:
    :param motivo_modificacion:
    :param fecha_constitucion:
    :param rfc:
    :param instrumento_publico:
    """
    
    def __init__(
            self,
            denominacion_razon: str,
            pais_nacionalidad: str,
            giro_mercantil: str,
            numero_total_acciones: str,
            motivo_modificacion: str,
            fecha_constitucion: date = None,
            rfc: str = None,
            instrumento_publico: str = None,
    ): 
        super().__init__({
            'DenominacionRazon': denominacion_razon,
            'PaisNacionalidad': pais_nacionalidad,
            'GiroMercantil': giro_mercantil,
            'NumeroTotalAcciones': numero_total_acciones,
            'MotivoModificacion': motivo_modificacion,
            'FechaConstitucion': fecha_constitucion,
            'Rfc': rfc,
            'InstrumentoPublico': instrumento_publico,
        })
        

class ModificacionPatrimonialType(ScalarMap):
    """
    
    :param persona_moral_modifica:
    :param datos_modificacion:
    """
    
    def __init__(
            self,
            persona_moral_modifica: PersonaMoralModificaType | dict,
            datos_modificacion: DatosModificacionType | dict,
    ): 
        super().__init__({
            'PersonaMoralModifica': persona_moral_modifica,
            'DatosModificacion': datos_modificacion,
        })
        

class CapitalSocialType(ScalarMap):
    """
    
    :param capital_fijo:
    :param capital_variable:
    """
    
    def __init__(
            self,
            capital_fijo: str,
            capital_variable: str = None,
    ): 
        super().__init__({
            'CapitalFijo': capital_fijo,
            'CapitalVariable': capital_variable,
        })
        

class DatosAccionistaType(ScalarMap):
    """
    
    :param cargo_accionista:
    :param tipo_persona:
    :param numero_acciones:
    """
    
    def __init__(
            self,
            cargo_accionista: str,
            tipo_persona: TipoPersonaSimpleType | dict,
            numero_acciones: str,
    ): 
        super().__init__({
            'CargoAccionista': cargo_accionista,
            'TipoPersona': tipo_persona,
            'NumeroAcciones': numero_acciones,
        })
        

class ConstitucionPersonasMoralesType(ScalarMap):
    """
    
    :param tipo_persona_moral:
    :param denominacion_razon:
    :param giro_mercantil:
    :param numero_total_acciones:
    :param entidad_federativa:
    :param consejo_vigilancia:
    :param motivo_constitucion:
    :param datos_accionista:
    :param capital_social:
    :param tipo_persona_moral_otra:
    :param folio_mercantil:
    :param instrumento_publico:
    """
    
    def __init__(
            self,
            tipo_persona_moral: str,
            denominacion_razon: str,
            giro_mercantil: str,
            numero_total_acciones: str,
            entidad_federativa: str,
            consejo_vigilancia: str,
            motivo_constitucion: str,
            datos_accionista: DatosAccionistaType | dict | Sequence[DatosAccionistaType | dict],
            capital_social: CapitalSocialType | dict,
            tipo_persona_moral_otra: str = None,
            folio_mercantil: str = None,
            instrumento_publico: str = None,
    ): 
        super().__init__({
            'TipoPersonaMoral': tipo_persona_moral,
            'DenominacionRazon': denominacion_razon,
            'GiroMercantil': giro_mercantil,
            'NumeroTotalAcciones': numero_total_acciones,
            'EntidadFederativa': entidad_federativa,
            'ConsejoVigilancia': consejo_vigilancia,
            'MotivoConstitucion': motivo_constitucion,
            'DatosAccionista': datos_accionista,
            'CapitalSocial': capital_social,
            'TipoPersonaMoralOtra': tipo_persona_moral_otra,
            'FolioMercantil': folio_mercantil,
            'InstrumentoPublico': instrumento_publico,
        })
        

class PersonaFisicaSimpleType(ScalarMap):
    """
    
    :param nombre:
    :param apellido_paterno:
    :param apellido_materno:
    :param pais_nacionalidad:
    :param fecha_nacimiento:
    :param rfc:
    :param curp:
    """
    
    def __init__(
            self,
            nombre: str,
            apellido_paterno: str,
            apellido_materno: str,
            pais_nacionalidad: str,
            fecha_nacimiento: date = None,
            rfc: str = None,
            curp: str = None,
    ): 
        super().__init__({
            'Nombre': nombre,
            'ApellidoPaterno': apellido_paterno,
            'ApellidoMaterno': apellido_materno,
            'PaisNacionalidad': pais_nacionalidad,
            'FechaNacimiento': fecha_nacimiento,
            'Rfc': rfc,
            'Curp': curp,
        })
        

class PersonaMoralSimpleType(ScalarMap):
    """
    
    :param denominacion_razon:
    :param pais_nacionalidad:
    :param fecha_constitucion:
    :param rfc:
    """
    
    def __init__(
            self,
            denominacion_razon: str,
            pais_nacionalidad: str,
            fecha_constitucion: date = None,
            rfc: str = None,
    ): 
        super().__init__({
            'DenominacionRazon': denominacion_razon,
            'PaisNacionalidad': pais_nacionalidad,
            'FechaConstitucion': fecha_constitucion,
            'Rfc': rfc,
        })
        

class TipoPersonaSimpleType(ScalarMap):
    """
    
    :param persona_fisica:
    :param persona_moral:
    :param fideicomiso:
    """
    
    def __init__(
            self,
            persona_fisica: PersonaFisicaSimpleType | dict = None,
            persona_moral: PersonaMoralSimpleType | dict = None,
            fideicomiso: FideicomisoType | dict = None,
    ): 
        super().__init__({
            'PersonaFisica': persona_fisica,
            'PersonaMoral': persona_moral,
            'Fideicomiso': fideicomiso,
        })
        

class FideicomisoType(ScalarMap):
    """
    
    :param denominacion_razon:
    :param rfc:
    :param identificador_fideicomiso:
    """
    
    def __init__(
            self,
            denominacion_razon: str,
            rfc: str = None,
            identificador_fideicomiso: str = None,
    ): 
        super().__init__({
            'DenominacionRazon': denominacion_razon,
            'Rfc': rfc,
            'IdentificadorFideicomiso': identificador_fideicomiso,
        })
        

class PersonaMoralType(ScalarMap):
    """
    
    :param denominacion_razon:
    :param pais_nacionalidad:
    :param giro_mercantil:
    :param fecha_constitucion:
    :param rfc:
    """
    
    def __init__(
            self,
            denominacion_razon: str,
            pais_nacionalidad: str,
            giro_mercantil: str,
            fecha_constitucion: date = None,
            rfc: str = None,
    ): 
        super().__init__({
            'DenominacionRazon': denominacion_razon,
            'PaisNacionalidad': pais_nacionalidad,
            'GiroMercantil': giro_mercantil,
            'FechaConstitucion': fecha_constitucion,
            'Rfc': rfc,
        })
        

class PersonaFisicaType(ScalarMap):
    """
    
    :param nombre:
    :param apellido_paterno:
    :param apellido_materno:
    :param pais_nacionalidad:
    :param actividad_economica:
    :param fecha_nacimiento:
    :param rfc:
    :param curp:
    """
    
    def __init__(
            self,
            nombre: str,
            apellido_paterno: str,
            apellido_materno: str,
            pais_nacionalidad: str,
            actividad_economica: str,
            fecha_nacimiento: date = None,
            rfc: str = None,
            curp: str = None,
    ): 
        super().__init__({
            'Nombre': nombre,
            'ApellidoPaterno': apellido_paterno,
            'ApellidoMaterno': apellido_materno,
            'PaisNacionalidad': pais_nacionalidad,
            'ActividadEconomica': actividad_economica,
            'FechaNacimiento': fecha_nacimiento,
            'Rfc': rfc,
            'Curp': curp,
        })
        

class TipoPersonaType(ScalarMap):
    """
    
    :param persona_fisica:
    :param persona_moral:
    :param fideicomiso:
    """
    
    def __init__(
            self,
            persona_fisica: PersonaFisicaType | dict = None,
            persona_moral: PersonaMoralType | dict = None,
            fideicomiso: FideicomisoType | dict = None,
    ): 
        super().__init__({
            'PersonaFisica': persona_fisica,
            'PersonaMoral': persona_moral,
            'Fideicomiso': fideicomiso,
        })
        

class DatosApoderadoType(ScalarMap):
    """
    
    :param tipo_poder:
    :param tipo_persona:
    """
    
    def __init__(
            self,
            tipo_poder: str,
            tipo_persona: TipoPersonaSimpleType | dict,
    ): 
        super().__init__({
            'TipoPoder': tipo_poder,
            'TipoPersona': tipo_persona,
        })
        

class DatosPoderdanteType(ScalarMap):
    """
    
    :param tipo_persona:
    """
    
    def __init__(
            self,
            tipo_persona: TipoPersonaType | dict,
    ): 
        super().__init__({
            'TipoPersona': tipo_persona,
        })
        

class OtorgamientoPoderType(ScalarMap):
    """
    
    :param datos_poderdante:
    :param datos_apoderado:
    """
    
    def __init__(
            self,
            datos_poderdante: DatosPoderdanteType | dict | Sequence[DatosPoderdanteType | dict],
            datos_apoderado: DatosApoderadoType | dict | Sequence[DatosApoderadoType | dict],
    ): 
        super().__init__({
            'DatosPoderdante': datos_poderdante,
            'DatosApoderado': datos_apoderado,
        })
        

class TipoActividadType(ScalarMap):
    """
    
    :param otorgamiento_poder:
    :param constitucion_personas_morales:
    :param modificacion_patrimonial:
    :param fusion:
    :param escision:
    :param compra_venta_acciones:
    :param constitucion_modificacion_fideicomiso:
    :param cesion_derechos_fideicomitente_fideicomisario:
    :param contrato_mutuo_credito:
    :param avaluo:
    """
    
    def __init__(
            self,
            otorgamiento_poder: OtorgamientoPoderType | dict = None,
            constitucion_personas_morales: ConstitucionPersonasMoralesType | dict = None,
            modificacion_patrimonial: ModificacionPatrimonialType | dict = None,
            fusion: FusionType | dict = None,
            escision: EscisionType | dict = None,
            compra_venta_acciones: CompraVentaAccionesType | dict = None,
            constitucion_modificacion_fideicomiso: ConstModFideicomisoType | dict = None,
            cesion_derechos_fideicomitente_fideicomisario: CesionDerechosType | dict = None,
            contrato_mutuo_credito: ContratoMutuoCredType | dict = None,
            avaluo: AvaluoType | dict = None,
    ): 
        super().__init__({
            'OtorgamientoPoder': otorgamiento_poder,
            'ConstitucionPersonasMorales': constitucion_personas_morales,
            'ModificacionPatrimonial': modificacion_patrimonial,
            'Fusion': fusion,
            'Escision': escision,
            'CompraVentaAcciones': compra_venta_acciones,
            'ConstitucionModificacionFideicomiso': constitucion_modificacion_fideicomiso,
            'CesionDerechosFideicomitenteFideicomisario': cesion_derechos_fideicomitente_fideicomisario,
            'ContratoMutuoCredito': contrato_mutuo_credito,
            'Avaluo': avaluo,
        })
        

class DatosOperacionType(ScalarMap):
    """
    
    :param instrumento_publico:
    :param fecha_operacion:
    :param tipo_actividad:
    """
    
    def __init__(
            self,
            instrumento_publico: str,
            fecha_operacion: date,
            tipo_actividad: TipoActividadType | dict,
    ): 
        super().__init__({
            'InstrumentoPublico': instrumento_publico,
            'FechaOperacion': fecha_operacion,
            'TipoActividad': tipo_actividad,
        })
        

class DetalleOperacionesType(ScalarMap):
    """
    
    :param datos_operacion:
    """
    
    def __init__(
            self,
            datos_operacion: DatosOperacionType | dict | Sequence[DatosOperacionType | dict],
    ): 
        super().__init__({
            'DatosOperacion': datos_operacion,
        })
        

class PersonaAvisoType(ScalarMap):
    """
    
    :param nombre:
    :param apellido_paterno:
    :param apellido_materno:
    :param fecha_nacimiento:
    :param rfc:
    :param curp:
    """
    
    def __init__(
            self,
            nombre: str,
            apellido_paterno: str,
            apellido_materno: str,
            fecha_nacimiento: date = None,
            rfc: str = None,
            curp: str = None,
    ): 
        super().__init__({
            'Nombre': nombre,
            'ApellidoPaterno': apellido_paterno,
            'ApellidoMaterno': apellido_materno,
            'FechaNacimiento': fecha_nacimiento,
            'Rfc': rfc,
            'Curp': curp,
        })
        

class AlertaType(ScalarMap):
    """
    
    :param tipo_alerta:
    :param descripcion_alerta:
    """
    
    def __init__(
            self,
            tipo_alerta: str,
            descripcion_alerta: str = None,
    ): 
        super().__init__({
            'TipoAlerta': tipo_alerta,
            'DescripcionAlerta': descripcion_alerta,
        })
        

class ModificatorioType(ScalarMap):
    """
    
    :param folio_modificacion:
    :param descripcion_modificacion:
    """
    
    def __init__(
            self,
            folio_modificacion: str,
            descripcion_modificacion: str,
    ): 
        super().__init__({
            'FolioModificacion': folio_modificacion,
            'DescripcionModificacion': descripcion_modificacion,
        })
        

class AvisoType(ScalarMap):
    """
    
    :param referencia_aviso:
    :param prioridad:
    :param alerta:
    :param persona_aviso:
    :param detalle_operaciones:
    :param modificatorio:
    """
    
    def __init__(
            self,
            referencia_aviso: str,
            prioridad: str,
            alerta: AlertaType | dict,
            persona_aviso: PersonaAvisoType | dict | Sequence[PersonaAvisoType | dict],
            detalle_operaciones: DetalleOperacionesType | dict,
            modificatorio: ModificatorioType | dict = None,
    ): 
        super().__init__({
            'ReferenciaAviso': referencia_aviso,
            'Prioridad': prioridad,
            'Alerta': alerta,
            'PersonaAviso': persona_aviso,
            'DetalleOperaciones': detalle_operaciones,
            'Modificatorio': modificatorio,
        })
        

class SujetoObligadoType(ScalarMap):
    """
    
    :param clave_sujeto_obligado:
    :param clave_actividad:
    :param clave_entidad_colegiada:
    :param exento:
    """
    
    def __init__(
            self,
            clave_sujeto_obligado: str,
            clave_actividad: str,
            clave_entidad_colegiada: str = None,
            exento: str = None,
    ): 
        super().__init__({
            'ClaveSujetoObligado': clave_sujeto_obligado,
            'ClaveActividad': clave_actividad,
            'ClaveEntidadColegiada': clave_entidad_colegiada,
            'Exento': exento,
        })
        

class InformeType(ScalarMap):
    """
    
    :param mes_reportado:
    :param sujeto_obligado:
    :param aviso:
    """
    
    def __init__(
            self,
            mes_reportado: str,
            sujeto_obligado: SujetoObligadoType | dict,
            aviso: AvisoType | dict | Sequence[AvisoType | dict] = None,
    ): 
        super().__init__({
            'MesReportado': mes_reportado,
            'SujetoObligado': sujeto_obligado,
            'Aviso': aviso,
        })
        

class ArchivoType(ScalarMap):
    """
    
    :param informe:
    """
    
    def __init__(
            self,
            informe: InformeType | dict | Sequence[InformeType | dict],
    ): 
        super().__init__({
            'Informe': informe,
        })
        

class TipoPersona1Type(ScalarMap):
    """
    
    :param tipo_movimiento_fideicomisario:
    :param persona_fisica:
    :param persona_moral:
    :param fideicomiso:
    """
    
    def __init__(
            self,
            tipo_movimiento_fideicomisario: str,
            persona_fisica: PersonaFisicaType | dict = None,
            persona_moral: PersonaMoralType | dict = None,
            fideicomiso: FideicomisoType | dict = None,
    ): 
        super().__init__({
            'TipoMovimientoFideicomisario': tipo_movimiento_fideicomisario,
            'PersonaFisica': persona_fisica,
            'PersonaMoral': persona_moral,
            'Fideicomiso': fideicomiso,
        })
        

class Archivo(ArchivoType, XElement):
    tag = '{http://www.uif.shcp.gob.mx/recepcion/fep}archivo'

