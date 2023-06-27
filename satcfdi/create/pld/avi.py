"""avi http://www.uif.shcp.gob.mx/recepcion/avi"""
from decimal import Decimal
from datetime import datetime, date, time
from collections.abc import Sequence
from ...cfdi import CFDI
from ...xelement import XElement
from ...utils import ScalarMap


class CuentaExtranjeraType(ScalarMap):
    """
    
    :param numero_cuenta:
    :param nombre_banco:
    """
    
    def __init__(
            self,
            numero_cuenta: str,
            nombre_banco: str,
    ): 
        super().__init__({
            'NumeroCuenta': numero_cuenta,
            'NombreBanco': nombre_banco,
        })
        

class CuentaNacionalType(ScalarMap):
    """
    
    :param clabe_destino:
    :param clave_institucion_financiera:
    """
    
    def __init__(
            self,
            clabe_destino: str,
            clave_institucion_financiera: int,
    ): 
        super().__init__({
            'ClabeDestino': clabe_destino,
            'ClaveInstitucionFinanciera': clave_institucion_financiera,
        })
        

class PaisCuentaType(ScalarMap):
    """
    
    :param nacional:
    :param extranjero:
    """
    
    def __init__(
            self,
            nacional: CuentaNacionalType | dict = None,
            extranjero: CuentaExtranjeraType | dict = None,
    ): 
        super().__init__({
            'Nacional': nacional,
            'Extranjero': extranjero,
        })
        

class PersonaMoralBasicoType(ScalarMap):
    """
    
    :param denominacion_razon:
    """
    
    def __init__(
            self,
            denominacion_razon: str,
    ): 
        super().__init__({
            'DenominacionRazon': denominacion_razon,
        })
        

class PersonaFisicaBasicoType(ScalarMap):
    """
    
    :param nombre:
    :param apellido_paterno:
    :param apellido_materno:
    """
    
    def __init__(
            self,
            nombre: str,
            apellido_paterno: str,
            apellido_materno: str,
    ): 
        super().__init__({
            'Nombre': nombre,
            'ApellidoPaterno': apellido_paterno,
            'ApellidoMaterno': apellido_materno,
        })
        

class TipoPersonaBasicoType(ScalarMap):
    """
    
    :param persona_fisica:
    :param persona_moral:
    """
    
    def __init__(
            self,
            persona_fisica: PersonaFisicaBasicoType | dict = None,
            persona_moral: PersonaMoralBasicoType | dict = None,
    ): 
        super().__init__({
            'PersonaFisica': persona_fisica,
            'PersonaMoral': persona_moral,
        })
        

class PersonaCuentaType(ScalarMap):
    """
    
    :param tipo_persona:
    :param nacionalidad_cuenta:
    """
    
    def __init__(
            self,
            tipo_persona: TipoPersonaBasicoType | dict,
            nacionalidad_cuenta: PaisCuentaType | dict,
    ): 
        super().__init__({
            'TipoPersona': tipo_persona,
            'NacionalidadCuenta': nacionalidad_cuenta,
        })
        

class ActivoVirtualCompuestoType(ScalarMap):
    """
    
    :param activo_virtual:
    :param monto_operacion_mn:
    """
    
    def __init__(
            self,
            activo_virtual: ActivoVirtualSimpleType | dict,
            monto_operacion_mn: str,
    ): 
        super().__init__({
            'ActivoVirtual': activo_virtual,
            'MontoOperacionMn': monto_operacion_mn,
        })
        

class ActivoVirtualSimpleType(ScalarMap):
    """
    
    :param activo_virtual_operado:
    :param tipo_cambio_mn:
    :param cantidad_activo_virtual:
    :param descripcion_activo_virtual:
    """
    
    def __init__(
            self,
            activo_virtual_operado: int,
            tipo_cambio_mn: str,
            cantidad_activo_virtual: str,
            descripcion_activo_virtual: str = None,
    ): 
        super().__init__({
            'ActivoVirtualOperado': activo_virtual_operado,
            'TipoCambioMn': tipo_cambio_mn,
            'CantidadActivoVirtual': cantidad_activo_virtual,
            'DescripcionActivoVirtual': descripcion_activo_virtual,
        })
        

