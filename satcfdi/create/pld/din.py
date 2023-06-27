"""din http://www.uif.shcp.gob.mx/recepcion/din"""
from decimal import Decimal
from datetime import datetime, date, time
from collections.abc import Sequence
from ...cfdi import CFDI
from ...xelement import XElement
from ...utils import ScalarMap


class FinanciamientoBursatilType(ScalarMap):
    """
    
    :param fecha_emision:
    :param monto_solicitado:
    :param monto_recibido:
    """
    
    def __init__(
            self,
            fecha_emision: date = None,
            monto_solicitado: str = None,
            monto_recibido: str = None,
    ): 
        super().__init__({
            'FechaEmision': fecha_emision,
            'MontoSolicitado': monto_solicitado,
            'MontoRecibido': monto_recibido,
        })
        

class DetalleAcreedoresType(ScalarMap):
    """
    
    :param tipo_persona_acreedor:
    """
    
    def __init__(
            self,
            tipo_persona_acreedor: TipoPersonaType | dict | Sequence[TipoPersonaType | dict] = None,
    ): 
        super().__init__({
            'TipoPersonaAcreedor': tipo_persona_acreedor,
        })
        

class DatosPrestamoNoFinType(ScalarMap):
    """
    
    :param detalle_acreedores:
    :param monto_prestamo:
    :param moneda:
    :param plazo_meses:
    """
    
    def __init__(
            self,
            detalle_acreedores: DetalleAcreedoresType | dict,
            monto_prestamo: str = None,
            moneda: str = None,
            plazo_meses: str = None,
    ): 
        super().__init__({
            'DetalleAcreedores': detalle_acreedores,
            'MontoPrestamo': monto_prestamo,
            'Moneda': moneda,
            'PlazoMeses': plazo_meses,
        })
        

class PrestamoNoFinancieroType(ScalarMap):
    """
    
    :param datos_prestamo:
    """
    
    def __init__(
            self,
            datos_prestamo: DatosPrestamoNoFinType | dict | Sequence[DatosPrestamoNoFinType | dict] = None,
    ): 
        super().__init__({
            'DatosPrestamo': datos_prestamo,
        })
        

class DatosPrestamoType(ScalarMap):
    """
    
    :param tipo_institucion:
    :param institucion:
    :param tipo_credito:
    :param monto_prestamo:
    :param moneda:
    :param plazo_meses:
    """
    
    def __init__(
            self,
            tipo_institucion: str = None,
            institucion: str = None,
            tipo_credito: str = None,
            monto_prestamo: str = None,
            moneda: str = None,
            plazo_meses: str = None,
    ): 
        super().__init__({
            'TipoInstitucion': tipo_institucion,
            'Institucion': institucion,
            'TipoCredito': tipo_credito,
            'MontoPrestamo': monto_prestamo,
            'Moneda': moneda,
            'PlazoMeses': plazo_meses,
        })
        

class PrestamoFinancieroType(ScalarMap):
    """
    
    :param datos_prestamo:
    """
    
    def __init__(
            self,
            datos_prestamo: DatosPrestamoType | dict | Sequence[DatosPrestamoType | dict] = None,
    ): 
        super().__init__({
            'DatosPrestamo': datos_prestamo,
        })
        

class AportacionNumerarioTercerosType(ScalarMap):
    """
    
    :param instrumento_monetario:
    :param moneda:
    :param monto_aportacion:
    :param aportacion_fideicomiso:
    :param nombre_institucion:
    :param valor_inmueble_preventa:
    """
    
    def __init__(
            self,
            instrumento_monetario: str = None,
            moneda: str = None,
            monto_aportacion: str = None,
            aportacion_fideicomiso: str = None,
            nombre_institucion: str = None,
            valor_inmueble_preventa: str = None,
    ): 
        super().__init__({
            'InstrumentoMonetario': instrumento_monetario,
            'Moneda': moneda,
            'MontoAportacion': monto_aportacion,
            'AportacionFideicomiso': aportacion_fideicomiso,
            'NombreInstitucion': nombre_institucion,
            'ValorInmueblePreventa': valor_inmueble_preventa,
        })
        

