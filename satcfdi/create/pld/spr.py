"""spr http://www.uif.shcp.gob.mx/recepcion/spr"""
from decimal import Decimal
from datetime import datetime, date, time
from collections.abc import Sequence
from ...cfdi import CFDI
from ...xelement import XElement
from ...utils import ScalarMap


class ActivoVirtualType(ScalarMap):
    """
    
    :param tipo_activo_virtual:
    :param cantidad_activo_virtual:
    :param descripcion_activo_virtual:
    """
    
    def __init__(
            self,
            tipo_activo_virtual: int,
            cantidad_activo_virtual: str,
            descripcion_activo_virtual: str = None,
    ): 
        super().__init__({
            'TipoActivoVirtual': tipo_activo_virtual,
            'CantidadActivoVirtual': cantidad_activo_virtual,
            'DescripcionActivoVirtual': descripcion_activo_virtual,
        })
        

class DatosOperacionFinancieraType(ScalarMap):
    """
    
    :param instrumento_monetario:
    :param monto_operacion:
    :param fecha_pago:
    :param activo_virtual:
    :param moneda:
    """
    
    def __init__(
            self,
            instrumento_monetario: str,
            monto_operacion: str,
            fecha_pago: date = None,
            activo_virtual: ActivoVirtualType | dict = None,
            moneda: str = None,
    ): 
        super().__init__({
            'InstrumentoMonetario': instrumento_monetario,
            'MontoOperacion': monto_operacion,
            'FechaPago': fecha_pago,
            'ActivoVirtual': activo_virtual,
            'Moneda': moneda,
        })
        

class DatosSociedadMercantilType(ScalarMap):
    """
    
    :param denominacion_razon:
    :param giro_mercantil:
    :param pais_nacionalidad:
    :param acciones_adquiridas:
    :param acciones_totales:
    :param datos_contraparte:
    :param fecha_constitucion:
    :param rfc:
    :param folio_mercantil:
    """
    
    def __init__(
            self,
            denominacion_razon: str,
            giro_mercantil: str,
            pais_nacionalidad: str,
            acciones_adquiridas: str,
            acciones_totales: str,
            datos_contraparte: TipoPersonaT1Type | dict,
            fecha_constitucion: date = None,
            rfc: str = None,
            folio_mercantil: str = None,
    ): 
        super().__init__({
            'DenominacionRazon': denominacion_razon,
            'GiroMercantil': giro_mercantil,
            'PaisNacionalidad': pais_nacionalidad,
            'AccionesAdquiridas': acciones_adquiridas,
            'AccionesTotales': acciones_totales,
            'DatosContraparte': datos_contraparte,
            'FechaConstitucion': fecha_constitucion,
            'Rfc': rfc,
            'FolioMercantil': folio_mercantil,
        })
        

class CompraVentaEntidadesMercantilesType(ScalarMap):
    """
    
    :param tipo_operacion:
    :param datos_sociedad_mercantil:
    """
    
    def __init__(
            self,
            tipo_operacion: str,
            datos_sociedad_mercantil: DatosSociedadMercantilType | dict | Sequence[DatosSociedadMercantilType | dict],
    ): 
        super().__init__({
            'TipoOperacion': tipo_operacion,
            'DatosSociedadMercantil': datos_sociedad_mercantil,
        })
        

class DatosComiteTecnicoType(ScalarMap):
    """
    
    :param comite_tecnico:
    """
    
    def __init__(
            self,
            comite_tecnico: str,
    ): 
        super().__init__({
            'ComiteTecnico': comite_tecnico,
        })
        