class DepositoType(ScalarMap):
    """
    
    :param fecha_hora_operacion:
    :param instrumento_monetario:
    :param moneda_operacion:
    :param monto_operacion:
    :param datos_ordenante:
    """
    
    def __init__(
            self,
            fecha_hora_operacion: str,
            instrumento_monetario: str,
            moneda_operacion: int,
            monto_operacion: str,
            datos_ordenante: PersonaCuentaType | dict,
    ): 
        super().__init__({
            'FechaHoraOperacion': fecha_hora_operacion,
            'InstrumentoMonetario': instrumento_monetario,
            'MonedaOperacion': moneda_operacion,
            'MontoOperacion': monto_operacion,
            'DatosOrdenante': datos_ordenante,
        })
        

class RetiroType(ScalarMap):
    """
    
    :param fecha_hora_operacion:
    :param instrumento_monetario:
    :param moneda_operacion:
    :param monto_operacion:
    :param datos_beneficiario:
    """
    
    def __init__(
            self,
            fecha_hora_operacion: str,
            instrumento_monetario: str,
            moneda_operacion: int,
            monto_operacion: str,
            datos_beneficiario: PersonaCuentaType | dict,
    ): 
        super().__init__({
            'FechaHoraOperacion': fecha_hora_operacion,
            'InstrumentoMonetario': instrumento_monetario,
            'MonedaOperacion': moneda_operacion,
            'MontoOperacion': monto_operacion,
            'DatosBeneficiario': datos_beneficiario,
        })
        

class RecepcionType(ScalarMap):
    """
    
    :param fecha_hora_operacion:
    :param monto_operacion_mn:
    :param activo_virtual:
    :param hash_operacion:
    """
    
    def __init__(
            self,
            fecha_hora_operacion: str,
            monto_operacion_mn: str,
            activo_virtual: ActivoVirtualSimpleType | dict,
            hash_operacion: str,
    ): 
        super().__init__({
            'FechaHoraOperacion': fecha_hora_operacion,
            'MontoOperacionMn': monto_operacion_mn,
            'ActivoVirtual': activo_virtual,
            'HashOperacion': hash_operacion,
        })
        

class EnvioType(ScalarMap):
    """
    
    :param fecha_hora_operacion:
    :param monto_operacion_mn:
    :param activo_virtual:
    :param hash_operacion:
    """
    
    def __init__(
            self,
            fecha_hora_operacion: str,
            monto_operacion_mn: str,
            activo_virtual: ActivoVirtualSimpleType | dict,
            hash_operacion: str,
    ): 
        super().__init__({
            'FechaHoraOperacion': fecha_hora_operacion,
            'MontoOperacionMn': monto_operacion_mn,
            'ActivoVirtual': activo_virtual,
            'HashOperacion': hash_operacion,
        })
        

class IntercambioType(ScalarMap):
    """
    
    :param fecha_hora_operacion:
    :param activo_virtual_enviado:
    :param activo_virtual_recibido:
    :param hash_operacion:
    """
    
    def __init__(
            self,
            fecha_hora_operacion: str,
            activo_virtual_enviado: ActivoVirtualCompuestoType | dict,
            activo_virtual_recibido: ActivoVirtualCompuestoType | dict,
            hash_operacion: str,
    ): 
        super().__init__({
            'FechaHoraOperacion': fecha_hora_operacion,
            'ActivoVirtualEnviado': activo_virtual_enviado,
            'ActivoVirtualRecibido': activo_virtual_recibido,
            'HashOperacion': hash_operacion,
        })
        

class VentaType(ScalarMap):
    """
    
    :param fecha_hora_operacion:
    :param moneda_operacion:
    :param monto_operacion:
    :param activo_virtual:
    :param hash_operacion:
    """
    
    def __init__(
            self,
            fecha_hora_operacion: str,
            moneda_operacion: int,
            monto_operacion: str,
            activo_virtual: ActivoVirtualSimpleType | dict,
            hash_operacion: str,
    ): 
        super().__init__({
            'FechaHoraOperacion': fecha_hora_operacion,
            'MonedaOperacion': moneda_operacion,
            'MontoOperacion': monto_operacion,
            'ActivoVirtual': activo_virtual,
            'HashOperacion': hash_operacion,
        })
        

class CompraType(ScalarMap):
    """
    
    :param fecha_hora_operacion:
    :param moneda_operacion:
    :param monto_operacion:
    :param activo_virtual:
    :param hash_operacion:
    """
    
    def __init__(
            self,
            fecha_hora_operacion: str,
            moneda_operacion: int,
            monto_operacion: str,
            activo_virtual: ActivoVirtualSimpleType | dict,
            hash_operacion: str,
    ): 
        super().__init__({
            'FechaHoraOperacion': fecha_hora_operacion,
            'MonedaOperacion': moneda_operacion,
            'MontoOperacion': monto_operacion,
            'ActivoVirtual': activo_virtual,
            'HashOperacion': hash_operacion,
        })
        