class DatosAportacionTercerosType(ScalarMap):
    """
    
    :param aportacion_numerario:
    :param aportacion_especie:
    """
    
    def __init__(
            self,
            aportacion_numerario: AportacionNumerarioTercerosType | dict = None,
            aportacion_especie: AportacionEspecieType | dict = None,
    ): 
        super().__init__({
            'AportacionNumerario': aportacion_numerario,
            'AportacionEspecie': aportacion_especie,
        })
        

class TercerosAportacionType(ScalarMap):
    """
    
    :param datos_aportacion:
    """
    
    def __init__(
            self,
            datos_aportacion: DatosAportacionTercerosType | dict,
    ): 
        super().__init__({
            'DatosAportacion': datos_aportacion,
        })
        

class FideicomisoType(ScalarMap):
    """
    
    :param denominacion_razon:
    :param rfc:
    :param identificador_fideicomiso:
    """
    
    def __init__(
            self,
            denominacion_razon: str = None,
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
    
    :param representante_apoderado:
    :param denominacion_razon:
    :param fecha_constitucion:
    :param rfc:
    :param pais_nacionalidad:
    :param giro_mercantil:
    """
    
    def __init__(
            self,
            representante_apoderado: RepresentanteApoderadoType | dict,
            denominacion_razon: str = None,
            fecha_constitucion: date = None,
            rfc: str = None,
            pais_nacionalidad: str = None,
            giro_mercantil: str = None,
    ): 
        super().__init__({
            'RepresentanteApoderado': representante_apoderado,
            'DenominacionRazon': denominacion_razon,
            'FechaConstitucion': fecha_constitucion,
            'Rfc': rfc,
            'PaisNacionalidad': pais_nacionalidad,
            'GiroMercantil': giro_mercantil,
        })
        

class PersonaFisicaType(ScalarMap):
    """
    
    :param nombre:
    :param apellido_paterno:
    :param apellido_materno:
    :param fecha_nacimiento:
    :param rfc:
    :param curp:
    :param pais_nacionalidad:
    :param actividad_economica:
    """
    
    def __init__(
            self,
            nombre: str = None,
            apellido_paterno: str = None,
            apellido_materno: str = None,
            fecha_nacimiento: date = None,
            rfc: str = None,
            curp: str = None,
            pais_nacionalidad: str = None,
            actividad_economica: str = None,
    ): 
        super().__init__({
            'Nombre': nombre,
            'ApellidoPaterno': apellido_paterno,
            'ApellidoMaterno': apellido_materno,
            'FechaNacimiento': fecha_nacimiento,
            'Rfc': rfc,
            'Curp': curp,
            'PaisNacionalidad': pais_nacionalidad,
            'ActividadEconomica': actividad_economica,
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
        

class DatosTerceroType(ScalarMap):
    """
    
    :param tipo_persona_tercero:
    :param detalle_aportaciones:
    :param tipo_tercero:
    :param descripcion_tercero:
    """
    
    def __init__(
            self,
            tipo_persona_tercero: TipoPersonaType | dict,
            detalle_aportaciones: TercerosAportacionType | dict,
            tipo_tercero: str = None,
            descripcion_tercero: str = None,
    ): 
        super().__init__({
            'TipoPersonaTercero': tipo_persona_tercero,
            'DetalleAportaciones': detalle_aportaciones,
            'TipoTercero': tipo_tercero,
            'DescripcionTercero': descripcion_tercero,
        })
        

class DetalleTercerosType(ScalarMap):
    """
    
    :param datos_tercero:
    """
    
    def __init__(
            self,
            datos_tercero: DatosTerceroType | dict | Sequence[DatosTerceroType | dict] = None,
    ): 
        super().__init__({
            'DatosTercero': datos_tercero,
        })
        

class TercerosType(ScalarMap):
    """
    
    :param detalle_terceros:
    :param numero_terceros:
    """
    
    def __init__(
            self,
            detalle_terceros: DetalleTercerosType | dict,
            numero_terceros: str = None,
    ): 
        super().__init__({
            'DetalleTerceros': detalle_terceros,
            'NumeroTerceros': numero_terceros,
        })
        

class DatosAportacionSociosType(ScalarMap):
    """
    
    :param aportacion_numerario:
    :param aportacion_especie:
    """
    
    def __init__(
            self,
            aportacion_numerario: AportacionNumerarioType | dict = None,
            aportacion_especie: AportacionEspecieType | dict = None,
    ): 
        super().__init__({
            'AportacionNumerario': aportacion_numerario,
            'AportacionEspecie': aportacion_especie,
        })
        

class SociosAportacionType(ScalarMap):
    """
    
    :param datos_aportacion:
    """
    
    def __init__(
            self,
            datos_aportacion: DatosAportacionSociosType | dict,
    ): 
        super().__init__({
            'DatosAportacion': datos_aportacion,
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
    :param numero_interior:
    :param codigo_postal:
    """
    
    def __init__(
            self,
            pais: str = None,
            estado_provincia: str = None,
            ciudad_poblacion: str = None,
            colonia: str = None,
            calle: str = None,
            numero_exterior: str = None,
            numero_interior: str = None,
            codigo_postal: str = None,
    ): 
        super().__init__({
            'Pais': pais,
            'EstadoProvincia': estado_provincia,
            'CiudadPoblacion': ciudad_poblacion,
            'Colonia': colonia,
            'Calle': calle,
            'NumeroExterior': numero_exterior,
            'NumeroInterior': numero_interior,
            'CodigoPostal': codigo_postal,
        })
        

class NacionalType(ScalarMap):
    """
    
    :param colonia:
    :param calle:
    :param numero_exterior:
    :param numero_interior:
    :param codigo_postal:
    """
    
    def __init__(
            self,
            colonia: str = None,
            calle: str = None,
            numero_exterior: str = None,
            numero_interior: str = None,
            codigo_postal: str = None,
    ): 
        super().__init__({
            'Colonia': colonia,
            'Calle': calle,
            'NumeroExterior': numero_exterior,
            'NumeroInterior': numero_interior,
            'CodigoPostal': codigo_postal,
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
            nombre: str = None,
            apellido_paterno: str = None,
            apellido_materno: str = None,
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
        

class PersonaMoralSocioType(ScalarMap):
    """
    
    :param representante_apoderado:
    :param denominacion_razon:
    :param fecha_constitucion:
    :param pais_nacionalidad:
    :param giro_mercantil:
    """
    
    def __init__(
            self,
            representante_apoderado: RepresentanteApoderadoType | dict,
            denominacion_razon: str = None,
            fecha_constitucion: date = None,
            pais_nacionalidad: str = None,
            giro_mercantil: str = None,
    ): 
        super().__init__({
            'RepresentanteApoderado': representante_apoderado,
            'DenominacionRazon': denominacion_razon,
            'FechaConstitucion': fecha_constitucion,
            'PaisNacionalidad': pais_nacionalidad,
            'GiroMercantil': giro_mercantil,
        })
        

class PersonaFisicaSocioType(ScalarMap):
    """
    
    :param nombre:
    :param apellido_paterno:
    :param apellido_materno:
    :param fecha_nacimiento:
    :param curp:
    :param pais_nacionalidad:
    :param actividad_economica:
    """
    
    def __init__(
            self,
            nombre: str = None,
            apellido_paterno: str = None,
            apellido_materno: str = None,
            fecha_nacimiento: date = None,
            curp: str = None,
            pais_nacionalidad: str = None,
            actividad_economica: str = None,
    ): 
        super().__init__({
            'Nombre': nombre,
            'ApellidoPaterno': apellido_paterno,
            'ApellidoMaterno': apellido_materno,
            'FechaNacimiento': fecha_nacimiento,
            'Curp': curp,
            'PaisNacionalidad': pais_nacionalidad,
            'ActividadEconomica': actividad_economica,
        })
        

class TipoPersonaSocioType(ScalarMap):
    """
    
    :param persona_fisica:
    :param persona_moral:
    :param fideicomiso:
    """
    
    def __init__(
            self,
            persona_fisica: PersonaFisicaSocioType | dict = None,
            persona_moral: PersonaMoralSocioType | dict = None,
            fideicomiso: FideicomisoType | dict = None,
    ): 
        super().__init__({
            'PersonaFisica': persona_fisica,
            'PersonaMoral': persona_moral,
            'Fideicomiso': fideicomiso,
        })
        

class DatosSocioType(ScalarMap):
    """
    
    :param tipo_persona_socio:
    :param tipo_domicilio_socio:
    :param detalle_aportaciones:
    :param aportacion_anterior_socio:
    :param rfc_socio:
    :param telefono:
    """
    
    def __init__(
            self,
            tipo_persona_socio: TipoPersonaSocioType | dict,
            tipo_domicilio_socio: TipoDomicilioType | dict,
            detalle_aportaciones: SociosAportacionType | dict,
            aportacion_anterior_socio: str = None,
            rfc_socio: str = None,
            telefono: TelefonoType | dict = None,
    ): 
        super().__init__({
            'TipoPersonaSocio': tipo_persona_socio,
            'TipoDomicilioSocio': tipo_domicilio_socio,
            'DetalleAportaciones': detalle_aportaciones,
            'AportacionAnteriorSocio': aportacion_anterior_socio,
            'RfcSocio': rfc_socio,
            'Telefono': telefono,
        })
        

class DetalleSociosType(ScalarMap):
    """
    
    :param datos_socio:
    """
    
    def __init__(
            self,
            datos_socio: DatosSocioType | dict | Sequence[DatosSocioType | dict] = None,
    ): 
        super().__init__({
            'DatosSocio': datos_socio,
        })
        

class SociosType(ScalarMap):
    """
    
    :param detalle_socios:
    :param numero_socios:
    """
    
    def __init__(
            self,
            detalle_socios: DetalleSociosType | dict,
            numero_socios: str = None,
    ): 
        super().__init__({
            'DetalleSocios': detalle_socios,
            'NumeroSocios': numero_socios,
        })
        

class AportacionEspecieType(ScalarMap):
    """
    
    :param descripcion_bien:
    :param monto_estimado:
    """
    
    def __init__(
            self,
            descripcion_bien: str = None,
            monto_estimado: str = None,
    ): 
        super().__init__({
            'DescripcionBien': descripcion_bien,
            'MontoEstimado': monto_estimado,
        })
        

class AportacionNumerarioType(ScalarMap):
    """
    
    :param instrumento_monetario:
    :param moneda:
    :param monto_aportacion:
    :param aportacion_fideicomiso:
    :param nombre_institucion:
    """
    
    def __init__(
            self,
            instrumento_monetario: str = None,
            moneda: str = None,
            monto_aportacion: str = None,
            aportacion_fideicomiso: str = None,
            nombre_institucion: str = None,
    ): 
        super().__init__({
            'InstrumentoMonetario': instrumento_monetario,
            'Moneda': moneda,
            'MontoAportacion': monto_aportacion,
            'AportacionFideicomiso': aportacion_fideicomiso,
            'NombreInstitucion': nombre_institucion,
        })
        

class DatosAportacionType(ScalarMap):
    """
    
    :param aportacion_numerario:
    :param aportacion_especie:
    """
    
    def __init__(
            self,
            aportacion_numerario: AportacionNumerarioType | dict = None,
            aportacion_especie: AportacionEspecieType | dict = None,
    ): 
        super().__init__({
            'AportacionNumerario': aportacion_numerario,
            'AportacionEspecie': aportacion_especie,
        })
        

class RecursosPropiosType(ScalarMap):
    """
    
    :param datos_aportacion:
    """
    
    def __init__(
            self,
            datos_aportacion: DatosAportacionType | dict | Sequence[DatosAportacionType | dict] = None,
    ): 
        super().__init__({
            'DatosAportacion': datos_aportacion,
        })
        

class TipoAportacionType(ScalarMap):
    """
    
    :param recursos_propios:
    :param socios:
    :param terceros:
    :param prestamo_financiero:
    :param prestamo_no_financiero:
    :param financiamiento_bursatil:
    """
    
    def __init__(
            self,
            recursos_propios: RecursosPropiosType | dict = None,
            socios: SociosType | dict = None,
            terceros: TercerosType | dict = None,
            prestamo_financiero: PrestamoFinancieroType | dict = None,
            prestamo_no_financiero: PrestamoNoFinancieroType | dict = None,
            financiamiento_bursatil: FinanciamientoBursatilType | dict = None,
    ): 
        super().__init__({
            'RecursosPropios': recursos_propios,
            'Socios': socios,
            'Terceros': terceros,
            'PrestamoFinanciero': prestamo_financiero,
            'PrestamoNoFinanciero': prestamo_no_financiero,
            'FinanciamientoBursatil': financiamiento_bursatil,
        })
        

class AportacionesType(ScalarMap):
    """
    
    :param fecha_aportacion:
    :param tipo_aportacion:
    """
    
    def __init__(
            self,
            fecha_aportacion: date = None,
            tipo_aportacion: TipoAportacionType | dict | Sequence[TipoAportacionType | dict] = None,
    ): 
        super().__init__({
            'FechaAportacion': fecha_aportacion,
            'TipoAportacion': tipo_aportacion,
        })
        

class CaracteristicasDesarrolloType(ScalarMap):
    """
    
    :param codigo_postal:
    :param colonia:
    :param calle:
    :param tipo_desarrollo:
    :param monto_desarrollo:
    :param unidades_comercializadas:
    :param costo_unidad:
    :param otras_empresas:
    :param descripcion_desarrollo:
    """
    
    def __init__(
            self,
            codigo_postal: str,
            colonia: str,
            calle: str,
            tipo_desarrollo: str,
            monto_desarrollo: str,
            unidades_comercializadas: str,
            costo_unidad: str,
            otras_empresas: str,
            descripcion_desarrollo: str = None,
    ): 
        super().__init__({
            'CodigoPostal': codigo_postal,
            'Colonia': colonia,
            'Calle': calle,
            'TipoDesarrollo': tipo_desarrollo,
            'MontoDesarrollo': monto_desarrollo,
            'UnidadesComercializadas': unidades_comercializadas,
            'CostoUnidad': costo_unidad,
            'OtrasEmpresas': otras_empresas,
            'DescripcionDesarrollo': descripcion_desarrollo,
        })
        

class DatosDesarrolloType(ScalarMap):
    """
    
    :param objeto_aviso_anterior:
    :param modificacion:
    :param entidad_federativa:
    :param registro_licencia:
    :param caracteristicas_desarrollo:
    """
    
    def __init__(
            self,
            objeto_aviso_anterior: str,
            modificacion: str,
            entidad_federativa: str,
            registro_licencia: str,
            caracteristicas_desarrollo: CaracteristicasDesarrolloType | dict | Sequence[CaracteristicasDesarrolloType | dict],
    ): 
        super().__init__({
            'ObjetoAvisoAnterior': objeto_aviso_anterior,
            'Modificacion': modificacion,
            'EntidadFederativa': entidad_federativa,
            'RegistroLicencia': registro_licencia,
            'CaracteristicasDesarrollo': caracteristicas_desarrollo,
        })
        

class DesarrollosInmobiliariosType(ScalarMap):
    """
    
    :param datos_desarrollo:
    """
    
    def __init__(
            self,
            datos_desarrollo: DatosDesarrolloType | dict | Sequence[DatosDesarrolloType | dict],
    ): 
        super().__init__({
            'DatosDesarrollo': datos_desarrollo,
        })
        

class DatosOperacionType(ScalarMap):
    """
    
    :param tipo_operacion:
    :param desarrollos_inmobiliarios:
    :param aportaciones:
    """
    
    def __init__(
            self,
            tipo_operacion: str,
            desarrollos_inmobiliarios: DesarrollosInmobiliariosType | dict,
            aportaciones: AportacionesType | dict,
    ): 
        super().__init__({
            'TipoOperacion': tipo_operacion,
            'DesarrollosInmobiliarios': desarrollos_inmobiliarios,
            'Aportaciones': aportaciones,
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
    :param detalle_operaciones:
    :param modificatorio:
    """
    
    def __init__(
            self,
            referencia_aviso: str,
            prioridad: str,
            alerta: AlertaType | dict,
            detalle_operaciones: DetalleOperacionesType | dict,
            modificatorio: ModificatorioType | dict = None,
    ): 
        super().__init__({
            'ReferenciaAviso': referencia_aviso,
            'Prioridad': prioridad,
            'Alerta': alerta,
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
        

class Archivo(ArchivoType, XElement):
    tag = '{http://www.uif.shcp.gob.mx/recepcion/din}archivo'