class DatosFideicomisarioType(ScalarMap):
    """
    
    :param datos_fideicomisarios_determinados:
    :param tipo_persona:
    """
    
    def __init__(
            self,
            datos_fideicomisarios_determinados: str,
            tipo_persona: TipoPersonaT1Type | dict = None,
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
        

class PatrimonioMonetarioType(ScalarMap):
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
            patrimonio_monetario: PatrimonioMonetarioType | dict = None,
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
    
    :param tipo_persona:
    :param datos_tipo_patrimonio:
    """
    
    def __init__(
            self,
            tipo_persona: TipoPersonaT1Type | dict,
            datos_tipo_patrimonio: DatosTipoPatrimonioType | dict | Sequence[DatosTipoPatrimonioType | dict],
    ): 
        super().__init__({
            'TipoPersona': tipo_persona,
            'DatosTipoPatrimonio': datos_tipo_patrimonio,
        })
        

class ConstitucionFideicomisoType(ScalarMap):
    """
    
    :param denominacion_razon:
    :param objeto_fideicomiso:
    :param monto_total_patrimonio:
    :param datos_fideicomitente:
    :param datos_fideicomisario:
    :param datos_miembro_comite_tecnico:
    :param rfc:
    :param identificador_fideicomiso:
    """
    
    def __init__(
            self,
            denominacion_razon: str,
            objeto_fideicomiso: str,
            monto_total_patrimonio: str,
            datos_fideicomitente: DatosFideicomitenteType | dict | Sequence[DatosFideicomitenteType | dict],
            datos_fideicomisario: DatosFideicomisarioType | dict | Sequence[DatosFideicomisarioType | dict],
            datos_miembro_comite_tecnico: DatosComiteTecnicoType | dict,
            rfc: str = None,
            identificador_fideicomiso: str = None,
    ): 
        super().__init__({
            'DenominacionRazon': denominacion_razon,
            'ObjetoFideicomiso': objeto_fideicomiso,
            'MontoTotalPatrimonio': monto_total_patrimonio,
            'DatosFideicomitente': datos_fideicomitente,
            'DatosFideicomisario': datos_fideicomisario,
            'DatosMiembroComiteTecnico': datos_miembro_comite_tecnico,
            'Rfc': rfc,
            'IdentificadorFideicomiso': identificador_fideicomiso,
        })
        

class TipoPersonaMoralType(ScalarMap):
    """
    
    :param persona_moral:
    :param fideicomiso:
    """
    
    def __init__(
            self,
            persona_moral: PersonaMoralSimpleType | dict = None,
            fideicomiso: FideicomisoSimpleType | dict = None,
    ): 
        super().__init__({
            'PersonaMoral': persona_moral,
            'Fideicomiso': fideicomiso,
        })
        

class AdmonPersonasMoralesType(ScalarMap):
    """
    
    :param tipo_administracion:
    :param tipo_operacion:
    :param persona_moral_aviso:
    :param tipo_persona:
    """
    
    def __init__(
            self,
            tipo_administracion: str,
            tipo_operacion: str,
            persona_moral_aviso: str,
            tipo_persona: TipoPersonaMoralType | dict = None,
    ): 
        super().__init__({
            'TipoAdministracion': tipo_administracion,
            'TipoOperacion': tipo_operacion,
            'PersonaMoralAviso': persona_moral_aviso,
            'TipoPersona': tipo_persona,
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
            datos_accionista: DatosAccionistaT2Type | dict | Sequence[DatosAccionistaT2Type | dict],
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
        

class DatosAccionistaT3Type(ScalarMap):
    """
    
    :param tipo_persona:
    :param numero_acciones:
    """
    
    def __init__(
            self,
            tipo_persona: TipoPersonaT1Type | dict,
            numero_acciones: str,
    ): 
        super().__init__({
            'TipoPersona': tipo_persona,
            'NumeroAcciones': numero_acciones,
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
            datos_accionista_escindente: DatosAccionistaT3Type | dict | Sequence[DatosAccionistaT3Type | dict] = None,
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
        

class DatosAccionistaT2Type(ScalarMap):
    """
    
    :param tipo_persona:
    :param numero_acciones:
    """
    
    def __init__(
            self,
            tipo_persona: TipoPersonaT1Type | dict,
            numero_acciones: str,
    ): 
        super().__init__({
            'TipoPersona': tipo_persona,
            'NumeroAcciones': numero_acciones,
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
            datos_accionista: DatosAccionistaT2Type | dict | Sequence[DatosAccionistaT2Type | dict],
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
        

class AportacionOtroBienType(ScalarMap):
    """
    
    :param descripcion:
    :param valor_aportacion:
    """
    
    def __init__(
            self,
            descripcion: str,
            valor_aportacion: str,
    ): 
        super().__init__({
            'Descripcion': descripcion,
            'ValorAportacion': valor_aportacion,
        })
        

class AportacionInmuebleType(ScalarMap):
    """
    
    :param tipo_inmueble:
    :param codigo_postal:
    :param folio_real:
    :param valor_aportacion:
    """
    
    def __init__(
            self,
            tipo_inmueble: str,
            codigo_postal: str,
            folio_real: str,
            valor_aportacion: str,
    ): 
        super().__init__({
            'TipoInmueble': tipo_inmueble,
            'CodigoPostal': codigo_postal,
            'FolioReal': folio_real,
            'ValorAportacion': valor_aportacion,
        })
        

class AportacionMonetariaType(ScalarMap):
    """
    
    :param instrumento_monetario:
    :param moneda:
    :param monto_operacion:
    """
    
    def __init__(
            self,
            instrumento_monetario: str,
            moneda: str,
            monto_operacion: str,
    ): 
        super().__init__({
            'InstrumentoMonetario': instrumento_monetario,
            'Moneda': moneda,
            'MontoOperacion': monto_operacion,
        })
        

class DatosTipoAportacionType(ScalarMap):
    """
    
    :param aportacion_monetaria:
    :param aportacion_inmueble:
    :param aportacion_otro_bien:
    """
    
    def __init__(
            self,
            aportacion_monetaria: AportacionMonetariaType | dict = None,
            aportacion_inmueble: AportacionInmuebleType | dict = None,
            aportacion_otro_bien: AportacionOtroBienType | dict = None,
    ): 
        super().__init__({
            'AportacionMonetaria': aportacion_monetaria,
            'AportacionInmueble': aportacion_inmueble,
            'AportacionOtroBien': aportacion_otro_bien,
        })
        

class PersonaMoralT2Type(ScalarMap):
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
        

class PersonaFisicaT2Type(ScalarMap):
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
        

class TipoPersonaT2Type(ScalarMap):
    """
    
    :param persona_fisica:
    :param persona_moral:
    :param fideicomiso:
    """
    
    def __init__(
            self,
            persona_fisica: PersonaFisicaT2Type | dict = None,
            persona_moral: PersonaMoralT2Type | dict = None,
            fideicomiso: FideicomisoSimpleType | dict = None,
    ): 
        super().__init__({
            'PersonaFisica': persona_fisica,
            'PersonaMoral': persona_moral,
            'Fideicomiso': fideicomiso,
        })
        

class DatosAportacionType(ScalarMap):
    """
    
    :param datos_persona_aporta:
    :param datos_tipo_aportacion:
    """
    
    def __init__(
            self,
            datos_persona_aporta: TipoPersonaT2Type | dict,
            datos_tipo_aportacion: DatosTipoAportacionType | dict | Sequence[DatosTipoAportacionType | dict],
    ): 
        super().__init__({
            'DatosPersonaAporta': datos_persona_aporta,
            'DatosTipoAportacion': datos_tipo_aportacion,
        })
        

class OrganizacionAportacionesType(ScalarMap):
    """
    
    :param motivo_aportacion:
    :param datos_aportacion:
    """
    
    def __init__(
            self,
            motivo_aportacion: str,
            datos_aportacion: DatosAportacionType | dict | Sequence[DatosAportacionType | dict],
    ): 
        super().__init__({
            'MotivoAportacion': motivo_aportacion,
            'DatosAportacion': datos_aportacion,
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
        

class DatosAccionistaT1Type(ScalarMap):
    """
    
    :param cargo_accionista:
    :param tipo_persona:
    :param numero_acciones:
    """
    
    def __init__(
            self,
            cargo_accionista: str,
            tipo_persona: TipoPersonaT1Type | dict,
            numero_acciones: str,
    ): 
        super().__init__({
            'CargoAccionista': cargo_accionista,
            'TipoPersona': tipo_persona,
            'NumeroAcciones': numero_acciones,
        })
        

class ConstitucionSociedadesMercantilesType(ScalarMap):
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
            tipo_persona_moral: int,
            denominacion_razon: str,
            giro_mercantil: str,
            numero_total_acciones: str,
            entidad_federativa: int,
            consejo_vigilancia: str,
            motivo_constitucion: str,
            datos_accionista: DatosAccionistaT1Type | dict | Sequence[DatosAccionistaT1Type | dict],
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
        

class ActivoOtrosType(ScalarMap):
    """
    
    :param descripcion_activo_administrado:
    """
    
    def __init__(
            self,
            descripcion_activo_administrado: str,
    ): 
        super().__init__({
            'DescripcionActivoAdministrado': descripcion_activo_administrado,
        })
        

class ActivoAdministradoType(ScalarMap):
    """
    
    :param tipo_activo_administrado:
    :param descripcion_otro_activo_administrado:
    """
    
    def __init__(
            self,
            tipo_activo_administrado: int,
            descripcion_otro_activo_administrado: str = None,
    ): 
        super().__init__({
            'TipoActivoAdministrado': tipo_activo_administrado,
            'DescripcionOtroActivoAdministrado': descripcion_otro_activo_administrado,
        })
        

class AreaServicioType(ScalarMap):
    """
    
    :param tipo_area_servicio:
    :param descripcion_otro_area_servicio:
    """
    
    def __init__(
            self,
            tipo_area_servicio: int,
            descripcion_otro_area_servicio: str = None,
    ): 
        super().__init__({
            'TipoAreaServicio': tipo_area_servicio,
            'DescripcionOtroAreaServicio': descripcion_otro_area_servicio,
        })
        

class ActivoOutsourcingType(ScalarMap):
    """
    
    :param area_servicio:
    :param activo_administrado:
    :param numero_empleados:
    """
    
    def __init__(
            self,
            area_servicio: AreaServicioType | dict,
            activo_administrado: ActivoAdministradoType | dict,
            numero_empleados: int,
    ): 
        super().__init__({
            'AreaServicio': area_servicio,
            'ActivoAdministrado': activo_administrado,
            'NumeroEmpleados': numero_empleados,
        })
        

class ActivoInmobiliarioType(ScalarMap):
    """
    
    :param tipo_inmueble:
    :param valor_referencia:
    :param colonia:
    :param calle:
    :param numero_exterior:
    :param codigo_postal:
    :param folio_real:
    :param numero_interior:
    """
    
    def __init__(
            self,
            tipo_inmueble: str,
            valor_referencia: str,
            colonia: str,
            calle: str,
            numero_exterior: str,
            codigo_postal: str,
            folio_real: str,
            numero_interior: str = None,
    ): 
        super().__init__({
            'TipoInmueble': tipo_inmueble,
            'ValorReferencia': valor_referencia,
            'Colonia': colonia,
            'Calle': calle,
            'NumeroExterior': numero_exterior,
            'CodigoPostal': codigo_postal,
            'FolioReal': folio_real,
            'NumeroInterior': numero_interior,
        })
        

class ActivoBancoType(ScalarMap):
    """
    
    :param estatus_manejo:
    :param clave_tipo_institucion:
    :param nombre_institucion:
    :param numero_cuenta:
    """
    
    def __init__(
            self,
            estatus_manejo: str,
            clave_tipo_institucion: int,
            nombre_institucion: str,
            numero_cuenta: str,
    ): 
        super().__init__({
            'EstatusManejo': estatus_manejo,
            'ClaveTipoInstitucion': clave_tipo_institucion,
            'NombreInstitucion': nombre_institucion,
            'NumeroCuenta': numero_cuenta,
        })
        

class TipoActivoType(ScalarMap):
    """
    
    :param activo_banco:
    :param activo_inmobiliario:
    :param activo_outsourcing:
    :param activo_otros:
    """
    
    def __init__(
            self,
            activo_banco: ActivoBancoType | dict = None,
            activo_inmobiliario: ActivoInmobiliarioType | dict = None,
            activo_outsourcing: ActivoOutsourcingType | dict = None,
            activo_otros: ActivoOtrosType | dict = None,
    ): 
        super().__init__({
            'ActivoBanco': activo_banco,
            'ActivoInmobiliario': activo_inmobiliario,
            'ActivoOutsourcing': activo_outsourcing,
            'ActivoOtros': activo_otros,
        })
        

class AdministracionRecursosType(ScalarMap):
    """
    
    :param tipo_activo:
    :param numero_operaciones:
    """
    
    def __init__(
            self,
            tipo_activo: TipoActivoType | dict | Sequence[TipoActivoType | dict],
            numero_operaciones: int,
    ): 
        super().__init__({
            'TipoActivo': tipo_activo,
            'NumeroOperaciones': numero_operaciones,
        })
        

class CaracteristicasInmueble2Type(ScalarMap):
    """
    
    :param tipo_inmueble:
    :param valor_referencia:
    :param colonia:
    :param calle:
    :param numero_exterior:
    :param codigo_postal:
    :param dimension_terreno:
    :param dimension_construido:
    :param folio_real:
    :param numero_interior:
    """
    
    def __init__(
            self,
            tipo_inmueble: str,
            valor_referencia: str,
            colonia: str,
            calle: str,
            numero_exterior: str,
            codigo_postal: str,
            dimension_terreno: str,
            dimension_construido: str,
            folio_real: str,
            numero_interior: str = None,
    ): 
        super().__init__({
            'TipoInmueble': tipo_inmueble,
            'ValorReferencia': valor_referencia,
            'Colonia': colonia,
            'Calle': calle,
            'NumeroExterior': numero_exterior,
            'CodigoPostal': codigo_postal,
            'DimensionTerreno': dimension_terreno,
            'DimensionConstruido': dimension_construido,
            'FolioReal': folio_real,
            'NumeroInterior': numero_interior,
        })
        

class CesionDerechosInmueblesType(ScalarMap):
    """
    
    :param figura_cliente:
    :param tipo_cesion:
    :param datos_contraparte:
    :param caracteristicas_inmueble:
    """
    
    def __init__(
            self,
            figura_cliente: str,
            tipo_cesion: str,
            datos_contraparte: DatosContraparteType | dict | Sequence[DatosContraparteType | dict],
            caracteristicas_inmueble: CaracteristicasInmueble2Type | dict | Sequence[CaracteristicasInmueble2Type | dict],
    ): 
        super().__init__({
            'FiguraCliente': figura_cliente,
            'TipoCesion': tipo_cesion,
            'DatosContraparte': datos_contraparte,
            'CaracteristicasInmueble': caracteristicas_inmueble,
        })
        

class ContratoType(ScalarMap):
    """
    
    :param fecha_contrato:
    :param valor_referencia:
    """
    
    def __init__(
            self,
            fecha_contrato: date,
            valor_referencia: str,
    ): 
        super().__init__({
            'FechaContrato': fecha_contrato,
            'ValorReferencia': valor_referencia,
        })
        

class DatosInstrumentoType(ScalarMap):
    """
    
    :param numero_instrumento_publico:
    :param fecha_instrumento_publico:
    :param notario_instrumento_publico:
    :param entidad_instrumento_publico:
    :param valor_referencia:
    """
    
    def __init__(
            self,
            numero_instrumento_publico: str,
            fecha_instrumento_publico: date,
            notario_instrumento_publico: str,
            entidad_instrumento_publico: int,
            valor_referencia: str,
    ): 
        super().__init__({
            'NumeroInstrumentoPublico': numero_instrumento_publico,
            'FechaInstrumentoPublico': fecha_instrumento_publico,
            'NotarioInstrumentoPublico': notario_instrumento_publico,
            'EntidadInstrumentoPublico': entidad_instrumento_publico,
            'ValorReferencia': valor_referencia,
        })
        

class ContratoInstrumentoType(ScalarMap):
    """
    
    :param datos_instrumento_publico:
    :param contrato:
    """
    
    def __init__(
            self,
            datos_instrumento_publico: DatosInstrumentoType | dict = None,
            contrato: ContratoType | dict = None,
    ): 
        super().__init__({
            'DatosInstrumentoPublico': datos_instrumento_publico,
            'Contrato': contrato,
        })
        

class CaracteristicasInmueble1Type(ScalarMap):
    """
    
    :param tipo_inmueble:
    :param colonia:
    :param calle:
    :param numero_exterior:
    :param codigo_postal:
    :param dimension_terreno:
    :param dimension_construido:
    :param folio_real:
    :param contrato_instrumento_publico:
    :param numero_interior:
    """
    
    def __init__(
            self,
            tipo_inmueble: str,
            colonia: str,
            calle: str,
            numero_exterior: str,
            codigo_postal: str,
            dimension_terreno: str,
            dimension_construido: str,
            folio_real: str,
            contrato_instrumento_publico: ContratoInstrumentoType | dict,
            numero_interior: str = None,
    ): 
        super().__init__({
            'TipoInmueble': tipo_inmueble,
            'Colonia': colonia,
            'Calle': calle,
            'NumeroExterior': numero_exterior,
            'CodigoPostal': codigo_postal,
            'DimensionTerreno': dimension_terreno,
            'DimensionConstruido': dimension_construido,
            'FolioReal': folio_real,
            'ContratoInstrumentoPublico': contrato_instrumento_publico,
            'NumeroInterior': numero_interior,
        })
        

class PersonaMoralT1Type(ScalarMap):
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
        

class PersonaFisicaT1Type(ScalarMap):
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
        

class TipoPersonaT1Type(ScalarMap):
    """
    
    :param persona_fisica:
    :param persona_moral:
    :param fideicomiso:
    """
    
    def __init__(
            self,
            persona_fisica: PersonaFisicaT1Type | dict = None,
            persona_moral: PersonaMoralT1Type | dict = None,
            fideicomiso: FideicomisoSimpleType | dict = None,
    ): 
        super().__init__({
            'PersonaFisica': persona_fisica,
            'PersonaMoral': persona_moral,
            'Fideicomiso': fideicomiso,
        })
        

class DatosContraparteType(ScalarMap):
    """
    
    :param tipo_persona:
    """
    
    def __init__(
            self,
            tipo_persona: TipoPersonaT1Type | dict,
    ): 
        super().__init__({
            'TipoPersona': tipo_persona,
        })
        

class CompraVentaInmueblesType(ScalarMap):
    """
    
    :param tipo_operacion:
    :param valor_pactado:
    :param datos_contraparte:
    :param caracteristicas_inmueble:
    """
    
    def __init__(
            self,
            tipo_operacion: str,
            valor_pactado: str,
            datos_contraparte: DatosContraparteType | dict | Sequence[DatosContraparteType | dict],
            caracteristicas_inmueble: CaracteristicasInmueble1Type | dict | Sequence[CaracteristicasInmueble1Type | dict],
    ): 
        super().__init__({
            'TipoOperacion': tipo_operacion,
            'ValorPactado': valor_pactado,
            'DatosContraparte': datos_contraparte,
            'CaracteristicasInmueble': caracteristicas_inmueble,
        })
        

class TipoActividadType(ScalarMap):
    """
    
    :param compra_venta_inmuebles:
    :param cesion_derechos_inmuebles:
    :param administracion_recursos:
    :param constitucion_sociedades_mercantiles:
    :param organizacion_aportaciones:
    :param fusion:
    :param escision:
    :param administracion_personas_morales:
    :param constitucion_fideicomiso:
    :param compra_venta_entidades_mercantiles:
    """
    
    def __init__(
            self,
            compra_venta_inmuebles: CompraVentaInmueblesType | dict = None,
            cesion_derechos_inmuebles: CesionDerechosInmueblesType | dict = None,
            administracion_recursos: AdministracionRecursosType | dict = None,
            constitucion_sociedades_mercantiles: ConstitucionSociedadesMercantilesType | dict = None,
            organizacion_aportaciones: OrganizacionAportacionesType | dict = None,
            fusion: FusionType | dict = None,
            escision: EscisionType | dict = None,
            administracion_personas_morales: AdmonPersonasMoralesType | dict = None,
            constitucion_fideicomiso: ConstitucionFideicomisoType | dict = None,
            compra_venta_entidades_mercantiles: CompraVentaEntidadesMercantilesType | dict = None,
    ): 
        super().__init__({
            'CompraVentaInmuebles': compra_venta_inmuebles,
            'CesionDerechosInmuebles': cesion_derechos_inmuebles,
            'AdministracionRecursos': administracion_recursos,
            'ConstitucionSociedadesMercantiles': constitucion_sociedades_mercantiles,
            'OrganizacionAportaciones': organizacion_aportaciones,
            'Fusion': fusion,
            'Escision': escision,
            'AdministracionPersonasMorales': administracion_personas_morales,
            'ConstitucionFideicomiso': constitucion_fideicomiso,
            'CompraVentaEntidadesMercantiles': compra_venta_entidades_mercantiles,
        })
        

class DatosOperacionType(ScalarMap):
    """
    
    :param fecha_operacion:
    :param tipo_actividad:
    :param datos_operacion_financiera:
    """
    
    def __init__(
            self,
            fecha_operacion: date,
            tipo_actividad: TipoActividadType | dict,
            datos_operacion_financiera: DatosOperacionFinancieraType | dict | Sequence[DatosOperacionFinancieraType | dict],
    ): 
        super().__init__({
            'FechaOperacion': fecha_operacion,
            'TipoActividad': tipo_actividad,
            'DatosOperacionFinanciera': datos_operacion_financiera,
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
        

class FideicomisoSimpleType(ScalarMap):
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
        

class PersonaMoralSimpleType(ScalarMap):
    """
    
    :param denominacion_razon:
    :param fecha_constitucion:
    :param rfc:
    :param pais_nacionalidad:
    """
    
    def __init__(
            self,
            denominacion_razon: str,
            fecha_constitucion: date = None,
            rfc: str = None,
            pais_nacionalidad: str = None,
    ): 
        super().__init__({
            'DenominacionRazon': denominacion_razon,
            'FechaConstitucion': fecha_constitucion,
            'Rfc': rfc,
            'PaisNacionalidad': pais_nacionalidad,
        })
        

class PersonaFisicaSimpleType(ScalarMap):
    """
    
    :param nombre:
    :param apellido_paterno:
    :param apellido_materno:
    :param fecha_nacimiento:
    :param rfc:
    :param curp:
    :param pais_nacionalidad:
    """
    
    def __init__(
            self,
            nombre: str,
            apellido_paterno: str,
            apellido_materno: str,
            fecha_nacimiento: date = None,
            rfc: str = None,
            curp: str = None,
            pais_nacionalidad: str = None,
    ): 
        super().__init__({
            'Nombre': nombre,
            'ApellidoPaterno': apellido_paterno,
            'ApellidoMaterno': apellido_materno,
            'FechaNacimiento': fecha_nacimiento,
            'Rfc': rfc,
            'Curp': curp,
            'PaisNacionalidad': pais_nacionalidad,
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
            fideicomiso: FideicomisoSimpleType | dict = None,
    ): 
        super().__init__({
            'PersonaFisica': persona_fisica,
            'PersonaMoral': persona_moral,
            'Fideicomiso': fideicomiso,
        })
        

class DuenoBeneficiarioType(ScalarMap):
    """
    
    :param tipo_persona:
    """
    
    def __init__(
            self,
            tipo_persona: TipoPersonaSimpleType | dict,
    ): 
        super().__init__({
            'TipoPersona': tipo_persona,
        })
        

class TelefonoType(ScalarMap):
    """
    
    :param clave_pais:
    :param numero_telefono:
    :param correo_electronico:
    """
    
    def __init__(
            self,
            clave_pais: str = None,
            numero_telefono: str = None,
            correo_electronico: str = None,
    ): 
        super().__init__({
            'ClavePais': clave_pais,
            'NumeroTelefono': numero_telefono,
            'CorreoElectronico': correo_electronico,
        })
        

class ExtranjeroType(ScalarMap):
    """
    
    :param pais:
    :param estado_provincia:
    :param ciudad_poblacion:
    :param colonia:
    :param calle:
    :param numero_exterior:
    :param codigo_postal:
    :param numero_interior:
    """
    
    def __init__(
            self,
            pais: str,
            estado_provincia: str,
            ciudad_poblacion: str,
            colonia: str,
            calle: str,
            numero_exterior: str,
            codigo_postal: str,
            numero_interior: str = None,
    ): 
        super().__init__({
            'Pais': pais,
            'EstadoProvincia': estado_provincia,
            'CiudadPoblacion': ciudad_poblacion,
            'Colonia': colonia,
            'Calle': calle,
            'NumeroExterior': numero_exterior,
            'CodigoPostal': codigo_postal,
            'NumeroInterior': numero_interior,
        })
        

class NacionalType(ScalarMap):
    """
    
    :param colonia:
    :param calle:
    :param numero_exterior:
    :param codigo_postal:
    :param numero_interior:
    """
    
    def __init__(
            self,
            colonia: str,
            calle: str,
            numero_exterior: str,
            codigo_postal: str,
            numero_interior: str = None,
    ): 
        super().__init__({
            'Colonia': colonia,
            'Calle': calle,
            'NumeroExterior': numero_exterior,
            'CodigoPostal': codigo_postal,
            'NumeroInterior': numero_interior,
        })
        

class TipoDomicilioType(ScalarMap):
    """
    
    :param nacional:
    :param extranjero:
    """
    
    def __init__(
            self,
            nacional: NacionalType | dict = None,
            extranjero: ExtranjeroType | dict = None,
    ): 
        super().__init__({
            'Nacional': nacional,
            'Extranjero': extranjero,
        })
        

class RepresentanteApoderadoType(ScalarMap):
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
        

class FideicomisoType(ScalarMap):
    """
    
    :param denominacion_razon:
    :param apoderado_delegado:
    :param rfc:
    :param identificador_fideicomiso:
    """
    
    def __init__(
            self,
            denominacion_razon: str,
            apoderado_delegado: RepresentanteApoderadoType | dict | Sequence[RepresentanteApoderadoType | dict],
            rfc: str = None,
            identificador_fideicomiso: str = None,
    ): 
        super().__init__({
            'DenominacionRazon': denominacion_razon,
            'ApoderadoDelegado': apoderado_delegado,
            'Rfc': rfc,
            'IdentificadorFideicomiso': identificador_fideicomiso,
        })
        

class PersonaMoralType(ScalarMap):
    """
    
    :param denominacion_razon:
    :param pais_nacionalidad:
    :param giro_mercantil:
    :param representante_apoderado:
    :param fecha_constitucion:
    :param rfc:
    """
    
    def __init__(
            self,
            denominacion_razon: str,
            pais_nacionalidad: str,
            giro_mercantil: str,
            representante_apoderado: RepresentanteApoderadoType | dict | Sequence[RepresentanteApoderadoType | dict],
            fecha_constitucion: date = None,
            rfc: str = None,
    ): 
        super().__init__({
            'DenominacionRazon': denominacion_razon,
            'PaisNacionalidad': pais_nacionalidad,
            'GiroMercantil': giro_mercantil,
            'RepresentanteApoderado': representante_apoderado,
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
    :param representante_apoderado:
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
            representante_apoderado: RepresentanteApoderadoType | dict | Sequence[RepresentanteApoderadoType | dict] = None,
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
            'RepresentanteApoderado': representante_apoderado,
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
        

class PersonaAvisoType(ScalarMap):
    """
    
    :param tipo_persona:
    :param tipo_domicilio:
    :param telefono:
    """
    
    def __init__(
            self,
            tipo_persona: TipoPersonaType | dict,
            tipo_domicilio: TipoDomicilioType | dict = None,
            telefono: TelefonoType | dict = None,
    ): 
        super().__init__({
            'TipoPersona': tipo_persona,
            'TipoDomicilio': tipo_domicilio,
            'Telefono': telefono,
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
    :param dueno_beneficiario:
    """
    
    def __init__(
            self,
            referencia_aviso: str,
            prioridad: str,
            alerta: AlertaType | dict,
            persona_aviso: PersonaAvisoType | dict | Sequence[PersonaAvisoType | dict],
            detalle_operaciones: DetalleOperacionesType | dict,
            modificatorio: ModificatorioType | dict = None,
            dueno_beneficiario: DuenoBeneficiarioType | dict | Sequence[DuenoBeneficiarioType | dict] = None,
    ): 
        super().__init__({
            'ReferenciaAviso': referencia_aviso,
            'Prioridad': prioridad,
            'Alerta': alerta,
            'PersonaAviso': persona_aviso,
            'DetalleOperaciones': detalle_operaciones,
            'Modificatorio': modificatorio,
            'DuenoBeneficiario': dueno_beneficiario,
        })
        

class OcupacionType(ScalarMap):
    """
    
    :param tipo_ocupacion:
    :param descripcion_otra_ocupacion:
    """
    
    def __init__(
            self,
            tipo_ocupacion: int,
            descripcion_otra_ocupacion: str = None,
    ): 
        super().__init__({
            'TipoOcupacion': tipo_ocupacion,
            'DescripcionOtraOcupacion': descripcion_otra_ocupacion,
        })
        

class SujetoObligadoType(ScalarMap):
    """
    
    :param clave_sujeto_obligado:
    :param clave_actividad:
    :param clave_entidad_colegiada:
    :param ocupacion:
    :param exento:
    """
    
    def __init__(
            self,
            clave_sujeto_obligado: str,
            clave_actividad: str,
            clave_entidad_colegiada: str = None,
            ocupacion: OcupacionType | dict = None,
            exento: str = None,
    ): 
        super().__init__({
            'ClaveSujetoObligado': clave_sujeto_obligado,
            'ClaveActividad': clave_actividad,
            'ClaveEntidadColegiada': clave_entidad_colegiada,
            'Ocupacion': ocupacion,
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
        

class Archivo(ArchivoType, XElement):
    tag = '{http://www.uif.shcp.gob.mx/recepcion/spr}archivo'

