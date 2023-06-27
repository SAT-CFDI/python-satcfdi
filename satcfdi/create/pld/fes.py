"""fes http://www.uif.shcp.gob.mx/recepcion/fes"""
from decimal import Decimal
from datetime import datetime, date, time
from collections.abc import Sequence
from ...cfdi import CFDI
from ...xelement import XElement
from ...utils import ScalarMap


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
        

class TribunalType(ScalarMap):
    """
    
    :param clave_tribunal_dependencia:
    :param clave_actividad:
    """
    
    def __init__(
            self,
            clave_tribunal_dependencia: str,
            clave_actividad: str,
    ): 
        super().__init__({
            'ClaveTribunalDependencia': clave_tribunal_dependencia,
            'ClaveActividad': clave_actividad,
        })
        

class PropietarioType(ScalarMap):
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
        

class DatosPropietarioType(ScalarMap):
    """
    
    :param propietario_solicita:
    :param dato_propietario:
    """
    
    def __init__(
            self,
            propietario_solicita: str,
            dato_propietario: PropietarioType | dict | Sequence[PropietarioType | dict] = None,
    ): 
        super().__init__({
            'PropietarioSolicita': propietario_solicita,
            'DatoPropietario': dato_propietario,
        })
        

class DatosLiquidacionType(ScalarMap):
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
        

class DatosGarantiaType(ScalarMap):
    """
    
    :param tipo_garantia:
    :param datos_bien_garantia:
    :param tipo_persona:
    """
    
    def __init__(
            self,
            tipo_garantia: str,
            datos_bien_garantia: BienGarantiaType | dict = None,
            tipo_persona: TipoGaranteType | dict = None,
    ): 
        super().__init__({
            'TipoGarantia': tipo_garantia,
            'DatosBienGarantia': datos_bien_garantia,
            'TipoPersona': tipo_persona,
        })
        

class BienGarantiaType(ScalarMap):
    """
    
    :param datos_inmueble:
    :param datos_otro:
    """
    
    def __init__(
            self,
            datos_inmueble: GarantiaInmuebleType | dict = None,
            datos_otro: GarantiaOtroType | dict = None,
    ): 
        super().__init__({
            'DatosInmueble': datos_inmueble,
            'DatosOtro': datos_otro,
        })
        

class GarantiaOtroType(ScalarMap):
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
        

class GarantiaInmuebleType(ScalarMap):
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
        

class TipoGaranteType(ScalarMap):
    """
    
    :param persona_fisica:
    :param persona_moral:
    :param fideicomiso:
    """
    
    def __init__(
            self,
            persona_fisica: GaranteFisicaType | dict = None,
            persona_moral: GaranteMoralType | dict = None,
            fideicomiso: GaranteFideicomisoType | dict = None,
    ): 
        super().__init__({
            'PersonaFisica': persona_fisica,
            'PersonaMoral': persona_moral,
            'Fideicomiso': fideicomiso,
        })
        

class GaranteFideicomisoType(ScalarMap):
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
        

class GaranteMoralType(ScalarMap):
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
        

class GaranteFisicaType(ScalarMap):
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
        

class DatosDeudorType(ScalarMap):
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
        

class DatosAcreedorType(ScalarMap):
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
        

class PersonaMoralConstType(ScalarMap):
    """
    
    :param tipo_persona_moral:
    :param denominacion_razon:
    :param giro_mercantil:
    :param numero_total_acciones:
    :param consejo_vigilancia:
    :param motivo_constitucion:
    :param datos_accionista:
    :param capital_social:
    :param tipo_persona_moral_otra:
    :param folio_mercantil:
    :param entidad_federativa:
    :param instrumento_publico:
    """
    
    def __init__(
            self,
            tipo_persona_moral: str,
            denominacion_razon: str,
            giro_mercantil: str,
            numero_total_acciones: str,
            consejo_vigilancia: str,
            motivo_constitucion: str,
            datos_accionista: DatosAccionistaType | dict | Sequence[DatosAccionistaType | dict],
            capital_social: CapitalSocialType | dict,
            tipo_persona_moral_otra: str = None,
            folio_mercantil: str = None,
            entidad_federativa: str = None,
            instrumento_publico: str = None,
    ): 
        super().__init__({
            'TipoPersonaMoral': tipo_persona_moral,
            'DenominacionRazon': denominacion_razon,
            'GiroMercantil': giro_mercantil,
            'NumeroTotalAcciones': numero_total_acciones,
            'ConsejoVigilancia': consejo_vigilancia,
            'MotivoConstitucion': motivo_constitucion,
            'DatosAccionista': datos_accionista,
            'CapitalSocial': capital_social,
            'TipoPersonaMoralOtra': tipo_persona_moral_otra,
            'FolioMercantil': folio_mercantil,
            'EntidadFederativa': entidad_federativa,
            'InstrumentoPublico': instrumento_publico,
        })
        