class FondosDepositadosType(ScalarMap):
    """
    
    :param deposito:
    """
    
    def __init__(
            self,
            deposito: DepositoType | dict | Sequence[DepositoType | dict],
    ): 
        super().__init__({
            'Deposito': deposito,
        })
        

class FondosRetiradosType(ScalarMap):
    """
    
    :param retiro:
    """
    
    def __init__(
            self,
            retiro: RetiroType | dict | Sequence[RetiroType | dict],
    ): 
        super().__init__({
            'Retiro': retiro,
        })
        

class OperacionesFondosType(ScalarMap):
    """
    
    :param fondos_retirados:
    :param fondos_depositados:
    """
    
    def __init__(
            self,
            fondos_retirados: FondosRetiradosType | dict = None,
            fondos_depositados: FondosDepositadosType | dict = None,
    ): 
        super().__init__({
            'FondosRetirados': fondos_retirados,
            'FondosDepositados': fondos_depositados,
        })
        

class TransferenciasRecibidasType(ScalarMap):
    """
    
    :param recepcion:
    """
    
    def __init__(
            self,
            recepcion: RecepcionType | dict | Sequence[RecepcionType | dict],
    ): 
        super().__init__({
            'Recepcion': recepcion,
        })
        

class TransferenciasEnviadasType(ScalarMap):
    """
    
    :param envio:
    """
    
    def __init__(
            self,
            envio: EnvioType | dict | Sequence[EnvioType | dict],
    ): 
        super().__init__({
            'Envio': envio,
        })
        

class OperacionesTransferenciaType(ScalarMap):
    """
    
    :param transferencias_enviadas:
    :param transferencias_recibidas:
    """
    
    def __init__(
            self,
            transferencias_enviadas: TransferenciasEnviadasType | dict = None,
            transferencias_recibidas: TransferenciasRecibidasType | dict = None,
    ): 
        super().__init__({
            'TransferenciasEnviadas': transferencias_enviadas,
            'TransferenciasRecibidas': transferencias_recibidas,
        })
        

class OperacionesIntercambioType(ScalarMap):
    """
    
    :param intercambio:
    """
    
    def __init__(
            self,
            intercambio: IntercambioType | dict | Sequence[IntercambioType | dict],
    ): 
        super().__init__({
            'Intercambio': intercambio,
        })
        

class OperacionesVentaType(ScalarMap):
    """
    
    :param venta:
    """
    
    def __init__(
            self,
            venta: VentaType | dict | Sequence[VentaType | dict],
    ): 
        super().__init__({
            'Venta': venta,
        })
        

class OperacionesCompraType(ScalarMap):
    """
    
    :param compra:
    """
    
    def __init__(
            self,
            compra: CompraType | dict | Sequence[CompraType | dict],
    ): 
        super().__init__({
            'Compra': compra,
        })
        