class Autoridad1Type(ScalarMap):
    """
    
    :param tipo_autoridad:
    :param domicilio_oficina:
    """
    
    def __init__(
            self,
            tipo_autoridad: TipoAutoridad1Type | dict,
            domicilio_oficina: DomicilioOficinaType | dict = None,
    ): 
        super().__init__({
            'TipoAutoridad': tipo_autoridad,
            'DomicilioOficina': domicilio_oficina,
        })
        

class TipoAutoridad1Type(ScalarMap):
    """
    
    :param administrativo:
    :param jurisdiccional:
    """
    
    def __init__(
            self,
            administrativo: Administrativo1Type | dict = None,
            jurisdiccional: JurisdiccionalType | dict = None,
    ): 
        super().__init__({
            'Administrativo': administrativo,
            'Jurisdiccional': jurisdiccional,
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
            tipo_persona: TipoPersonaSimpleType | dict,
    ): 
        super().__init__({
            'TipoPersona': tipo_persona,
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
        

class AutoridadType(ScalarMap):
    """
    
    :param tipo_autoridad:
    :param domicilio_oficina:
    """
    
    def __init__(
            self,
            tipo_autoridad: TipoAutoridadType | dict,
            domicilio_oficina: DomicilioOficinaType | dict = None,
    ): 
        super().__init__({
            'TipoAutoridad': tipo_autoridad,
            'DomicilioOficina': domicilio_oficina,
        })
        

class DomicilioOficinaType(ScalarMap):
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
        

class TipoAutoridadType(ScalarMap):
    """
    
    :param administrativo:
    :param jurisdiccional:
    """
    
    def __init__(
            self,
            administrativo: AdministrativoType | dict = None,
            jurisdiccional: JurisdiccionalType | dict = None,
    ): 
        super().__init__({
            'Administrativo': administrativo,
            'Jurisdiccional': jurisdiccional,
        })
        

class JurisdiccionalType(ScalarMap):
    """
    
    :param organo:
    :param tipo_juicio:
    :param materia:
    :param expediente:
    """
    
    def __init__(
            self,
            organo: str,
            tipo_juicio: str,
            materia: str,
            expediente: str,
    ): 
        super().__init__({
            'Organo': organo,
            'TipoJuicio': tipo_juicio,
            'Materia': materia,
            'Expediente': expediente,
        })
        

class AdministrativoType(ScalarMap):
    """
    
    :param organo:
    :param cargo:
    :param instrumento_publico:
    """
    
    def __init__(
            self,
            organo: str,
            cargo: str,
            instrumento_publico: str,
    ): 
        super().__init__({
            'Organo': organo,
            'Cargo': cargo,
            'InstrumentoPublico': instrumento_publico,
        })
        

class TelefonoType(ScalarMap):
    """
    
    :param numero_telefono:
    :param clave_pais:
    :param correo_electronico:
    """
    
    def __init__(
            self,
            numero_telefono: str,
            clave_pais: str = None,
            correo_electronico: str = None,
    ): 
        super().__init__({
            'NumeroTelefono': numero_telefono,
            'ClavePais': clave_pais,
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
        

class DatosPersonaActoType(ScalarMap):
    """
    
    :param caracter:
    :param tipo_persona:
    :param caracter_otro:
    :param tipo_domicilio:
    :param telefono:
    """
    
    def __init__(
            self,
            caracter: str,
            tipo_persona: TipoPersonaType | dict,
            caracter_otro: str = None,
            tipo_domicilio: TipoDomicilioType | dict = None,
            telefono: TelefonoType | dict = None,
    ): 
        super().__init__({
            'Caracter': caracter,
            'TipoPersona': tipo_persona,
            'CaracterOtro': caracter_otro,
            'TipoDomicilio': tipo_domicilio,
            'Telefono': telefono,
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
            apoderado_delegado: RepresentanteApoderadoType | dict,
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
    :param representante_apoderado:
    :param fecha_constitucion:
    :param rfc:
    """
    
    def __init__(
            self,
            denominacion_razon: str,
            pais_nacionalidad: str,
            representante_apoderado: RepresentanteApoderadoType | dict,
            fecha_constitucion: date = None,
            rfc: str = None,
    ): 
        super().__init__({
            'DenominacionRazon': denominacion_razon,
            'PaisNacionalidad': pais_nacionalidad,
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
        

class PersonasActoType(ScalarMap):
    """
    
    :param datos_persona_acto:
    """
    
    def __init__(
            self,
            datos_persona_acto: DatosPersonaActoType | dict | Sequence[DatosPersonaActoType | dict],
    ): 
        super().__init__({
            'DatosPersonaActo': datos_persona_acto,
        })
        

class InmuebleType(ScalarMap):
    """
    
    :param tipo_inmueble:
    :param valor_catastral:
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
            valor_catastral: str,
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
            'ValorCatastral': valor_catastral,
            'Colonia': colonia,
            'Calle': calle,
            'NumeroExterior': numero_exterior,
            'CodigoPostal': codigo_postal,
            'DimensionTerreno': dimension_terreno,
            'DimensionConstruido': dimension_construido,
            'FolioReal': folio_real,
            'NumeroInterior': numero_interior,
        })
        

class DatosInmueblesType(ScalarMap):
    """
    
    :param caracteristicas_inmueble:
    """
    
    def __init__(
            self,
            caracteristicas_inmueble: InmuebleType | dict | Sequence[InmuebleType | dict],
    ): 
        super().__init__({
            'CaracteristicasInmueble': caracteristicas_inmueble,
        })
        

class AvaluoType(ScalarMap):
    """
    
    :param organo:
    :param cargo:
    :param expediente_oficio:
    :param persona_solicita:
    :param tipo_bien:
    :param valor_avaluo:
    :param datos_propietario:
    :param descripcion:
    """
    
    def __init__(
            self,
            organo: str,
            cargo: str,
            expediente_oficio: str,
            persona_solicita: PersonaFisicaType | dict,
            tipo_bien: str,
            valor_avaluo: str,
            datos_propietario: DatosPropietarioType | dict,
            descripcion: str = None,
    ): 
        super().__init__({
            'Organo': organo,
            'Cargo': cargo,
            'ExpedienteOficio': expediente_oficio,
            'PersonaSolicita': persona_solicita,
            'TipoBien': tipo_bien,
            'ValorAvaluo': valor_avaluo,
            'DatosPropietario': datos_propietario,
            'Descripcion': descripcion,
        })
        

class ContratoMutuoType(ScalarMap):
    """
    
    :param autoridad:
    :param tipo_otorgamiento:
    :param persona_solicita:
    :param datos_acreedor:
    :param datos_deudor:
    :param datos_liquidacion:
    :param datos_garantia:
    """
    
    def __init__(
            self,
            autoridad: AutoridadType | dict,
            tipo_otorgamiento: str,
            persona_solicita: PersonaFisicaSimpleType | dict,
            datos_acreedor: DatosAcreedorType | dict | Sequence[DatosAcreedorType | dict],
            datos_deudor: DatosDeudorType | dict | Sequence[DatosDeudorType | dict],
            datos_liquidacion: DatosLiquidacionType | dict | Sequence[DatosLiquidacionType | dict],
            datos_garantia: DatosGarantiaType | dict | Sequence[DatosGarantiaType | dict] = None,
    ): 
        super().__init__({
            'Autoridad': autoridad,
            'TipoOtorgamiento': tipo_otorgamiento,
            'PersonaSolicita': persona_solicita,
            'DatosAcreedor': datos_acreedor,
            'DatosDeudor': datos_deudor,
            'DatosLiquidacion': datos_liquidacion,
            'DatosGarantia': datos_garantia,
        })
        

class ModificacionPatrimonialType(ScalarMap):
    """
    
    :param autoridad:
    :param persona_moral_modifica:
    :param datos_modificacion:
    """
    
    def __init__(
            self,
            autoridad: Autoridad1Type | dict,
            persona_moral_modifica: PersonaMoralModificaType | dict,
            datos_modificacion: DatosModificacionType | dict,
    ): 
        super().__init__({
            'Autoridad': autoridad,
            'PersonaMoralModifica': persona_moral_modifica,
            'DatosModificacion': datos_modificacion,
        })
        

class ConstitucionPmType(ScalarMap):
    """
    
    :param autoridad:
    :param persona_solicita:
    :param persona_moral_constitucion:
    """
    
    def __init__(
            self,
            autoridad: Autoridad1Type | dict,
            persona_solicita: PersonaFisicaType | dict,
            persona_moral_constitucion: PersonaMoralConstType | dict,
    ): 
        super().__init__({
            'Autoridad': autoridad,
            'PersonaSolicita': persona_solicita,
            'PersonaMoralConstitucion': persona_moral_constitucion,
        })
        

class OtorgamientoPoderType(ScalarMap):
    """
    
    :param autoridad:
    :param persona_solicita:
    :param datos_poderdante:
    :param datos_apoderado:
    """
    
    def __init__(
            self,
            autoridad: AutoridadType | dict,
            persona_solicita: PersonaFisicaType | dict,
            datos_poderdante: DatosPoderdanteType | dict | Sequence[DatosPoderdanteType | dict],
            datos_apoderado: DatosApoderadoType | dict | Sequence[DatosApoderadoType | dict],
    ): 
        super().__init__({
            'Autoridad': autoridad,
            'PersonaSolicita': persona_solicita,
            'DatosPoderdante': datos_poderdante,
            'DatosApoderado': datos_apoderado,
        })
        

class DerechosInmuebleType(ScalarMap):
    """
    
    :param organo:
    :param tipo_juicio:
    :param materia:
    :param expediente:
    :param tipo_acto:
    :param datos_inmuebles:
    :param personas_acto:
    :param tipo_acto_otro:
    """
    
    def __init__(
            self,
            organo: str,
            tipo_juicio: str,
            materia: str,
            expediente: str,
            tipo_acto: str,
            datos_inmuebles: DatosInmueblesType | dict,
            personas_acto: PersonasActoType | dict,
            tipo_acto_otro: str = None,
    ): 
        super().__init__({
            'Organo': organo,
            'TipoJuicio': tipo_juicio,
            'Materia': materia,
            'Expediente': expediente,
            'TipoActo': tipo_acto,
            'DatosInmuebles': datos_inmuebles,
            'PersonasActo': personas_acto,
            'TipoActoOtro': tipo_acto_otro,
        })
        

class ActividadType(ScalarMap):
    """
    
    :param derechos_inmuebles:
    :param otorgamiento_poder:
    :param constitucion_personas_morales:
    :param modificacion_patrimonial:
    :param contrato_mutuo_credito:
    :param avaluo:
    """
    
    def __init__(
            self,
            derechos_inmuebles: DerechosInmuebleType | dict = None,
            otorgamiento_poder: OtorgamientoPoderType | dict = None,
            constitucion_personas_morales: ConstitucionPmType | dict = None,
            modificacion_patrimonial: ModificacionPatrimonialType | dict = None,
            contrato_mutuo_credito: ContratoMutuoType | dict = None,
            avaluo: AvaluoType | dict = None,
    ): 
        super().__init__({
            'DerechosInmuebles': derechos_inmuebles,
            'OtorgamientoPoder': otorgamiento_poder,
            'ConstitucionPersonasMorales': constitucion_personas_morales,
            'ModificacionPatrimonial': modificacion_patrimonial,
            'ContratoMutuoCredito': contrato_mutuo_credito,
            'Avaluo': avaluo,
        })
        

class AvisoType(ScalarMap):
    """
    
    :param referencia_aviso:
    :param prioridad:
    :param alerta:
    :param detalle_operaciones:
    :param modificatorio:
    """
    
    def __init__(
            self,
            referencia_aviso: str,
            prioridad: str,
            alerta: AlertaType | dict,
            detalle_operaciones: OperacionesType | dict,
            modificatorio: ModificatorioType | dict = None,
    ): 
        super().__init__({
            'ReferenciaAviso': referencia_aviso,
            'Prioridad': prioridad,
            'Alerta': alerta,
            'DetalleOperaciones': detalle_operaciones,
            'Modificatorio': modificatorio,
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
        

class OperacionType(ScalarMap):
    """
    
    :param fecha_operacion:
    :param tipo_actividad:
    """
    
    def __init__(
            self,
            fecha_operacion: date,
            tipo_actividad: ActividadType | dict,
    ): 
        super().__init__({
            'FechaOperacion': fecha_operacion,
            'TipoActividad': tipo_actividad,
        })
        

class OperacionesType(ScalarMap):
    """
    
    :param datos_operacion:
    """
    
    def __init__(
            self,
            datos_operacion: OperacionType | dict | Sequence[OperacionType | dict],
    ): 
        super().__init__({
            'DatosOperacion': datos_operacion,
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
        

class InformeType(ScalarMap):
    """
    
    :param mes_reportado:
    :param tribunal_dependencia:
    :param aviso:
    :param version:
    """
    
    def __init__(
            self,
            mes_reportado: str,
            tribunal_dependencia: TribunalType | dict,
            aviso: AvisoType | dict | Sequence[AvisoType | dict] = None,
            version: str = None,
    ): 
        super().__init__({
            'MesReportado': mes_reportado,
            'TribunalDependencia': tribunal_dependencia,
            'Aviso': aviso,
            'Version': version,
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
        

class Administrativo1Type(ScalarMap):
    """
    
    :param organo:
    :param cargo:
    :param instrumento_publico_oficio:
    """
    
    def __init__(
            self,
            organo: str,
            cargo: str,
            instrumento_publico_oficio: str,
    ): 
        super().__init__({
            'Organo': organo,
            'Cargo': cargo,
            'InstrumentoPublicoOficio': instrumento_publico_oficio,
        })
        

class Archivo(ArchivoType, XElement):
    tag = '{http://www.uif.shcp.gob.mx/recepcion/fes}archivo'