class DetalleOperacionesType(ScalarMap):
    """
    
    :param operaciones_compra:
    :param operaciones_venta:
    :param operaciones_intercambio:
    :param operaciones_transferencia:
    :param operaciones_fondos:
    """
    
    def __init__(
            self,
            operaciones_compra: OperacionesCompraType | dict = None,
            operaciones_venta: OperacionesVentaType | dict = None,
            operaciones_intercambio: OperacionesIntercambioType | dict = None,
            operaciones_transferencia: OperacionesTransferenciaType | dict = None,
            operaciones_fondos: OperacionesFondosType | dict = None,
    ): 
        super().__init__({
            'OperacionesCompra': operaciones_compra,
            'OperacionesVenta': operaciones_venta,
            'OperacionesIntercambio': operaciones_intercambio,
            'OperacionesTransferencia': operaciones_transferencia,
            'OperacionesFondos': operaciones_fondos,
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
            clave_pais: str,
            numero_telefono: str,
            correo_electronico: str,
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
        

class DocumentoIdentificacionType(ScalarMap):
    """
    
    :param tipo_identificacion:
    :param numero_identificacion:
    """
    
    def __init__(
            self,
            tipo_identificacion: int,
            numero_identificacion: str,
    ): 
        super().__init__({
            'TipoIdentificacion': tipo_identificacion,
            'NumeroIdentificacion': numero_identificacion,
        })
        

class RepresentanteApoderadoType(ScalarMap):
    """
    
    :param nombre:
    :param apellido_paterno:
    :param apellido_materno:
    :param documento_identificacion:
    :param fecha_nacimiento:
    :param rfc:
    :param curp:
    """
    
    def __init__(
            self,
            nombre: str,
            apellido_paterno: str,
            apellido_materno: str,
            documento_identificacion: DocumentoIdentificacionType | dict,
            fecha_nacimiento: date = None,
            rfc: str = None,
            curp: str = None,
    ): 
        super().__init__({
            'Nombre': nombre,
            'ApellidoPaterno': apellido_paterno,
            'ApellidoMaterno': apellido_materno,
            'DocumentoIdentificacion': documento_identificacion,
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
            representante_apoderado: RepresentanteApoderadoType | dict,
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
    :param documento_identificacion:
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
            documento_identificacion: DocumentoIdentificacionType | dict,
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
            'DocumentoIdentificacion': documento_identificacion,
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
        

class DatosCuentaPlataformaType(ScalarMap):
    """
    
    :param id_usuario:
    :param cuenta_relacionada:
    :param moneda_cuenta:
    :param clabe_interbancaria:
    """
    
    def __init__(
            self,
            id_usuario: str,
            cuenta_relacionada: str,
            moneda_cuenta: int,
            clabe_interbancaria: str = None,
    ): 
        super().__init__({
            'IdUsuario': id_usuario,
            'CuentaRelacionada': cuenta_relacionada,
            'MonedaCuenta': moneda_cuenta,
            'ClabeInterbancaria': clabe_interbancaria,
        })
        

class PersonaAvisoType(ScalarMap):
    """
    
    :param datos_cuenta_plataforma:
    :param tipo_persona:
    :param tipo_domicilio:
    :param telefono:
    """
    
    def __init__(
            self,
            datos_cuenta_plataforma: DatosCuentaPlataformaType | dict,
            tipo_persona: TipoPersonaType | dict,
            tipo_domicilio: TipoDomicilioType | dict = None,
            telefono: TelefonoType | dict = None,
    ): 
        super().__init__({
            'DatosCuentaPlataforma': datos_cuenta_plataforma,
            'TipoPersona': tipo_persona,
            'TipoDomicilio': tipo_domicilio,
            'Telefono': telefono,
        })
        

class OperacionesPersonaType(ScalarMap):
    """
    
    :param persona_aviso:
    :param detalle_operaciones:
    :param dueno_beneficiario:
    """
    
    def __init__(
            self,
            persona_aviso: PersonaAvisoType | dict,
            detalle_operaciones: DetalleOperacionesType | dict,
            dueno_beneficiario: DuenoBeneficiarioType | dict | Sequence[DuenoBeneficiarioType | dict] = None,
    ): 
        super().__init__({
            'PersonaAviso': persona_aviso,
            'DetalleOperaciones': detalle_operaciones,
            'DuenoBeneficiario': dueno_beneficiario,
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
    :param operaciones_persona:
    :param modificatorio:
    """
    
    def __init__(
            self,
            referencia_aviso: str,
            prioridad: str,
            alerta: AlertaType | dict,
            operaciones_persona: OperacionesPersonaType | dict,
            modificatorio: ModificatorioType | dict = None,
    ): 
        super().__init__({
            'ReferenciaAviso': referencia_aviso,
            'Prioridad': prioridad,
            'Alerta': alerta,
            'OperacionesPersona': operaciones_persona,
            'Modificatorio': modificatorio,
        })
        

class SujetoObligadoType(ScalarMap):
    """
    
    :param clave_sujeto_obligado:
    :param clave_actividad:
    :param dominio_plataforma:
    :param clave_entidad_colegiada:
    :param exento:
    """
    
    def __init__(
            self,
            clave_sujeto_obligado: str,
            clave_actividad: str,
            dominio_plataforma: str,
            clave_entidad_colegiada: str = None,
            exento: str = None,
    ): 
        super().__init__({
            'ClaveSujetoObligado': clave_sujeto_obligado,
            'ClaveActividad': clave_actividad,
            'DominioPlataforma': dominio_plataforma,
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
    tag = '{http://www.uif.shcp.gob.mx/recepcion/avi}archivo'

