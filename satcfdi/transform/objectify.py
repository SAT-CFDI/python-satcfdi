from decimal import Decimal
from datetime import datetime, date, time
from .helpers import Xint, impuesto_index, default_objectify
from ..exceptions import NamespaceMismatchError
from ..utils import ScalarMap
from ..catalogs import catalog_code

def ubicacion0(cls, node):
    self = ScalarMap()
    if (a := node.attrib.get('taxID')) is not None:
        self['TaxID'] = a
    if (a := node.attrib.get('codigoSitio')) is not None:
        self['CodigoSitio'] = a
    if (a := node.attrib.get('calle')) is not None:
        self['Calle'] = a
    if (a := node.attrib.get('numero')) is not None:
        self['Numero'] = a
    if (a := node.attrib.get('colonia')) is not None:
        self['Colonia'] = a
    if (a := node.attrib.get('ciudad')) is not None:
        self['Ciudad'] = a
    if (a := node.attrib.get('municipio')) is not None:
        self['Municipio'] = a
    if (a := node.attrib.get('estado')) is not None:
        self['Estado'] = a
    if (a := node.attrib.get('pais')) is not None:
        self['Pais'] = a
    if (a := node.attrib.get('codigoPostal')) is not None:
        self['CodigoPostal'] = a
    return self
def datos_contacto0(cls, node):
    self = ScalarMap()
    if (a := node.attrib.get('telefono')) is not None:
        self['Telefono'] = a
    if (a := node.attrib.get('emailComercial')) is not None:
        self['EmailComercial'] = a
    if (a := node.attrib.get('emailContacto')) is not None:
        self['EmailContacto'] = a
    if (a := node.attrib.get('web')) is not None:
        self['Web'] = a
    return self
def extra0(cls, node):
    self = ScalarMap()
    if (a := node.attrib.get('indicador')) is not None:
        self['Indicador'] = a
    if (a := node.attrib.get('atributo')) is not None:
        self['Atributo'] = a
    if (a := node.attrib.get('valor')) is not None:
        self['Valor'] = a
    if (a := node.attrib.get('prefijo')) is not None:
        self['Prefijo'] = a
    if (a := node.attrib.get('sufijo')) is not None:
        self['Sufijo'] = a
    return self
def archivo_type0(cls, node):
    self = ScalarMap()
    self['Informe'] = [informe0(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/ari}informe')]
    return self
def informe0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/ari}mes_reportado')
    self['MesReportado'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/ari}sujeto_obligado')
    self['SujetoObligado'] = sujeto_obligado0(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/ari}aviso')
    if el is not None:
        self['Aviso'] = [aviso0(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/ari}aviso')]
    return self
def sujeto_obligado0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/ari}clave_entidad_colegiada')
    if el is not None:
        self['ClaveEntidadColegiada'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/ari}clave_sujeto_obligado')
    self['ClaveSujetoObligado'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/ari}clave_actividad')
    self['ClaveActividad'] = catalog_code('C329_clave_actividad_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/ari}exento')
    if el is not None:
        self['Exento'] = el.text
    return self
def aviso0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/ari}referencia_aviso')
    self['ReferenciaAviso'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/ari}modificatorio')
    if el is not None:
        self['Modificatorio'] = modificatorio0(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/ari}prioridad')
    self['Prioridad'] = catalog_code('C329_prioridad_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/ari}alerta')
    self['Alerta'] = alerta0(cls, el)
    self['PersonaAviso'] = [persona_aviso0(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/ari}persona_aviso')]
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/ari}dueno_beneficiario')
    if el is not None:
        self['DuenoBeneficiario'] = [dueno_beneficiario0(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/ari}dueno_beneficiario')]
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/ari}detalle_operaciones')
    self['DetalleOperaciones'] = detalle_operaciones0(cls, el)
    return self
def modificatorio0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/ari}folio_modificacion')
    self['FolioModificacion'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/ari}descripcion_modificacion')
    self['DescripcionModificacion'] = el.text
    return self
def alerta0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/ari}tipo_alerta')
    self['TipoAlerta'] = catalog_code('C329_tipo_alerta_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/ari}descripcion_alerta')
    if el is not None:
        self['DescripcionAlerta'] = el.text
    return self
def persona_aviso0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/ari}tipo_persona')
    self['TipoPersona'] = tipo_persona0(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/ari}tipo_domicilio')
    if el is not None:
        self['TipoDomicilio'] = tipo_domicilio0(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/ari}telefono')
    if el is not None:
        self['Telefono'] = telefono0(cls, el)
    return self
def tipo_persona0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/ari}persona_fisica')
    if el is not None:
        self['PersonaFisica'] = persona_fisica0(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/ari}persona_moral')
    if el is not None:
        self['PersonaMoral'] = persona_moral0(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/ari}fideicomiso')
    if el is not None:
        self['Fideicomiso'] = fideicomiso0(cls, el)
    return self
def persona_fisica0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/ari}nombre')
    self['Nombre'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/ari}apellido_paterno')
    self['ApellidoPaterno'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/ari}apellido_materno')
    self['ApellidoMaterno'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/ari}fecha_nacimiento')
    if el is not None:
        self['FechaNacimiento'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/ari}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/ari}curp')
    if el is not None:
        self['Curp'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/ari}pais_nacionalidad')
    self['PaisNacionalidad'] = catalog_code('C329_pais_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/ari}actividad_economica')
    self['ActividadEconomica'] = catalog_code('C329_actividad_economica_type', el.text)
    return self
def persona_moral0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/ari}denominacion_razon')
    self['DenominacionRazon'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/ari}fecha_constitucion')
    if el is not None:
        self['FechaConstitucion'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/ari}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/ari}pais_nacionalidad')
    self['PaisNacionalidad'] = catalog_code('C329_pais_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/ari}giro_mercantil')
    self['GiroMercantil'] = catalog_code('C329_giro_mercantil_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/ari}representante_apoderado')
    self['RepresentanteApoderado'] = representante_apoderado0(cls, el)
    return self
def fideicomiso0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/ari}denominacion_razon')
    self['DenominacionRazon'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/ari}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/ari}identificador_fideicomiso')
    if el is not None:
        self['IdentificadorFideicomiso'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/ari}apoderado_delegado')
    self['ApoderadoDelegado'] = representante_apoderado0(cls, el)
    return self
def representante_apoderado0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/ari}nombre')
    self['Nombre'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/ari}apellido_paterno')
    self['ApellidoPaterno'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/ari}apellido_materno')
    self['ApellidoMaterno'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/ari}fecha_nacimiento')
    if el is not None:
        self['FechaNacimiento'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/ari}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/ari}curp')
    if el is not None:
        self['Curp'] = el.text
    return self
def tipo_domicilio0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/ari}nacional')
    if el is not None:
        self['Nacional'] = nacional0(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/ari}extranjero')
    if el is not None:
        self['Extranjero'] = extranjero0(cls, el)
    return self
def nacional0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/ari}colonia')
    self['Colonia'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/ari}calle')
    self['Calle'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/ari}numero_exterior')
    self['NumeroExterior'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/ari}numero_interior')
    if el is not None:
        self['NumeroInterior'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/ari}codigo_postal')
    self['CodigoPostal'] = el.text
    return self
def extranjero0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/ari}pais')
    self['Pais'] = catalog_code('C329_pais_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/ari}estado_provincia')
    self['EstadoProvincia'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/ari}ciudad_poblacion')
    self['CiudadPoblacion'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/ari}colonia')
    self['Colonia'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/ari}calle')
    self['Calle'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/ari}numero_exterior')
    self['NumeroExterior'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/ari}numero_interior')
    if el is not None:
        self['NumeroInterior'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/ari}codigo_postal')
    self['CodigoPostal'] = el.text
    return self
def telefono0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/ari}clave_pais')
    if el is not None:
        self['ClavePais'] = catalog_code('C329_pais_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/ari}numero_telefono')
    if el is not None:
        self['NumeroTelefono'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/ari}correo_electronico')
    if el is not None:
        self['CorreoElectronico'] = el.text
    return self
def dueno_beneficiario0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/ari}tipo_persona')
    self['TipoPersona'] = tipo_persona1(cls, el)
    return self
def tipo_persona1(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/ari}persona_fisica')
    if el is not None:
        self['PersonaFisica'] = persona_fisica1(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/ari}persona_moral')
    if el is not None:
        self['PersonaMoral'] = persona_moral1(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/ari}fideicomiso')
    if el is not None:
        self['Fideicomiso'] = fideicomiso1(cls, el)
    return self
def persona_fisica1(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/ari}nombre')
    self['Nombre'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/ari}apellido_paterno')
    self['ApellidoPaterno'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/ari}apellido_materno')
    self['ApellidoMaterno'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/ari}fecha_nacimiento')
    if el is not None:
        self['FechaNacimiento'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/ari}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/ari}curp')
    if el is not None:
        self['Curp'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/ari}pais_nacionalidad')
    if el is not None:
        self['PaisNacionalidad'] = catalog_code('C329_pais_type', el.text)
    return self
def persona_moral1(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/ari}denominacion_razon')
    self['DenominacionRazon'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/ari}fecha_constitucion')
    if el is not None:
        self['FechaConstitucion'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/ari}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/ari}pais_nacionalidad')
    if el is not None:
        self['PaisNacionalidad'] = catalog_code('C329_pais_type', el.text)
    return self
def fideicomiso1(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/ari}denominacion_razon')
    self['DenominacionRazon'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/ari}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/ari}identificador_fideicomiso')
    if el is not None:
        self['IdentificadorFideicomiso'] = el.text
    return self
def detalle_operaciones0(cls, node):
    self = ScalarMap()
    self['DatosOperacion'] = [datos_operacion0(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/ari}datos_operacion')]
    return self
def datos_operacion0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/ari}fecha_operacion')
    self['FechaOperacion'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/ari}tipo_operacion')
    self['TipoOperacion'] = catalog_code('C329_tipo_operacion_type', el.text)
    self['Caracteristicas'] = [caracteristicas0(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/ari}caracteristicas')]
    self['DatosLiquidacion'] = [datos_liquidacion0(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/ari}datos_liquidacion')]
    return self
def caracteristicas0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/ari}fecha_inicio')
    self['FechaInicio'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/ari}fecha_termino')
    self['FechaTermino'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/ari}tipo_inmueble')
    self['TipoInmueble'] = catalog_code('C329_tipo_inmueble_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/ari}valor_referencia')
    self['ValorReferencia'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/ari}colonia')
    self['Colonia'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/ari}calle')
    self['Calle'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/ari}numero_exterior')
    self['NumeroExterior'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/ari}numero_interior')
    if el is not None:
        self['NumeroInterior'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/ari}codigo_postal')
    self['CodigoPostal'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/ari}folio_real')
    self['FolioReal'] = el.text
    return self
def datos_liquidacion0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/ari}fecha_pago')
    self['FechaPago'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/ari}forma_pago')
    self['FormaPago'] = catalog_code('C329_forma_pago_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/ari}instrumento_monetario')
    self['InstrumentoMonetario'] = catalog_code('C329_instrumento_monetario_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/ari}moneda')
    self['Moneda'] = catalog_code('C329_moneda_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/ari}monto_operacion')
    self['MontoOperacion'] = el.text
    return self
def archivo_type1(cls, node):
    self = ScalarMap()
    self['Informe'] = [informe1(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/avi}informe')]
    return self
def informe1(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}mes_reportado')
    self['MesReportado'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}sujeto_obligado')
    self['SujetoObligado'] = sujeto_obligado1(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}aviso')
    if el is not None:
        self['Aviso'] = [aviso1(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/avi}aviso')]
    return self
def sujeto_obligado1(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}clave_entidad_colegiada')
    if el is not None:
        self['ClaveEntidadColegiada'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}clave_sujeto_obligado')
    self['ClaveSujetoObligado'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}clave_actividad')
    self['ClaveActividad'] = catalog_code('C329_clave_actividad_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}exento')
    if el is not None:
        self['Exento'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}dominio_plataforma')
    self['DominioPlataforma'] = el.text
    return self
def aviso1(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}referencia_aviso')
    self['ReferenciaAviso'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}prioridad')
    self['Prioridad'] = catalog_code('C329_prioridad_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}modificatorio')
    if el is not None:
        self['Modificatorio'] = modificatorio1(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}alerta')
    self['Alerta'] = alerta1(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}operaciones_persona')
    self['OperacionesPersona'] = operaciones_persona0(cls, el)
    return self
def modificatorio1(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}folio_modificacion')
    self['FolioModificacion'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}descripcion_modificacion')
    self['DescripcionModificacion'] = el.text
    return self
def alerta1(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}tipo_alerta')
    self['TipoAlerta'] = catalog_code('C329_tipo_alerta_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}descripcion_alerta')
    if el is not None:
        self['DescripcionAlerta'] = el.text
    return self
def operaciones_persona0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}persona_aviso')
    self['PersonaAviso'] = persona_aviso1(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}dueno_beneficiario')
    if el is not None:
        self['DuenoBeneficiario'] = [dueno_beneficiario1(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/avi}dueno_beneficiario')]
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}detalle_operaciones')
    self['DetalleOperaciones'] = detalle_operaciones1(cls, el)
    return self
def persona_aviso1(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}datos_cuenta_plataforma')
    self['DatosCuentaPlataforma'] = datos_cuenta_plataforma0(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}tipo_persona')
    self['TipoPersona'] = tipo_persona2(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}tipo_domicilio')
    if el is not None:
        self['TipoDomicilio'] = tipo_domicilio1(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}telefono')
    if el is not None:
        self['Telefono'] = telefono1(cls, el)
    return self
def datos_cuenta_plataforma0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}id_usuario')
    self['IdUsuario'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}cuenta_relacionada')
    self['CuentaRelacionada'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}clabe_interbancaria')
    if el is not None:
        self['ClabeInterbancaria'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}moneda_cuenta')
    self['MonedaCuenta'] = Xint(el.text)
    return self
def tipo_persona2(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}persona_fisica')
    if el is not None:
        self['PersonaFisica'] = persona_fisica2(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}persona_moral')
    if el is not None:
        self['PersonaMoral'] = persona_moral2(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}fideicomiso')
    if el is not None:
        self['Fideicomiso'] = fideicomiso2(cls, el)
    return self
def persona_fisica2(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}nombre')
    self['Nombre'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}apellido_paterno')
    self['ApellidoPaterno'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}apellido_materno')
    self['ApellidoMaterno'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}fecha_nacimiento')
    if el is not None:
        self['FechaNacimiento'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}curp')
    if el is not None:
        self['Curp'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}pais_nacionalidad')
    self['PaisNacionalidad'] = catalog_code('C329_pais_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}actividad_economica')
    self['ActividadEconomica'] = catalog_code('C329_actividad_economica_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}documento_identificacion')
    self['DocumentoIdentificacion'] = documento_identificacion0(cls, el)
    return self
def persona_moral2(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}denominacion_razon')
    self['DenominacionRazon'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}fecha_constitucion')
    if el is not None:
        self['FechaConstitucion'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}pais_nacionalidad')
    self['PaisNacionalidad'] = catalog_code('C329_pais_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}giro_mercantil')
    self['GiroMercantil'] = catalog_code('C329_giro_mercantil_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}representante_apoderado')
    self['RepresentanteApoderado'] = representante_apoderado1(cls, el)
    return self
def fideicomiso2(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}denominacion_razon')
    self['DenominacionRazon'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}identificador_fideicomiso')
    if el is not None:
        self['IdentificadorFideicomiso'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}apoderado_delegado')
    self['ApoderadoDelegado'] = representante_apoderado1(cls, el)
    return self
def representante_apoderado1(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}nombre')
    self['Nombre'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}apellido_paterno')
    self['ApellidoPaterno'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}apellido_materno')
    self['ApellidoMaterno'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}fecha_nacimiento')
    if el is not None:
        self['FechaNacimiento'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}curp')
    if el is not None:
        self['Curp'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}documento_identificacion')
    self['DocumentoIdentificacion'] = documento_identificacion0(cls, el)
    return self
def documento_identificacion0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}tipo_identificacion')
    self['TipoIdentificacion'] = Xint(el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}numero_identificacion')
    self['NumeroIdentificacion'] = el.text
    return self
def tipo_domicilio1(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}nacional')
    if el is not None:
        self['Nacional'] = nacional1(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}extranjero')
    if el is not None:
        self['Extranjero'] = extranjero1(cls, el)
    return self
def nacional1(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}colonia')
    self['Colonia'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}calle')
    self['Calle'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}numero_exterior')
    self['NumeroExterior'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}numero_interior')
    if el is not None:
        self['NumeroInterior'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}codigo_postal')
    self['CodigoPostal'] = el.text
    return self
def extranjero1(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}pais')
    self['Pais'] = catalog_code('C329_pais_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}estado_provincia')
    self['EstadoProvincia'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}ciudad_poblacion')
    self['CiudadPoblacion'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}colonia')
    self['Colonia'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}calle')
    self['Calle'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}numero_exterior')
    self['NumeroExterior'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}numero_interior')
    if el is not None:
        self['NumeroInterior'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}codigo_postal')
    self['CodigoPostal'] = el.text
    return self
def telefono1(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}clave_pais')
    self['ClavePais'] = catalog_code('C329_pais_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}numero_telefono')
    self['NumeroTelefono'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}correo_electronico')
    self['CorreoElectronico'] = el.text
    return self
def dueno_beneficiario1(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}tipo_persona')
    self['TipoPersona'] = tipo_persona3(cls, el)
    return self
def tipo_persona3(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}persona_fisica')
    if el is not None:
        self['PersonaFisica'] = persona_fisica3(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}persona_moral')
    if el is not None:
        self['PersonaMoral'] = persona_moral3(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}fideicomiso')
    if el is not None:
        self['Fideicomiso'] = fideicomiso3(cls, el)
    return self
def persona_fisica3(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}nombre')
    self['Nombre'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}apellido_paterno')
    self['ApellidoPaterno'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}apellido_materno')
    self['ApellidoMaterno'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}fecha_nacimiento')
    if el is not None:
        self['FechaNacimiento'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}curp')
    if el is not None:
        self['Curp'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}pais_nacionalidad')
    self['PaisNacionalidad'] = catalog_code('C329_pais_type', el.text)
    return self
def persona_moral3(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}denominacion_razon')
    self['DenominacionRazon'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}fecha_constitucion')
    if el is not None:
        self['FechaConstitucion'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}pais_nacionalidad')
    self['PaisNacionalidad'] = catalog_code('C329_pais_type', el.text)
    return self
def fideicomiso3(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}denominacion_razon')
    self['DenominacionRazon'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}identificador_fideicomiso')
    if el is not None:
        self['IdentificadorFideicomiso'] = el.text
    return self
def detalle_operaciones1(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}operaciones_compra')
    if el is not None:
        self['OperacionesCompra'] = operaciones_compra0(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}operaciones_venta')
    if el is not None:
        self['OperacionesVenta'] = operaciones_venta0(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}operaciones_intercambio')
    if el is not None:
        self['OperacionesIntercambio'] = operaciones_intercambio0(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}operaciones_transferencia')
    if el is not None:
        self['OperacionesTransferencia'] = operaciones_transferencia0(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}operaciones_fondos')
    if el is not None:
        self['OperacionesFondos'] = operaciones_fondos0(cls, el)
    return self
def operaciones_compra0(cls, node):
    self = ScalarMap()
    self['Compra'] = [compra0(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/avi}compra')]
    return self
def operaciones_venta0(cls, node):
    self = ScalarMap()
    self['Venta'] = [venta0(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/avi}venta')]
    return self
def operaciones_intercambio0(cls, node):
    self = ScalarMap()
    self['Intercambio'] = [intercambio0(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/avi}intercambio')]
    return self
def operaciones_transferencia0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}transferencias_enviadas')
    if el is not None:
        self['TransferenciasEnviadas'] = transferencias_enviadas0(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}transferencias_recibidas')
    if el is not None:
        self['TransferenciasRecibidas'] = transferencias_recibidas0(cls, el)
    return self
def transferencias_enviadas0(cls, node):
    self = ScalarMap()
    self['Envio'] = [envio0(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/avi}envio')]
    return self
def transferencias_recibidas0(cls, node):
    self = ScalarMap()
    self['Recepcion'] = [recepcion0(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/avi}recepcion')]
    return self
def operaciones_fondos0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}fondos_retirados')
    if el is not None:
        self['FondosRetirados'] = fondos_retirados0(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}fondos_depositados')
    if el is not None:
        self['FondosDepositados'] = fondos_depositados0(cls, el)
    return self
def fondos_retirados0(cls, node):
    self = ScalarMap()
    self['Retiro'] = [retiro0(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/avi}retiro')]
    return self
def fondos_depositados0(cls, node):
    self = ScalarMap()
    self['Deposito'] = [deposito0(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/avi}deposito')]
    return self
def compra0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}fecha_hora_operacion')
    self['FechaHoraOperacion'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}moneda_operacion')
    self['MonedaOperacion'] = Xint(el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}monto_operacion')
    self['MontoOperacion'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}activo_virtual')
    self['ActivoVirtual'] = activo_virtual0(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}hash_operacion')
    self['HashOperacion'] = el.text
    return self
def venta0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}fecha_hora_operacion')
    self['FechaHoraOperacion'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}moneda_operacion')
    self['MonedaOperacion'] = Xint(el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}monto_operacion')
    self['MontoOperacion'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}activo_virtual')
    self['ActivoVirtual'] = activo_virtual0(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}hash_operacion')
    self['HashOperacion'] = el.text
    return self
def intercambio0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}fecha_hora_operacion')
    self['FechaHoraOperacion'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}activo_virtual_enviado')
    self['ActivoVirtualEnviado'] = activo_virtual_enviado0(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}activo_virtual_recibido')
    self['ActivoVirtualRecibido'] = activo_virtual_enviado0(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}hash_operacion')
    self['HashOperacion'] = el.text
    return self
def envio0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}fecha_hora_operacion')
    self['FechaHoraOperacion'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}monto_operacion_mn')
    self['MontoOperacionMn'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}activo_virtual')
    self['ActivoVirtual'] = activo_virtual0(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}hash_operacion')
    self['HashOperacion'] = el.text
    return self
def recepcion0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}fecha_hora_operacion')
    self['FechaHoraOperacion'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}monto_operacion_mn')
    self['MontoOperacionMn'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}activo_virtual')
    self['ActivoVirtual'] = activo_virtual0(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}hash_operacion')
    self['HashOperacion'] = el.text
    return self
def retiro0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}fecha_hora_operacion')
    self['FechaHoraOperacion'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}instrumento_monetario')
    self['InstrumentoMonetario'] = catalog_code('C329_instrumento_monetario_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}moneda_operacion')
    self['MonedaOperacion'] = Xint(el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}monto_operacion')
    self['MontoOperacion'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}datos_beneficiario')
    self['DatosBeneficiario'] = datos_beneficiario0(cls, el)
    return self
def deposito0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}fecha_hora_operacion')
    self['FechaHoraOperacion'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}instrumento_monetario')
    self['InstrumentoMonetario'] = catalog_code('C329_instrumento_monetario_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}moneda_operacion')
    self['MonedaOperacion'] = Xint(el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}monto_operacion')
    self['MontoOperacion'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}datos_ordenante')
    self['DatosOrdenante'] = datos_beneficiario0(cls, el)
    return self
def activo_virtual0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}activo_virtual_operado')
    self['ActivoVirtualOperado'] = Xint(el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}descripcion_activo_virtual')
    if el is not None:
        self['DescripcionActivoVirtual'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}tipo_cambio_mn')
    self['TipoCambioMn'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}cantidad_activo_virtual')
    self['CantidadActivoVirtual'] = el.text
    return self
def activo_virtual_enviado0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}activo_virtual')
    self['ActivoVirtual'] = activo_virtual0(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}monto_operacion_mn')
    self['MontoOperacionMn'] = el.text
    return self
def datos_beneficiario0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}tipo_persona')
    self['TipoPersona'] = tipo_persona4(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}nacionalidad_cuenta')
    self['NacionalidadCuenta'] = nacionalidad_cuenta0(cls, el)
    return self
def tipo_persona4(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}persona_fisica')
    if el is not None:
        self['PersonaFisica'] = persona_fisica4(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}persona_moral')
    if el is not None:
        self['PersonaMoral'] = persona_moral4(cls, el)
    return self
def persona_fisica4(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}nombre')
    self['Nombre'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}apellido_paterno')
    self['ApellidoPaterno'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}apellido_materno')
    self['ApellidoMaterno'] = el.text
    return self
def persona_moral4(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}denominacion_razon')
    self['DenominacionRazon'] = el.text
    return self
def nacionalidad_cuenta0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}nacional')
    if el is not None:
        self['Nacional'] = nacional2(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}extranjero')
    if el is not None:
        self['Extranjero'] = extranjero2(cls, el)
    return self
def nacional2(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}clabe_destino')
    self['ClabeDestino'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}clave_institucion_financiera')
    self['ClaveInstitucionFinanciera'] = Xint(el.text)
    return self
def extranjero2(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}numero_cuenta')
    self['NumeroCuenta'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/avi}nombre_banco')
    self['NombreBanco'] = el.text
    return self
def archivo_type2(cls, node):
    self = ScalarMap()
    self['Informe'] = [informe2(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/bli}informe')]
    return self
def informe2(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/bli}mes_reportado')
    self['MesReportado'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/bli}sujeto_obligado')
    self['SujetoObligado'] = sujeto_obligado2(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/bli}aviso')
    if el is not None:
        self['Aviso'] = [aviso2(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/bli}aviso')]
    return self
def sujeto_obligado2(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/bli}clave_entidad_colegiada')
    if el is not None:
        self['ClaveEntidadColegiada'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/bli}clave_sujeto_obligado')
    self['ClaveSujetoObligado'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/bli}clave_actividad')
    self['ClaveActividad'] = catalog_code('C329_clave_actividad_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/bli}exento')
    if el is not None:
        self['Exento'] = el.text
    return self
def aviso2(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/bli}referencia_aviso')
    self['ReferenciaAviso'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/bli}modificatorio')
    if el is not None:
        self['Modificatorio'] = modificatorio2(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/bli}prioridad')
    self['Prioridad'] = catalog_code('C329_prioridad_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/bli}alerta')
    self['Alerta'] = alerta2(cls, el)
    self['PersonaAviso'] = [persona_aviso2(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/bli}persona_aviso')]
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/bli}dueno_beneficiario')
    if el is not None:
        self['DuenoBeneficiario'] = [dueno_beneficiario2(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/bli}dueno_beneficiario')]
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/bli}detalle_operaciones')
    self['DetalleOperaciones'] = detalle_operaciones2(cls, el)
    return self
def modificatorio2(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/bli}folio_modificacion')
    self['FolioModificacion'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/bli}descripcion_modificacion')
    self['DescripcionModificacion'] = el.text
    return self
def alerta2(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/bli}tipo_alerta')
    self['TipoAlerta'] = catalog_code('C329_tipo_alerta_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/bli}descripcion_alerta')
    if el is not None:
        self['DescripcionAlerta'] = el.text
    return self
def persona_aviso2(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/bli}tipo_persona')
    self['TipoPersona'] = tipo_persona5(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/bli}tipo_domicilio')
    if el is not None:
        self['TipoDomicilio'] = tipo_domicilio2(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/bli}telefono')
    if el is not None:
        self['Telefono'] = telefono2(cls, el)
    return self
def tipo_persona5(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/bli}persona_fisica')
    if el is not None:
        self['PersonaFisica'] = persona_fisica5(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/bli}persona_moral')
    if el is not None:
        self['PersonaMoral'] = persona_moral5(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/bli}fideicomiso')
    if el is not None:
        self['Fideicomiso'] = fideicomiso4(cls, el)
    return self
def persona_fisica5(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/bli}nombre')
    self['Nombre'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/bli}apellido_paterno')
    self['ApellidoPaterno'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/bli}apellido_materno')
    self['ApellidoMaterno'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/bli}fecha_nacimiento')
    if el is not None:
        self['FechaNacimiento'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/bli}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/bli}curp')
    if el is not None:
        self['Curp'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/bli}pais_nacionalidad')
    self['PaisNacionalidad'] = catalog_code('C329_pais_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/bli}actividad_economica')
    self['ActividadEconomica'] = catalog_code('C329_actividad_economica_type', el.text)
    return self
def persona_moral5(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/bli}denominacion_razon')
    self['DenominacionRazon'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/bli}fecha_constitucion')
    if el is not None:
        self['FechaConstitucion'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/bli}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/bli}pais_nacionalidad')
    self['PaisNacionalidad'] = catalog_code('C329_pais_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/bli}giro_mercantil')
    self['GiroMercantil'] = catalog_code('C329_giro_mercantil_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/bli}representante_apoderado')
    self['RepresentanteApoderado'] = representante_apoderado2(cls, el)
    return self
def fideicomiso4(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/bli}denominacion_razon')
    self['DenominacionRazon'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/bli}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/bli}identificador_fideicomiso')
    if el is not None:
        self['IdentificadorFideicomiso'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/bli}apoderado_delegado')
    self['ApoderadoDelegado'] = representante_apoderado2(cls, el)
    return self
def representante_apoderado2(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/bli}nombre')
    self['Nombre'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/bli}apellido_paterno')
    self['ApellidoPaterno'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/bli}apellido_materno')
    self['ApellidoMaterno'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/bli}fecha_nacimiento')
    if el is not None:
        self['FechaNacimiento'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/bli}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/bli}curp')
    if el is not None:
        self['Curp'] = el.text
    return self
def tipo_domicilio2(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/bli}nacional')
    if el is not None:
        self['Nacional'] = nacional3(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/bli}extranjero')
    if el is not None:
        self['Extranjero'] = extranjero3(cls, el)
    return self
def nacional3(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/bli}colonia')
    self['Colonia'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/bli}calle')
    self['Calle'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/bli}numero_exterior')
    self['NumeroExterior'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/bli}numero_interior')
    if el is not None:
        self['NumeroInterior'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/bli}codigo_postal')
    self['CodigoPostal'] = el.text
    return self
def extranjero3(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/bli}pais')
    self['Pais'] = catalog_code('C329_pais_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/bli}estado_provincia')
    self['EstadoProvincia'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/bli}ciudad_poblacion')
    self['CiudadPoblacion'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/bli}colonia')
    self['Colonia'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/bli}calle')
    self['Calle'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/bli}numero_exterior')
    self['NumeroExterior'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/bli}numero_interior')
    if el is not None:
        self['NumeroInterior'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/bli}codigo_postal')
    self['CodigoPostal'] = el.text
    return self
def telefono2(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/bli}clave_pais')
    if el is not None:
        self['ClavePais'] = catalog_code('C329_pais_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/bli}numero_telefono')
    if el is not None:
        self['NumeroTelefono'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/bli}correo_electronico')
    if el is not None:
        self['CorreoElectronico'] = el.text
    return self
def dueno_beneficiario2(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/bli}tipo_persona')
    self['TipoPersona'] = tipo_persona6(cls, el)
    return self
def tipo_persona6(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/bli}persona_fisica')
    if el is not None:
        self['PersonaFisica'] = persona_fisica6(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/bli}persona_moral')
    if el is not None:
        self['PersonaMoral'] = persona_moral6(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/bli}fideicomiso')
    if el is not None:
        self['Fideicomiso'] = fideicomiso5(cls, el)
    return self
def persona_fisica6(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/bli}nombre')
    self['Nombre'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/bli}apellido_paterno')
    self['ApellidoPaterno'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/bli}apellido_materno')
    self['ApellidoMaterno'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/bli}fecha_nacimiento')
    if el is not None:
        self['FechaNacimiento'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/bli}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/bli}curp')
    if el is not None:
        self['Curp'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/bli}pais_nacionalidad')
    if el is not None:
        self['PaisNacionalidad'] = catalog_code('C329_pais_type', el.text)
    return self
def persona_moral6(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/bli}denominacion_razon')
    self['DenominacionRazon'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/bli}fecha_constitucion')
    if el is not None:
        self['FechaConstitucion'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/bli}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/bli}pais_nacionalidad')
    if el is not None:
        self['PaisNacionalidad'] = catalog_code('C329_pais_type', el.text)
    return self
def fideicomiso5(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/bli}denominacion_razon')
    self['DenominacionRazon'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/bli}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/bli}identificador_fideicomiso')
    if el is not None:
        self['IdentificadorFideicomiso'] = el.text
    return self
def detalle_operaciones2(cls, node):
    self = ScalarMap()
    self['DatosOperacion'] = [datos_operacion1(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/bli}datos_operacion')]
    return self
def datos_operacion1(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/bli}fecha_operacion')
    self['FechaOperacion'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/bli}codigo_postal')
    self['CodigoPostal'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/bli}tipo_operacion')
    self['TipoOperacion'] = catalog_code('C329_tipo_operacion_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/bli}tipo_bien')
    self['TipoBien'] = tipo_bien0(cls, el)
    self['DatosLiquidacion'] = [datos_liquidacion1(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/bli}datos_liquidacion')]
    return self
def tipo_bien0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/bli}datos_vehiculo_terrestre')
    if el is not None:
        self['DatosVehiculoTerrestre'] = datos_vehiculo_terrestre0(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/bli}datos_inmueble')
    if el is not None:
        self['DatosInmueble'] = datos_inmueble0(cls, el)
    return self
def datos_vehiculo_terrestre0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/bli}marca_fabricante')
    self['MarcaFabricante'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/bli}modelo')
    self['Modelo'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/bli}anio')
    self['Anio'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/bli}vin')
    if el is not None:
        self['Vin'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/bli}repuve')
    if el is not None:
        self['Repuve'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/bli}placas')
    if el is not None:
        self['Placas'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/bli}estado_bien')
    self['EstadoBien'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/bli}nivel_blindaje')
    self['NivelBlindaje'] = el.text
    return self
def datos_inmueble0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/bli}tipo_inmueble')
    self['TipoInmueble'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/bli}codigo_postal')
    self['CodigoPostal'] = el.text
    self['DatosParteBlindada'] = [datos_parte_blindada0(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/bli}datos_parte_blindada')]
    return self
def datos_parte_blindada0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/bli}parte_blindada')
    self['ParteBlindada'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/bli}nivel_blindaje')
    self['NivelBlindaje'] = el.text
    return self
def datos_liquidacion1(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/bli}fecha_pago')
    self['FechaPago'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/bli}instrumento_monetario')
    self['InstrumentoMonetario'] = catalog_code('C329_instrumento_monetario_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/bli}moneda')
    self['Moneda'] = catalog_code('C329_moneda_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/bli}monto_operacion')
    self['MontoOperacion'] = el.text
    return self
def archivo_type3(cls, node):
    self = ScalarMap()
    self['Informe'] = [informe3(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/chv}informe')]
    return self
def informe3(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/chv}mes_reportado')
    self['MesReportado'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/chv}sujeto_obligado')
    self['SujetoObligado'] = sujeto_obligado3(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/chv}aviso')
    if el is not None:
        self['Aviso'] = [aviso3(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/chv}aviso')]
    return self
def sujeto_obligado3(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/chv}clave_entidad_colegiada')
    if el is not None:
        self['ClaveEntidadColegiada'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/chv}clave_sujeto_obligado')
    self['ClaveSujetoObligado'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/chv}clave_actividad')
    self['ClaveActividad'] = catalog_code('C329_clave_actividad_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/chv}exento')
    if el is not None:
        self['Exento'] = el.text
    return self
def aviso3(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/chv}referencia_aviso')
    self['ReferenciaAviso'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/chv}modificatorio')
    if el is not None:
        self['Modificatorio'] = modificatorio3(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/chv}prioridad')
    self['Prioridad'] = catalog_code('C329_prioridad_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/chv}alerta')
    self['Alerta'] = alerta3(cls, el)
    self['PersonaAviso'] = [persona_aviso3(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/chv}persona_aviso')]
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/chv}dueno_beneficiario')
    if el is not None:
        self['DuenoBeneficiario'] = [dueno_beneficiario3(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/chv}dueno_beneficiario')]
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/chv}detalle_operaciones')
    self['DetalleOperaciones'] = detalle_operaciones3(cls, el)
    return self
def modificatorio3(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/chv}folio_modificacion')
    self['FolioModificacion'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/chv}descripcion_modificacion')
    self['DescripcionModificacion'] = el.text
    return self
def alerta3(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/chv}tipo_alerta')
    self['TipoAlerta'] = catalog_code('C329_tipo_alerta_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/chv}descripcion_alerta')
    if el is not None:
        self['DescripcionAlerta'] = el.text
    return self
def persona_aviso3(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/chv}tipo_persona')
    self['TipoPersona'] = tipo_persona7(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/chv}tipo_domicilio')
    if el is not None:
        self['TipoDomicilio'] = tipo_domicilio3(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/chv}telefono')
    if el is not None:
        self['Telefono'] = telefono3(cls, el)
    return self
def tipo_persona7(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/chv}persona_fisica')
    if el is not None:
        self['PersonaFisica'] = persona_fisica7(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/chv}persona_moral')
    if el is not None:
        self['PersonaMoral'] = persona_moral7(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/chv}fideicomiso')
    if el is not None:
        self['Fideicomiso'] = fideicomiso6(cls, el)
    return self
def persona_fisica7(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/chv}nombre')
    self['Nombre'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/chv}apellido_paterno')
    self['ApellidoPaterno'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/chv}apellido_materno')
    self['ApellidoMaterno'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/chv}fecha_nacimiento')
    if el is not None:
        self['FechaNacimiento'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/chv}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/chv}curp')
    if el is not None:
        self['Curp'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/chv}pais_nacionalidad')
    self['PaisNacionalidad'] = catalog_code('C329_pais_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/chv}actividad_economica')
    self['ActividadEconomica'] = catalog_code('C329_actividad_economica_type', el.text)
    return self
def persona_moral7(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/chv}denominacion_razon')
    self['DenominacionRazon'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/chv}fecha_constitucion')
    if el is not None:
        self['FechaConstitucion'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/chv}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/chv}pais_nacionalidad')
    self['PaisNacionalidad'] = catalog_code('C329_pais_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/chv}giro_mercantil')
    self['GiroMercantil'] = catalog_code('C329_giro_mercantil_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/chv}representante_apoderado')
    self['RepresentanteApoderado'] = representante_apoderado3(cls, el)
    return self
def fideicomiso6(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/chv}denominacion_razon')
    self['DenominacionRazon'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/chv}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/chv}identificador_fideicomiso')
    if el is not None:
        self['IdentificadorFideicomiso'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/chv}apoderado_delegado')
    self['ApoderadoDelegado'] = representante_apoderado3(cls, el)
    return self
def representante_apoderado3(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/chv}nombre')
    self['Nombre'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/chv}apellido_paterno')
    self['ApellidoPaterno'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/chv}apellido_materno')
    self['ApellidoMaterno'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/chv}fecha_nacimiento')
    if el is not None:
        self['FechaNacimiento'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/chv}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/chv}curp')
    if el is not None:
        self['Curp'] = el.text
    return self
def tipo_domicilio3(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/chv}nacional')
    if el is not None:
        self['Nacional'] = nacional4(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/chv}extranjero')
    if el is not None:
        self['Extranjero'] = extranjero4(cls, el)
    return self
def nacional4(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/chv}colonia')
    self['Colonia'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/chv}calle')
    self['Calle'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/chv}numero_exterior')
    self['NumeroExterior'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/chv}numero_interior')
    if el is not None:
        self['NumeroInterior'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/chv}codigo_postal')
    self['CodigoPostal'] = el.text
    return self
def extranjero4(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/chv}pais')
    self['Pais'] = catalog_code('C329_pais_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/chv}estado_provincia')
    self['EstadoProvincia'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/chv}ciudad_poblacion')
    self['CiudadPoblacion'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/chv}colonia')
    self['Colonia'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/chv}calle')
    self['Calle'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/chv}numero_exterior')
    self['NumeroExterior'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/chv}numero_interior')
    if el is not None:
        self['NumeroInterior'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/chv}codigo_postal')
    self['CodigoPostal'] = el.text
    return self
def telefono3(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/chv}clave_pais')
    if el is not None:
        self['ClavePais'] = catalog_code('C329_pais_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/chv}numero_telefono')
    if el is not None:
        self['NumeroTelefono'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/chv}correo_electronico')
    if el is not None:
        self['CorreoElectronico'] = el.text
    return self
def dueno_beneficiario3(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/chv}tipo_persona')
    self['TipoPersona'] = tipo_persona8(cls, el)
    return self
def tipo_persona8(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/chv}persona_fisica')
    if el is not None:
        self['PersonaFisica'] = persona_fisica8(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/chv}persona_moral')
    if el is not None:
        self['PersonaMoral'] = persona_moral8(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/chv}fideicomiso')
    if el is not None:
        self['Fideicomiso'] = fideicomiso7(cls, el)
    return self
def persona_fisica8(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/chv}nombre')
    self['Nombre'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/chv}apellido_paterno')
    self['ApellidoPaterno'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/chv}apellido_materno')
    self['ApellidoMaterno'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/chv}fecha_nacimiento')
    if el is not None:
        self['FechaNacimiento'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/chv}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/chv}curp')
    if el is not None:
        self['Curp'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/chv}pais_nacionalidad')
    if el is not None:
        self['PaisNacionalidad'] = catalog_code('C329_pais_type', el.text)
    return self
def persona_moral8(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/chv}denominacion_razon')
    self['DenominacionRazon'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/chv}fecha_constitucion')
    if el is not None:
        self['FechaConstitucion'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/chv}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/chv}pais_nacionalidad')
    if el is not None:
        self['PaisNacionalidad'] = catalog_code('C329_pais_type', el.text)
    return self
def fideicomiso7(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/chv}denominacion_razon')
    self['DenominacionRazon'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/chv}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/chv}identificador_fideicomiso')
    if el is not None:
        self['IdentificadorFideicomiso'] = el.text
    return self
def detalle_operaciones3(cls, node):
    self = ScalarMap()
    self['DatosOperacion'] = [datos_operacion2(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/chv}datos_operacion')]
    return self
def datos_operacion2(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/chv}fecha_operacion')
    self['FechaOperacion'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/chv}codigo_postal')
    self['CodigoPostal'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/chv}tipo_operacion')
    self['TipoOperacion'] = catalog_code('C329_tipo_operacion_type', el.text)
    self['DatosCheque'] = [datos_cheque0(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/chv}datos_cheque')]
    self['DatosLiquidacion'] = [datos_liquidacion2(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/chv}datos_liquidacion')]
    return self
def datos_cheque0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/chv}numero_cheques')
    self['NumeroCheques'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/chv}moneda_cheques')
    self['MonedaCheques'] = el.text
    return self
def datos_liquidacion2(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/chv}fecha_pago')
    self['FechaPago'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/chv}instrumento_monetario')
    self['InstrumentoMonetario'] = catalog_code('C329_instrumento_monetario_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/chv}moneda')
    self['Moneda'] = catalog_code('C329_moneda_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/chv}monto_operacion')
    self['MontoOperacion'] = el.text
    return self
def archivo_type4(cls, node):
    self = ScalarMap()
    self['Informe'] = [informe4(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/din}informe')]
    return self
def informe4(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/din}mes_reportado')
    self['MesReportado'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/din}sujeto_obligado')
    self['SujetoObligado'] = sujeto_obligado4(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/din}aviso')
    if el is not None:
        self['Aviso'] = [aviso4(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/din}aviso')]
    return self
def sujeto_obligado4(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/din}clave_entidad_colegiada')
    if el is not None:
        self['ClaveEntidadColegiada'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/din}clave_sujeto_obligado')
    self['ClaveSujetoObligado'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/din}clave_actividad')
    self['ClaveActividad'] = catalog_code('C329_clave_actividad_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/din}exento')
    if el is not None:
        self['Exento'] = el.text
    return self
def aviso4(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/din}referencia_aviso')
    self['ReferenciaAviso'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/din}modificatorio')
    if el is not None:
        self['Modificatorio'] = modificatorio4(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/din}prioridad')
    self['Prioridad'] = catalog_code('C329_prioridad_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/din}alerta')
    self['Alerta'] = alerta4(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/din}detalle_operaciones')
    self['DetalleOperaciones'] = detalle_operaciones4(cls, el)
    return self
def modificatorio4(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/din}folio_modificacion')
    self['FolioModificacion'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/din}descripcion_modificacion')
    self['DescripcionModificacion'] = el.text
    return self
def alerta4(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/din}tipo_alerta')
    self['TipoAlerta'] = catalog_code('C329_tipo_alerta_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/din}descripcion_alerta')
    if el is not None:
        self['DescripcionAlerta'] = el.text
    return self
def detalle_operaciones4(cls, node):
    self = ScalarMap()
    self['DatosOperacion'] = [datos_operacion3(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/din}datos_operacion')]
    return self
def datos_operacion3(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/din}tipo_operacion')
    self['TipoOperacion'] = catalog_code('C329_tipo_operacion_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/din}desarrollos_inmobiliarios')
    self['DesarrollosInmobiliarios'] = desarrollos_inmobiliarios0(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/din}aportaciones')
    self['Aportaciones'] = aportaciones0(cls, el)
    return self
def desarrollos_inmobiliarios0(cls, node):
    self = ScalarMap()
    self['DatosDesarrollo'] = [datos_desarrollo0(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/din}datos_desarrollo')]
    return self
def datos_desarrollo0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/din}objeto_aviso_anterior')
    self['ObjetoAvisoAnterior'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/din}modificacion')
    self['Modificacion'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/din}entidad_federativa')
    self['EntidadFederativa'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/din}registro_licencia')
    self['RegistroLicencia'] = el.text
    self['CaracteristicasDesarrollo'] = [caracteristicas_desarrollo0(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/din}caracteristicas_desarrollo')]
    return self
def caracteristicas_desarrollo0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/din}codigo_postal')
    self['CodigoPostal'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/din}colonia')
    self['Colonia'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/din}calle')
    self['Calle'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/din}tipo_desarrollo')
    self['TipoDesarrollo'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/din}descripcion_desarrollo')
    if el is not None:
        self['DescripcionDesarrollo'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/din}monto_desarrollo')
    self['MontoDesarrollo'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/din}unidades_comercializadas')
    self['UnidadesComercializadas'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/din}costo_unidad')
    self['CostoUnidad'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/din}otras_empresas')
    self['OtrasEmpresas'] = el.text
    return self
def aportaciones0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/din}fecha_aportacion')
    if el is not None:
        self['FechaAportacion'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/din}tipo_aportacion')
    if el is not None:
        self['TipoAportacion'] = [tipo_aportacion0(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/din}tipo_aportacion')]
    return self
def tipo_aportacion0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/din}recursos_propios')
    if el is not None:
        self['RecursosPropios'] = recursos_propios0(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/din}socios')
    if el is not None:
        self['Socios'] = socios0(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/din}terceros')
    if el is not None:
        self['Terceros'] = terceros0(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/din}prestamo_financiero')
    if el is not None:
        self['PrestamoFinanciero'] = prestamo_financiero0(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/din}prestamo_no_financiero')
    if el is not None:
        self['PrestamoNoFinanciero'] = prestamo_no_financiero0(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/din}financiamiento_bursatil')
    if el is not None:
        self['FinanciamientoBursatil'] = financiamiento_bursatil0(cls, el)
    return self
def recursos_propios0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/din}datos_aportacion')
    if el is not None:
        self['DatosAportacion'] = [datos_aportacion0(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/din}datos_aportacion')]
    return self
def datos_aportacion0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/din}aportacion_numerario')
    if el is not None:
        self['AportacionNumerario'] = aportacion_numerario0(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/din}aportacion_especie')
    if el is not None:
        self['AportacionEspecie'] = aportacion_especie0(cls, el)
    return self
def aportacion_numerario0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/din}instrumento_monetario')
    if el is not None:
        self['InstrumentoMonetario'] = catalog_code('C329_instrumento_monetario_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/din}moneda')
    if el is not None:
        self['Moneda'] = catalog_code('C329_moneda_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/din}monto_aportacion')
    if el is not None:
        self['MontoAportacion'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/din}aportacion_fideicomiso')
    if el is not None:
        self['AportacionFideicomiso'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/din}nombre_institucion')
    if el is not None:
        self['NombreInstitucion'] = el.text
    return self
def aportacion_especie0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/din}descripcion_bien')
    if el is not None:
        self['DescripcionBien'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/din}monto_estimado')
    if el is not None:
        self['MontoEstimado'] = el.text
    return self
def socios0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/din}numero_socios')
    if el is not None:
        self['NumeroSocios'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/din}detalle_socios')
    self['DetalleSocios'] = detalle_socios0(cls, el)
    return self
def detalle_socios0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/din}datos_socio')
    if el is not None:
        self['DatosSocio'] = [datos_socio0(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/din}datos_socio')]
    return self
def datos_socio0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/din}aportacion_anterior_socio')
    if el is not None:
        self['AportacionAnteriorSocio'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/din}rfc_socio')
    if el is not None:
        self['RfcSocio'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/din}tipo_persona_socio')
    self['TipoPersonaSocio'] = tipo_persona_socio0(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/din}tipo_domicilio_socio')
    self['TipoDomicilioSocio'] = tipo_domicilio_socio0(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/din}telefono')
    if el is not None:
        self['Telefono'] = telefono4(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/din}detalle_aportaciones')
    self['DetalleAportaciones'] = detalle_aportaciones0(cls, el)
    return self
def tipo_persona_socio0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/din}persona_fisica')
    if el is not None:
        self['PersonaFisica'] = persona_fisica9(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/din}persona_moral')
    if el is not None:
        self['PersonaMoral'] = persona_moral9(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/din}fideicomiso')
    if el is not None:
        self['Fideicomiso'] = fideicomiso8(cls, el)
    return self
def persona_fisica9(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/din}nombre')
    if el is not None:
        self['Nombre'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/din}apellido_paterno')
    if el is not None:
        self['ApellidoPaterno'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/din}apellido_materno')
    if el is not None:
        self['ApellidoMaterno'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/din}fecha_nacimiento')
    if el is not None:
        self['FechaNacimiento'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/din}curp')
    if el is not None:
        self['Curp'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/din}pais_nacionalidad')
    if el is not None:
        self['PaisNacionalidad'] = catalog_code('C329_pais_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/din}actividad_economica')
    if el is not None:
        self['ActividadEconomica'] = catalog_code('C329_actividad_economica_type', el.text)
    return self
def persona_moral9(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/din}denominacion_razon')
    if el is not None:
        self['DenominacionRazon'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/din}fecha_constitucion')
    if el is not None:
        self['FechaConstitucion'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/din}pais_nacionalidad')
    if el is not None:
        self['PaisNacionalidad'] = catalog_code('C329_pais_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/din}giro_mercantil')
    if el is not None:
        self['GiroMercantil'] = catalog_code('C329_giro_mercantil_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/din}representante_apoderado')
    self['RepresentanteApoderado'] = representante_apoderado4(cls, el)
    return self
def representante_apoderado4(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/din}nombre')
    if el is not None:
        self['Nombre'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/din}apellido_paterno')
    if el is not None:
        self['ApellidoPaterno'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/din}apellido_materno')
    if el is not None:
        self['ApellidoMaterno'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/din}fecha_nacimiento')
    if el is not None:
        self['FechaNacimiento'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/din}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/din}curp')
    if el is not None:
        self['Curp'] = el.text
    return self
def tipo_domicilio_socio0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/din}nacional')
    if el is not None:
        self['Nacional'] = nacional5(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/din}extranjero')
    if el is not None:
        self['Extranjero'] = extranjero5(cls, el)
    return self
def nacional5(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/din}colonia')
    if el is not None:
        self['Colonia'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/din}calle')
    if el is not None:
        self['Calle'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/din}numero_exterior')
    if el is not None:
        self['NumeroExterior'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/din}numero_interior')
    if el is not None:
        self['NumeroInterior'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/din}codigo_postal')
    if el is not None:
        self['CodigoPostal'] = el.text
    return self
def extranjero5(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/din}pais')
    if el is not None:
        self['Pais'] = catalog_code('C329_pais_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/din}estado_provincia')
    if el is not None:
        self['EstadoProvincia'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/din}ciudad_poblacion')
    if el is not None:
        self['CiudadPoblacion'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/din}colonia')
    if el is not None:
        self['Colonia'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/din}calle')
    if el is not None:
        self['Calle'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/din}numero_exterior')
    if el is not None:
        self['NumeroExterior'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/din}numero_interior')
    if el is not None:
        self['NumeroInterior'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/din}codigo_postal')
    if el is not None:
        self['CodigoPostal'] = el.text
    return self
def telefono4(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/din}clave_pais')
    if el is not None:
        self['ClavePais'] = catalog_code('C329_pais_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/din}numero_telefono')
    if el is not None:
        self['NumeroTelefono'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/din}correo_electronico')
    if el is not None:
        self['CorreoElectronico'] = el.text
    return self
def detalle_aportaciones0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/din}datos_aportacion')
    self['DatosAportacion'] = datos_aportacion1(cls, el)
    return self
def datos_aportacion1(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/din}aportacion_numerario')
    if el is not None:
        self['AportacionNumerario'] = aportacion_numerario0(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/din}aportacion_especie')
    if el is not None:
        self['AportacionEspecie'] = aportacion_especie0(cls, el)
    return self
def terceros0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/din}numero_terceros')
    if el is not None:
        self['NumeroTerceros'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/din}detalle_terceros')
    self['DetalleTerceros'] = detalle_terceros0(cls, el)
    return self
def detalle_terceros0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/din}datos_tercero')
    if el is not None:
        self['DatosTercero'] = [datos_tercero0(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/din}datos_tercero')]
    return self
def datos_tercero0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/din}tipo_tercero')
    if el is not None:
        self['TipoTercero'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/din}descripcion_tercero')
    if el is not None:
        self['DescripcionTercero'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/din}tipo_persona_tercero')
    self['TipoPersonaTercero'] = tipo_persona_tercero0(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/din}detalle_aportaciones')
    self['DetalleAportaciones'] = detalle_aportaciones1(cls, el)
    return self
def tipo_persona_tercero0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/din}persona_fisica')
    if el is not None:
        self['PersonaFisica'] = persona_fisicaa(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/din}persona_moral')
    if el is not None:
        self['PersonaMoral'] = persona_morala(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/din}fideicomiso')
    if el is not None:
        self['Fideicomiso'] = fideicomiso8(cls, el)
    return self
def persona_fisicaa(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/din}nombre')
    if el is not None:
        self['Nombre'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/din}apellido_paterno')
    if el is not None:
        self['ApellidoPaterno'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/din}apellido_materno')
    if el is not None:
        self['ApellidoMaterno'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/din}fecha_nacimiento')
    if el is not None:
        self['FechaNacimiento'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/din}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/din}curp')
    if el is not None:
        self['Curp'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/din}pais_nacionalidad')
    if el is not None:
        self['PaisNacionalidad'] = catalog_code('C329_pais_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/din}actividad_economica')
    if el is not None:
        self['ActividadEconomica'] = catalog_code('C329_actividad_economica_type', el.text)
    return self
def persona_morala(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/din}denominacion_razon')
    if el is not None:
        self['DenominacionRazon'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/din}fecha_constitucion')
    if el is not None:
        self['FechaConstitucion'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/din}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/din}pais_nacionalidad')
    if el is not None:
        self['PaisNacionalidad'] = catalog_code('C329_pais_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/din}giro_mercantil')
    if el is not None:
        self['GiroMercantil'] = catalog_code('C329_giro_mercantil_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/din}representante_apoderado')
    self['RepresentanteApoderado'] = representante_apoderado4(cls, el)
    return self
def fideicomiso8(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/din}denominacion_razon')
    if el is not None:
        self['DenominacionRazon'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/din}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/din}identificador_fideicomiso')
    if el is not None:
        self['IdentificadorFideicomiso'] = el.text
    return self
def detalle_aportaciones1(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/din}datos_aportacion')
    self['DatosAportacion'] = datos_aportacion2(cls, el)
    return self
def datos_aportacion2(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/din}aportacion_numerario')
    if el is not None:
        self['AportacionNumerario'] = aportacion_numerario1(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/din}aportacion_especie')
    if el is not None:
        self['AportacionEspecie'] = aportacion_especie0(cls, el)
    return self
def aportacion_numerario1(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/din}instrumento_monetario')
    if el is not None:
        self['InstrumentoMonetario'] = catalog_code('C329_instrumento_monetario_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/din}moneda')
    if el is not None:
        self['Moneda'] = catalog_code('C329_moneda_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/din}monto_aportacion')
    if el is not None:
        self['MontoAportacion'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/din}aportacion_fideicomiso')
    if el is not None:
        self['AportacionFideicomiso'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/din}nombre_institucion')
    if el is not None:
        self['NombreInstitucion'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/din}valor_inmueble_preventa')
    if el is not None:
        self['ValorInmueblePreventa'] = el.text
    return self
def prestamo_financiero0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/din}datos_prestamo')
    if el is not None:
        self['DatosPrestamo'] = [datos_prestamo0(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/din}datos_prestamo')]
    return self
def datos_prestamo0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/din}tipo_institucion')
    if el is not None:
        self['TipoInstitucion'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/din}institucion')
    if el is not None:
        self['Institucion'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/din}tipo_credito')
    if el is not None:
        self['TipoCredito'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/din}monto_prestamo')
    if el is not None:
        self['MontoPrestamo'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/din}moneda')
    if el is not None:
        self['Moneda'] = catalog_code('C329_moneda_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/din}plazo_meses')
    if el is not None:
        self['PlazoMeses'] = el.text
    return self
def prestamo_no_financiero0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/din}datos_prestamo')
    if el is not None:
        self['DatosPrestamo'] = [datos_prestamo1(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/din}datos_prestamo')]
    return self
def datos_prestamo1(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/din}monto_prestamo')
    if el is not None:
        self['MontoPrestamo'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/din}moneda')
    if el is not None:
        self['Moneda'] = catalog_code('C329_moneda_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/din}plazo_meses')
    if el is not None:
        self['PlazoMeses'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/din}detalle_acreedores')
    self['DetalleAcreedores'] = detalle_acreedores0(cls, el)
    return self
def detalle_acreedores0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/din}tipo_persona_acreedor')
    if el is not None:
        self['TipoPersonaAcreedor'] = [tipo_persona_tercero0(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/din}tipo_persona_acreedor')]
    return self
def financiamiento_bursatil0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/din}fecha_emision')
    if el is not None:
        self['FechaEmision'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/din}monto_solicitado')
    if el is not None:
        self['MontoSolicitado'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/din}monto_recibido')
    if el is not None:
        self['MontoRecibido'] = el.text
    return self
def archivo_type5(cls, node):
    self = ScalarMap()
    self['Informe'] = [informe5(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/don}informe')]
    return self
def informe5(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/don}mes_reportado')
    self['MesReportado'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/don}sujeto_obligado')
    self['SujetoObligado'] = sujeto_obligado5(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/don}aviso')
    if el is not None:
        self['Aviso'] = [aviso5(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/don}aviso')]
    return self
def sujeto_obligado5(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/don}clave_entidad_colegiada')
    if el is not None:
        self['ClaveEntidadColegiada'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/don}clave_sujeto_obligado')
    self['ClaveSujetoObligado'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/don}clave_actividad')
    self['ClaveActividad'] = catalog_code('C329_clave_actividad_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/don}exento')
    if el is not None:
        self['Exento'] = el.text
    return self
def aviso5(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/don}referencia_aviso')
    self['ReferenciaAviso'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/don}modificatorio')
    if el is not None:
        self['Modificatorio'] = modificatorio5(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/don}prioridad')
    self['Prioridad'] = catalog_code('C329_prioridad_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/don}alerta')
    self['Alerta'] = alerta5(cls, el)
    self['PersonaAviso'] = [persona_aviso4(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/don}persona_aviso')]
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/don}dueno_beneficiario')
    if el is not None:
        self['DuenoBeneficiario'] = [dueno_beneficiario4(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/don}dueno_beneficiario')]
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/don}detalle_operaciones')
    self['DetalleOperaciones'] = detalle_operaciones5(cls, el)
    return self
def modificatorio5(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/don}folio_modificacion')
    self['FolioModificacion'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/don}descripcion_modificacion')
    self['DescripcionModificacion'] = el.text
    return self
def alerta5(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/don}tipo_alerta')
    self['TipoAlerta'] = catalog_code('C329_tipo_alerta_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/don}descripcion_alerta')
    if el is not None:
        self['DescripcionAlerta'] = el.text
    return self
def persona_aviso4(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/don}tipo_persona')
    self['TipoPersona'] = tipo_persona9(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/don}tipo_domicilio')
    if el is not None:
        self['TipoDomicilio'] = tipo_domicilio4(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/don}telefono')
    if el is not None:
        self['Telefono'] = telefono5(cls, el)
    return self
def tipo_persona9(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/don}persona_fisica')
    if el is not None:
        self['PersonaFisica'] = persona_fisicab(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/don}persona_moral')
    if el is not None:
        self['PersonaMoral'] = persona_moralb(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/don}fideicomiso')
    if el is not None:
        self['Fideicomiso'] = fideicomiso9(cls, el)
    return self
def persona_fisicab(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/don}nombre')
    self['Nombre'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/don}apellido_paterno')
    self['ApellidoPaterno'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/don}apellido_materno')
    self['ApellidoMaterno'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/don}fecha_nacimiento')
    if el is not None:
        self['FechaNacimiento'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/don}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/don}curp')
    if el is not None:
        self['Curp'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/don}pais_nacionalidad')
    self['PaisNacionalidad'] = catalog_code('C329_pais_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/don}actividad_economica')
    self['ActividadEconomica'] = catalog_code('C329_actividad_economica_type', el.text)
    return self
def persona_moralb(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/don}denominacion_razon')
    self['DenominacionRazon'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/don}fecha_constitucion')
    if el is not None:
        self['FechaConstitucion'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/don}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/don}pais_nacionalidad')
    self['PaisNacionalidad'] = catalog_code('C329_pais_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/don}giro_mercantil')
    self['GiroMercantil'] = catalog_code('C329_giro_mercantil_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/don}representante_apoderado')
    self['RepresentanteApoderado'] = representante_apoderado5(cls, el)
    return self
def fideicomiso9(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/don}denominacion_razon')
    self['DenominacionRazon'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/don}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/don}identificador_fideicomiso')
    if el is not None:
        self['IdentificadorFideicomiso'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/don}apoderado_delegado')
    self['ApoderadoDelegado'] = representante_apoderado5(cls, el)
    return self
def representante_apoderado5(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/don}nombre')
    self['Nombre'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/don}apellido_paterno')
    self['ApellidoPaterno'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/don}apellido_materno')
    self['ApellidoMaterno'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/don}fecha_nacimiento')
    if el is not None:
        self['FechaNacimiento'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/don}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/don}curp')
    if el is not None:
        self['Curp'] = el.text
    return self
def tipo_domicilio4(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/don}nacional')
    if el is not None:
        self['Nacional'] = nacional6(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/don}extranjero')
    if el is not None:
        self['Extranjero'] = extranjero6(cls, el)
    return self
def nacional6(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/don}colonia')
    self['Colonia'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/don}calle')
    self['Calle'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/don}numero_exterior')
    self['NumeroExterior'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/don}numero_interior')
    if el is not None:
        self['NumeroInterior'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/don}codigo_postal')
    self['CodigoPostal'] = el.text
    return self
def extranjero6(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/don}pais')
    self['Pais'] = catalog_code('C329_pais_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/don}estado_provincia')
    self['EstadoProvincia'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/don}ciudad_poblacion')
    self['CiudadPoblacion'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/don}colonia')
    self['Colonia'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/don}calle')
    self['Calle'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/don}numero_exterior')
    self['NumeroExterior'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/don}numero_interior')
    if el is not None:
        self['NumeroInterior'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/don}codigo_postal')
    self['CodigoPostal'] = el.text
    return self
def telefono5(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/don}clave_pais')
    if el is not None:
        self['ClavePais'] = catalog_code('C329_pais_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/don}numero_telefono')
    if el is not None:
        self['NumeroTelefono'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/don}correo_electronico')
    if el is not None:
        self['CorreoElectronico'] = el.text
    return self
def dueno_beneficiario4(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/don}tipo_persona')
    self['TipoPersona'] = tipo_personaa(cls, el)
    return self
def tipo_personaa(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/don}persona_fisica')
    if el is not None:
        self['PersonaFisica'] = persona_fisicac(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/don}persona_moral')
    if el is not None:
        self['PersonaMoral'] = persona_moralc(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/don}fideicomiso')
    if el is not None:
        self['Fideicomiso'] = fideicomisoa(cls, el)
    return self
def persona_fisicac(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/don}nombre')
    self['Nombre'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/don}apellido_paterno')
    self['ApellidoPaterno'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/don}apellido_materno')
    self['ApellidoMaterno'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/don}fecha_nacimiento')
    if el is not None:
        self['FechaNacimiento'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/don}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/don}curp')
    if el is not None:
        self['Curp'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/don}pais_nacionalidad')
    if el is not None:
        self['PaisNacionalidad'] = catalog_code('C329_pais_type', el.text)
    return self
def persona_moralc(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/don}denominacion_razon')
    self['DenominacionRazon'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/don}fecha_constitucion')
    if el is not None:
        self['FechaConstitucion'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/don}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/don}pais_nacionalidad')
    if el is not None:
        self['PaisNacionalidad'] = catalog_code('C329_pais_type', el.text)
    return self
def fideicomisoa(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/don}denominacion_razon')
    self['DenominacionRazon'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/don}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/don}identificador_fideicomiso')
    if el is not None:
        self['IdentificadorFideicomiso'] = el.text
    return self
def detalle_operaciones5(cls, node):
    self = ScalarMap()
    self['DatosOperacion'] = [datos_operacion4(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/don}datos_operacion')]
    return self
def datos_operacion4(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/don}fecha_operacion')
    self['FechaOperacion'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/don}codigo_postal')
    self['CodigoPostal'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/don}tipo_operacion')
    self['TipoOperacion'] = catalog_code('C329_tipo_operacion_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/don}datos_donativo')
    self['DatosDonativo'] = datos_donativo0(cls, el)
    return self
def datos_donativo0(cls, node):
    self = ScalarMap()
    self['TipoDonativo'] = [tipo_donativo0(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/don}tipo_donativo')]
    return self
def tipo_donativo0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/don}liquidacion_numerario')
    if el is not None:
        self['LiquidacionNumerario'] = liquidacion_numerario0(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/don}liquidacion_especie')
    if el is not None:
        self['LiquidacionEspecie'] = liquidacion_especie0(cls, el)
    return self
def liquidacion_numerario0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/don}fecha_pago')
    self['FechaPago'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/don}instrumento_monetario')
    self['InstrumentoMonetario'] = catalog_code('C329_instrumento_monetario_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/don}moneda')
    self['Moneda'] = catalog_code('C329_moneda_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/don}monto_operacion')
    self['MontoOperacion'] = el.text
    return self
def liquidacion_especie0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/don}monto_operacion')
    self['MontoOperacion'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/don}moneda')
    self['Moneda'] = catalog_code('C329_moneda_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/don}bien_donado')
    self['BienDonado'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/don}datos_bien_donado')
    if el is not None:
        self['DatosBienDonado'] = datos_bien_donado0(cls, el)
    return self
def datos_bien_donado0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/don}datos_inmueble')
    if el is not None:
        self['DatosInmueble'] = datos_inmueble1(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/don}datos_otro')
    if el is not None:
        self['DatosOtro'] = datos_otro0(cls, el)
    return self
def datos_inmueble1(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/don}tipo_inmueble')
    self['TipoInmueble'] = catalog_code('C329_tipo_inmueble_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/don}codigo_postal')
    self['CodigoPostal'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/don}folio_real')
    self['FolioReal'] = el.text
    return self
def datos_otro0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/don}descripcion_bien_donado')
    self['DescripcionBienDonado'] = el.text
    return self
def tipo_persona_1_type0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}tipo_movimiento_fideicomisario')
    self['TipoMovimientoFideicomisario'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}persona_fisica')
    if el is not None:
        self['PersonaFisica'] = persona_fisicad(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}persona_moral')
    if el is not None:
        self['PersonaMoral'] = persona_morald(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}fideicomiso')
    if el is not None:
        self['Fideicomiso'] = fideicomisob(cls, el)
    return self
def archivo_type6(cls, node):
    self = ScalarMap()
    self['Informe'] = [informe6(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/fep}informe')]
    return self
def informe6(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}mes_reportado')
    self['MesReportado'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}sujeto_obligado')
    self['SujetoObligado'] = sujeto_obligado6(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}aviso')
    if el is not None:
        self['Aviso'] = [aviso6(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/fep}aviso')]
    return self
def sujeto_obligado6(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}clave_entidad_colegiada')
    if el is not None:
        self['ClaveEntidadColegiada'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}clave_sujeto_obligado')
    self['ClaveSujetoObligado'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}clave_actividad')
    self['ClaveActividad'] = catalog_code('C329_clave_actividad_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}exento')
    if el is not None:
        self['Exento'] = el.text
    return self
def aviso6(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}referencia_aviso')
    self['ReferenciaAviso'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}modificatorio')
    if el is not None:
        self['Modificatorio'] = modificatorio6(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}prioridad')
    self['Prioridad'] = catalog_code('C329_prioridad_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}alerta')
    self['Alerta'] = alerta6(cls, el)
    self['PersonaAviso'] = [persona_aviso5(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/fep}persona_aviso')]
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}detalle_operaciones')
    self['DetalleOperaciones'] = detalle_operaciones6(cls, el)
    return self
def modificatorio6(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}folio_modificacion')
    self['FolioModificacion'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}descripcion_modificacion')
    self['DescripcionModificacion'] = el.text
    return self
def alerta6(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}tipo_alerta')
    self['TipoAlerta'] = catalog_code('C329_tipo_alerta_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}descripcion_alerta')
    if el is not None:
        self['DescripcionAlerta'] = el.text
    return self
def persona_aviso5(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}nombre')
    self['Nombre'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}apellido_paterno')
    self['ApellidoPaterno'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}apellido_materno')
    self['ApellidoMaterno'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}fecha_nacimiento')
    if el is not None:
        self['FechaNacimiento'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}curp')
    if el is not None:
        self['Curp'] = el.text
    return self
def detalle_operaciones6(cls, node):
    self = ScalarMap()
    self['DatosOperacion'] = [datos_operacion5(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/fep}datos_operacion')]
    return self
def datos_operacion5(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}instrumento_publico')
    self['InstrumentoPublico'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}fecha_operacion')
    self['FechaOperacion'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}tipo_actividad')
    self['TipoActividad'] = tipo_actividad0(cls, el)
    return self
def tipo_actividad0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}otorgamiento_poder')
    if el is not None:
        self['OtorgamientoPoder'] = otorgamiento_poder0(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}constitucion_personas_morales')
    if el is not None:
        self['ConstitucionPersonasMorales'] = constitucion_personas_morales0(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}modificacion_patrimonial')
    if el is not None:
        self['ModificacionPatrimonial'] = modificacion_patrimonial0(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}fusion')
    if el is not None:
        self['Fusion'] = fusion0(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}escision')
    if el is not None:
        self['Escision'] = escision0(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}compra_venta_acciones')
    if el is not None:
        self['CompraVentaAcciones'] = compra_venta_acciones0(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}constitucion_modificacion_fideicomiso')
    if el is not None:
        self['ConstitucionModificacionFideicomiso'] = constitucion_modificacion_fideicomiso0(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}cesion_derechos_fideicomitente_fideicomisario')
    if el is not None:
        self['CesionDerechosFideicomitenteFideicomisario'] = cesion_derechos_fideicomitente_fideicomisario0(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}contrato_mutuo_credito')
    if el is not None:
        self['ContratoMutuoCredito'] = contrato_mutuo_credito0(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}avaluo')
    if el is not None:
        self['Avaluo'] = avaluo0(cls, el)
    return self
def otorgamiento_poder0(cls, node):
    self = ScalarMap()
    self['DatosPoderdante'] = [datos_poderdante0(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/fep}datos_poderdante')]
    self['DatosApoderado'] = [datos_apoderado0(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/fep}datos_apoderado')]
    return self
def datos_poderdante0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}tipo_persona')
    self['TipoPersona'] = tipo_personab(cls, el)
    return self
def datos_apoderado0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}tipo_poder')
    self['TipoPoder'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}tipo_persona')
    self['TipoPersona'] = tipo_personac(cls, el)
    return self
def tipo_personab(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}persona_fisica')
    if el is not None:
        self['PersonaFisica'] = persona_fisicad(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}persona_moral')
    if el is not None:
        self['PersonaMoral'] = persona_morald(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}fideicomiso')
    if el is not None:
        self['Fideicomiso'] = fideicomisob(cls, el)
    return self
def persona_fisicad(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}nombre')
    self['Nombre'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}apellido_paterno')
    self['ApellidoPaterno'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}apellido_materno')
    self['ApellidoMaterno'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}fecha_nacimiento')
    if el is not None:
        self['FechaNacimiento'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}curp')
    if el is not None:
        self['Curp'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}pais_nacionalidad')
    self['PaisNacionalidad'] = catalog_code('C329_pais_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}actividad_economica')
    self['ActividadEconomica'] = catalog_code('C329_actividad_economica_type', el.text)
    return self
def persona_morald(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}denominacion_razon')
    self['DenominacionRazon'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}fecha_constitucion')
    if el is not None:
        self['FechaConstitucion'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}pais_nacionalidad')
    self['PaisNacionalidad'] = catalog_code('C329_pais_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}giro_mercantil')
    self['GiroMercantil'] = catalog_code('C329_giro_mercantil_type', el.text)
    return self
def fideicomisob(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}denominacion_razon')
    self['DenominacionRazon'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}identificador_fideicomiso')
    if el is not None:
        self['IdentificadorFideicomiso'] = el.text
    return self
def tipo_personac(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}persona_fisica')
    if el is not None:
        self['PersonaFisica'] = persona_fisicae(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}persona_moral')
    if el is not None:
        self['PersonaMoral'] = persona_morale(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}fideicomiso')
    if el is not None:
        self['Fideicomiso'] = fideicomisob(cls, el)
    return self
def persona_morale(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}denominacion_razon')
    self['DenominacionRazon'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}fecha_constitucion')
    if el is not None:
        self['FechaConstitucion'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}pais_nacionalidad')
    self['PaisNacionalidad'] = catalog_code('C329_pais_type', el.text)
    return self
def persona_fisicae(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}nombre')
    self['Nombre'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}apellido_paterno')
    self['ApellidoPaterno'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}apellido_materno')
    self['ApellidoMaterno'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}fecha_nacimiento')
    if el is not None:
        self['FechaNacimiento'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}curp')
    if el is not None:
        self['Curp'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}pais_nacionalidad')
    self['PaisNacionalidad'] = catalog_code('C329_pais_type', el.text)
    return self
def constitucion_personas_morales0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}tipo_persona_moral')
    self['TipoPersonaMoral'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}tipo_persona_moral_otra')
    if el is not None:
        self['TipoPersonaMoralOtra'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}denominacion_razon')
    self['DenominacionRazon'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}giro_mercantil')
    self['GiroMercantil'] = catalog_code('C329_giro_mercantil_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}folio_mercantil')
    if el is not None:
        self['FolioMercantil'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}numero_total_acciones')
    self['NumeroTotalAcciones'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}entidad_federativa')
    self['EntidadFederativa'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}consejo_vigilancia')
    self['ConsejoVigilancia'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}motivo_constitucion')
    self['MotivoConstitucion'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}instrumento_publico')
    if el is not None:
        self['InstrumentoPublico'] = el.text
    self['DatosAccionista'] = [datos_accionista0(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/fep}datos_accionista')]
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}capital_social')
    self['CapitalSocial'] = capital_social0(cls, el)
    return self
def datos_accionista0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}cargo_accionista')
    self['CargoAccionista'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}tipo_persona')
    self['TipoPersona'] = tipo_personac(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}numero_acciones')
    self['NumeroAcciones'] = el.text
    return self
def capital_social0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}capital_fijo')
    self['CapitalFijo'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}capital_variable')
    if el is not None:
        self['CapitalVariable'] = el.text
    return self
def modificacion_patrimonial0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}persona_moral_modifica')
    self['PersonaMoralModifica'] = persona_moral_modifica0(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}datos_modificacion')
    self['DatosModificacion'] = datos_modificacion0(cls, el)
    return self
def persona_moral_modifica0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}denominacion_razon')
    self['DenominacionRazon'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}fecha_constitucion')
    if el is not None:
        self['FechaConstitucion'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}pais_nacionalidad')
    self['PaisNacionalidad'] = catalog_code('C329_pais_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}giro_mercantil')
    self['GiroMercantil'] = catalog_code('C329_giro_mercantil_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}numero_total_acciones')
    self['NumeroTotalAcciones'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}motivo_modificacion')
    self['MotivoModificacion'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}instrumento_publico')
    if el is not None:
        self['InstrumentoPublico'] = el.text
    return self
def datos_modificacion0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}tipo_modificacion_capital_fijo')
    self['TipoModificacionCapitalFijo'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}inicial_capital_fijo')
    self['InicialCapitalFijo'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}final_capital_fijo')
    self['FinalCapitalFijo'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}tipo_modificacion_capital_variable')
    self['TipoModificacionCapitalVariable'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}inicial_capital_variable')
    self['InicialCapitalVariable'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}final_capital_variable')
    self['FinalCapitalVariable'] = el.text
    self['DatosAccionista'] = [datos_accionista1(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/fep}datos_accionista')]
    return self
def datos_accionista1(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}tipo_persona')
    self['TipoPersona'] = tipo_personac(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}numero_acciones')
    self['NumeroAcciones'] = el.text
    return self
def fusion0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}tipo_fusion')
    self['TipoFusion'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}datos_fusionadas')
    self['DatosFusionadas'] = datos_fusionadas0(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}datos_fusionante')
    self['DatosFusionante'] = datos_fusionante0(cls, el)
    return self
def datos_fusionadas0(cls, node):
    self = ScalarMap()
    self['DatosFusionada'] = [datos_fusionada0(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/fep}datos_fusionada')]
    return self
def datos_fusionada0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}denominacion_razon')
    self['DenominacionRazon'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}fecha_constitucion')
    if el is not None:
        self['FechaConstitucion'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}pais_nacionalidad')
    self['PaisNacionalidad'] = catalog_code('C329_pais_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}giro_mercantil')
    self['GiroMercantil'] = catalog_code('C329_giro_mercantil_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}capital_social_fijo')
    self['CapitalSocialFijo'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}capital_social_variable')
    if el is not None:
        self['CapitalSocialVariable'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}folio_mercantil')
    if el is not None:
        self['FolioMercantil'] = el.text
    return self
def datos_fusionante0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}fusionante_determinadas')
    self['FusionanteDeterminadas'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}fusionante')
    if el is not None:
        self['Fusionante'] = fusionante0(cls, el)
    return self
def fusionante0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}denominacion_razon')
    self['DenominacionRazon'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}fecha_constitucion')
    if el is not None:
        self['FechaConstitucion'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}pais_nacionalidad')
    self['PaisNacionalidad'] = catalog_code('C329_pais_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}giro_mercantil')
    self['GiroMercantil'] = catalog_code('C329_giro_mercantil_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}capital_social_fijo')
    self['CapitalSocialFijo'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}capital_social_variable')
    if el is not None:
        self['CapitalSocialVariable'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}folio_mercantil')
    if el is not None:
        self['FolioMercantil'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}numero_total_acciones')
    self['NumeroTotalAcciones'] = el.text
    self['DatosAccionista'] = [datos_accionista1(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/fep}datos_accionista')]
    return self
def escision0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}datos_escindente')
    self['DatosEscindente'] = datos_escindente0(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}datos_escindidas')
    self['DatosEscindidas'] = datos_escindidas0(cls, el)
    return self
def datos_escindente0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}denominacion_razon')
    self['DenominacionRazon'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}fecha_constitucion')
    if el is not None:
        self['FechaConstitucion'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}pais_nacionalidad')
    self['PaisNacionalidad'] = catalog_code('C329_pais_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}giro_mercantil')
    self['GiroMercantil'] = catalog_code('C329_giro_mercantil_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}capital_social_fijo')
    self['CapitalSocialFijo'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}capital_social_variable')
    if el is not None:
        self['CapitalSocialVariable'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}folio_mercantil')
    if el is not None:
        self['FolioMercantil'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}escindente_subsiste')
    self['EscindenteSubsiste'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}datos_accionista_escindente')
    if el is not None:
        self['DatosAccionistaEscindente'] = [datos_accionista1(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/fep}datos_accionista_escindente')]
    return self
def datos_escindidas0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}escindidas_determinadas')
    self['EscindidasDeterminadas'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}dato_escindida')
    if el is not None:
        self['DatoEscindida'] = [dato_escindida0(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/fep}dato_escindida')]
    return self
def dato_escindida0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}denominacion_razon')
    self['DenominacionRazon'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}fecha_constitucion')
    if el is not None:
        self['FechaConstitucion'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}pais_nacionalidad')
    self['PaisNacionalidad'] = catalog_code('C329_pais_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}giro_mercantil')
    self['GiroMercantil'] = catalog_code('C329_giro_mercantil_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}capital_social_fijo')
    self['CapitalSocialFijo'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}capital_social_variable')
    if el is not None:
        self['CapitalSocialVariable'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}folio_mercantil')
    if el is not None:
        self['FolioMercantil'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}numero_total_acciones')
    self['NumeroTotalAcciones'] = el.text
    self['DatosAccionista'] = [datos_accionista1(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/fep}datos_accionista')]
    return self
def compra_venta_acciones0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}tipo_operacion')
    self['TipoOperacion'] = el.text
    self['PersonaMoralAcciones'] = [persona_moral_acciones0(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/fep}persona_moral_acciones')]
    self['DatosLiquidacion'] = [datos_liquidacion3(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/fep}datos_liquidacion')]
    return self
def persona_moral_acciones0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}denominacion_razon')
    self['DenominacionRazon'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}fecha_constitucion')
    if el is not None:
        self['FechaConstitucion'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}pais_nacionalidad')
    self['PaisNacionalidad'] = catalog_code('C329_pais_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}valor_nominal')
    self['ValorNominal'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}numero_acciones')
    self['NumeroAcciones'] = el.text
    self['DatosVendedor'] = [datos_vendedor0(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/fep}datos_vendedor')]
    self['DatosComprador'] = [datos_comprador0(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/fep}datos_comprador')]
    return self
def datos_vendedor0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}numero_acciones_vendidas')
    self['NumeroAccionesVendidas'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}tipo_persona')
    self['TipoPersona'] = tipo_personac(cls, el)
    return self
def datos_comprador0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}numero_acciones_compradas')
    self['NumeroAccionesCompradas'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}tipo_persona')
    self['TipoPersona'] = tipo_personac(cls, el)
    return self
def datos_liquidacion3(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}fecha_pago')
    self['FechaPago'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}instrumento_monetario')
    if el is not None:
        self['InstrumentoMonetario'] = catalog_code('C329_instrumento_monetario_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}moneda')
    self['Moneda'] = catalog_code('C329_moneda_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}monto_operacion')
    self['MontoOperacion'] = el.text
    return self
def constitucion_modificacion_fideicomiso0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}tipo_movimiento')
    self['TipoMovimiento'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}tipo_fideicomiso')
    self['TipoFideicomiso'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}descripcion')
    if el is not None:
        self['Descripcion'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}identificador_fideicomiso')
    if el is not None:
        self['IdentificadorFideicomiso'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}denominacion_razon')
    self['DenominacionRazon'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}monto_patrimonio')
    self['MontoPatrimonio'] = el.text
    self['DatosFideicomitente'] = [datos_fideicomitente0(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/fep}datos_fideicomitente')]
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}datos_fideicomisarios')
    if el is not None:
        self['DatosFideicomisarios'] = [datos_fideicomisarios0(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/fep}datos_fideicomisarios')]
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}datos_miembro_comite_tecnico')
    if el is not None:
        self['DatosMiembroComiteTecnico'] = datos_miembro_comite_tecnico0(cls, el)
    return self
def datos_fideicomitente0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}tipo_movimiento_fideicomitente')
    self['TipoMovimientoFideicomitente'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}tipo_persona')
    self['TipoPersona'] = tipo_personab(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}datos_tipo_patrimonio')
    if el is not None:
        self['DatosTipoPatrimonio'] = [datos_tipo_patrimonio0(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/fep}datos_tipo_patrimonio')]
    return self
def datos_tipo_patrimonio0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}patrimonio_monetario')
    if el is not None:
        self['PatrimonioMonetario'] = patrimonio_monetario0(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}patrimonio_inmueble')
    if el is not None:
        self['PatrimonioInmueble'] = patrimonio_inmueble0(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}patrimonio_otro_bien')
    if el is not None:
        self['PatrimonioOtroBien'] = patrimonio_otro_bien0(cls, el)
    return self
def patrimonio_monetario0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}moneda')
    self['Moneda'] = catalog_code('C329_moneda_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}monto_operacion')
    self['MontoOperacion'] = el.text
    return self
def patrimonio_inmueble0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}tipo_inmueble')
    self['TipoInmueble'] = catalog_code('C329_tipo_inmueble_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}codigo_postal')
    self['CodigoPostal'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}folio_real')
    self['FolioReal'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}importe_garantia')
    self['ImporteGarantia'] = el.text
    return self
def patrimonio_otro_bien0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}descripcion')
    self['Descripcion'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}valor_bien')
    self['ValorBien'] = el.text
    return self
def datos_fideicomisarios0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}datos_fideicomisarios_determinados')
    self['DatosFideicomisariosDeterminados'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}tipo_persona')
    if el is not None:
        self['TipoPersona'] = [tipo_persona_1_type0(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/fep}tipo_persona')]
    return self
def cesion_derechos_fideicomitente_fideicomisario0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}identificador_fideicomiso')
    if el is not None:
        self['IdentificadorFideicomiso'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}denominacion_razon')
    self['DenominacionRazon'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}tipo_cesion')
    self['TipoCesion'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}datos_cedente')
    self['DatosCedente'] = datos_cedente0(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}datos_cesionario')
    self['DatosCesionario'] = datos_cesionario0(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}datos_cesion')
    self['DatosCesion'] = datos_cesion0(cls, el)
    return self
def datos_cedente0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}tipo_persona')
    self['TipoPersona'] = tipo_personab(cls, el)
    return self
def datos_cesionario0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}tipo_persona')
    self['TipoPersona'] = tipo_personab(cls, el)
    return self
def datos_cesion0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}monto_cesion')
    self['MontoCesion'] = el.text
    return self
def contrato_mutuo_credito0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}tipo_otorgamiento')
    self['TipoOtorgamiento'] = el.text
    self['DatosAcreedor'] = [datos_acreedor0(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/fep}datos_acreedor')]
    self['DatosDeudor'] = [datos_deudor0(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/fep}datos_deudor')]
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}datos_garantia')
    if el is not None:
        self['DatosGarantia'] = [datos_garantia0(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/fep}datos_garantia')]
    self['DatosLiquidacion'] = [datos_liquidacion4(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/fep}datos_liquidacion')]
    return self
def datos_acreedor0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}tipo_persona')
    self['TipoPersona'] = tipo_personab(cls, el)
    return self
def datos_deudor0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}tipo_persona')
    self['TipoPersona'] = tipo_personab(cls, el)
    return self
def datos_garantia0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}tipo_garantia')
    self['TipoGarantia'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}datos_bien_mutuo')
    if el is not None:
        self['DatosBienMutuo'] = datos_bien_mutuo0(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}tipo_persona')
    if el is not None:
        self['TipoPersona'] = tipo_personad(cls, el)
    return self
def datos_bien_mutuo0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}datos_inmueble')
    if el is not None:
        self['DatosInmueble'] = datos_inmueble2(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}datos_otro')
    if el is not None:
        self['DatosOtro'] = datos_otro1(cls, el)
    return self
def datos_inmueble2(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}tipo_inmueble')
    self['TipoInmueble'] = catalog_code('C329_tipo_inmueble_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}valor_referencia')
    self['ValorReferencia'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}codigo_postal')
    self['CodigoPostal'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}folio_real')
    self['FolioReal'] = el.text
    return self
def datos_otro1(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}descripcion_garantia')
    self['DescripcionGarantia'] = el.text
    return self
def tipo_personad(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}persona_fisica')
    if el is not None:
        self['PersonaFisica'] = persona_fisicaf(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}persona_moral')
    if el is not None:
        self['PersonaMoral'] = persona_moralf(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}fideicomiso')
    if el is not None:
        self['Fideicomiso'] = fideicomisob(cls, el)
    return self
def persona_fisicaf(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}nombre')
    self['Nombre'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}apellido_paterno')
    self['ApellidoPaterno'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}apellido_materno')
    self['ApellidoMaterno'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}fecha_nacimiento')
    if el is not None:
        self['FechaNacimiento'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}curp')
    if el is not None:
        self['Curp'] = el.text
    return self
def persona_moralf(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}denominacion_razon')
    self['DenominacionRazon'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}fecha_constitucion')
    if el is not None:
        self['FechaConstitucion'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}rfc')
    if el is not None:
        self['Rfc'] = el.text
    return self
def datos_liquidacion4(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}moneda')
    self['Moneda'] = catalog_code('C329_moneda_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}monto_operacion')
    self['MontoOperacion'] = el.text
    return self
def avaluo0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}tipo_bien')
    self['TipoBien'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}descripcion')
    if el is not None:
        self['Descripcion'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}valor_avaluo')
    self['ValorAvaluo'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}datos_propietario')
    self['DatosPropietario'] = datos_propietario0(cls, el)
    return self
def datos_propietario0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}propietario_solicita')
    self['PropietarioSolicita'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}tipo_persona')
    if el is not None:
        self['TipoPersona'] = tipo_personac(cls, el)
    return self
def datos_miembro_comite_tecnico0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}comite_tecnico')
    self['ComiteTecnico'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fep}modificacion_comite_tecnico')
    self['ModificacionComiteTecnico'] = el.text
    return self
def administrativo1_type0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}organo')
    self['Organo'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}cargo')
    self['Cargo'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}instrumento_publico_oficio')
    self['InstrumentoPublicoOficio'] = el.text
    return self
def persona_moral_simple_type0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}denominacion_razon')
    self['DenominacionRazon'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}fecha_constitucion')
    if el is not None:
        self['FechaConstitucion'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}pais_nacionalidad')
    self['PaisNacionalidad'] = catalog_code('C329_pais_type', el.text)
    return self
def persona_fisica_simple_type0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}nombre')
    self['Nombre'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}apellido_paterno')
    self['ApellidoPaterno'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}apellido_materno')
    self['ApellidoMaterno'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}fecha_nacimiento')
    if el is not None:
        self['FechaNacimiento'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}curp')
    if el is not None:
        self['Curp'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}pais_nacionalidad')
    self['PaisNacionalidad'] = catalog_code('C329_pais_type', el.text)
    return self
def fideicomiso_simple_type0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}denominacion_razon')
    self['DenominacionRazon'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}identificador_fideicomiso')
    if el is not None:
        self['IdentificadorFideicomiso'] = el.text
    return self
def representante_apoderado_type0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}nombre')
    self['Nombre'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}apellido_paterno')
    self['ApellidoPaterno'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}apellido_materno')
    self['ApellidoMaterno'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}fecha_nacimiento')
    if el is not None:
        self['FechaNacimiento'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}curp')
    if el is not None:
        self['Curp'] = el.text
    return self
def informe_type0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}mes_reportado')
    self['MesReportado'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}tribunal_dependencia')
    self['TribunalDependencia'] = tribunal_dependencia0(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}aviso')
    if el is not None:
        self['Aviso'] = [aviso7(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/fes}aviso')]
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}version')
    if el is not None:
        self['Version'] = el.text
    return self
def archivo_type7(cls, node):
    self = ScalarMap()
    self['Informe'] = [informe_type0(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/fes}informe')]
    return self
def operaciones_type0(cls, node):
    self = ScalarMap()
    self['DatosOperacion'] = [datos_operacion6(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/fes}datos_operacion')]
    return self
def datos_operacion6(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}fecha_operacion')
    self['FechaOperacion'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}tipo_actividad')
    self['TipoActividad'] = tipo_actividad1(cls, el)
    return self
def modificatorio_type0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}folio_modificacion')
    self['FolioModificacion'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}descripcion_modificacion')
    self['DescripcionModificacion'] = el.text
    return self
def aviso7(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}referencia_aviso')
    self['ReferenciaAviso'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}modificatorio')
    if el is not None:
        self['Modificatorio'] = modificatorio_type0(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}prioridad')
    self['Prioridad'] = catalog_code('C329_prioridad_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}alerta')
    self['Alerta'] = alerta7(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}detalle_operaciones')
    self['DetalleOperaciones'] = operaciones_type0(cls, el)
    return self
def tipo_actividad1(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}derechos_inmuebles')
    if el is not None:
        self['DerechosInmuebles'] = derechos_inmuebles0(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}otorgamiento_poder')
    if el is not None:
        self['OtorgamientoPoder'] = otorgamiento_poder1(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}constitucion_personas_morales')
    if el is not None:
        self['ConstitucionPersonasMorales'] = constitucion_personas_morales1(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}modificacion_patrimonial')
    if el is not None:
        self['ModificacionPatrimonial'] = modificacion_patrimonial1(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}contrato_mutuo_credito')
    if el is not None:
        self['ContratoMutuoCredito'] = contrato_mutuo_credito1(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}avaluo')
    if el is not None:
        self['Avaluo'] = avaluo1(cls, el)
    return self
def derechos_inmuebles0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}organo')
    self['Organo'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}tipo_juicio')
    self['TipoJuicio'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}materia')
    self['Materia'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}expediente')
    self['Expediente'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}tipo_acto')
    self['TipoActo'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}tipo_acto_otro')
    if el is not None:
        self['TipoActoOtro'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}datos_inmuebles')
    self['DatosInmuebles'] = datos_inmuebles0(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}personas_acto')
    self['PersonasActo'] = personas_acto0(cls, el)
    return self
def otorgamiento_poder1(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}autoridad')
    self['Autoridad'] = autoridad0(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}persona_solicita')
    self['PersonaSolicita'] = persona_solicita0(cls, el)
    self['DatosPoderdante'] = [datos_poderdante1(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/fes}datos_poderdante')]
    self['DatosApoderado'] = [datos_apoderado1(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/fes}datos_apoderado')]
    return self
def constitucion_personas_morales1(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}autoridad')
    self['Autoridad'] = autoridad1(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}persona_solicita')
    self['PersonaSolicita'] = persona_solicita0(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}persona_moral_constitucion')
    self['PersonaMoralConstitucion'] = persona_moral_constitucion0(cls, el)
    return self
def modificacion_patrimonial1(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}autoridad')
    self['Autoridad'] = autoridad1(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}persona_moral_modifica')
    self['PersonaMoralModifica'] = persona_moral_modifica1(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}datos_modificacion')
    self['DatosModificacion'] = datos_modificacion1(cls, el)
    return self
def contrato_mutuo_credito1(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}autoridad')
    self['Autoridad'] = autoridad0(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}tipo_otorgamiento')
    self['TipoOtorgamiento'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}persona_solicita')
    self['PersonaSolicita'] = persona_fisica_simple_type0(cls, el)
    self['DatosAcreedor'] = [datos_acreedor1(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/fes}datos_acreedor')]
    self['DatosDeudor'] = [datos_deudor1(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/fes}datos_deudor')]
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}datos_garantia')
    if el is not None:
        self['DatosGarantia'] = [datos_garantia1(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/fes}datos_garantia')]
    self['DatosLiquidacion'] = [datos_liquidacion5(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/fes}datos_liquidacion')]
    return self
def avaluo1(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}organo')
    self['Organo'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}cargo')
    self['Cargo'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}expediente_oficio')
    self['ExpedienteOficio'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}persona_solicita')
    self['PersonaSolicita'] = persona_solicita0(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}tipo_bien')
    self['TipoBien'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}descripcion')
    if el is not None:
        self['Descripcion'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}valor_avaluo')
    self['ValorAvaluo'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}datos_propietario')
    self['DatosPropietario'] = datos_propietario1(cls, el)
    return self
def datos_inmuebles0(cls, node):
    self = ScalarMap()
    self['CaracteristicasInmueble'] = [caracteristicas_inmueble0(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/fes}caracteristicas_inmueble')]
    return self
def caracteristicas_inmueble0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}tipo_inmueble')
    self['TipoInmueble'] = catalog_code('C329_tipo_inmueble_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}valor_catastral')
    self['ValorCatastral'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}colonia')
    self['Colonia'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}calle')
    self['Calle'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}numero_exterior')
    self['NumeroExterior'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}numero_interior')
    if el is not None:
        self['NumeroInterior'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}codigo_postal')
    self['CodigoPostal'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}dimension_terreno')
    self['DimensionTerreno'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}dimension_construido')
    self['DimensionConstruido'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}folio_real')
    self['FolioReal'] = el.text
    return self
def personas_acto0(cls, node):
    self = ScalarMap()
    self['DatosPersonaActo'] = [datos_persona_acto0(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/fes}datos_persona_acto')]
    return self
def tipo_persona_type0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}persona_fisica')
    if el is not None:
        self['PersonaFisica'] = persona_solicita0(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}persona_moral')
    if el is not None:
        self['PersonaMoral'] = persona_moral10(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}fideicomiso')
    if el is not None:
        self['Fideicomiso'] = fideicomisoc(cls, el)
    return self
def persona_solicita0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}nombre')
    self['Nombre'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}apellido_paterno')
    self['ApellidoPaterno'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}apellido_materno')
    self['ApellidoMaterno'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}fecha_nacimiento')
    if el is not None:
        self['FechaNacimiento'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}curp')
    if el is not None:
        self['Curp'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}pais_nacionalidad')
    self['PaisNacionalidad'] = catalog_code('C329_pais_type', el.text)
    return self
def persona_moral10(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}denominacion_razon')
    self['DenominacionRazon'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}fecha_constitucion')
    if el is not None:
        self['FechaConstitucion'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}pais_nacionalidad')
    self['PaisNacionalidad'] = catalog_code('C329_pais_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}representante_apoderado')
    self['RepresentanteApoderado'] = representante_apoderado_type0(cls, el)
    return self
def fideicomisoc(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}denominacion_razon')
    self['DenominacionRazon'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}identificador_fideicomiso')
    if el is not None:
        self['IdentificadorFideicomiso'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}apoderado_delegado')
    self['ApoderadoDelegado'] = representante_apoderado_type0(cls, el)
    return self
def datos_persona_acto0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}caracter')
    self['Caracter'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}caracter_otro')
    if el is not None:
        self['CaracterOtro'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}tipo_persona')
    self['TipoPersona'] = tipo_persona_type0(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}tipo_domicilio')
    if el is not None:
        self['TipoDomicilio'] = tipo_domicilio5(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}telefono')
    if el is not None:
        self['Telefono'] = telefono6(cls, el)
    return self
def tipo_domicilio5(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}nacional')
    if el is not None:
        self['Nacional'] = nacional7(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}extranjero')
    if el is not None:
        self['Extranjero'] = extranjero7(cls, el)
    return self
def nacional7(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}colonia')
    self['Colonia'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}calle')
    self['Calle'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}numero_exterior')
    self['NumeroExterior'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}numero_interior')
    if el is not None:
        self['NumeroInterior'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}codigo_postal')
    self['CodigoPostal'] = el.text
    return self
def extranjero7(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}pais')
    self['Pais'] = catalog_code('C329_pais_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}estado_provincia')
    self['EstadoProvincia'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}ciudad_poblacion')
    self['CiudadPoblacion'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}colonia')
    self['Colonia'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}calle')
    self['Calle'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}numero_exterior')
    self['NumeroExterior'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}numero_interior')
    if el is not None:
        self['NumeroInterior'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}codigo_postal')
    self['CodigoPostal'] = el.text
    return self
def telefono6(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}clave_pais')
    if el is not None:
        self['ClavePais'] = catalog_code('C329_pais_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}numero_telefono')
    self['NumeroTelefono'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}correo_electronico')
    if el is not None:
        self['CorreoElectronico'] = el.text
    return self
def administrativo_type0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}organo')
    self['Organo'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}cargo')
    self['Cargo'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}instrumento_publico')
    self['InstrumentoPublico'] = el.text
    return self
def jurisdiccional_type0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}organo')
    self['Organo'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}tipo_juicio')
    self['TipoJuicio'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}materia')
    self['Materia'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}expediente')
    self['Expediente'] = el.text
    return self
def tipo_autoridad_type0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}administrativo')
    if el is not None:
        self['Administrativo'] = administrativo_type0(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}jurisdiccional')
    if el is not None:
        self['Jurisdiccional'] = jurisdiccional_type0(cls, el)
    return self
def domicilio_oficina_type0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}nacional')
    if el is not None:
        self['Nacional'] = nacional7(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}extranjero')
    if el is not None:
        self['Extranjero'] = extranjero7(cls, el)
    return self
def autoridad0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}tipo_autoridad')
    self['TipoAutoridad'] = tipo_autoridad_type0(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}domicilio_oficina')
    if el is not None:
        self['DomicilioOficina'] = domicilio_oficina_type0(cls, el)
    return self
def tipo_persona_simple_type0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}persona_fisica')
    if el is not None:
        self['PersonaFisica'] = persona_fisica_simple_type0(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}persona_moral')
    if el is not None:
        self['PersonaMoral'] = persona_moral_simple_type0(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}fideicomiso')
    if el is not None:
        self['Fideicomiso'] = fideicomiso_simple_type0(cls, el)
    return self
def datos_poderdante1(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}tipo_persona')
    self['TipoPersona'] = tipo_persona_simple_type0(cls, el)
    return self
def datos_apoderado1(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}tipo_poder')
    self['TipoPoder'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}tipo_persona')
    self['TipoPersona'] = tipo_persona_simple_type0(cls, el)
    return self
def tipo_autoridad1_type0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}administrativo')
    if el is not None:
        self['Administrativo'] = administrativo1_type0(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}jurisdiccional')
    if el is not None:
        self['Jurisdiccional'] = jurisdiccional_type0(cls, el)
    return self
def autoridad1(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}tipo_autoridad')
    self['TipoAutoridad'] = tipo_autoridad1_type0(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}domicilio_oficina')
    if el is not None:
        self['DomicilioOficina'] = domicilio_oficina_type0(cls, el)
    return self
def persona_moral_constitucion0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}tipo_persona_moral')
    self['TipoPersonaMoral'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}tipo_persona_moral_otra')
    if el is not None:
        self['TipoPersonaMoralOtra'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}denominacion_razon')
    self['DenominacionRazon'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}giro_mercantil')
    self['GiroMercantil'] = catalog_code('C329_giro_mercantil_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}folio_mercantil')
    if el is not None:
        self['FolioMercantil'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}numero_total_acciones')
    self['NumeroTotalAcciones'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}entidad_federativa')
    if el is not None:
        self['EntidadFederativa'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}consejo_vigilancia')
    self['ConsejoVigilancia'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}motivo_constitucion')
    self['MotivoConstitucion'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}instrumento_publico')
    if el is not None:
        self['InstrumentoPublico'] = el.text
    self['DatosAccionista'] = [datos_accionista2(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/fes}datos_accionista')]
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}capital_social')
    self['CapitalSocial'] = capital_social1(cls, el)
    return self
def datos_accionista2(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}cargo_accionista')
    self['CargoAccionista'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}tipo_persona')
    self['TipoPersona'] = tipo_persona_simple_type0(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}numero_acciones')
    self['NumeroAcciones'] = el.text
    return self
def capital_social1(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}capital_fijo')
    self['CapitalFijo'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}capital_variable')
    if el is not None:
        self['CapitalVariable'] = el.text
    return self
def datos_accionista1_type0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}tipo_persona')
    self['TipoPersona'] = tipo_persona_simple_type0(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}numero_acciones')
    self['NumeroAcciones'] = el.text
    return self
def persona_moral_modifica1(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}denominacion_razon')
    self['DenominacionRazon'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}fecha_constitucion')
    if el is not None:
        self['FechaConstitucion'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}pais_nacionalidad')
    self['PaisNacionalidad'] = catalog_code('C329_pais_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}giro_mercantil')
    self['GiroMercantil'] = catalog_code('C329_giro_mercantil_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}numero_total_acciones')
    self['NumeroTotalAcciones'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}motivo_modificacion')
    self['MotivoModificacion'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}instrumento_publico')
    if el is not None:
        self['InstrumentoPublico'] = el.text
    return self
def datos_modificacion1(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}tipo_modificacion_capital_fijo')
    self['TipoModificacionCapitalFijo'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}inicial_capital_fijo')
    self['InicialCapitalFijo'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}final_capital_fijo')
    self['FinalCapitalFijo'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}tipo_modificacion_capital_variable')
    self['TipoModificacionCapitalVariable'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}inicial_capital_variable')
    self['InicialCapitalVariable'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}final_capital_variable')
    self['FinalCapitalVariable'] = el.text
    self['DatosAccionista'] = [datos_accionista1_type0(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/fes}datos_accionista')]
    return self
def datos_acreedor1(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}tipo_persona')
    self['TipoPersona'] = tipo_persona_simple_type0(cls, el)
    return self
def datos_deudor1(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}tipo_persona')
    self['TipoPersona'] = tipo_persona_simple_type0(cls, el)
    return self
def garante_fisica_type0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}nombre')
    self['Nombre'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}apellido_paterno')
    self['ApellidoPaterno'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}apellido_materno')
    self['ApellidoMaterno'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}fecha_nacimiento')
    if el is not None:
        self['FechaNacimiento'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}curp')
    if el is not None:
        self['Curp'] = el.text
    return self
def garante_moral_type0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}denominacion_razon')
    self['DenominacionRazon'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}fecha_constitucion')
    if el is not None:
        self['FechaConstitucion'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}rfc')
    if el is not None:
        self['Rfc'] = el.text
    return self
def garante_fideicomiso_type0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}denominacion_razon')
    self['DenominacionRazon'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}identificador_fideicomiso')
    if el is not None:
        self['IdentificadorFideicomiso'] = el.text
    return self
def tipo_garante_type0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}persona_fisica')
    if el is not None:
        self['PersonaFisica'] = garante_fisica_type0(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}persona_moral')
    if el is not None:
        self['PersonaMoral'] = garante_moral_type0(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}fideicomiso')
    if el is not None:
        self['Fideicomiso'] = garante_fideicomiso_type0(cls, el)
    return self
def garantia_inmueble_type0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}tipo_inmueble')
    self['TipoInmueble'] = catalog_code('C329_tipo_inmueble_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}valor_referencia')
    self['ValorReferencia'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}codigo_postal')
    self['CodigoPostal'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}folio_real')
    self['FolioReal'] = el.text
    return self
def garantia_otro_type0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}descripcion_garantia')
    self['DescripcionGarantia'] = el.text
    return self
def bien_garantia_type0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}datos_inmueble')
    if el is not None:
        self['DatosInmueble'] = garantia_inmueble_type0(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}datos_otro')
    if el is not None:
        self['DatosOtro'] = garantia_otro_type0(cls, el)
    return self
def datos_garantia1(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}tipo_garantia')
    self['TipoGarantia'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}datos_bien_garantia')
    if el is not None:
        self['DatosBienGarantia'] = bien_garantia_type0(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}tipo_persona')
    if el is not None:
        self['TipoPersona'] = tipo_garante_type0(cls, el)
    return self
def datos_liquidacion5(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}moneda')
    self['Moneda'] = catalog_code('C329_moneda_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}monto_operacion')
    self['MontoOperacion'] = el.text
    return self
def datos_propietario1(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}propietario_solicita')
    self['PropietarioSolicita'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}dato_propietario')
    if el is not None:
        self['DatoPropietario'] = [dato_propietario0(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/fes}dato_propietario')]
    return self
def dato_propietario0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}tipo_persona')
    self['TipoPersona'] = tipo_persona_simple_type0(cls, el)
    return self
def tribunal_dependencia0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}clave_tribunal_dependencia')
    self['ClaveTribunalDependencia'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}clave_actividad')
    self['ClaveActividad'] = catalog_code('C329_clave_actividad_type', el.text)
    return self
def alerta7(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}tipo_alerta')
    self['TipoAlerta'] = catalog_code('C329_tipo_alerta_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/fes}descripcion_alerta')
    if el is not None:
        self['DescripcionAlerta'] = el.text
    return self
def archivo_type8(cls, node):
    self = ScalarMap()
    self['Informe'] = [informe7(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/inm}informe')]
    return self
def informe7(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/inm}mes_reportado')
    self['MesReportado'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/inm}sujeto_obligado')
    self['SujetoObligado'] = sujeto_obligado7(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/inm}aviso')
    if el is not None:
        self['Aviso'] = [aviso8(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/inm}aviso')]
    return self
def sujeto_obligado7(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/inm}clave_entidad_colegiada')
    if el is not None:
        self['ClaveEntidadColegiada'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/inm}clave_sujeto_obligado')
    self['ClaveSujetoObligado'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/inm}clave_actividad')
    self['ClaveActividad'] = catalog_code('C329_clave_actividad_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/inm}exento')
    if el is not None:
        self['Exento'] = el.text
    return self
def aviso8(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/inm}referencia_aviso')
    self['ReferenciaAviso'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/inm}modificatorio')
    if el is not None:
        self['Modificatorio'] = modificatorio7(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/inm}prioridad')
    self['Prioridad'] = catalog_code('C329_prioridad_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/inm}alerta')
    self['Alerta'] = alerta8(cls, el)
    self['PersonaAviso'] = [persona_aviso6(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/inm}persona_aviso')]
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/inm}dueno_beneficiario')
    if el is not None:
        self['DuenoBeneficiario'] = [dueno_beneficiario5(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/inm}dueno_beneficiario')]
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/inm}detalle_operaciones')
    self['DetalleOperaciones'] = detalle_operaciones7(cls, el)
    return self
def modificatorio7(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/inm}folio_modificacion')
    self['FolioModificacion'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/inm}descripcion_modificacion')
    self['DescripcionModificacion'] = el.text
    return self
def alerta8(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/inm}tipo_alerta')
    self['TipoAlerta'] = catalog_code('C329_tipo_alerta_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/inm}descripcion_alerta')
    if el is not None:
        self['DescripcionAlerta'] = el.text
    return self
def persona_aviso6(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/inm}tipo_persona')
    self['TipoPersona'] = tipo_personae(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/inm}tipo_domicilio')
    if el is not None:
        self['TipoDomicilio'] = tipo_domicilio6(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/inm}telefono')
    if el is not None:
        self['Telefono'] = telefono7(cls, el)
    return self
def tipo_personae(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/inm}persona_fisica')
    if el is not None:
        self['PersonaFisica'] = persona_fisica10(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/inm}persona_moral')
    if el is not None:
        self['PersonaMoral'] = persona_moral11(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/inm}fideicomiso')
    if el is not None:
        self['Fideicomiso'] = fideicomisod(cls, el)
    return self
def persona_fisica10(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/inm}nombre')
    self['Nombre'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/inm}apellido_paterno')
    self['ApellidoPaterno'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/inm}apellido_materno')
    self['ApellidoMaterno'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/inm}fecha_nacimiento')
    if el is not None:
        self['FechaNacimiento'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/inm}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/inm}curp')
    if el is not None:
        self['Curp'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/inm}pais_nacionalidad')
    self['PaisNacionalidad'] = catalog_code('C329_pais_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/inm}actividad_economica')
    self['ActividadEconomica'] = catalog_code('C329_actividad_economica_type', el.text)
    return self
def persona_moral11(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/inm}denominacion_razon')
    self['DenominacionRazon'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/inm}fecha_constitucion')
    if el is not None:
        self['FechaConstitucion'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/inm}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/inm}pais_nacionalidad')
    self['PaisNacionalidad'] = catalog_code('C329_pais_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/inm}giro_mercantil')
    self['GiroMercantil'] = catalog_code('C329_giro_mercantil_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/inm}representante_apoderado')
    self['RepresentanteApoderado'] = representante_apoderado6(cls, el)
    return self
def fideicomisod(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/inm}denominacion_razon')
    self['DenominacionRazon'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/inm}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/inm}identificador_fideicomiso')
    if el is not None:
        self['IdentificadorFideicomiso'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/inm}apoderado_delegado')
    self['ApoderadoDelegado'] = representante_apoderado6(cls, el)
    return self
def representante_apoderado6(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/inm}nombre')
    self['Nombre'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/inm}apellido_paterno')
    self['ApellidoPaterno'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/inm}apellido_materno')
    self['ApellidoMaterno'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/inm}fecha_nacimiento')
    if el is not None:
        self['FechaNacimiento'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/inm}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/inm}curp')
    if el is not None:
        self['Curp'] = el.text
    return self
def tipo_domicilio6(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/inm}nacional')
    if el is not None:
        self['Nacional'] = nacional8(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/inm}extranjero')
    if el is not None:
        self['Extranjero'] = extranjero8(cls, el)
    return self
def nacional8(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/inm}colonia')
    self['Colonia'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/inm}calle')
    self['Calle'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/inm}numero_exterior')
    self['NumeroExterior'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/inm}numero_interior')
    if el is not None:
        self['NumeroInterior'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/inm}codigo_postal')
    self['CodigoPostal'] = el.text
    return self
def extranjero8(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/inm}pais')
    self['Pais'] = catalog_code('C329_pais_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/inm}estado_provincia')
    self['EstadoProvincia'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/inm}ciudad_poblacion')
    self['CiudadPoblacion'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/inm}colonia')
    self['Colonia'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/inm}calle')
    self['Calle'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/inm}numero_exterior')
    self['NumeroExterior'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/inm}numero_interior')
    if el is not None:
        self['NumeroInterior'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/inm}codigo_postal')
    self['CodigoPostal'] = el.text
    return self
def telefono7(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/inm}clave_pais')
    if el is not None:
        self['ClavePais'] = catalog_code('C329_pais_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/inm}numero_telefono')
    if el is not None:
        self['NumeroTelefono'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/inm}correo_electronico')
    if el is not None:
        self['CorreoElectronico'] = el.text
    return self
def dueno_beneficiario5(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/inm}tipo_persona')
    self['TipoPersona'] = tipo_personaf(cls, el)
    return self
def tipo_personaf(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/inm}persona_fisica')
    if el is not None:
        self['PersonaFisica'] = persona_fisica11(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/inm}persona_moral')
    if el is not None:
        self['PersonaMoral'] = persona_moral12(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/inm}fideicomiso')
    if el is not None:
        self['Fideicomiso'] = fideicomisoe(cls, el)
    return self
def persona_fisica11(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/inm}nombre')
    self['Nombre'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/inm}apellido_paterno')
    self['ApellidoPaterno'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/inm}apellido_materno')
    self['ApellidoMaterno'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/inm}fecha_nacimiento')
    if el is not None:
        self['FechaNacimiento'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/inm}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/inm}curp')
    if el is not None:
        self['Curp'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/inm}pais_nacionalidad')
    if el is not None:
        self['PaisNacionalidad'] = catalog_code('C329_pais_type', el.text)
    return self
def persona_moral12(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/inm}denominacion_razon')
    self['DenominacionRazon'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/inm}fecha_constitucion')
    if el is not None:
        self['FechaConstitucion'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/inm}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/inm}pais_nacionalidad')
    if el is not None:
        self['PaisNacionalidad'] = catalog_code('C329_pais_type', el.text)
    return self
def fideicomisoe(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/inm}denominacion_razon')
    self['DenominacionRazon'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/inm}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/inm}identificador_fideicomiso')
    if el is not None:
        self['IdentificadorFideicomiso'] = el.text
    return self
def detalle_operaciones7(cls, node):
    self = ScalarMap()
    self['DatosOperacion'] = [datos_operacion7(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/inm}datos_operacion')]
    return self
def datos_operacion7(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/inm}fecha_operacion')
    self['FechaOperacion'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/inm}tipo_operacion')
    self['TipoOperacion'] = catalog_code('C329_tipo_operacion_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/inm}figura_cliente')
    self['FiguraCliente'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/inm}figura_so')
    self['FiguraSo'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/inm}datos_contraparte')
    if el is not None:
        self['DatosContraparte'] = [datos_contraparte0(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/inm}datos_contraparte')]
    self['CaracteristicasInmueble'] = [caracteristicas_inmueble1(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/inm}caracteristicas_inmueble')]
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/inm}contrato_instrumento_publico')
    self['ContratoInstrumentoPublico'] = contrato_instrumento_publico0(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/inm}datos_liquidacion')
    if el is not None:
        self['DatosLiquidacion'] = [datos_liquidacion6(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/inm}datos_liquidacion')]
    return self
def datos_contraparte0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/inm}tipo_persona')
    self['TipoPersona'] = tipo_personaf(cls, el)
    return self
def caracteristicas_inmueble1(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/inm}tipo_inmueble')
    self['TipoInmueble'] = catalog_code('C329_tipo_inmueble_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/inm}valor_pactado')
    self['ValorPactado'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/inm}colonia')
    self['Colonia'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/inm}calle')
    self['Calle'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/inm}numero_exterior')
    self['NumeroExterior'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/inm}numero_interior')
    if el is not None:
        self['NumeroInterior'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/inm}codigo_postal')
    self['CodigoPostal'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/inm}dimension_terreno')
    self['DimensionTerreno'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/inm}dimension_construido')
    self['DimensionConstruido'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/inm}folio_real')
    self['FolioReal'] = el.text
    return self
def contrato_instrumento_publico0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/inm}datos_instrumento_publico')
    if el is not None:
        self['DatosInstrumentoPublico'] = datos_instrumento_publico0(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/inm}datos_contrato')
    if el is not None:
        self['DatosContrato'] = datos_contrato0(cls, el)
    return self
def datos_instrumento_publico0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/inm}numero_instrumento_publico')
    self['NumeroInstrumentoPublico'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/inm}fecha_instrumento_publico')
    self['FechaInstrumentoPublico'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/inm}notario_instrumento_publico')
    self['NotarioInstrumentoPublico'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/inm}entidad_instrumento_publico')
    self['EntidadInstrumentoPublico'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/inm}valor_avaluo_catastral')
    self['ValorAvaluoCatastral'] = el.text
    return self
def datos_contrato0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/inm}fecha_contrato')
    self['FechaContrato'] = datetime.strptime(el.text, '%Y%m%d').date()
    return self
def datos_liquidacion6(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/inm}fecha_pago')
    self['FechaPago'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/inm}forma_pago')
    self['FormaPago'] = catalog_code('C329_forma_pago_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/inm}instrumento_monetario')
    if el is not None:
        self['InstrumentoMonetario'] = catalog_code('C329_instrumento_monetario_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/inm}moneda')
    self['Moneda'] = catalog_code('C329_moneda_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/inm}monto_operacion')
    self['MontoOperacion'] = el.text
    return self
def archivo_type9(cls, node):
    self = ScalarMap()
    self['Informe'] = [informe8(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/jys}informe')]
    return self
def informe8(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/jys}mes_reportado')
    self['MesReportado'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/jys}sujeto_obligado')
    self['SujetoObligado'] = sujeto_obligado8(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/jys}aviso')
    if el is not None:
        self['Aviso'] = [aviso9(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/jys}aviso')]
    return self
def sujeto_obligado8(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/jys}clave_entidad_colegiada')
    if el is not None:
        self['ClaveEntidadColegiada'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/jys}clave_sujeto_obligado')
    self['ClaveSujetoObligado'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/jys}clave_actividad')
    self['ClaveActividad'] = catalog_code('C329_clave_actividad_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/jys}exento')
    if el is not None:
        self['Exento'] = el.text
    return self
def aviso9(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/jys}referencia_aviso')
    self['ReferenciaAviso'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/jys}modificatorio')
    if el is not None:
        self['Modificatorio'] = modificatorio8(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/jys}prioridad')
    self['Prioridad'] = catalog_code('C329_prioridad_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/jys}alerta')
    self['Alerta'] = alerta9(cls, el)
    self['PersonaAviso'] = [persona_aviso7(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/jys}persona_aviso')]
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/jys}dueno_beneficiario')
    if el is not None:
        self['DuenoBeneficiario'] = [dueno_beneficiario6(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/jys}dueno_beneficiario')]
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/jys}detalle_operaciones')
    self['DetalleOperaciones'] = detalle_operaciones8(cls, el)
    return self
def modificatorio8(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/jys}folio_modificacion')
    self['FolioModificacion'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/jys}descripcion_modificacion')
    self['DescripcionModificacion'] = el.text
    return self
def alerta9(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/jys}tipo_alerta')
    self['TipoAlerta'] = catalog_code('C329_tipo_alerta_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/jys}descripcion_alerta')
    if el is not None:
        self['DescripcionAlerta'] = el.text
    return self
def persona_aviso7(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/jys}tipo_persona')
    self['TipoPersona'] = tipo_persona10(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/jys}tipo_domicilio')
    if el is not None:
        self['TipoDomicilio'] = tipo_domicilio7(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/jys}telefono')
    if el is not None:
        self['Telefono'] = telefono8(cls, el)
    return self
def tipo_persona10(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/jys}persona_fisica')
    if el is not None:
        self['PersonaFisica'] = persona_fisica12(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/jys}persona_moral')
    if el is not None:
        self['PersonaMoral'] = persona_moral13(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/jys}fideicomiso')
    if el is not None:
        self['Fideicomiso'] = fideicomisof(cls, el)
    return self
def persona_fisica12(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/jys}nombre')
    self['Nombre'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/jys}apellido_paterno')
    self['ApellidoPaterno'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/jys}apellido_materno')
    self['ApellidoMaterno'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/jys}fecha_nacimiento')
    if el is not None:
        self['FechaNacimiento'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/jys}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/jys}curp')
    if el is not None:
        self['Curp'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/jys}pais_nacionalidad')
    self['PaisNacionalidad'] = catalog_code('C329_pais_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/jys}actividad_economica')
    self['ActividadEconomica'] = catalog_code('C329_actividad_economica_type', el.text)
    return self
def persona_moral13(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/jys}denominacion_razon')
    self['DenominacionRazon'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/jys}fecha_constitucion')
    if el is not None:
        self['FechaConstitucion'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/jys}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/jys}pais_nacionalidad')
    self['PaisNacionalidad'] = catalog_code('C329_pais_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/jys}giro_mercantil')
    self['GiroMercantil'] = catalog_code('C329_giro_mercantil_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/jys}representante_apoderado')
    self['RepresentanteApoderado'] = representante_apoderado7(cls, el)
    return self
def fideicomisof(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/jys}denominacion_razon')
    self['DenominacionRazon'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/jys}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/jys}identificador_fideicomiso')
    if el is not None:
        self['IdentificadorFideicomiso'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/jys}apoderado_delegado')
    self['ApoderadoDelegado'] = representante_apoderado7(cls, el)
    return self
def representante_apoderado7(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/jys}nombre')
    self['Nombre'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/jys}apellido_paterno')
    self['ApellidoPaterno'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/jys}apellido_materno')
    self['ApellidoMaterno'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/jys}fecha_nacimiento')
    if el is not None:
        self['FechaNacimiento'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/jys}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/jys}curp')
    if el is not None:
        self['Curp'] = el.text
    return self
def tipo_domicilio7(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/jys}nacional')
    if el is not None:
        self['Nacional'] = nacional9(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/jys}extranjero')
    if el is not None:
        self['Extranjero'] = extranjero9(cls, el)
    return self
def nacional9(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/jys}colonia')
    self['Colonia'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/jys}calle')
    self['Calle'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/jys}numero_exterior')
    self['NumeroExterior'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/jys}numero_interior')
    if el is not None:
        self['NumeroInterior'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/jys}codigo_postal')
    self['CodigoPostal'] = el.text
    return self
def extranjero9(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/jys}pais')
    self['Pais'] = catalog_code('C329_pais_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/jys}estado_provincia')
    self['EstadoProvincia'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/jys}ciudad_poblacion')
    self['CiudadPoblacion'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/jys}colonia')
    self['Colonia'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/jys}calle')
    self['Calle'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/jys}numero_exterior')
    self['NumeroExterior'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/jys}numero_interior')
    if el is not None:
        self['NumeroInterior'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/jys}codigo_postal')
    self['CodigoPostal'] = el.text
    return self
def telefono8(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/jys}clave_pais')
    if el is not None:
        self['ClavePais'] = catalog_code('C329_pais_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/jys}numero_telefono')
    if el is not None:
        self['NumeroTelefono'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/jys}correo_electronico')
    if el is not None:
        self['CorreoElectronico'] = el.text
    return self
def dueno_beneficiario6(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/jys}tipo_persona')
    self['TipoPersona'] = tipo_persona11(cls, el)
    return self
def tipo_persona11(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/jys}persona_fisica')
    if el is not None:
        self['PersonaFisica'] = persona_fisica13(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/jys}persona_moral')
    if el is not None:
        self['PersonaMoral'] = persona_moral14(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/jys}fideicomiso')
    if el is not None:
        self['Fideicomiso'] = fideicomiso10(cls, el)
    return self
def persona_fisica13(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/jys}nombre')
    self['Nombre'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/jys}apellido_paterno')
    self['ApellidoPaterno'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/jys}apellido_materno')
    self['ApellidoMaterno'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/jys}fecha_nacimiento')
    if el is not None:
        self['FechaNacimiento'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/jys}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/jys}curp')
    if el is not None:
        self['Curp'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/jys}pais_nacionalidad')
    if el is not None:
        self['PaisNacionalidad'] = catalog_code('C329_pais_type', el.text)
    return self
def persona_moral14(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/jys}denominacion_razon')
    self['DenominacionRazon'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/jys}fecha_constitucion')
    if el is not None:
        self['FechaConstitucion'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/jys}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/jys}pais_nacionalidad')
    if el is not None:
        self['PaisNacionalidad'] = catalog_code('C329_pais_type', el.text)
    return self
def fideicomiso10(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/jys}denominacion_razon')
    self['DenominacionRazon'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/jys}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/jys}identificador_fideicomiso')
    if el is not None:
        self['IdentificadorFideicomiso'] = el.text
    return self
def detalle_operaciones8(cls, node):
    self = ScalarMap()
    self['DatosOperacion'] = [datos_operacion8(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/jys}datos_operacion')]
    return self
def datos_operacion8(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/jys}fecha_operacion')
    self['FechaOperacion'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/jys}tipo_sucursal')
    self['TipoSucursal'] = tipo_sucursal0(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/jys}tipo_operacion')
    self['TipoOperacion'] = catalog_code('C329_tipo_operacion_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/jys}linea_negocio')
    self['LineaNegocio'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/jys}medio_operacion')
    self['MedioOperacion'] = el.text
    self['DatosLiquidacion'] = [datos_liquidacion7(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/jys}datos_liquidacion')]
    return self
def tipo_sucursal0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/jys}datos_sucursal_propia')
    if el is not None:
        self['DatosSucursalPropia'] = datos_sucursal_propia0(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/jys}datos_sucursal_operador')
    if el is not None:
        self['DatosSucursalOperador'] = datos_sucursal_operador0(cls, el)
    return self
def datos_sucursal_propia0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/jys}codigo_postal')
    self['CodigoPostal'] = el.text
    return self
def datos_sucursal_operador0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/jys}nombre_operador')
    self['NombreOperador'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/jys}codigo_postal')
    self['CodigoPostal'] = el.text
    return self
def datos_liquidacion7(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/jys}liquidacion_numerario')
    if el is not None:
        self['LiquidacionNumerario'] = liquidacion_numerario1(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/jys}liquidacion_especie')
    if el is not None:
        self['LiquidacionEspecie'] = liquidacion_especie1(cls, el)
    return self
def liquidacion_numerario1(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/jys}fecha_pago')
    self['FechaPago'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/jys}instrumento_monetario')
    self['InstrumentoMonetario'] = catalog_code('C329_instrumento_monetario_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/jys}moneda')
    self['Moneda'] = catalog_code('C329_moneda_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/jys}monto_operacion')
    self['MontoOperacion'] = el.text
    return self
def liquidacion_especie1(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/jys}valor_bien')
    self['ValorBien'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/jys}moneda')
    self['Moneda'] = catalog_code('C329_moneda_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/jys}bien_liquidacion')
    self['BienLiquidacion'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/jys}datos_bien_liquidacion')
    if el is not None:
        self['DatosBienLiquidacion'] = datos_bien_liquidacion0(cls, el)
    return self
def datos_bien_liquidacion0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/jys}datos_inmueble')
    if el is not None:
        self['DatosInmueble'] = datos_inmueble3(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/jys}datos_otro')
    if el is not None:
        self['DatosOtro'] = datos_otro2(cls, el)
    return self
def datos_inmueble3(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/jys}tipo_inmueble')
    self['TipoInmueble'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/jys}codigo_postal')
    self['CodigoPostal'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/jys}folio_real')
    self['FolioReal'] = el.text
    return self
def datos_otro2(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/jys}descripcion_bien_liquidacion')
    self['DescripcionBienLiquidacion'] = el.text
    return self
def archivo_typea(cls, node):
    self = ScalarMap()
    self['Informe'] = [informe9(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/mjr}informe')]
    return self
def informe9(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mjr}mes_reportado')
    self['MesReportado'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mjr}sujeto_obligado')
    self['SujetoObligado'] = sujeto_obligado9(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mjr}aviso')
    if el is not None:
        self['Aviso'] = [avisoa(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/mjr}aviso')]
    return self
def sujeto_obligado9(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mjr}clave_entidad_colegiada')
    if el is not None:
        self['ClaveEntidadColegiada'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mjr}clave_sujeto_obligado')
    self['ClaveSujetoObligado'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mjr}clave_actividad')
    self['ClaveActividad'] = catalog_code('C329_clave_actividad_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mjr}exento')
    if el is not None:
        self['Exento'] = el.text
    return self
def avisoa(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mjr}referencia_aviso')
    self['ReferenciaAviso'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mjr}modificatorio')
    if el is not None:
        self['Modificatorio'] = modificatorio9(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mjr}prioridad')
    self['Prioridad'] = catalog_code('C329_prioridad_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mjr}alerta')
    self['Alerta'] = alertaa(cls, el)
    self['PersonaAviso'] = [persona_aviso8(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/mjr}persona_aviso')]
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mjr}dueno_beneficiario')
    if el is not None:
        self['DuenoBeneficiario'] = [dueno_beneficiario7(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/mjr}dueno_beneficiario')]
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mjr}detalle_operaciones')
    self['DetalleOperaciones'] = detalle_operaciones9(cls, el)
    return self
def modificatorio9(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mjr}folio_modificacion')
    self['FolioModificacion'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mjr}descripcion_modificacion')
    self['DescripcionModificacion'] = el.text
    return self
def alertaa(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mjr}tipo_alerta')
    self['TipoAlerta'] = catalog_code('C329_tipo_alerta_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mjr}descripcion_alerta')
    if el is not None:
        self['DescripcionAlerta'] = el.text
    return self
def persona_aviso8(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mjr}tipo_persona')
    self['TipoPersona'] = tipo_persona12(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mjr}tipo_domicilio')
    if el is not None:
        self['TipoDomicilio'] = tipo_domicilio8(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mjr}telefono')
    if el is not None:
        self['Telefono'] = telefono9(cls, el)
    return self
def tipo_persona12(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mjr}persona_fisica')
    if el is not None:
        self['PersonaFisica'] = persona_fisica14(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mjr}persona_moral')
    if el is not None:
        self['PersonaMoral'] = persona_moral15(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mjr}fideicomiso')
    if el is not None:
        self['Fideicomiso'] = fideicomiso11(cls, el)
    return self
def persona_fisica14(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mjr}nombre')
    self['Nombre'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mjr}apellido_paterno')
    self['ApellidoPaterno'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mjr}apellido_materno')
    self['ApellidoMaterno'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mjr}fecha_nacimiento')
    if el is not None:
        self['FechaNacimiento'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mjr}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mjr}curp')
    if el is not None:
        self['Curp'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mjr}pais_nacionalidad')
    self['PaisNacionalidad'] = catalog_code('C329_pais_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mjr}actividad_economica')
    self['ActividadEconomica'] = catalog_code('C329_actividad_economica_type', el.text)
    return self
def persona_moral15(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mjr}denominacion_razon')
    self['DenominacionRazon'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mjr}fecha_constitucion')
    if el is not None:
        self['FechaConstitucion'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mjr}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mjr}pais_nacionalidad')
    self['PaisNacionalidad'] = catalog_code('C329_pais_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mjr}giro_mercantil')
    self['GiroMercantil'] = catalog_code('C329_giro_mercantil_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mjr}representante_apoderado')
    self['RepresentanteApoderado'] = representante_apoderado8(cls, el)
    return self
def fideicomiso11(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mjr}denominacion_razon')
    self['DenominacionRazon'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mjr}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mjr}identificador_fideicomiso')
    if el is not None:
        self['IdentificadorFideicomiso'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mjr}apoderado_delegado')
    self['ApoderadoDelegado'] = representante_apoderado8(cls, el)
    return self
def representante_apoderado8(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mjr}nombre')
    self['Nombre'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mjr}apellido_paterno')
    self['ApellidoPaterno'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mjr}apellido_materno')
    self['ApellidoMaterno'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mjr}fecha_nacimiento')
    if el is not None:
        self['FechaNacimiento'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mjr}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mjr}curp')
    if el is not None:
        self['Curp'] = el.text
    return self
def tipo_domicilio8(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mjr}nacional')
    if el is not None:
        self['Nacional'] = nacionala(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mjr}extranjero')
    if el is not None:
        self['Extranjero'] = extranjeroa(cls, el)
    return self
def nacionala(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mjr}colonia')
    self['Colonia'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mjr}calle')
    self['Calle'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mjr}numero_exterior')
    self['NumeroExterior'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mjr}numero_interior')
    if el is not None:
        self['NumeroInterior'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mjr}codigo_postal')
    self['CodigoPostal'] = el.text
    return self
def extranjeroa(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mjr}pais')
    self['Pais'] = catalog_code('C329_pais_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mjr}estado_provincia')
    self['EstadoProvincia'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mjr}ciudad_poblacion')
    self['CiudadPoblacion'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mjr}colonia')
    self['Colonia'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mjr}calle')
    self['Calle'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mjr}numero_exterior')
    self['NumeroExterior'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mjr}numero_interior')
    if el is not None:
        self['NumeroInterior'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mjr}codigo_postal')
    self['CodigoPostal'] = el.text
    return self
def telefono9(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mjr}clave_pais')
    if el is not None:
        self['ClavePais'] = catalog_code('C329_pais_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mjr}numero_telefono')
    if el is not None:
        self['NumeroTelefono'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mjr}correo_electronico')
    if el is not None:
        self['CorreoElectronico'] = el.text
    return self
def dueno_beneficiario7(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mjr}tipo_persona')
    self['TipoPersona'] = tipo_persona13(cls, el)
    return self
def tipo_persona13(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mjr}persona_fisica')
    if el is not None:
        self['PersonaFisica'] = persona_fisica15(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mjr}persona_moral')
    if el is not None:
        self['PersonaMoral'] = persona_moral16(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mjr}fideicomiso')
    if el is not None:
        self['Fideicomiso'] = fideicomiso12(cls, el)
    return self
def persona_fisica15(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mjr}nombre')
    self['Nombre'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mjr}apellido_paterno')
    self['ApellidoPaterno'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mjr}apellido_materno')
    self['ApellidoMaterno'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mjr}fecha_nacimiento')
    if el is not None:
        self['FechaNacimiento'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mjr}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mjr}curp')
    if el is not None:
        self['Curp'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mjr}pais_nacionalidad')
    if el is not None:
        self['PaisNacionalidad'] = catalog_code('C329_pais_type', el.text)
    return self
def persona_moral16(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mjr}denominacion_razon')
    self['DenominacionRazon'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mjr}fecha_constitucion')
    if el is not None:
        self['FechaConstitucion'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mjr}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mjr}pais_nacionalidad')
    if el is not None:
        self['PaisNacionalidad'] = catalog_code('C329_pais_type', el.text)
    return self
def fideicomiso12(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mjr}denominacion_razon')
    self['DenominacionRazon'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mjr}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mjr}identificador_fideicomiso')
    if el is not None:
        self['IdentificadorFideicomiso'] = el.text
    return self
def detalle_operaciones9(cls, node):
    self = ScalarMap()
    self['DatosOperacion'] = [datos_operacion9(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/mjr}datos_operacion')]
    return self
def datos_operacion9(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mjr}fecha_operacion')
    self['FechaOperacion'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mjr}codigo_postal')
    self['CodigoPostal'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mjr}tipo_operacion')
    self['TipoOperacion'] = catalog_code('C329_tipo_operacion_type', el.text)
    self['DatosBien'] = [datos_bien0(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/mjr}datos_bien')]
    self['DatosLiquidacion'] = [datos_liquidacion8(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/mjr}datos_liquidacion')]
    return self
def datos_bien0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mjr}tipo_bien')
    self['TipoBien'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mjr}unidad_comercializada')
    self['UnidadComercializada'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mjr}cantidad_comercializada')
    self['CantidadComercializada'] = el.text
    return self
def datos_liquidacion8(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mjr}fecha_pago')
    self['FechaPago'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mjr}forma_pago')
    self['FormaPago'] = catalog_code('C329_forma_pago_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mjr}instrumento_monetario')
    self['InstrumentoMonetario'] = catalog_code('C329_instrumento_monetario_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mjr}moneda')
    self['Moneda'] = catalog_code('C329_moneda_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mjr}monto_operacion')
    self['MontoOperacion'] = el.text
    return self
def archivo_typeb(cls, node):
    self = ScalarMap()
    self['Informe'] = [informea(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/mpc}informe')]
    return self
def informea(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mpc}mes_reportado')
    self['MesReportado'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mpc}sujeto_obligado')
    self['SujetoObligado'] = sujeto_obligadoa(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mpc}aviso')
    if el is not None:
        self['Aviso'] = [avisob(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/mpc}aviso')]
    return self
def sujeto_obligadoa(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mpc}clave_entidad_colegiada')
    if el is not None:
        self['ClaveEntidadColegiada'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mpc}clave_sujeto_obligado')
    self['ClaveSujetoObligado'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mpc}clave_actividad')
    self['ClaveActividad'] = catalog_code('C329_clave_actividad_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mpc}exento')
    if el is not None:
        self['Exento'] = el.text
    return self
def avisob(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mpc}referencia_aviso')
    self['ReferenciaAviso'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mpc}modificatorio')
    if el is not None:
        self['Modificatorio'] = modificatorioa(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mpc}prioridad')
    self['Prioridad'] = catalog_code('C329_prioridad_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mpc}alerta')
    self['Alerta'] = alertab(cls, el)
    self['PersonaAviso'] = [persona_aviso9(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/mpc}persona_aviso')]
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mpc}dueno_beneficiario')
    if el is not None:
        self['DuenoBeneficiario'] = [dueno_beneficiario8(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/mpc}dueno_beneficiario')]
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mpc}detalle_operaciones')
    self['DetalleOperaciones'] = detalle_operacionesa(cls, el)
    return self
def modificatorioa(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mpc}folio_modificacion')
    self['FolioModificacion'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mpc}descripcion_modificacion')
    self['DescripcionModificacion'] = el.text
    return self
def alertab(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mpc}tipo_alerta')
    self['TipoAlerta'] = catalog_code('C329_tipo_alerta_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mpc}descripcion_alerta')
    if el is not None:
        self['DescripcionAlerta'] = el.text
    return self
def persona_aviso9(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mpc}tipo_persona')
    self['TipoPersona'] = tipo_persona14(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mpc}tipo_domicilio')
    if el is not None:
        self['TipoDomicilio'] = tipo_domicilio9(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mpc}telefono')
    if el is not None:
        self['Telefono'] = telefonoa(cls, el)
    return self
def tipo_persona14(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mpc}persona_fisica')
    if el is not None:
        self['PersonaFisica'] = persona_fisica16(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mpc}persona_moral')
    if el is not None:
        self['PersonaMoral'] = persona_moral17(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mpc}fideicomiso')
    if el is not None:
        self['Fideicomiso'] = fideicomiso13(cls, el)
    return self
def persona_fisica16(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mpc}nombre')
    self['Nombre'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mpc}apellido_paterno')
    self['ApellidoPaterno'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mpc}apellido_materno')
    self['ApellidoMaterno'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mpc}fecha_nacimiento')
    if el is not None:
        self['FechaNacimiento'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mpc}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mpc}curp')
    if el is not None:
        self['Curp'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mpc}pais_nacionalidad')
    self['PaisNacionalidad'] = catalog_code('C329_pais_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mpc}actividad_economica')
    self['ActividadEconomica'] = catalog_code('C329_actividad_economica_type', el.text)
    return self
def persona_moral17(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mpc}denominacion_razon')
    self['DenominacionRazon'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mpc}fecha_constitucion')
    if el is not None:
        self['FechaConstitucion'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mpc}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mpc}pais_nacionalidad')
    self['PaisNacionalidad'] = catalog_code('C329_pais_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mpc}giro_mercantil')
    self['GiroMercantil'] = catalog_code('C329_giro_mercantil_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mpc}representante_apoderado')
    self['RepresentanteApoderado'] = representante_apoderado9(cls, el)
    return self
def fideicomiso13(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mpc}denominacion_razon')
    self['DenominacionRazon'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mpc}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mpc}identificador_fideicomiso')
    if el is not None:
        self['IdentificadorFideicomiso'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mpc}apoderado_delegado')
    self['ApoderadoDelegado'] = representante_apoderado9(cls, el)
    return self
def representante_apoderado9(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mpc}nombre')
    self['Nombre'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mpc}apellido_paterno')
    self['ApellidoPaterno'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mpc}apellido_materno')
    self['ApellidoMaterno'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mpc}fecha_nacimiento')
    if el is not None:
        self['FechaNacimiento'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mpc}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mpc}curp')
    if el is not None:
        self['Curp'] = el.text
    return self
def tipo_domicilio9(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mpc}nacional')
    if el is not None:
        self['Nacional'] = nacionalb(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mpc}extranjero')
    if el is not None:
        self['Extranjero'] = extranjerob(cls, el)
    return self
def nacionalb(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mpc}colonia')
    self['Colonia'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mpc}calle')
    self['Calle'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mpc}numero_exterior')
    self['NumeroExterior'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mpc}numero_interior')
    if el is not None:
        self['NumeroInterior'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mpc}codigo_postal')
    self['CodigoPostal'] = el.text
    return self
def extranjerob(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mpc}pais')
    self['Pais'] = catalog_code('C329_pais_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mpc}estado_provincia')
    self['EstadoProvincia'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mpc}ciudad_poblacion')
    self['CiudadPoblacion'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mpc}colonia')
    self['Colonia'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mpc}calle')
    self['Calle'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mpc}numero_exterior')
    self['NumeroExterior'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mpc}numero_interior')
    if el is not None:
        self['NumeroInterior'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mpc}codigo_postal')
    self['CodigoPostal'] = el.text
    return self
def telefonoa(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mpc}clave_pais')
    if el is not None:
        self['ClavePais'] = catalog_code('C329_pais_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mpc}numero_telefono')
    if el is not None:
        self['NumeroTelefono'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mpc}correo_electronico')
    if el is not None:
        self['CorreoElectronico'] = el.text
    return self
def dueno_beneficiario8(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mpc}tipo_persona')
    self['TipoPersona'] = tipo_persona15(cls, el)
    return self
def tipo_persona15(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mpc}persona_fisica')
    if el is not None:
        self['PersonaFisica'] = persona_fisica17(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mpc}persona_moral')
    if el is not None:
        self['PersonaMoral'] = persona_moral18(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mpc}fideicomiso')
    if el is not None:
        self['Fideicomiso'] = fideicomiso14(cls, el)
    return self
def persona_fisica17(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mpc}nombre')
    self['Nombre'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mpc}apellido_paterno')
    self['ApellidoPaterno'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mpc}apellido_materno')
    self['ApellidoMaterno'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mpc}fecha_nacimiento')
    if el is not None:
        self['FechaNacimiento'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mpc}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mpc}curp')
    if el is not None:
        self['Curp'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mpc}pais_nacionalidad')
    if el is not None:
        self['PaisNacionalidad'] = catalog_code('C329_pais_type', el.text)
    return self
def persona_moral18(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mpc}denominacion_razon')
    self['DenominacionRazon'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mpc}fecha_constitucion')
    if el is not None:
        self['FechaConstitucion'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mpc}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mpc}pais_nacionalidad')
    if el is not None:
        self['PaisNacionalidad'] = catalog_code('C329_pais_type', el.text)
    return self
def fideicomiso14(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mpc}denominacion_razon')
    self['DenominacionRazon'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mpc}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mpc}identificador_fideicomiso')
    if el is not None:
        self['IdentificadorFideicomiso'] = el.text
    return self
def detalle_operacionesa(cls, node):
    self = ScalarMap()
    self['DatosOperacion'] = [datos_operaciona(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/mpc}datos_operacion')]
    return self
def datos_operaciona(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mpc}fecha_operacion')
    self['FechaOperacion'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mpc}codigo_postal')
    self['CodigoPostal'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mpc}tipo_operacion')
    self['TipoOperacion'] = catalog_code('C329_tipo_operacion_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mpc}datos_garantia')
    if el is not None:
        self['DatosGarantia'] = [datos_garantia2(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/mpc}datos_garantia')]
    self['DatosLiquidacion'] = [datos_liquidacion9(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/mpc}datos_liquidacion')]
    return self
def datos_garantia2(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mpc}tipo_garantia')
    self['TipoGarantia'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mpc}datos_bien_mutuo')
    if el is not None:
        self['DatosBienMutuo'] = datos_bien_mutuo1(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mpc}tipo_persona')
    if el is not None:
        self['TipoPersona'] = tipo_persona16(cls, el)
    return self
def datos_bien_mutuo1(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mpc}datos_inmueble')
    if el is not None:
        self['DatosInmueble'] = datos_inmueble4(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mpc}datos_otro')
    if el is not None:
        self['DatosOtro'] = datos_otro3(cls, el)
    return self
def datos_inmueble4(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mpc}tipo_inmueble')
    self['TipoInmueble'] = catalog_code('C329_tipo_inmueble_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mpc}valor_referencia')
    self['ValorReferencia'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mpc}codigo_postal')
    self['CodigoPostal'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mpc}folio_real')
    self['FolioReal'] = el.text
    return self
def datos_otro3(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mpc}descripcion_garantia')
    self['DescripcionGarantia'] = el.text
    return self
def tipo_persona16(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mpc}persona_fisica')
    if el is not None:
        self['PersonaFisica'] = persona_fisica18(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mpc}persona_moral')
    if el is not None:
        self['PersonaMoral'] = persona_moral19(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mpc}fideicomiso')
    if el is not None:
        self['Fideicomiso'] = fideicomiso15(cls, el)
    return self
def persona_fisica18(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mpc}nombre')
    self['Nombre'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mpc}apellido_paterno')
    self['ApellidoPaterno'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mpc}apellido_materno')
    self['ApellidoMaterno'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mpc}fecha_nacimiento')
    if el is not None:
        self['FechaNacimiento'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mpc}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mpc}curp')
    if el is not None:
        self['Curp'] = el.text
    return self
def persona_moral19(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mpc}denominacion_razon')
    self['DenominacionRazon'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mpc}fecha_constitucion')
    if el is not None:
        self['FechaConstitucion'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mpc}rfc')
    if el is not None:
        self['Rfc'] = el.text
    return self
def fideicomiso15(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mpc}denominacion_razon')
    self['DenominacionRazon'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mpc}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mpc}identificador_fideicomiso')
    if el is not None:
        self['IdentificadorFideicomiso'] = el.text
    return self
def datos_liquidacion9(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mpc}fecha_disposicion')
    self['FechaDisposicion'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mpc}instrumento_monetario')
    self['InstrumentoMonetario'] = catalog_code('C329_instrumento_monetario_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mpc}moneda')
    self['Moneda'] = catalog_code('C329_moneda_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/mpc}monto_operacion')
    self['MontoOperacion'] = el.text
    return self
def datos_liquidacion_type0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/oba}fecha_pago')
    self['FechaPago'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/oba}forma_pago')
    self['FormaPago'] = catalog_code('C329_forma_pago_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/oba}instrumento_monetario')
    if el is not None:
        self['InstrumentoMonetario'] = catalog_code('C329_instrumento_monetario_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/oba}moneda')
    self['Moneda'] = catalog_code('C329_moneda_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/oba}monto_operacion')
    self['MontoOperacion'] = el.text
    return self
def detalle_operaciones_type0(cls, node):
    self = ScalarMap()
    self['DatosOperacion'] = [datos_operacionb(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/oba}datos_operacion')]
    return self
def datos_operacionb(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/oba}fecha_operacion')
    self['FechaOperacion'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/oba}codigo_postal')
    self['CodigoPostal'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/oba}tipo_operacion')
    self['TipoOperacion'] = catalog_code('C329_tipo_operacion_type', el.text)
    self['DatosObjeto'] = [datos_objeto0(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/oba}datos_objeto')]
    self['DatosLiquidacion'] = [datos_liquidacion_type0(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/oba}datos_liquidacion')]
    return self
def datos_objeto0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/oba}tipo_objeto')
    self['TipoObjeto'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/oba}descripcion')
    self['Descripcion'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/oba}numero_registro')
    if el is not None:
        self['NumeroRegistro'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/oba}valor_referencia')
    if el is not None:
        self['ValorReferencia'] = el.text
    return self
def archivo_typec(cls, node):
    self = ScalarMap()
    self['Informe'] = [informeb(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/oba}informe')]
    return self
def informeb(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/oba}mes_reportado')
    self['MesReportado'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/oba}sujeto_obligado')
    self['SujetoObligado'] = sujeto_obligadob(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/oba}aviso')
    if el is not None:
        self['Aviso'] = [avisoc(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/oba}aviso')]
    return self
def sujeto_obligadob(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/oba}clave_entidad_colegiada')
    if el is not None:
        self['ClaveEntidadColegiada'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/oba}clave_sujeto_obligado')
    self['ClaveSujetoObligado'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/oba}clave_actividad')
    self['ClaveActividad'] = catalog_code('C329_clave_actividad_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/oba}exento')
    if el is not None:
        self['Exento'] = el.text
    return self
def avisoc(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/oba}referencia_aviso')
    self['ReferenciaAviso'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/oba}modificatorio')
    if el is not None:
        self['Modificatorio'] = modificatoriob(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/oba}prioridad')
    self['Prioridad'] = catalog_code('C329_prioridad_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/oba}alerta')
    self['Alerta'] = alertac(cls, el)
    self['PersonaAviso'] = [persona_avisoa(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/oba}persona_aviso')]
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/oba}dueno_beneficiario')
    if el is not None:
        self['DuenoBeneficiario'] = [dueno_beneficiario9(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/oba}dueno_beneficiario')]
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/oba}detalle_operaciones')
    self['DetalleOperaciones'] = detalle_operaciones_type0(cls, el)
    return self
def modificatoriob(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/oba}folio_modificacion')
    self['FolioModificacion'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/oba}descripcion_modificacion')
    self['DescripcionModificacion'] = el.text
    return self
def alertac(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/oba}tipo_alerta')
    self['TipoAlerta'] = catalog_code('C329_tipo_alerta_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/oba}descripcion_alerta')
    if el is not None:
        self['DescripcionAlerta'] = el.text
    return self
def persona_avisoa(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/oba}tipo_persona')
    self['TipoPersona'] = tipo_persona17(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/oba}tipo_domicilio')
    if el is not None:
        self['TipoDomicilio'] = tipo_domicilioa(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/oba}telefono')
    if el is not None:
        self['Telefono'] = telefonob(cls, el)
    return self
def tipo_persona17(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/oba}persona_fisica')
    if el is not None:
        self['PersonaFisica'] = persona_fisica19(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/oba}persona_moral')
    if el is not None:
        self['PersonaMoral'] = persona_moral1a(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/oba}fideicomiso')
    if el is not None:
        self['Fideicomiso'] = fideicomiso16(cls, el)
    return self
def persona_fisica19(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/oba}nombre')
    self['Nombre'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/oba}apellido_paterno')
    self['ApellidoPaterno'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/oba}apellido_materno')
    self['ApellidoMaterno'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/oba}fecha_nacimiento')
    if el is not None:
        self['FechaNacimiento'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/oba}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/oba}curp')
    if el is not None:
        self['Curp'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/oba}pais_nacionalidad')
    self['PaisNacionalidad'] = catalog_code('C329_pais_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/oba}actividad_economica')
    self['ActividadEconomica'] = catalog_code('C329_actividad_economica_type', el.text)
    return self
def persona_moral1a(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/oba}denominacion_razon')
    self['DenominacionRazon'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/oba}fecha_constitucion')
    if el is not None:
        self['FechaConstitucion'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/oba}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/oba}pais_nacionalidad')
    self['PaisNacionalidad'] = catalog_code('C329_pais_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/oba}giro_mercantil')
    self['GiroMercantil'] = catalog_code('C329_giro_mercantil_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/oba}representante_apoderado')
    self['RepresentanteApoderado'] = representante_apoderadoa(cls, el)
    return self
def fideicomiso16(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/oba}denominacion_razon')
    self['DenominacionRazon'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/oba}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/oba}identificador_fideicomiso')
    if el is not None:
        self['IdentificadorFideicomiso'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/oba}apoderado_delegado')
    self['ApoderadoDelegado'] = representante_apoderadoa(cls, el)
    return self
def representante_apoderadoa(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/oba}nombre')
    self['Nombre'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/oba}apellido_paterno')
    self['ApellidoPaterno'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/oba}apellido_materno')
    self['ApellidoMaterno'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/oba}fecha_nacimiento')
    if el is not None:
        self['FechaNacimiento'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/oba}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/oba}curp')
    if el is not None:
        self['Curp'] = el.text
    return self
def tipo_domicilioa(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/oba}nacional')
    if el is not None:
        self['Nacional'] = nacionalc(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/oba}extranjero')
    if el is not None:
        self['Extranjero'] = extranjeroc(cls, el)
    return self
def nacionalc(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/oba}colonia')
    self['Colonia'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/oba}calle')
    self['Calle'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/oba}numero_exterior')
    self['NumeroExterior'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/oba}numero_interior')
    if el is not None:
        self['NumeroInterior'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/oba}codigo_postal')
    self['CodigoPostal'] = el.text
    return self
def extranjeroc(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/oba}pais')
    self['Pais'] = catalog_code('C329_pais_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/oba}estado_provincia')
    self['EstadoProvincia'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/oba}ciudad_poblacion')
    self['CiudadPoblacion'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/oba}colonia')
    self['Colonia'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/oba}calle')
    self['Calle'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/oba}numero_exterior')
    self['NumeroExterior'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/oba}numero_interior')
    if el is not None:
        self['NumeroInterior'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/oba}codigo_postal')
    self['CodigoPostal'] = el.text
    return self
def telefonob(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/oba}clave_pais')
    if el is not None:
        self['ClavePais'] = catalog_code('C329_pais_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/oba}numero_telefono')
    if el is not None:
        self['NumeroTelefono'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/oba}correo_electronico')
    if el is not None:
        self['CorreoElectronico'] = el.text
    return self
def dueno_beneficiario9(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/oba}tipo_persona')
    self['TipoPersona'] = tipo_persona18(cls, el)
    return self
def tipo_persona18(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/oba}persona_fisica')
    if el is not None:
        self['PersonaFisica'] = persona_fisica1a(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/oba}persona_moral')
    if el is not None:
        self['PersonaMoral'] = persona_moral1b(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/oba}fideicomiso')
    if el is not None:
        self['Fideicomiso'] = fideicomiso17(cls, el)
    return self
def persona_fisica1a(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/oba}nombre')
    self['Nombre'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/oba}apellido_paterno')
    self['ApellidoPaterno'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/oba}apellido_materno')
    self['ApellidoMaterno'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/oba}fecha_nacimiento')
    if el is not None:
        self['FechaNacimiento'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/oba}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/oba}curp')
    if el is not None:
        self['Curp'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/oba}pais_nacionalidad')
    if el is not None:
        self['PaisNacionalidad'] = catalog_code('C329_pais_type', el.text)
    return self
def persona_moral1b(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/oba}denominacion_razon')
    self['DenominacionRazon'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/oba}fecha_constitucion')
    if el is not None:
        self['FechaConstitucion'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/oba}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/oba}pais_nacionalidad')
    if el is not None:
        self['PaisNacionalidad'] = catalog_code('C329_pais_type', el.text)
    return self
def fideicomiso17(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/oba}denominacion_razon')
    self['DenominacionRazon'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/oba}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/oba}identificador_fideicomiso')
    if el is not None:
        self['IdentificadorFideicomiso'] = el.text
    return self
def archivo_typed(cls, node):
    self = ScalarMap()
    self['Informe'] = [informec(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/spr}informe')]
    return self
def informec(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}mes_reportado')
    self['MesReportado'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}sujeto_obligado')
    self['SujetoObligado'] = sujeto_obligadoc(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}aviso')
    if el is not None:
        self['Aviso'] = [avisod(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/spr}aviso')]
    return self
def sujeto_obligadoc(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}clave_entidad_colegiada')
    if el is not None:
        self['ClaveEntidadColegiada'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}clave_sujeto_obligado')
    self['ClaveSujetoObligado'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}ocupacion')
    if el is not None:
        self['Ocupacion'] = ocupacion0(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}clave_actividad')
    self['ClaveActividad'] = catalog_code('C329_clave_actividad_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}exento')
    if el is not None:
        self['Exento'] = el.text
    return self
def ocupacion0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}tipo_ocupacion')
    self['TipoOcupacion'] = Xint(el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}descripcion_otra_ocupacion')
    if el is not None:
        self['DescripcionOtraOcupacion'] = el.text
    return self
def avisod(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}referencia_aviso')
    self['ReferenciaAviso'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}modificatorio')
    if el is not None:
        self['Modificatorio'] = modificatorioc(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}prioridad')
    self['Prioridad'] = catalog_code('C329_prioridad_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}alerta')
    self['Alerta'] = alertad(cls, el)
    self['PersonaAviso'] = [persona_avisob(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/spr}persona_aviso')]
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}dueno_beneficiario')
    if el is not None:
        self['DuenoBeneficiario'] = [dueno_beneficiarioa(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/spr}dueno_beneficiario')]
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}detalle_operaciones')
    self['DetalleOperaciones'] = detalle_operacionesb(cls, el)
    return self
def modificatorioc(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}folio_modificacion')
    self['FolioModificacion'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}descripcion_modificacion')
    self['DescripcionModificacion'] = el.text
    return self
def alertad(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}tipo_alerta')
    self['TipoAlerta'] = catalog_code('C329_tipo_alerta_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}descripcion_alerta')
    if el is not None:
        self['DescripcionAlerta'] = el.text
    return self
def persona_avisob(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}tipo_persona')
    self['TipoPersona'] = tipo_persona19(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}tipo_domicilio')
    if el is not None:
        self['TipoDomicilio'] = tipo_domiciliob(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}telefono')
    if el is not None:
        self['Telefono'] = telefonoc(cls, el)
    return self
def tipo_persona19(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}persona_fisica')
    if el is not None:
        self['PersonaFisica'] = persona_fisica1b(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}persona_moral')
    if el is not None:
        self['PersonaMoral'] = persona_moral1c(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}fideicomiso')
    if el is not None:
        self['Fideicomiso'] = fideicomiso18(cls, el)
    return self
def persona_fisica1b(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}nombre')
    self['Nombre'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}apellido_paterno')
    self['ApellidoPaterno'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}apellido_materno')
    self['ApellidoMaterno'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}fecha_nacimiento')
    if el is not None:
        self['FechaNacimiento'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}curp')
    if el is not None:
        self['Curp'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}pais_nacionalidad')
    self['PaisNacionalidad'] = catalog_code('C329_pais_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}actividad_economica')
    self['ActividadEconomica'] = catalog_code('C329_actividad_economica_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}representante_apoderado')
    if el is not None:
        self['RepresentanteApoderado'] = [representante_apoderadob(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/spr}representante_apoderado')]
    return self
def persona_moral1c(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}denominacion_razon')
    self['DenominacionRazon'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}fecha_constitucion')
    if el is not None:
        self['FechaConstitucion'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}pais_nacionalidad')
    self['PaisNacionalidad'] = catalog_code('C329_pais_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}giro_mercantil')
    self['GiroMercantil'] = catalog_code('C329_giro_mercantil_type', el.text)
    self['RepresentanteApoderado'] = [representante_apoderadob(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/spr}representante_apoderado')]
    return self
def fideicomiso18(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}denominacion_razon')
    self['DenominacionRazon'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}identificador_fideicomiso')
    if el is not None:
        self['IdentificadorFideicomiso'] = el.text
    self['ApoderadoDelegado'] = [representante_apoderadob(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/spr}apoderado_delegado')]
    return self
def representante_apoderadob(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}nombre')
    self['Nombre'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}apellido_paterno')
    self['ApellidoPaterno'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}apellido_materno')
    self['ApellidoMaterno'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}fecha_nacimiento')
    if el is not None:
        self['FechaNacimiento'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}curp')
    if el is not None:
        self['Curp'] = el.text
    return self
def tipo_domiciliob(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}nacional')
    if el is not None:
        self['Nacional'] = nacionald(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}extranjero')
    if el is not None:
        self['Extranjero'] = extranjerod(cls, el)
    return self
def nacionald(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}colonia')
    self['Colonia'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}calle')
    self['Calle'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}numero_exterior')
    self['NumeroExterior'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}numero_interior')
    if el is not None:
        self['NumeroInterior'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}codigo_postal')
    self['CodigoPostal'] = el.text
    return self
def extranjerod(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}pais')
    self['Pais'] = catalog_code('C329_pais_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}estado_provincia')
    self['EstadoProvincia'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}ciudad_poblacion')
    self['CiudadPoblacion'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}colonia')
    self['Colonia'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}calle')
    self['Calle'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}numero_exterior')
    self['NumeroExterior'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}numero_interior')
    if el is not None:
        self['NumeroInterior'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}codigo_postal')
    self['CodigoPostal'] = el.text
    return self
def telefonoc(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}clave_pais')
    if el is not None:
        self['ClavePais'] = catalog_code('C329_pais_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}numero_telefono')
    if el is not None:
        self['NumeroTelefono'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}correo_electronico')
    if el is not None:
        self['CorreoElectronico'] = el.text
    return self
def dueno_beneficiarioa(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}tipo_persona')
    self['TipoPersona'] = tipo_persona1a(cls, el)
    return self
def tipo_persona1a(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}persona_fisica')
    if el is not None:
        self['PersonaFisica'] = persona_fisica1c(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}persona_moral')
    if el is not None:
        self['PersonaMoral'] = persona_moral1d(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}fideicomiso')
    if el is not None:
        self['Fideicomiso'] = fideicomiso19(cls, el)
    return self
def persona_fisica1c(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}nombre')
    self['Nombre'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}apellido_paterno')
    self['ApellidoPaterno'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}apellido_materno')
    self['ApellidoMaterno'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}fecha_nacimiento')
    if el is not None:
        self['FechaNacimiento'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}curp')
    if el is not None:
        self['Curp'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}pais_nacionalidad')
    if el is not None:
        self['PaisNacionalidad'] = catalog_code('C329_pais_type', el.text)
    return self
def persona_moral1d(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}denominacion_razon')
    self['DenominacionRazon'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}fecha_constitucion')
    if el is not None:
        self['FechaConstitucion'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}pais_nacionalidad')
    if el is not None:
        self['PaisNacionalidad'] = catalog_code('C329_pais_type', el.text)
    return self
def fideicomiso19(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}denominacion_razon')
    self['DenominacionRazon'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}identificador_fideicomiso')
    if el is not None:
        self['IdentificadorFideicomiso'] = el.text
    return self
def detalle_operacionesb(cls, node):
    self = ScalarMap()
    self['DatosOperacion'] = [datos_operacionc(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/spr}datos_operacion')]
    return self
def datos_operacionc(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}fecha_operacion')
    self['FechaOperacion'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}tipo_actividad')
    self['TipoActividad'] = tipo_actividad2(cls, el)
    self['DatosOperacionFinanciera'] = [datos_operacion_financiera0(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/spr}datos_operacion_financiera')]
    return self
def tipo_actividad2(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}compra_venta_inmuebles')
    if el is not None:
        self['CompraVentaInmuebles'] = compra_venta_inmuebles0(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}cesion_derechos_inmuebles')
    if el is not None:
        self['CesionDerechosInmuebles'] = cesion_derechos_inmuebles0(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}administracion_recursos')
    if el is not None:
        self['AdministracionRecursos'] = administracion_recursos0(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}constitucion_sociedades_mercantiles')
    if el is not None:
        self['ConstitucionSociedadesMercantiles'] = constitucion_sociedades_mercantiles0(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}organizacion_aportaciones')
    if el is not None:
        self['OrganizacionAportaciones'] = organizacion_aportaciones0(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}fusion')
    if el is not None:
        self['Fusion'] = fusion1(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}escision')
    if el is not None:
        self['Escision'] = escision1(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}administracion_personas_morales')
    if el is not None:
        self['AdministracionPersonasMorales'] = administracion_personas_morales0(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}constitucion_fideicomiso')
    if el is not None:
        self['ConstitucionFideicomiso'] = constitucion_fideicomiso0(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}compra_venta_entidades_mercantiles')
    if el is not None:
        self['CompraVentaEntidadesMercantiles'] = compra_venta_entidades_mercantiles0(cls, el)
    return self
def compra_venta_inmuebles0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}tipo_operacion')
    self['TipoOperacion'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}valor_pactado')
    self['ValorPactado'] = el.text
    self['DatosContraparte'] = [datos_contraparte1(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/spr}datos_contraparte')]
    self['CaracteristicasInmueble'] = [caracteristicas_inmueble2(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/spr}caracteristicas_inmueble')]
    return self
def datos_contraparte1(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}tipo_persona')
    self['TipoPersona'] = tipo_persona1b(cls, el)
    return self
def tipo_persona1b(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}persona_fisica')
    if el is not None:
        self['PersonaFisica'] = persona_fisica1d(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}persona_moral')
    if el is not None:
        self['PersonaMoral'] = persona_moral1e(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}fideicomiso')
    if el is not None:
        self['Fideicomiso'] = fideicomiso19(cls, el)
    return self
def persona_fisica1d(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}nombre')
    self['Nombre'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}apellido_paterno')
    self['ApellidoPaterno'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}apellido_materno')
    self['ApellidoMaterno'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}fecha_nacimiento')
    if el is not None:
        self['FechaNacimiento'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}curp')
    if el is not None:
        self['Curp'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}pais_nacionalidad')
    self['PaisNacionalidad'] = catalog_code('C329_pais_type', el.text)
    return self
def persona_moral1e(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}denominacion_razon')
    self['DenominacionRazon'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}fecha_constitucion')
    if el is not None:
        self['FechaConstitucion'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}pais_nacionalidad')
    self['PaisNacionalidad'] = catalog_code('C329_pais_type', el.text)
    return self
def caracteristicas_inmueble2(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}tipo_inmueble')
    self['TipoInmueble'] = catalog_code('C329_tipo_inmueble_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}colonia')
    self['Colonia'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}calle')
    self['Calle'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}numero_exterior')
    self['NumeroExterior'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}numero_interior')
    if el is not None:
        self['NumeroInterior'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}codigo_postal')
    self['CodigoPostal'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}dimension_terreno')
    self['DimensionTerreno'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}dimension_construido')
    self['DimensionConstruido'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}folio_real')
    self['FolioReal'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}contrato_instrumento_publico')
    self['ContratoInstrumentoPublico'] = contrato_instrumento_publico1(cls, el)
    return self
def contrato_instrumento_publico1(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}datos_instrumento_publico')
    if el is not None:
        self['DatosInstrumentoPublico'] = datos_instrumento_publico1(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}contrato')
    if el is not None:
        self['Contrato'] = contrato0(cls, el)
    return self
def datos_instrumento_publico1(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}numero_instrumento_publico')
    self['NumeroInstrumentoPublico'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}fecha_instrumento_publico')
    self['FechaInstrumentoPublico'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}notario_instrumento_publico')
    self['NotarioInstrumentoPublico'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}entidad_instrumento_publico')
    self['EntidadInstrumentoPublico'] = Xint(el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}valor_referencia')
    self['ValorReferencia'] = el.text
    return self
def contrato0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}fecha_contrato')
    self['FechaContrato'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}valor_referencia')
    self['ValorReferencia'] = el.text
    return self
def cesion_derechos_inmuebles0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}figura_cliente')
    self['FiguraCliente'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}tipo_cesion')
    self['TipoCesion'] = el.text
    self['DatosContraparte'] = [datos_contraparte1(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/spr}datos_contraparte')]
    self['CaracteristicasInmueble'] = [caracteristicas_inmueble3(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/spr}caracteristicas_inmueble')]
    return self
def caracteristicas_inmueble3(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}tipo_inmueble')
    self['TipoInmueble'] = catalog_code('C329_tipo_inmueble_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}valor_referencia')
    self['ValorReferencia'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}colonia')
    self['Colonia'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}calle')
    self['Calle'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}numero_exterior')
    self['NumeroExterior'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}numero_interior')
    if el is not None:
        self['NumeroInterior'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}codigo_postal')
    self['CodigoPostal'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}dimension_terreno')
    self['DimensionTerreno'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}dimension_construido')
    self['DimensionConstruido'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}folio_real')
    self['FolioReal'] = el.text
    return self
def administracion_recursos0(cls, node):
    self = ScalarMap()
    self['TipoActivo'] = [tipo_activo0(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/spr}tipo_activo')]
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}numero_operaciones')
    self['NumeroOperaciones'] = Xint(el.text)
    return self
def tipo_activo0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}activo_banco')
    if el is not None:
        self['ActivoBanco'] = activo_banco0(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}activo_inmobiliario')
    if el is not None:
        self['ActivoInmobiliario'] = activo_inmobiliario0(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}activo_outsourcing')
    if el is not None:
        self['ActivoOutsourcing'] = activo_outsourcing0(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}activo_otros')
    if el is not None:
        self['ActivoOtros'] = activo_otros0(cls, el)
    return self
def activo_banco0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}estatus_manejo')
    self['EstatusManejo'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}clave_tipo_institucion')
    self['ClaveTipoInstitucion'] = Xint(el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}nombre_institucion')
    self['NombreInstitucion'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}numero_cuenta')
    self['NumeroCuenta'] = el.text
    return self
def activo_inmobiliario0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}tipo_inmueble')
    self['TipoInmueble'] = catalog_code('C329_tipo_inmueble_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}valor_referencia')
    self['ValorReferencia'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}colonia')
    self['Colonia'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}calle')
    self['Calle'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}numero_exterior')
    self['NumeroExterior'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}numero_interior')
    if el is not None:
        self['NumeroInterior'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}codigo_postal')
    self['CodigoPostal'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}folio_real')
    self['FolioReal'] = el.text
    return self
def activo_outsourcing0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}area_servicio')
    self['AreaServicio'] = area_servicio0(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}activo_administrado')
    self['ActivoAdministrado'] = activo_administrado0(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}numero_empleados')
    self['NumeroEmpleados'] = Xint(el.text)
    return self
def area_servicio0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}tipo_area_servicio')
    self['TipoAreaServicio'] = Xint(el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}descripcion_otro_area_servicio')
    if el is not None:
        self['DescripcionOtroAreaServicio'] = el.text
    return self
def activo_administrado0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}tipo_activo_administrado')
    self['TipoActivoAdministrado'] = Xint(el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}descripcion_otro_activo_administrado')
    if el is not None:
        self['DescripcionOtroActivoAdministrado'] = el.text
    return self
def activo_otros0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}descripcion_activo_administrado')
    self['DescripcionActivoAdministrado'] = el.text
    return self
def constitucion_sociedades_mercantiles0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}tipo_persona_moral')
    self['TipoPersonaMoral'] = Xint(el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}tipo_persona_moral_otra')
    if el is not None:
        self['TipoPersonaMoralOtra'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}denominacion_razon')
    self['DenominacionRazon'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}giro_mercantil')
    self['GiroMercantil'] = catalog_code('C329_giro_mercantil_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}folio_mercantil')
    if el is not None:
        self['FolioMercantil'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}numero_total_acciones')
    self['NumeroTotalAcciones'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}entidad_federativa')
    self['EntidadFederativa'] = Xint(el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}consejo_vigilancia')
    self['ConsejoVigilancia'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}motivo_constitucion')
    self['MotivoConstitucion'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}instrumento_publico')
    if el is not None:
        self['InstrumentoPublico'] = el.text
    self['DatosAccionista'] = [datos_accionista3(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/spr}datos_accionista')]
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}capital_social')
    self['CapitalSocial'] = capital_social2(cls, el)
    return self
def datos_accionista3(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}cargo_accionista')
    self['CargoAccionista'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}tipo_persona')
    self['TipoPersona'] = tipo_persona1b(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}numero_acciones')
    self['NumeroAcciones'] = el.text
    return self
def capital_social2(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}capital_fijo')
    self['CapitalFijo'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}capital_variable')
    if el is not None:
        self['CapitalVariable'] = el.text
    return self
def organizacion_aportaciones0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}motivo_aportacion')
    self['MotivoAportacion'] = el.text
    self['DatosAportacion'] = [datos_aportacion3(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/spr}datos_aportacion')]
    return self
def datos_aportacion3(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}datos_persona_aporta')
    self['DatosPersonaAporta'] = datos_persona_aporta0(cls, el)
    self['DatosTipoAportacion'] = [datos_tipo_aportacion0(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/spr}datos_tipo_aportacion')]
    return self
def datos_persona_aporta0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}persona_fisica')
    if el is not None:
        self['PersonaFisica'] = persona_fisica1e(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}persona_moral')
    if el is not None:
        self['PersonaMoral'] = persona_moral1f(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}fideicomiso')
    if el is not None:
        self['Fideicomiso'] = fideicomiso19(cls, el)
    return self
def persona_fisica1e(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}nombre')
    self['Nombre'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}apellido_paterno')
    self['ApellidoPaterno'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}apellido_materno')
    self['ApellidoMaterno'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}fecha_nacimiento')
    if el is not None:
        self['FechaNacimiento'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}curp')
    if el is not None:
        self['Curp'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}pais_nacionalidad')
    self['PaisNacionalidad'] = catalog_code('C329_pais_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}actividad_economica')
    self['ActividadEconomica'] = catalog_code('C329_actividad_economica_type', el.text)
    return self
def persona_moral1f(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}denominacion_razon')
    self['DenominacionRazon'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}fecha_constitucion')
    if el is not None:
        self['FechaConstitucion'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}pais_nacionalidad')
    self['PaisNacionalidad'] = catalog_code('C329_pais_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}giro_mercantil')
    self['GiroMercantil'] = catalog_code('C329_giro_mercantil_type', el.text)
    return self
def datos_tipo_aportacion0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}aportacion_monetaria')
    if el is not None:
        self['AportacionMonetaria'] = aportacion_monetaria0(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}aportacion_inmueble')
    if el is not None:
        self['AportacionInmueble'] = aportacion_inmueble0(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}aportacion_otro_bien')
    if el is not None:
        self['AportacionOtroBien'] = aportacion_otro_bien0(cls, el)
    return self
def aportacion_monetaria0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}instrumento_monetario')
    self['InstrumentoMonetario'] = catalog_code('C329_instrumento_monetario_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}moneda')
    self['Moneda'] = catalog_code('C329_moneda_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}monto_operacion')
    self['MontoOperacion'] = el.text
    return self
def aportacion_inmueble0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}tipo_inmueble')
    self['TipoInmueble'] = catalog_code('C329_tipo_inmueble_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}codigo_postal')
    self['CodigoPostal'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}folio_real')
    self['FolioReal'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}valor_aportacion')
    self['ValorAportacion'] = el.text
    return self
def aportacion_otro_bien0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}descripcion')
    self['Descripcion'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}valor_aportacion')
    self['ValorAportacion'] = el.text
    return self
def fusion1(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}tipo_fusion')
    self['TipoFusion'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}datos_fusionadas')
    self['DatosFusionadas'] = datos_fusionadas1(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}datos_fusionante')
    self['DatosFusionante'] = datos_fusionante1(cls, el)
    return self
def datos_fusionadas1(cls, node):
    self = ScalarMap()
    self['DatosFusionada'] = [datos_fusionada1(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/spr}datos_fusionada')]
    return self
def datos_fusionada1(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}denominacion_razon')
    self['DenominacionRazon'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}fecha_constitucion')
    if el is not None:
        self['FechaConstitucion'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}pais_nacionalidad')
    self['PaisNacionalidad'] = catalog_code('C329_pais_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}giro_mercantil')
    self['GiroMercantil'] = catalog_code('C329_giro_mercantil_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}capital_social_fijo')
    self['CapitalSocialFijo'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}capital_social_variable')
    if el is not None:
        self['CapitalSocialVariable'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}folio_mercantil')
    if el is not None:
        self['FolioMercantil'] = el.text
    return self
def datos_fusionante1(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}fusionante_determinadas')
    self['FusionanteDeterminadas'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}fusionante')
    if el is not None:
        self['Fusionante'] = fusionante1(cls, el)
    return self
def fusionante1(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}denominacion_razon')
    self['DenominacionRazon'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}fecha_constitucion')
    if el is not None:
        self['FechaConstitucion'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}pais_nacionalidad')
    self['PaisNacionalidad'] = catalog_code('C329_pais_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}giro_mercantil')
    self['GiroMercantil'] = catalog_code('C329_giro_mercantil_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}capital_social_fijo')
    self['CapitalSocialFijo'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}capital_social_variable')
    if el is not None:
        self['CapitalSocialVariable'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}folio_mercantil')
    if el is not None:
        self['FolioMercantil'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}numero_total_acciones')
    self['NumeroTotalAcciones'] = el.text
    self['DatosAccionista'] = [datos_accionista4(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/spr}datos_accionista')]
    return self
def datos_accionista4(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}tipo_persona')
    self['TipoPersona'] = tipo_persona1b(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}numero_acciones')
    self['NumeroAcciones'] = el.text
    return self
def escision1(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}datos_escindente')
    self['DatosEscindente'] = datos_escindente1(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}datos_escindidas')
    self['DatosEscindidas'] = datos_escindidas1(cls, el)
    return self
def datos_escindente1(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}denominacion_razon')
    self['DenominacionRazon'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}fecha_constitucion')
    if el is not None:
        self['FechaConstitucion'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}pais_nacionalidad')
    self['PaisNacionalidad'] = catalog_code('C329_pais_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}giro_mercantil')
    self['GiroMercantil'] = catalog_code('C329_giro_mercantil_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}capital_social_fijo')
    self['CapitalSocialFijo'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}capital_social_variable')
    if el is not None:
        self['CapitalSocialVariable'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}folio_mercantil')
    if el is not None:
        self['FolioMercantil'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}escindente_subsiste')
    self['EscindenteSubsiste'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}datos_accionista_escindente')
    if el is not None:
        self['DatosAccionistaEscindente'] = [datos_accionista_escindente0(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/spr}datos_accionista_escindente')]
    return self
def datos_accionista_escindente0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}tipo_persona')
    self['TipoPersona'] = tipo_persona1b(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}numero_acciones')
    self['NumeroAcciones'] = el.text
    return self
def datos_escindidas1(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}escindidas_determinadas')
    self['EscindidasDeterminadas'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}dato_escindida')
    if el is not None:
        self['DatoEscindida'] = [dato_escindida1(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/spr}dato_escindida')]
    return self
def dato_escindida1(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}denominacion_razon')
    self['DenominacionRazon'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}fecha_constitucion')
    if el is not None:
        self['FechaConstitucion'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}pais_nacionalidad')
    self['PaisNacionalidad'] = catalog_code('C329_pais_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}giro_mercantil')
    self['GiroMercantil'] = catalog_code('C329_giro_mercantil_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}capital_social_fijo')
    self['CapitalSocialFijo'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}capital_social_variable')
    if el is not None:
        self['CapitalSocialVariable'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}folio_mercantil')
    if el is not None:
        self['FolioMercantil'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}numero_total_acciones')
    self['NumeroTotalAcciones'] = el.text
    self['DatosAccionista'] = [datos_accionista4(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/spr}datos_accionista')]
    return self
def administracion_personas_morales0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}tipo_administracion')
    self['TipoAdministracion'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}tipo_operacion')
    self['TipoOperacion'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}persona_moral_aviso')
    self['PersonaMoralAviso'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}tipo_persona')
    if el is not None:
        self['TipoPersona'] = tipo_persona1c(cls, el)
    return self
def tipo_persona1c(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}persona_moral')
    if el is not None:
        self['PersonaMoral'] = persona_moral1d(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}fideicomiso')
    if el is not None:
        self['Fideicomiso'] = fideicomiso19(cls, el)
    return self
def constitucion_fideicomiso0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}identificador_fideicomiso')
    if el is not None:
        self['IdentificadorFideicomiso'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}denominacion_razon')
    self['DenominacionRazon'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}objeto_fideicomiso')
    self['ObjetoFideicomiso'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}monto_total_patrimonio')
    self['MontoTotalPatrimonio'] = el.text
    self['DatosFideicomitente'] = [datos_fideicomitente1(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/spr}datos_fideicomitente')]
    self['DatosFideicomisario'] = [datos_fideicomisario0(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/spr}datos_fideicomisario')]
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}datos_miembro_comite_tecnico')
    self['DatosMiembroComiteTecnico'] = datos_miembro_comite_tecnico1(cls, el)
    return self
def datos_fideicomitente1(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}tipo_persona')
    self['TipoPersona'] = tipo_persona1b(cls, el)
    self['DatosTipoPatrimonio'] = [datos_tipo_patrimonio1(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/spr}datos_tipo_patrimonio')]
    return self
def datos_tipo_patrimonio1(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}patrimonio_monetario')
    if el is not None:
        self['PatrimonioMonetario'] = patrimonio_monetario1(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}patrimonio_inmueble')
    if el is not None:
        self['PatrimonioInmueble'] = patrimonio_inmueble1(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}patrimonio_otro_bien')
    if el is not None:
        self['PatrimonioOtroBien'] = patrimonio_otro_bien1(cls, el)
    return self
def patrimonio_monetario1(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}moneda')
    self['Moneda'] = catalog_code('C329_moneda_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}monto_operacion')
    self['MontoOperacion'] = el.text
    return self
def patrimonio_inmueble1(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}tipo_inmueble')
    self['TipoInmueble'] = catalog_code('C329_tipo_inmueble_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}codigo_postal')
    self['CodigoPostal'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}folio_real')
    self['FolioReal'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}importe_garantia')
    self['ImporteGarantia'] = el.text
    return self
def patrimonio_otro_bien1(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}descripcion')
    self['Descripcion'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}valor_bien')
    self['ValorBien'] = el.text
    return self
def datos_fideicomisario0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}datos_fideicomisarios_determinados')
    self['DatosFideicomisariosDeterminados'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}tipo_persona')
    if el is not None:
        self['TipoPersona'] = tipo_persona1b(cls, el)
    return self
def datos_miembro_comite_tecnico1(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}comite_tecnico')
    self['ComiteTecnico'] = el.text
    return self
def compra_venta_entidades_mercantiles0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}tipo_operacion')
    self['TipoOperacion'] = el.text
    self['DatosSociedadMercantil'] = [datos_sociedad_mercantil0(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/spr}datos_sociedad_mercantil')]
    return self
def datos_sociedad_mercantil0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}denominacion_razon')
    self['DenominacionRazon'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}giro_mercantil')
    self['GiroMercantil'] = catalog_code('C329_giro_mercantil_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}fecha_constitucion')
    if el is not None:
        self['FechaConstitucion'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}pais_nacionalidad')
    self['PaisNacionalidad'] = catalog_code('C329_pais_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}folio_mercantil')
    if el is not None:
        self['FolioMercantil'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}acciones_adquiridas')
    self['AccionesAdquiridas'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}acciones_totales')
    self['AccionesTotales'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}datos_contraparte')
    self['DatosContraparte'] = tipo_persona1b(cls, el)
    return self
def datos_operacion_financiera0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}fecha_pago')
    if el is not None:
        self['FechaPago'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}instrumento_monetario')
    self['InstrumentoMonetario'] = catalog_code('C329_instrumento_monetario_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}activo_virtual')
    if el is not None:
        self['ActivoVirtual'] = activo_virtual1(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}moneda')
    if el is not None:
        self['Moneda'] = catalog_code('C329_moneda_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}monto_operacion')
    self['MontoOperacion'] = el.text
    return self
def activo_virtual1(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}tipo_activo_virtual')
    self['TipoActivoVirtual'] = Xint(el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}descripcion_activo_virtual')
    if el is not None:
        self['DescripcionActivoVirtual'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/spr}cantidad_activo_virtual')
    self['CantidadActivoVirtual'] = el.text
    return self
def archivo_typee(cls, node):
    self = ScalarMap()
    self['Informe'] = [informed(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/tcv}informe')]
    return self
def informed(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tcv}mes_reportado')
    self['MesReportado'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tcv}sujeto_obligado')
    self['SujetoObligado'] = sujeto_obligadod(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tcv}aviso')
    if el is not None:
        self['Aviso'] = [avisoe(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/tcv}aviso')]
    return self
def sujeto_obligadod(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tcv}clave_entidad_colegiada')
    if el is not None:
        self['ClaveEntidadColegiada'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tcv}clave_sujeto_obligado')
    self['ClaveSujetoObligado'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tcv}clave_actividad')
    self['ClaveActividad'] = catalog_code('C329_clave_actividad_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tcv}exento')
    if el is not None:
        self['Exento'] = el.text
    return self
def avisoe(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tcv}referencia_aviso')
    self['ReferenciaAviso'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tcv}modificatorio')
    if el is not None:
        self['Modificatorio'] = modificatoriod(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tcv}prioridad')
    self['Prioridad'] = catalog_code('C329_prioridad_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tcv}alerta')
    self['Alerta'] = alertae(cls, el)
    self['PersonaAviso'] = [persona_avisoc(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/tcv}persona_aviso')]
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tcv}dueno_beneficiario')
    if el is not None:
        self['DuenoBeneficiario'] = [dueno_beneficiariob(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/tcv}dueno_beneficiario')]
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tcv}detalle_operaciones')
    self['DetalleOperaciones'] = detalle_operacionesc(cls, el)
    return self
def modificatoriod(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tcv}folio_modificacion')
    self['FolioModificacion'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tcv}descripcion_modificacion')
    self['DescripcionModificacion'] = el.text
    return self
def alertae(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tcv}tipo_alerta')
    self['TipoAlerta'] = catalog_code('C329_tipo_alerta_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tcv}descripcion_alerta')
    if el is not None:
        self['DescripcionAlerta'] = el.text
    return self
def persona_avisoc(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tcv}tipo_persona')
    self['TipoPersona'] = tipo_persona1d(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tcv}tipo_domicilio')
    if el is not None:
        self['TipoDomicilio'] = tipo_domicilioc(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tcv}telefono')
    if el is not None:
        self['Telefono'] = telefonod(cls, el)
    return self
def tipo_persona1d(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tcv}persona_fisica')
    if el is not None:
        self['PersonaFisica'] = persona_fisica1f(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tcv}persona_moral')
    if el is not None:
        self['PersonaMoral'] = persona_moral20(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tcv}fideicomiso')
    if el is not None:
        self['Fideicomiso'] = fideicomiso1a(cls, el)
    return self
def persona_fisica1f(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tcv}nombre')
    self['Nombre'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tcv}apellido_paterno')
    self['ApellidoPaterno'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tcv}apellido_materno')
    self['ApellidoMaterno'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tcv}fecha_nacimiento')
    if el is not None:
        self['FechaNacimiento'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tcv}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tcv}curp')
    if el is not None:
        self['Curp'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tcv}pais_nacionalidad')
    self['PaisNacionalidad'] = catalog_code('C329_pais_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tcv}actividad_economica')
    self['ActividadEconomica'] = catalog_code('C329_actividad_economica_type', el.text)
    return self
def persona_moral20(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tcv}denominacion_razon')
    self['DenominacionRazon'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tcv}fecha_constitucion')
    if el is not None:
        self['FechaConstitucion'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tcv}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tcv}pais_nacionalidad')
    self['PaisNacionalidad'] = catalog_code('C329_pais_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tcv}giro_mercantil')
    self['GiroMercantil'] = catalog_code('C329_giro_mercantil_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tcv}representante_apoderado')
    self['RepresentanteApoderado'] = representante_apoderadoc(cls, el)
    return self
def fideicomiso1a(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tcv}denominacion_razon')
    self['DenominacionRazon'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tcv}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tcv}identificador_fideicomiso')
    if el is not None:
        self['IdentificadorFideicomiso'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tcv}apoderado_delegado')
    self['ApoderadoDelegado'] = representante_apoderadoc(cls, el)
    return self
def representante_apoderadoc(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tcv}nombre')
    self['Nombre'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tcv}apellido_paterno')
    self['ApellidoPaterno'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tcv}apellido_materno')
    self['ApellidoMaterno'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tcv}fecha_nacimiento')
    if el is not None:
        self['FechaNacimiento'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tcv}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tcv}curp')
    if el is not None:
        self['Curp'] = el.text
    return self
def tipo_domicilioc(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tcv}nacional')
    if el is not None:
        self['Nacional'] = nacionale(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tcv}extranjero')
    if el is not None:
        self['Extranjero'] = extranjeroe(cls, el)
    return self
def nacionale(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tcv}colonia')
    self['Colonia'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tcv}calle')
    self['Calle'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tcv}numero_exterior')
    self['NumeroExterior'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tcv}numero_interior')
    if el is not None:
        self['NumeroInterior'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tcv}codigo_postal')
    self['CodigoPostal'] = el.text
    return self
def extranjeroe(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tcv}pais')
    self['Pais'] = catalog_code('C329_pais_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tcv}estado_provincia')
    self['EstadoProvincia'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tcv}ciudad_poblacion')
    self['CiudadPoblacion'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tcv}colonia')
    self['Colonia'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tcv}calle')
    self['Calle'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tcv}numero_exterior')
    self['NumeroExterior'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tcv}numero_interior')
    if el is not None:
        self['NumeroInterior'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tcv}codigo_postal')
    self['CodigoPostal'] = el.text
    return self
def telefonod(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tcv}clave_pais')
    if el is not None:
        self['ClavePais'] = catalog_code('C329_pais_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tcv}numero_telefono')
    if el is not None:
        self['NumeroTelefono'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tcv}correo_electronico')
    if el is not None:
        self['CorreoElectronico'] = el.text
    return self
def dueno_beneficiariob(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tcv}tipo_persona')
    self['TipoPersona'] = tipo_persona1e(cls, el)
    return self
def tipo_persona1e(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tcv}persona_fisica')
    if el is not None:
        self['PersonaFisica'] = persona_fisica20(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tcv}persona_moral')
    if el is not None:
        self['PersonaMoral'] = persona_moral21(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tcv}fideicomiso')
    if el is not None:
        self['Fideicomiso'] = fideicomiso1b(cls, el)
    return self
def persona_fisica20(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tcv}nombre')
    self['Nombre'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tcv}apellido_paterno')
    self['ApellidoPaterno'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tcv}apellido_materno')
    self['ApellidoMaterno'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tcv}fecha_nacimiento')
    if el is not None:
        self['FechaNacimiento'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tcv}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tcv}curp')
    if el is not None:
        self['Curp'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tcv}pais_nacionalidad')
    if el is not None:
        self['PaisNacionalidad'] = catalog_code('C329_pais_type', el.text)
    return self
def persona_moral21(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tcv}denominacion_razon')
    self['DenominacionRazon'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tcv}fecha_constitucion')
    if el is not None:
        self['FechaConstitucion'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tcv}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tcv}pais_nacionalidad')
    if el is not None:
        self['PaisNacionalidad'] = catalog_code('C329_pais_type', el.text)
    return self
def fideicomiso1b(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tcv}denominacion_razon')
    self['DenominacionRazon'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tcv}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tcv}identificador_fideicomiso')
    if el is not None:
        self['IdentificadorFideicomiso'] = el.text
    return self
def detalle_operacionesc(cls, node):
    self = ScalarMap()
    self['DatosOperacion'] = [datos_operaciond(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/tcv}datos_operacion')]
    return self
def datos_operaciond(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tcv}fecha_operacion')
    self['FechaOperacion'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tcv}tipo_operacion')
    self['TipoOperacion'] = catalog_code('C329_tipo_operacion_type', el.text)
    self['TipoBien'] = [tipo_bien1(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/tcv}tipo_bien')]
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tcv}recepcion')
    if el is not None:
        self['Recepcion'] = recepcion1(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tcv}custodia')
    if el is not None:
        self['Custodia'] = custodia0(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tcv}entrega')
    if el is not None:
        self['Entrega'] = entrega0(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tcv}destinatario')
    if el is not None:
        self['Destinatario'] = destinatario0(cls, el)
    return self
def tipo_bien1(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tcv}datos_efectivo_instrumentos')
    if el is not None:
        self['DatosEfectivoInstrumentos'] = datos_efectivo_instrumentos0(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tcv}datos_valores')
    if el is not None:
        self['DatosValores'] = datos_valores0(cls, el)
    return self
def datos_efectivo_instrumentos0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tcv}instrumento_monetario')
    self['InstrumentoMonetario'] = catalog_code('C329_instrumento_monetario_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tcv}moneda')
    self['Moneda'] = catalog_code('C329_moneda_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tcv}monto_operacion')
    self['MontoOperacion'] = el.text
    return self
def datos_valores0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tcv}tipo_valor')
    self['TipoValor'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tcv}valor_objeto')
    self['ValorObjeto'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tcv}descripcion')
    self['Descripcion'] = el.text
    return self
def recepcion1(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tcv}tipo_servicio')
    self['TipoServicio'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tcv}fecha_recepcion')
    self['FechaRecepcion'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tcv}codigo_postal')
    self['CodigoPostal'] = el.text
    return self
def custodia0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tcv}fecha_inicio')
    self['FechaInicio'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tcv}fecha_fin')
    self['FechaFin'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tcv}tipo_custodia')
    self['TipoCustodia'] = tipo_custodia0(cls, el)
    return self
def tipo_custodia0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tcv}datos_sucursal')
    if el is not None:
        self['DatosSucursal'] = datos_sucursal0(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tcv}datos_no_sucursal')
    if el is not None:
        self['DatosNoSucursal'] = datos_no_sucursal0(cls, el)
    return self
def datos_sucursal0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tcv}codigo_postal')
    self['CodigoPostal'] = el.text
    return self
def datos_no_sucursal0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tcv}colonia')
    self['Colonia'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tcv}calle')
    self['Calle'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tcv}numero_exterior')
    self['NumeroExterior'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tcv}numero_interior')
    if el is not None:
        self['NumeroInterior'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tcv}codigo_postal')
    self['CodigoPostal'] = el.text
    return self
def entrega0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tcv}fecha_entrega')
    self['FechaEntrega'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tcv}tipo_entrega')
    self['TipoEntrega'] = tipo_entrega0(cls, el)
    return self
def tipo_entrega0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tcv}nacional')
    if el is not None:
        self['Nacional'] = nacionalf(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tcv}extranjero')
    if el is not None:
        self['Extranjero'] = extranjerof(cls, el)
    return self
def nacionalf(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tcv}codigo_postal')
    self['CodigoPostal'] = el.text
    return self
def extranjerof(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tcv}pais')
    self['Pais'] = catalog_code('C329_pais_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tcv}estado_provincia')
    self['EstadoProvincia'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tcv}ciudad_poblacion')
    self['CiudadPoblacion'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tcv}codigo_postal')
    self['CodigoPostal'] = el.text
    return self
def destinatario0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tcv}destinatario_persona_aviso')
    self['DestinatarioPersonaAviso'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tcv}tipo_persona')
    if el is not None:
        self['TipoPersona'] = tipo_persona1f(cls, el)
    return self
def tipo_persona1f(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tcv}persona_fisica')
    if el is not None:
        self['PersonaFisica'] = persona_fisica21(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tcv}persona_moral')
    if el is not None:
        self['PersonaMoral'] = persona_moral22(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tcv}fideicomiso')
    if el is not None:
        self['Fideicomiso'] = fideicomiso1c(cls, el)
    return self
def persona_fisica21(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tcv}nombre')
    self['Nombre'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tcv}apellido_paterno')
    self['ApellidoPaterno'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tcv}apellido_materno')
    self['ApellidoMaterno'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tcv}fecha_nacimiento')
    if el is not None:
        self['FechaNacimiento'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tcv}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tcv}curp')
    if el is not None:
        self['Curp'] = el.text
    return self
def persona_moral22(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tcv}denominacion_razon')
    self['DenominacionRazon'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tcv}fecha_constitucion')
    if el is not None:
        self['FechaConstitucion'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tcv}rfc')
    if el is not None:
        self['Rfc'] = el.text
    return self
def fideicomiso1c(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tcv}denominacion_razon')
    self['DenominacionRazon'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tcv}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tcv}identificador_fideicomiso')
    if el is not None:
        self['IdentificadorFideicomiso'] = el.text
    return self
def archivo_typef(cls, node):
    self = ScalarMap()
    self['Informe'] = [informee(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/tdr}informe')]
    return self
def informee(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tdr}mes_reportado')
    self['MesReportado'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tdr}sujeto_obligado')
    self['SujetoObligado'] = sujeto_obligadoe(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tdr}aviso')
    if el is not None:
        self['Aviso'] = [avisof(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/tdr}aviso')]
    return self
def sujeto_obligadoe(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tdr}clave_entidad_colegiada')
    if el is not None:
        self['ClaveEntidadColegiada'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tdr}clave_sujeto_obligado')
    self['ClaveSujetoObligado'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tdr}clave_actividad')
    self['ClaveActividad'] = catalog_code('C329_clave_actividad_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tdr}exento')
    if el is not None:
        self['Exento'] = el.text
    return self
def avisof(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tdr}referencia_aviso')
    self['ReferenciaAviso'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tdr}modificatorio')
    if el is not None:
        self['Modificatorio'] = modificatorioe(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tdr}prioridad')
    self['Prioridad'] = catalog_code('C329_prioridad_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tdr}alerta')
    self['Alerta'] = alertaf(cls, el)
    self['PersonaAviso'] = [persona_avisod(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/tdr}persona_aviso')]
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tdr}dueno_beneficiario')
    if el is not None:
        self['DuenoBeneficiario'] = [dueno_beneficiarioc(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/tdr}dueno_beneficiario')]
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tdr}detalle_operaciones')
    self['DetalleOperaciones'] = detalle_operacionesd(cls, el)
    return self
def modificatorioe(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tdr}folio_modificacion')
    self['FolioModificacion'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tdr}descripcion_modificacion')
    self['DescripcionModificacion'] = el.text
    return self
def alertaf(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tdr}tipo_alerta')
    self['TipoAlerta'] = catalog_code('C329_tipo_alerta_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tdr}descripcion_alerta')
    if el is not None:
        self['DescripcionAlerta'] = el.text
    return self
def persona_avisod(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tdr}tipo_persona')
    self['TipoPersona'] = tipo_persona20(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tdr}tipo_domicilio')
    if el is not None:
        self['TipoDomicilio'] = tipo_domiciliod(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tdr}telefono')
    if el is not None:
        self['Telefono'] = telefonoe(cls, el)
    return self
def tipo_persona20(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tdr}persona_fisica')
    if el is not None:
        self['PersonaFisica'] = persona_fisica22(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tdr}persona_moral')
    if el is not None:
        self['PersonaMoral'] = persona_moral23(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tdr}fideicomiso')
    if el is not None:
        self['Fideicomiso'] = fideicomiso1d(cls, el)
    return self
def persona_fisica22(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tdr}nombre')
    self['Nombre'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tdr}apellido_paterno')
    self['ApellidoPaterno'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tdr}apellido_materno')
    self['ApellidoMaterno'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tdr}fecha_nacimiento')
    if el is not None:
        self['FechaNacimiento'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tdr}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tdr}curp')
    if el is not None:
        self['Curp'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tdr}pais_nacionalidad')
    self['PaisNacionalidad'] = catalog_code('C329_pais_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tdr}actividad_economica')
    self['ActividadEconomica'] = catalog_code('C329_actividad_economica_type', el.text)
    return self
def persona_moral23(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tdr}denominacion_razon')
    self['DenominacionRazon'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tdr}fecha_constitucion')
    if el is not None:
        self['FechaConstitucion'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tdr}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tdr}pais_nacionalidad')
    self['PaisNacionalidad'] = catalog_code('C329_pais_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tdr}giro_mercantil')
    self['GiroMercantil'] = catalog_code('C329_giro_mercantil_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tdr}representante_apoderado')
    self['RepresentanteApoderado'] = representante_apoderadod(cls, el)
    return self
def fideicomiso1d(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tdr}denominacion_razon')
    self['DenominacionRazon'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tdr}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tdr}identificador_fideicomiso')
    if el is not None:
        self['IdentificadorFideicomiso'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tdr}apoderado_delegado')
    self['ApoderadoDelegado'] = representante_apoderadod(cls, el)
    return self
def representante_apoderadod(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tdr}nombre')
    self['Nombre'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tdr}apellido_paterno')
    self['ApellidoPaterno'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tdr}apellido_materno')
    self['ApellidoMaterno'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tdr}fecha_nacimiento')
    if el is not None:
        self['FechaNacimiento'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tdr}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tdr}curp')
    if el is not None:
        self['Curp'] = el.text
    return self
def tipo_domiciliod(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tdr}nacional')
    if el is not None:
        self['Nacional'] = nacional10(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tdr}extranjero')
    if el is not None:
        self['Extranjero'] = extranjero10(cls, el)
    return self
def nacional10(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tdr}colonia')
    self['Colonia'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tdr}calle')
    self['Calle'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tdr}numero_exterior')
    self['NumeroExterior'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tdr}numero_interior')
    if el is not None:
        self['NumeroInterior'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tdr}codigo_postal')
    self['CodigoPostal'] = el.text
    return self
def extranjero10(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tdr}pais')
    self['Pais'] = catalog_code('C329_pais_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tdr}estado_provincia')
    self['EstadoProvincia'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tdr}ciudad_poblacion')
    self['CiudadPoblacion'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tdr}colonia')
    self['Colonia'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tdr}calle')
    self['Calle'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tdr}numero_exterior')
    self['NumeroExterior'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tdr}numero_interior')
    if el is not None:
        self['NumeroInterior'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tdr}codigo_postal')
    self['CodigoPostal'] = el.text
    return self
def telefonoe(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tdr}clave_pais')
    if el is not None:
        self['ClavePais'] = catalog_code('C329_pais_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tdr}numero_telefono')
    if el is not None:
        self['NumeroTelefono'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tdr}correo_electronico')
    if el is not None:
        self['CorreoElectronico'] = el.text
    return self
def dueno_beneficiarioc(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tdr}tipo_persona')
    self['TipoPersona'] = tipo_persona21(cls, el)
    return self
def tipo_persona21(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tdr}persona_fisica')
    if el is not None:
        self['PersonaFisica'] = persona_fisica23(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tdr}persona_moral')
    if el is not None:
        self['PersonaMoral'] = persona_moral24(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tdr}fideicomiso')
    if el is not None:
        self['Fideicomiso'] = fideicomiso1e(cls, el)
    return self
def persona_fisica23(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tdr}nombre')
    self['Nombre'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tdr}apellido_paterno')
    self['ApellidoPaterno'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tdr}apellido_materno')
    self['ApellidoMaterno'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tdr}fecha_nacimiento')
    if el is not None:
        self['FechaNacimiento'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tdr}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tdr}curp')
    if el is not None:
        self['Curp'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tdr}pais_nacionalidad')
    if el is not None:
        self['PaisNacionalidad'] = catalog_code('C329_pais_type', el.text)
    return self
def persona_moral24(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tdr}denominacion_razon')
    self['DenominacionRazon'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tdr}fecha_constitucion')
    if el is not None:
        self['FechaConstitucion'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tdr}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tdr}pais_nacionalidad')
    if el is not None:
        self['PaisNacionalidad'] = catalog_code('C329_pais_type', el.text)
    return self
def fideicomiso1e(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tdr}denominacion_razon')
    self['DenominacionRazon'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tdr}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tdr}identificador_fideicomiso')
    if el is not None:
        self['IdentificadorFideicomiso'] = el.text
    return self
def detalle_operacionesd(cls, node):
    self = ScalarMap()
    self['DatosOperacion'] = [datos_operacione(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/tdr}datos_operacion')]
    return self
def datos_operacione(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tdr}fecha_operacion')
    self['FechaOperacion'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tdr}codigo_postal')
    self['CodigoPostal'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tdr}tipo_operacion')
    self['TipoOperacion'] = catalog_code('C329_tipo_operacion_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tdr}cantidad')
    self['Cantidad'] = el.text
    self['DatosLiquidacion'] = [datos_liquidaciona(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/tdr}datos_liquidacion')]
    return self
def datos_liquidaciona(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tdr}moneda')
    self['Moneda'] = catalog_code('C329_moneda_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tdr}monto_operacion')
    self['MontoOperacion'] = el.text
    return self
def archivo_type10(cls, node):
    self = ScalarMap()
    self['Informe'] = [informef(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/tpp}informe')]
    return self
def informef(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tpp}mes_reportado')
    self['MesReportado'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tpp}sujeto_obligado')
    self['SujetoObligado'] = sujeto_obligadof(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tpp}aviso')
    if el is not None:
        self['Aviso'] = [aviso10(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/tpp}aviso')]
    return self
def sujeto_obligadof(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tpp}clave_entidad_colegiada')
    if el is not None:
        self['ClaveEntidadColegiada'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tpp}clave_sujeto_obligado')
    self['ClaveSujetoObligado'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tpp}clave_actividad')
    self['ClaveActividad'] = catalog_code('C329_clave_actividad_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tpp}exento')
    if el is not None:
        self['Exento'] = el.text
    return self
def aviso10(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tpp}referencia_aviso')
    self['ReferenciaAviso'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tpp}modificatorio')
    if el is not None:
        self['Modificatorio'] = modificatoriof(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tpp}prioridad')
    self['Prioridad'] = catalog_code('C329_prioridad_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tpp}alerta')
    self['Alerta'] = alerta10(cls, el)
    self['PersonaAviso'] = [persona_avisoe(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/tpp}persona_aviso')]
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tpp}dueno_beneficiario')
    if el is not None:
        self['DuenoBeneficiario'] = [dueno_beneficiariod(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/tpp}dueno_beneficiario')]
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tpp}detalle_operaciones')
    self['DetalleOperaciones'] = detalle_operacionese(cls, el)
    return self
def modificatoriof(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tpp}folio_modificacion')
    self['FolioModificacion'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tpp}descripcion_modificacion')
    self['DescripcionModificacion'] = el.text
    return self
def alerta10(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tpp}tipo_alerta')
    self['TipoAlerta'] = catalog_code('C329_tipo_alerta_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tpp}descripcion_alerta')
    if el is not None:
        self['DescripcionAlerta'] = el.text
    return self
def persona_avisoe(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tpp}tipo_persona')
    self['TipoPersona'] = tipo_persona22(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tpp}tipo_domicilio')
    if el is not None:
        self['TipoDomicilio'] = tipo_domicilioe(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tpp}telefono')
    if el is not None:
        self['Telefono'] = telefonof(cls, el)
    return self
def tipo_persona22(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tpp}persona_fisica')
    if el is not None:
        self['PersonaFisica'] = persona_fisica24(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tpp}persona_moral')
    if el is not None:
        self['PersonaMoral'] = persona_moral25(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tpp}fideicomiso')
    if el is not None:
        self['Fideicomiso'] = fideicomiso1f(cls, el)
    return self
def persona_fisica24(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tpp}nombre')
    self['Nombre'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tpp}apellido_paterno')
    self['ApellidoPaterno'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tpp}apellido_materno')
    self['ApellidoMaterno'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tpp}fecha_nacimiento')
    if el is not None:
        self['FechaNacimiento'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tpp}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tpp}curp')
    if el is not None:
        self['Curp'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tpp}pais_nacionalidad')
    self['PaisNacionalidad'] = catalog_code('C329_pais_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tpp}actividad_economica')
    self['ActividadEconomica'] = catalog_code('C329_actividad_economica_type', el.text)
    return self
def persona_moral25(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tpp}denominacion_razon')
    self['DenominacionRazon'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tpp}fecha_constitucion')
    if el is not None:
        self['FechaConstitucion'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tpp}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tpp}pais_nacionalidad')
    self['PaisNacionalidad'] = catalog_code('C329_pais_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tpp}giro_mercantil')
    self['GiroMercantil'] = catalog_code('C329_giro_mercantil_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tpp}representante_apoderado')
    self['RepresentanteApoderado'] = representante_apoderadoe(cls, el)
    return self
def fideicomiso1f(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tpp}denominacion_razon')
    self['DenominacionRazon'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tpp}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tpp}identificador_fideicomiso')
    if el is not None:
        self['IdentificadorFideicomiso'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tpp}apoderado_delegado')
    self['ApoderadoDelegado'] = representante_apoderadoe(cls, el)
    return self
def representante_apoderadoe(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tpp}nombre')
    self['Nombre'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tpp}apellido_paterno')
    self['ApellidoPaterno'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tpp}apellido_materno')
    self['ApellidoMaterno'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tpp}fecha_nacimiento')
    if el is not None:
        self['FechaNacimiento'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tpp}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tpp}curp')
    if el is not None:
        self['Curp'] = el.text
    return self
def tipo_domicilioe(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tpp}nacional')
    if el is not None:
        self['Nacional'] = nacional11(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tpp}extranjero')
    if el is not None:
        self['Extranjero'] = extranjero11(cls, el)
    return self
def nacional11(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tpp}colonia')
    self['Colonia'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tpp}calle')
    self['Calle'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tpp}numero_exterior')
    self['NumeroExterior'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tpp}numero_interior')
    if el is not None:
        self['NumeroInterior'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tpp}codigo_postal')
    self['CodigoPostal'] = el.text
    return self
def extranjero11(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tpp}pais')
    self['Pais'] = catalog_code('C329_pais_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tpp}estado_provincia')
    self['EstadoProvincia'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tpp}ciudad_poblacion')
    self['CiudadPoblacion'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tpp}colonia')
    self['Colonia'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tpp}calle')
    self['Calle'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tpp}numero_exterior')
    self['NumeroExterior'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tpp}numero_interior')
    if el is not None:
        self['NumeroInterior'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tpp}codigo_postal')
    self['CodigoPostal'] = el.text
    return self
def telefonof(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tpp}clave_pais')
    if el is not None:
        self['ClavePais'] = catalog_code('C329_pais_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tpp}numero_telefono')
    if el is not None:
        self['NumeroTelefono'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tpp}correo_electronico')
    if el is not None:
        self['CorreoElectronico'] = el.text
    return self
def dueno_beneficiariod(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tpp}tipo_persona')
    self['TipoPersona'] = tipo_persona23(cls, el)
    return self
def tipo_persona23(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tpp}persona_fisica')
    if el is not None:
        self['PersonaFisica'] = persona_fisica25(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tpp}persona_moral')
    if el is not None:
        self['PersonaMoral'] = persona_moral26(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tpp}fideicomiso')
    if el is not None:
        self['Fideicomiso'] = fideicomiso20(cls, el)
    return self
def persona_fisica25(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tpp}nombre')
    self['Nombre'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tpp}apellido_paterno')
    self['ApellidoPaterno'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tpp}apellido_materno')
    self['ApellidoMaterno'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tpp}fecha_nacimiento')
    if el is not None:
        self['FechaNacimiento'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tpp}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tpp}curp')
    if el is not None:
        self['Curp'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tpp}pais_nacionalidad')
    if el is not None:
        self['PaisNacionalidad'] = catalog_code('C329_pais_type', el.text)
    return self
def persona_moral26(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tpp}denominacion_razon')
    self['DenominacionRazon'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tpp}fecha_constitucion')
    if el is not None:
        self['FechaConstitucion'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tpp}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tpp}pais_nacionalidad')
    if el is not None:
        self['PaisNacionalidad'] = catalog_code('C329_pais_type', el.text)
    return self
def fideicomiso20(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tpp}denominacion_razon')
    self['DenominacionRazon'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tpp}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tpp}identificador_fideicomiso')
    if el is not None:
        self['IdentificadorFideicomiso'] = el.text
    return self
def detalle_operacionese(cls, node):
    self = ScalarMap()
    self['DatosOperacion'] = [datos_operacionf(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/tpp}datos_operacion')]
    return self
def datos_operacionf(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tpp}fecha_operacion')
    self['FechaOperacion'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tpp}codigo_postal')
    self['CodigoPostal'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tpp}tipo_operacion')
    self['TipoOperacion'] = catalog_code('C329_tipo_operacion_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tpp}cantidad')
    self['Cantidad'] = el.text
    self['DatosLiquidacion'] = [datos_liquidacionb(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/tpp}datos_liquidacion')]
    return self
def datos_liquidacionb(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tpp}fecha_pago')
    self['FechaPago'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tpp}instrumento_monetario')
    self['InstrumentoMonetario'] = catalog_code('C329_instrumento_monetario_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tpp}moneda')
    self['Moneda'] = catalog_code('C329_moneda_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tpp}monto_operacion')
    self['MontoOperacion'] = el.text
    return self
def detalle_operaciones_type1(cls, node):
    self = ScalarMap()
    self['DatosOperacion'] = [datos_operacion10(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/tsc}datos_operacion')]
    return self
def datos_operacion10(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tsc}fecha_periodo')
    self['FechaPeriodo'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tsc}tipo_operacion')
    self['TipoOperacion'] = catalog_code('C329_tipo_operacion_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tsc}tipo_tarjeta')
    self['TipoTarjeta'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tsc}numero_identificador')
    self['NumeroIdentificador'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tsc}monto_gasto')
    self['MontoGasto'] = el.text
    return self
def archivo_type11(cls, node):
    self = ScalarMap()
    self['Informe'] = [informe10(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/tsc}informe')]
    return self
def informe10(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tsc}mes_reportado')
    self['MesReportado'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tsc}sujeto_obligado')
    self['SujetoObligado'] = sujeto_obligado10(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tsc}aviso')
    if el is not None:
        self['Aviso'] = [aviso11(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/tsc}aviso')]
    return self
def sujeto_obligado10(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tsc}clave_entidad_colegiada')
    if el is not None:
        self['ClaveEntidadColegiada'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tsc}clave_sujeto_obligado')
    self['ClaveSujetoObligado'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tsc}clave_actividad')
    self['ClaveActividad'] = catalog_code('C329_clave_actividad_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tsc}exento')
    if el is not None:
        self['Exento'] = el.text
    return self
def aviso11(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tsc}referencia_aviso')
    self['ReferenciaAviso'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tsc}modificatorio')
    if el is not None:
        self['Modificatorio'] = modificatorio10(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tsc}prioridad')
    self['Prioridad'] = catalog_code('C329_prioridad_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tsc}alerta')
    self['Alerta'] = alerta11(cls, el)
    self['PersonaAviso'] = [persona_avisof(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/tsc}persona_aviso')]
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tsc}dueno_beneficiario')
    if el is not None:
        self['DuenoBeneficiario'] = [dueno_beneficiarioe(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/tsc}dueno_beneficiario')]
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tsc}detalle_operaciones')
    self['DetalleOperaciones'] = detalle_operaciones_type1(cls, el)
    return self
def modificatorio10(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tsc}folio_modificacion')
    self['FolioModificacion'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tsc}descripcion_modificacion')
    self['DescripcionModificacion'] = el.text
    return self
def alerta11(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tsc}tipo_alerta')
    self['TipoAlerta'] = catalog_code('C329_tipo_alerta_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tsc}descripcion_alerta')
    if el is not None:
        self['DescripcionAlerta'] = el.text
    return self
def persona_avisof(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tsc}tipo_persona')
    self['TipoPersona'] = tipo_persona24(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tsc}tipo_domicilio')
    if el is not None:
        self['TipoDomicilio'] = tipo_domiciliof(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tsc}telefono')
    if el is not None:
        self['Telefono'] = telefono10(cls, el)
    return self
def tipo_persona24(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tsc}persona_fisica')
    if el is not None:
        self['PersonaFisica'] = persona_fisica26(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tsc}persona_moral')
    if el is not None:
        self['PersonaMoral'] = persona_moral27(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tsc}fideicomiso')
    if el is not None:
        self['Fideicomiso'] = fideicomiso21(cls, el)
    return self
def persona_fisica26(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tsc}nombre')
    self['Nombre'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tsc}apellido_paterno')
    self['ApellidoPaterno'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tsc}apellido_materno')
    self['ApellidoMaterno'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tsc}fecha_nacimiento')
    if el is not None:
        self['FechaNacimiento'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tsc}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tsc}curp')
    if el is not None:
        self['Curp'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tsc}pais_nacionalidad')
    self['PaisNacionalidad'] = catalog_code('C329_pais_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tsc}actividad_economica')
    self['ActividadEconomica'] = catalog_code('C329_actividad_economica_type', el.text)
    return self
def persona_moral27(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tsc}denominacion_razon')
    self['DenominacionRazon'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tsc}fecha_constitucion')
    if el is not None:
        self['FechaConstitucion'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tsc}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tsc}pais_nacionalidad')
    self['PaisNacionalidad'] = catalog_code('C329_pais_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tsc}giro_mercantil')
    self['GiroMercantil'] = catalog_code('C329_giro_mercantil_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tsc}representante_apoderado')
    self['RepresentanteApoderado'] = representante_apoderadof(cls, el)
    return self
def fideicomiso21(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tsc}denominacion_razon')
    self['DenominacionRazon'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tsc}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tsc}identificador_fideicomiso')
    if el is not None:
        self['IdentificadorFideicomiso'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tsc}apoderado_delegado')
    self['ApoderadoDelegado'] = representante_apoderadof(cls, el)
    return self
def representante_apoderadof(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tsc}nombre')
    self['Nombre'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tsc}apellido_paterno')
    self['ApellidoPaterno'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tsc}apellido_materno')
    self['ApellidoMaterno'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tsc}fecha_nacimiento')
    if el is not None:
        self['FechaNacimiento'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tsc}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tsc}curp')
    if el is not None:
        self['Curp'] = el.text
    return self
def tipo_domiciliof(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tsc}nacional')
    if el is not None:
        self['Nacional'] = nacional12(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tsc}extranjero')
    if el is not None:
        self['Extranjero'] = extranjero12(cls, el)
    return self
def nacional12(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tsc}colonia')
    self['Colonia'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tsc}calle')
    self['Calle'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tsc}numero_exterior')
    self['NumeroExterior'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tsc}numero_interior')
    if el is not None:
        self['NumeroInterior'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tsc}codigo_postal')
    self['CodigoPostal'] = el.text
    return self
def extranjero12(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tsc}pais')
    self['Pais'] = catalog_code('C329_pais_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tsc}estado_provincia')
    self['EstadoProvincia'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tsc}ciudad_poblacion')
    self['CiudadPoblacion'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tsc}colonia')
    self['Colonia'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tsc}calle')
    self['Calle'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tsc}numero_exterior')
    self['NumeroExterior'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tsc}numero_interior')
    if el is not None:
        self['NumeroInterior'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tsc}codigo_postal')
    self['CodigoPostal'] = el.text
    return self
def telefono10(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tsc}clave_pais')
    if el is not None:
        self['ClavePais'] = catalog_code('C329_pais_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tsc}numero_telefono')
    if el is not None:
        self['NumeroTelefono'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tsc}correo_electronico')
    if el is not None:
        self['CorreoElectronico'] = el.text
    return self
def dueno_beneficiarioe(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tsc}tipo_persona')
    self['TipoPersona'] = tipo_persona25(cls, el)
    return self
def tipo_persona25(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tsc}persona_fisica')
    if el is not None:
        self['PersonaFisica'] = persona_fisica27(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tsc}persona_moral')
    if el is not None:
        self['PersonaMoral'] = persona_moral28(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tsc}fideicomiso')
    if el is not None:
        self['Fideicomiso'] = fideicomiso22(cls, el)
    return self
def persona_fisica27(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tsc}nombre')
    self['Nombre'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tsc}apellido_paterno')
    self['ApellidoPaterno'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tsc}apellido_materno')
    self['ApellidoMaterno'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tsc}fecha_nacimiento')
    if el is not None:
        self['FechaNacimiento'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tsc}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tsc}curp')
    if el is not None:
        self['Curp'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tsc}pais_nacionalidad')
    if el is not None:
        self['PaisNacionalidad'] = catalog_code('C329_pais_type', el.text)
    return self
def persona_moral28(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tsc}denominacion_razon')
    self['DenominacionRazon'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tsc}fecha_constitucion')
    if el is not None:
        self['FechaConstitucion'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tsc}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tsc}pais_nacionalidad')
    if el is not None:
        self['PaisNacionalidad'] = catalog_code('C329_pais_type', el.text)
    return self
def fideicomiso22(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tsc}denominacion_razon')
    self['DenominacionRazon'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tsc}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/tsc}identificador_fideicomiso')
    if el is not None:
        self['IdentificadorFideicomiso'] = el.text
    return self
def archivo_type12(cls, node):
    self = ScalarMap()
    self['Informe'] = [informe11(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/veh}informe')]
    return self
def informe11(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/veh}mes_reportado')
    self['MesReportado'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/veh}sujeto_obligado')
    self['SujetoObligado'] = sujeto_obligado11(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/veh}aviso')
    if el is not None:
        self['Aviso'] = [aviso12(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/veh}aviso')]
    return self
def sujeto_obligado11(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/veh}clave_entidad_colegiada')
    if el is not None:
        self['ClaveEntidadColegiada'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/veh}clave_sujeto_obligado')
    self['ClaveSujetoObligado'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/veh}clave_actividad')
    self['ClaveActividad'] = catalog_code('C329_clave_actividad_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/veh}exento')
    if el is not None:
        self['Exento'] = el.text
    return self
def aviso12(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/veh}referencia_aviso')
    self['ReferenciaAviso'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/veh}modificatorio')
    if el is not None:
        self['Modificatorio'] = modificatorio11(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/veh}prioridad')
    self['Prioridad'] = catalog_code('C329_prioridad_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/veh}alerta')
    self['Alerta'] = alerta12(cls, el)
    self['PersonaAviso'] = [persona_aviso10(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/veh}persona_aviso')]
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/veh}dueno_beneficiario')
    if el is not None:
        self['DuenoBeneficiario'] = [dueno_beneficiariof(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/veh}dueno_beneficiario')]
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/veh}detalle_operaciones')
    self['DetalleOperaciones'] = detalle_operacionesf(cls, el)
    return self
def modificatorio11(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/veh}folio_modificacion')
    self['FolioModificacion'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/veh}descripcion_modificacion')
    self['DescripcionModificacion'] = el.text
    return self
def alerta12(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/veh}tipo_alerta')
    self['TipoAlerta'] = catalog_code('C329_tipo_alerta_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/veh}descripcion_alerta')
    if el is not None:
        self['DescripcionAlerta'] = el.text
    return self
def persona_aviso10(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/veh}tipo_persona')
    self['TipoPersona'] = tipo_persona26(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/veh}tipo_domicilio')
    if el is not None:
        self['TipoDomicilio'] = tipo_domicilio10(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/veh}telefono')
    if el is not None:
        self['Telefono'] = telefono11(cls, el)
    return self
def tipo_persona26(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/veh}persona_fisica')
    if el is not None:
        self['PersonaFisica'] = persona_fisica28(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/veh}persona_moral')
    if el is not None:
        self['PersonaMoral'] = persona_moral29(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/veh}fideicomiso')
    if el is not None:
        self['Fideicomiso'] = fideicomiso23(cls, el)
    return self
def persona_fisica28(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/veh}nombre')
    self['Nombre'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/veh}apellido_paterno')
    self['ApellidoPaterno'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/veh}apellido_materno')
    self['ApellidoMaterno'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/veh}fecha_nacimiento')
    if el is not None:
        self['FechaNacimiento'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/veh}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/veh}curp')
    if el is not None:
        self['Curp'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/veh}pais_nacionalidad')
    self['PaisNacionalidad'] = catalog_code('C329_pais_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/veh}actividad_economica')
    self['ActividadEconomica'] = catalog_code('C329_actividad_economica_type', el.text)
    return self
def persona_moral29(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/veh}denominacion_razon')
    self['DenominacionRazon'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/veh}fecha_constitucion')
    if el is not None:
        self['FechaConstitucion'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/veh}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/veh}pais_nacionalidad')
    self['PaisNacionalidad'] = catalog_code('C329_pais_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/veh}giro_mercantil')
    self['GiroMercantil'] = catalog_code('C329_giro_mercantil_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/veh}representante_apoderado')
    self['RepresentanteApoderado'] = representante_apoderado10(cls, el)
    return self
def fideicomiso23(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/veh}denominacion_razon')
    self['DenominacionRazon'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/veh}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/veh}identificador_fideicomiso')
    if el is not None:
        self['IdentificadorFideicomiso'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/veh}apoderado_delegado')
    self['ApoderadoDelegado'] = representante_apoderado10(cls, el)
    return self
def representante_apoderado10(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/veh}nombre')
    self['Nombre'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/veh}apellido_paterno')
    self['ApellidoPaterno'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/veh}apellido_materno')
    self['ApellidoMaterno'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/veh}fecha_nacimiento')
    if el is not None:
        self['FechaNacimiento'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/veh}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/veh}curp')
    if el is not None:
        self['Curp'] = el.text
    return self
def tipo_domicilio10(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/veh}nacional')
    if el is not None:
        self['Nacional'] = nacional13(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/veh}extranjero')
    if el is not None:
        self['Extranjero'] = extranjero13(cls, el)
    return self
def nacional13(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/veh}colonia')
    self['Colonia'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/veh}calle')
    self['Calle'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/veh}numero_exterior')
    self['NumeroExterior'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/veh}numero_interior')
    if el is not None:
        self['NumeroInterior'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/veh}codigo_postal')
    self['CodigoPostal'] = el.text
    return self
def extranjero13(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/veh}pais')
    self['Pais'] = catalog_code('C329_pais_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/veh}estado_provincia')
    self['EstadoProvincia'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/veh}ciudad_poblacion')
    self['CiudadPoblacion'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/veh}colonia')
    self['Colonia'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/veh}calle')
    self['Calle'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/veh}numero_exterior')
    self['NumeroExterior'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/veh}numero_interior')
    if el is not None:
        self['NumeroInterior'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/veh}codigo_postal')
    self['CodigoPostal'] = el.text
    return self
def telefono11(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/veh}clave_pais')
    if el is not None:
        self['ClavePais'] = catalog_code('C329_pais_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/veh}numero_telefono')
    if el is not None:
        self['NumeroTelefono'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/veh}correo_electronico')
    if el is not None:
        self['CorreoElectronico'] = el.text
    return self
def dueno_beneficiariof(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/veh}tipo_persona')
    self['TipoPersona'] = tipo_persona27(cls, el)
    return self
def tipo_persona27(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/veh}persona_fisica')
    if el is not None:
        self['PersonaFisica'] = persona_fisica29(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/veh}persona_moral')
    if el is not None:
        self['PersonaMoral'] = persona_moral2a(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/veh}fideicomiso')
    if el is not None:
        self['Fideicomiso'] = fideicomiso24(cls, el)
    return self
def persona_fisica29(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/veh}nombre')
    self['Nombre'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/veh}apellido_paterno')
    self['ApellidoPaterno'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/veh}apellido_materno')
    self['ApellidoMaterno'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/veh}fecha_nacimiento')
    if el is not None:
        self['FechaNacimiento'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/veh}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/veh}curp')
    if el is not None:
        self['Curp'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/veh}pais_nacionalidad')
    if el is not None:
        self['PaisNacionalidad'] = catalog_code('C329_pais_type', el.text)
    return self
def persona_moral2a(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/veh}denominacion_razon')
    self['DenominacionRazon'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/veh}fecha_constitucion')
    if el is not None:
        self['FechaConstitucion'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/veh}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/veh}pais_nacionalidad')
    if el is not None:
        self['PaisNacionalidad'] = catalog_code('C329_pais_type', el.text)
    return self
def fideicomiso24(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/veh}denominacion_razon')
    self['DenominacionRazon'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/veh}rfc')
    if el is not None:
        self['Rfc'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/veh}identificador_fideicomiso')
    if el is not None:
        self['IdentificadorFideicomiso'] = el.text
    return self
def detalle_operacionesf(cls, node):
    self = ScalarMap()
    self['DatosOperacion'] = [datos_operacion11(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/veh}datos_operacion')]
    return self
def datos_operacion11(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/veh}fecha_operacion')
    self['FechaOperacion'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/veh}codigo_postal')
    self['CodigoPostal'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/veh}tipo_operacion')
    self['TipoOperacion'] = catalog_code('C329_tipo_operacion_type', el.text)
    self['TipoVehiculo'] = [tipo_vehiculo0(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/veh}tipo_vehiculo')]
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/veh}datos_liquidacion')
    if el is not None:
        self['DatosLiquidacion'] = [datos_liquidacionc(cls, n) for n in node.iterfind('{http://www.uif.shcp.gob.mx/recepcion/veh}datos_liquidacion')]
    return self
def tipo_vehiculo0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/veh}datos_vehiculo_terrestre')
    if el is not None:
        self['DatosVehiculoTerrestre'] = datos_vehiculo_terrestre1(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/veh}datos_vehiculo_maritimo')
    if el is not None:
        self['DatosVehiculoMaritimo'] = datos_vehiculo_maritimo0(cls, el)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/veh}datos_vehiculo_aereo')
    if el is not None:
        self['DatosVehiculoAereo'] = datos_vehiculo_aereo0(cls, el)
    return self
def datos_vehiculo_terrestre1(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/veh}marca_fabricante')
    self['MarcaFabricante'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/veh}modelo')
    self['Modelo'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/veh}anio')
    self['Anio'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/veh}vin')
    if el is not None:
        self['Vin'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/veh}repuve')
    if el is not None:
        self['Repuve'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/veh}placas')
    if el is not None:
        self['Placas'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/veh}nivel_blindaje')
    self['NivelBlindaje'] = el.text
    return self
def datos_vehiculo_maritimo0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/veh}marca_fabricante')
    self['MarcaFabricante'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/veh}modelo')
    self['Modelo'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/veh}anio')
    self['Anio'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/veh}numero_serie')
    self['NumeroSerie'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/veh}bandera')
    if el is not None:
        self['Bandera'] = catalog_code('C329_pais_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/veh}matricula')
    if el is not None:
        self['Matricula'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/veh}nivel_blindaje')
    self['NivelBlindaje'] = el.text
    return self
def datos_vehiculo_aereo0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/veh}marca_fabricante')
    self['MarcaFabricante'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/veh}modelo')
    self['Modelo'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/veh}anio')
    self['Anio'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/veh}numero_serie')
    self['NumeroSerie'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/veh}bandera')
    if el is not None:
        self['Bandera'] = catalog_code('C329_pais_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/veh}matricula')
    if el is not None:
        self['Matricula'] = el.text
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/veh}nivel_blindaje')
    self['NivelBlindaje'] = el.text
    return self
def datos_liquidacionc(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/veh}fecha_pago')
    self['FechaPago'] = datetime.strptime(el.text, '%Y%m%d').date()
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/veh}forma_pago')
    self['FormaPago'] = catalog_code('C329_forma_pago_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/veh}instrumento_monetario')
    if el is not None:
        self['InstrumentoMonetario'] = catalog_code('C329_instrumento_monetario_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/veh}moneda')
    self['Moneda'] = catalog_code('C329_moneda_type', el.text)
    el = node.find('{http://www.uif.shcp.gob.mx/recepcion/veh}monto_operacion')
    self['MontoOperacion'] = el.text
    return self
def t_ubicacion0(cls, node):
    self = ScalarMap()
    if (a := node.attrib.get('calle')) is not None:
        self['Calle'] = a
    if (a := node.attrib.get('noExterior')) is not None:
        self['NoExterior'] = a
    if (a := node.attrib.get('noInterior')) is not None:
        self['NoInterior'] = a
    if (a := node.attrib.get('colonia')) is not None:
        self['Colonia'] = a
    if (a := node.attrib.get('localidad')) is not None:
        self['Localidad'] = a
    if (a := node.attrib.get('referencia')) is not None:
        self['Referencia'] = a
    if (a := node.attrib.get('municipio')) is not None:
        self['Municipio'] = a
    if (a := node.attrib.get('estado')) is not None:
        self['Estado'] = a
    self['Pais'] = node.attrib['pais']
    if (a := node.attrib.get('codigoPostal')) is not None:
        self['CodigoPostal'] = a
    return self
def t_ubicacion_fiscal0(cls, node):
    self = ScalarMap()
    self['Calle'] = node.attrib['calle']
    if (a := node.attrib.get('noExterior')) is not None:
        self['NoExterior'] = a
    if (a := node.attrib.get('noInterior')) is not None:
        self['NoInterior'] = a
    if (a := node.attrib.get('colonia')) is not None:
        self['Colonia'] = a
    if (a := node.attrib.get('localidad')) is not None:
        self['Localidad'] = a
    if (a := node.attrib.get('referencia')) is not None:
        self['Referencia'] = a
    self['Municipio'] = node.attrib['municipio']
    self['Estado'] = node.attrib['estado']
    self['Pais'] = node.attrib['pais']
    self['CodigoPostal'] = node.attrib['codigoPostal']
    return self
def t_informacion_aduanera0(cls, node):
    self = ScalarMap()
    self['Numero'] = node.attrib['numero']
    self['Fecha'] = date.fromisoformat(node.attrib['fecha'])
    if (a := node.attrib.get('aduana')) is not None:
        self['Aduana'] = a
    return self
def t_ubicacion_fiscal1(cls, node):
    self = ScalarMap()
    self['Calle'] = node.attrib['calle']
    if (a := node.attrib.get('noExterior')) is not None:
        self['NoExterior'] = a
    if (a := node.attrib.get('noInterior')) is not None:
        self['NoInterior'] = a
    if (a := node.attrib.get('colonia')) is not None:
        self['Colonia'] = a
    if (a := node.attrib.get('localidad')) is not None:
        self['Localidad'] = a
    if (a := node.attrib.get('referencia')) is not None:
        self['Referencia'] = a
    self['Municipio'] = node.attrib['municipio']
    self['Estado'] = node.attrib['estado']
    self['Pais'] = node.attrib['pais']
    self['CodigoPostal'] = node.attrib['codigoPostal']
    return self
def t_informacion_aduanera1(cls, node):
    self = ScalarMap()
    self['Numero'] = node.attrib['numero']
    self['Fecha'] = date.fromisoformat(node.attrib['fecha'])
    if (a := node.attrib.get('aduana')) is not None:
        self['Aduana'] = a
    return self
def t_informacion_aduanera2(cls, node):
    self = ScalarMap()
    self['Numero'] = node.attrib['numero']
    self['Fecha'] = date.fromisoformat(node.attrib['fecha'])
    if (a := node.attrib.get('aduana')) is not None:
        self['Aduana'] = a
    return self
def t_informacion_aduanera3(cls, node):
    self = ScalarMap()
    self['Numero'] = node.attrib['numero']
    self['Fecha'] = date.fromisoformat(node.attrib['fecha'])
    if (a := node.attrib.get('aduana')) is not None:
        self['Aduana'] = a
    return self
def signature_type0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.w3.org/2000/09/xmldsig#}SignedInfo')
    self['SignedInfo'] = signed_info0(cls, el)
    el = node.find('{http://www.w3.org/2000/09/xmldsig#}SignatureValue')
    self['SignatureValue'] = signature_value0(cls, el)
    el = node.find('{http://www.w3.org/2000/09/xmldsig#}KeyInfo')
    self['KeyInfo'] = key_info0(cls, el)
    el = node.find('{http://www.w3.org/2000/09/xmldsig#}Object')
    self['Object'] = object0(cls, el)
    if (a := node.attrib.get('Id')) is not None:
        self['Id'] = a
    return self
def signature_value0(cls, node):
    self = ScalarMap()
    self['_text'] = node.text
    if (a := node.attrib.get('Id')) is not None:
        self['Id'] = a
    return self
def signed_info0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.w3.org/2000/09/xmldsig#}CanonicalizationMethod')
    self['CanonicalizationMethod'] = canonicalization_method0(cls, el)
    el = node.find('{http://www.w3.org/2000/09/xmldsig#}SignatureMethod')
    self['SignatureMethod'] = signature_method0(cls, el)
    el = node.find('{http://www.w3.org/2000/09/xmldsig#}Reference')
    self['Reference'] = reference0(cls, el)
    if (a := node.attrib.get('Id')) is not None:
        self['Id'] = a
    return self
def canonicalization_method0(cls, node):
    self = {n.tag.rsplit('}', 1)[-1]: cfdi_objectify.get(n.tag, default_objectify)(cls, n) for n in node}
    self['Algorithm'] = node.attrib['Algorithm']
    return self
def signature_method0(cls, node):
    self = {n.tag.rsplit('}', 1)[-1]: cfdi_objectify.get(n.tag, default_objectify)(cls, n) for n in node}
    el = node.find('{http://www.w3.org/2000/09/xmldsig#}HMACOutputLength')
    if el is not None:
        self['HMACOutputLength'] = Xint(el.text)
    self['Algorithm'] = node.attrib['Algorithm']
    return self
def reference0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.w3.org/2000/09/xmldsig#}Transforms')
    self['Transforms'] = transforms0(cls, el)
    el = node.find('{http://www.w3.org/2000/09/xmldsig#}DigestMethod')
    self['DigestMethod'] = digest_method0(cls, el)
    el = node.find('{http://www.w3.org/2000/09/xmldsig#}DigestValue')
    self['DigestValue'] = el.text
    if (a := node.attrib.get('Id')) is not None:
        self['Id'] = a
    if (a := node.attrib.get('URI')) is not None:
        self['URI'] = a
    if (a := node.attrib.get('Type')) is not None:
        self['Type'] = a
    return self
def transforms0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.w3.org/2000/09/xmldsig#}Transform')
    self['Transform'] = transform0(cls, el)
    return self
def transform0(cls, node):
    self = {n.tag.rsplit('}', 1)[-1]: cfdi_objectify.get(n.tag, default_objectify)(cls, n) for n in node}
    el = node.find('{http://www.w3.org/2000/09/xmldsig#}XPath')
    if el is not None:
        self['XPath'] = el.text
    self['Algorithm'] = node.attrib['Algorithm']
    return self
def digest_method0(cls, node):
    self = {n.tag.rsplit('}', 1)[-1]: cfdi_objectify.get(n.tag, default_objectify)(cls, n) for n in node}
    self['Algorithm'] = node.attrib['Algorithm']
    return self
def key_info0(cls, node):
    self = {n.tag.rsplit('}', 1)[-1]: cfdi_objectify.get(n.tag, default_objectify)(cls, n) for n in node}
    el = node.find('{http://www.w3.org/2000/09/xmldsig#}KeyName')
    if el is not None:
        self['KeyName'] = el.text
    el = node.find('{http://www.w3.org/2000/09/xmldsig#}KeyValue')
    if el is not None:
        self['KeyValue'] = key_value0(cls, el)
    el = node.find('{http://www.w3.org/2000/09/xmldsig#}RetrievalMethod')
    if el is not None:
        self['RetrievalMethod'] = retrieval_method0(cls, el)
    el = node.find('{http://www.w3.org/2000/09/xmldsig#}X509Data')
    if el is not None:
        self['X509Data'] = x509data0(cls, el)
    el = node.find('{http://www.w3.org/2000/09/xmldsig#}PGPData')
    if el is not None:
        self['PGPData'] = pgpdata0(cls, el)
    el = node.find('{http://www.w3.org/2000/09/xmldsig#}SPKIData')
    if el is not None:
        self['SPKIData'] = spkid_ata0(cls, el)
    el = node.find('{http://www.w3.org/2000/09/xmldsig#}MgmtData')
    if el is not None:
        self['MgmtData'] = el.text
    if (a := node.attrib.get('Id')) is not None:
        self['Id'] = a
    return self
def key_value0(cls, node):
    self = {n.tag.rsplit('}', 1)[-1]: cfdi_objectify.get(n.tag, default_objectify)(cls, n) for n in node}
    el = node.find('{http://www.w3.org/2000/09/xmldsig#}DSAKeyValue')
    if el is not None:
        self['DSAKeyValue'] = dsakey_value0(cls, el)
    el = node.find('{http://www.w3.org/2000/09/xmldsig#}RSAKeyValue')
    if el is not None:
        self['RSAKeyValue'] = rsakey_value0(cls, el)
    return self
def retrieval_method0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.w3.org/2000/09/xmldsig#}Transforms')
    self['Transforms'] = transforms0(cls, el)
    if (a := node.attrib.get('URI')) is not None:
        self['URI'] = a
    if (a := node.attrib.get('Type')) is not None:
        self['Type'] = a
    return self
def x509data0(cls, node):
    self = {n.tag.rsplit('}', 1)[-1]: cfdi_objectify.get(n.tag, default_objectify)(cls, n) for n in node}
    el = node.find('{http://www.w3.org/2000/09/xmldsig#}X509IssuerSerial')
    if el is not None:
        self['X509IssuerSerial'] = x509issuer_serial0(cls, el)
    el = node.find('{http://www.w3.org/2000/09/xmldsig#}X509SKI')
    if el is not None:
        self['X509SKI'] = el.text
    el = node.find('{http://www.w3.org/2000/09/xmldsig#}X509SubjectName')
    if el is not None:
        self['X509SubjectName'] = el.text
    el = node.find('{http://www.w3.org/2000/09/xmldsig#}X509Certificate')
    if el is not None:
        self['X509Certificate'] = el.text
    el = node.find('{http://www.w3.org/2000/09/xmldsig#}X509CRL')
    if el is not None:
        self['X509CRL'] = el.text
    return self
def x509issuer_serial0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.w3.org/2000/09/xmldsig#}X509IssuerName')
    self['X509IssuerName'] = el.text
    el = node.find('{http://www.w3.org/2000/09/xmldsig#}X509SerialNumber')
    self['X509SerialNumber'] = Xint(el.text)
    return self
def pgpdata0(cls, node):
    self = {n.tag.rsplit('}', 1)[-1]: cfdi_objectify.get(n.tag, default_objectify)(cls, n) for n in node}
    el = node.find('{http://www.w3.org/2000/09/xmldsig#}PGPKeyID')
    self['PGPKeyID'] = el.text
    el = node.find('{http://www.w3.org/2000/09/xmldsig#}PGPKeyPacket')
    if el is not None:
        self['PGPKeyPacket'] = el.text
    el = node.find('{http://www.w3.org/2000/09/xmldsig#}PGPKeyPacket')
    self['PGPKeyPacket'] = el.text
    return self
def spkid_ata0(cls, node):
    self = {n.tag.rsplit('}', 1)[-1]: cfdi_objectify.get(n.tag, default_objectify)(cls, n) for n in node}
    el = node.find('{http://www.w3.org/2000/09/xmldsig#}SPKISexp')
    self['SPKISexp'] = el.text
    return self
def object0(cls, node):
    self = {n.tag.rsplit('}', 1)[-1]: cfdi_objectify.get(n.tag, default_objectify)(cls, n) for n in node}
    if (a := node.attrib.get('Id')) is not None:
        self['Id'] = a
    if (a := node.attrib.get('MimeType')) is not None:
        self['MimeType'] = a
    if (a := node.attrib.get('Encoding')) is not None:
        self['Encoding'] = a
    return self
def manifest_type0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.w3.org/2000/09/xmldsig#}Reference')
    self['Reference'] = reference0(cls, el)
    if (a := node.attrib.get('Id')) is not None:
        self['Id'] = a
    return self
def signature_properties_type0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.w3.org/2000/09/xmldsig#}SignatureProperty')
    self['SignatureProperty'] = signature_property0(cls, el)
    if (a := node.attrib.get('Id')) is not None:
        self['Id'] = a
    return self
def signature_property0(cls, node):
    self = {n.tag.rsplit('}', 1)[-1]: cfdi_objectify.get(n.tag, default_objectify)(cls, n) for n in node}
    self['Target'] = node.attrib['Target']
    if (a := node.attrib.get('Id')) is not None:
        self['Id'] = a
    return self
def dsakey_value0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.w3.org/2000/09/xmldsig#}P')
    self['P'] = el.text
    el = node.find('{http://www.w3.org/2000/09/xmldsig#}Q')
    self['Q'] = el.text
    el = node.find('{http://www.w3.org/2000/09/xmldsig#}G')
    if el is not None:
        self['G'] = el.text
    el = node.find('{http://www.w3.org/2000/09/xmldsig#}Y')
    self['Y'] = el.text
    el = node.find('{http://www.w3.org/2000/09/xmldsig#}J')
    if el is not None:
        self['J'] = el.text
    el = node.find('{http://www.w3.org/2000/09/xmldsig#}Seed')
    self['Seed'] = el.text
    el = node.find('{http://www.w3.org/2000/09/xmldsig#}PgenCounter')
    self['PgenCounter'] = el.text
    return self
def rsakey_value0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.w3.org/2000/09/xmldsig#}Modulus')
    self['Modulus'] = el.text
    el = node.find('{http://www.w3.org/2000/09/xmldsig#}Exponent')
    self['Exponent'] = el.text
    return self
def cancelacion0(cls, node):
    self = cls()
    self.tag = node.tag
    el = node.find('{http://cancelacfd.sat.gob.mx}Folios')
    self['Folios'] = [folio0(cls, n) for n in el.iterfind('{http://cancelacfd.sat.gob.mx}Folio')]
    el = node.find('{http://cancelacfd.sat.gob.mx}Signature')
    self['Signature'] = signature_type0(cls, el)
    self['RfcEmisor'] = node.attrib['RfcEmisor']
    self['Fecha'] = datetime.fromisoformat(node.attrib['Fecha'])
    return self
def folio0(cls, node):
    self = ScalarMap()
    self['UUID'] = node.attrib['UUID']
    self['Motivo'] = node.attrib['Motivo']
    if (a := node.attrib.get('FolioSustitucion')) is not None:
        self['FolioSustitucion'] = a
    return self
def cancelacion1(cls, node):
    self = cls()
    self.tag = node.tag
    el = node.find('{http://www.sat.gob.mx/esquemas/retencionpago/1}Folios')
    self['Folios'] = [folio1(cls, n) for n in el.iterfind('{http://www.sat.gob.mx/esquemas/retencionpago/1}Folio')]
    el = node.find('{http://www.sat.gob.mx/esquemas/retencionpago/1}Signature')
    self['Signature'] = signature_type0(cls, el)
    self['RfcEmisor'] = node.attrib['RfcEmisor']
    self['Fecha'] = datetime.fromisoformat(node.attrib['Fecha'])
    return self
def folio1(cls, node):
    self = ScalarMap()
    self['UUID'] = node.attrib['UUID']
    self['Motivo'] = node.attrib['Motivo']
    if (a := node.attrib.get('FolioSustitucion')) is not None:
        self['FolioSustitucion'] = a
    return self
def solicitud_aceptacion_rechazo0(cls, node):
    self = cls()
    self.tag = node.tag
    el = node.find('{http://cancelacfd.sat.gob.mx}Folios')
    if el is not None:
        self['Folios'] = [folios0(cls, n) for n in node.iterfind('{http://cancelacfd.sat.gob.mx}Folios')]
    el = node.find('{http://cancelacfd.sat.gob.mx}Signature')
    self['Signature'] = signature_type0(cls, el)
    if (a := node.attrib.get('RfcReceptor')) is not None:
        self['RfcReceptor'] = a
    if (a := node.attrib.get('RfcPacEnviaSolicitud')) is not None:
        self['RfcPacEnviaSolicitud'] = a
    self['Fecha'] = datetime.fromisoformat(node.attrib['Fecha'])
    return self
def folios0(cls, node):
    self = ScalarMap()
    el = node.find('{http://cancelacfd.sat.gob.mx}UUID')
    if el is not None:
        self['UUID'] = el.text
    el = node.find('{http://cancelacfd.sat.gob.mx}Respuesta')
    self['Respuesta'] = el.text
    return self
def spei_tercero0(cls, node):
    self = cls()
    self.tag = node.tag
    el = node.find('Ordenante')
    self['Ordenante'] = ordenante0(cls, el)
    el = node.find('Beneficiario')
    self['Beneficiario'] = beneficiario0(cls, el)
    self['FechaOperacion'] = date.fromisoformat(node.attrib['FechaOperacion'])
    self['Hora'] = time.fromisoformat(node.attrib['Hora'])
    self['ClaveSPEI'] = Xint(node.attrib['ClaveSPEI'])
    self['Sello'] = node.attrib['sello']
    self['NumeroCertificado'] = node.attrib['numeroCertificado']
    self['CadenaCDA'] = node.attrib['cadenaCDA']
    self['ClaveRastreo'] = node.attrib['claveRastreo']
    return self
def ordenante0(cls, node):
    self = ScalarMap()
    self['BancoEmisor'] = node.attrib['BancoEmisor']
    self['Nombre'] = node.attrib['Nombre']
    self['TipoCuenta'] = Decimal(node.attrib['TipoCuenta'])
    self['Cuenta'] = Decimal(node.attrib['Cuenta'])
    self['RFC'] = node.attrib['RFC']
    return self
def beneficiario0(cls, node):
    self = ScalarMap()
    self['BancoReceptor'] = node.attrib['BancoReceptor']
    self['Nombre'] = node.attrib['Nombre']
    self['TipoCuenta'] = Decimal(node.attrib['TipoCuenta'])
    self['Cuenta'] = Decimal(node.attrib['Cuenta'])
    self['RFC'] = node.attrib['RFC']
    self['Concepto'] = node.attrib['Concepto']
    if (a := node.attrib.get('IVA')) is not None:
        self['IVA'] = Decimal(a)
    self['MontoPago'] = Decimal(node.attrib['MontoPago'])
    return self
def diverza0(cls, node):
    self = cls()
    self.tag = node.tag
    el = node.find('{http://www.diverza.com/ns/addenda/diverza/1}generales')
    if el is not None:
        self['Generales'] = generales0(cls, el)
    el = node.find('{http://www.diverza.com/ns/addenda/diverza/1}clavesDescripcion')
    if el is not None:
        self['ClavesDescripcion'] = claves_descripcion0(cls, el)
    el = node.find('{http://www.diverza.com/ns/addenda/diverza/1}emisor')
    if el is not None:
        self['Emisor'] = emisor0(cls, el)
    el = node.find('{http://www.diverza.com/ns/addenda/diverza/1}receptor')
    if el is not None:
        self['Receptor'] = receptor0(cls, el)
    el = node.find('{http://www.diverza.com/ns/addenda/diverza/1}conceptos')
    if el is not None:
        self['Conceptos'] = conceptos0(cls, el)
    el = node.find('{http://www.diverza.com/ns/addenda/diverza/1}complemento')
    if el is not None:
        self['Complemento'] = [extra0(cls, n) for n in el.iterfind('{http://www.diverza.com/ns/addenda/diverza/1}datosExtra')]
    self['Version'] = node.attrib['version']
    return self
def generales0(cls, node):
    self = ScalarMap()
    if (a := node.attrib.get('tipoDocumento')) is not None:
        self['TipoDocumento'] = a
    if (a := node.attrib.get('totalConLetra')) is not None:
        self['TotalConLetra'] = a
    if (a := node.attrib.get('observaciones')) is not None:
        self['Observaciones'] = a
    if (a := node.attrib.get('numeroOrden')) is not None:
        self['NumeroOrden'] = a
    if (a := node.attrib.get('nombreTransportista')) is not None:
        self['NombreTransportista'] = a
    if (a := node.attrib.get('embarque')) is not None:
        self['Embarque'] = a
    if (a := node.attrib.get('numeroEntrega')) is not None:
        self['NumeroEntrega'] = a
    if (a := node.attrib.get('terminosPago')) is not None:
        self['TerminosPago'] = a
    if (a := node.attrib.get('fechaEntrega')) is not None:
        self['FechaEntrega'] = date.fromisoformat(a)
    if (a := node.attrib.get('fechaTipoCambio')) is not None:
        self['FechaTipoCambio'] = date.fromisoformat(a)
    return self
def claves_descripcion0(cls, node):
    self = ScalarMap()
    if (a := node.attrib.get('c_FormaPago')) is not None:
        self['CFormaPago'] = a
    if (a := node.attrib.get('c_Moneda')) is not None:
        self['CMoneda'] = a
    if (a := node.attrib.get('c_TipoDeComprobante')) is not None:
        self['CTipoDeComprobante'] = a
    if (a := node.attrib.get('c_MetodoPago')) is not None:
        self['CMetodoPago'] = a
    if (a := node.attrib.get('c_LugarExpedicion')) is not None:
        self['CLugarExpedicion'] = a
    if (a := node.attrib.get('c_TipoRelacion')) is not None:
        self['CTipoRelacion'] = a
    if (a := node.attrib.get('c_RegimenFiscal')) is not None:
        self['CRegimenFiscal'] = a
    if (a := node.attrib.get('c_ResidenciaFiscal')) is not None:
        self['CResidenciaFiscal'] = a
    if (a := node.attrib.get('c_UsoCFDI')) is not None:
        self['CUsoCFDI'] = a
    return self
def emisor0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.diverza.com/ns/addenda/diverza/1}datosContactoE')
    if el is not None:
        self['DatosContactoE'] = datos_contacto0(cls, el)
    el = node.find('{http://www.diverza.com/ns/addenda/diverza/1}domicilioFiscalE')
    if el is not None:
        self['DomicilioFiscalE'] = ubicacion0(cls, el)
    el = node.find('{http://www.diverza.com/ns/addenda/diverza/1}domicilioOrigenE')
    if el is not None:
        self['DomicilioOrigenE'] = ubicacion0(cls, el)
    el = node.find('{http://www.diverza.com/ns/addenda/diverza/1}sucursalE')
    if el is not None:
        self['SucursalE'] = sucursal_e0(cls, el)
    if (a := node.attrib.get('vendedor')) is not None:
        self['Vendedor'] = a
    if (a := node.attrib.get('numeroProveedor')) is not None:
        self['NumeroProveedor'] = a
    if (a := node.attrib.get('tipoProveedor')) is not None:
        self['TipoProveedor'] = a
    if (a := node.attrib.get('gln')) is not None:
        self['Gln'] = a
    return self
def sucursal_e0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.diverza.com/ns/addenda/diverza/1}domicilioSucursal')
    if el is not None:
        self['DomicilioSucursal'] = ubicacion0(cls, el)
    el = node.find('{http://www.diverza.com/ns/addenda/diverza/1}datosContacto')
    if el is not None:
        self['DatosContacto'] = datos_contacto0(cls, el)
    if (a := node.attrib.get('alias')) is not None:
        self['Alias'] = a
    return self
def receptor0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.diverza.com/ns/addenda/diverza/1}datosContactoR')
    if el is not None:
        self['DatosContactoR'] = datos_contacto0(cls, el)
    el = node.find('{http://www.diverza.com/ns/addenda/diverza/1}domicilioFiscalR')
    if el is not None:
        self['DomicilioFiscalR'] = ubicacion0(cls, el)
    el = node.find('{http://www.diverza.com/ns/addenda/diverza/1}destino')
    if el is not None:
        self['Destino'] = [ubicacion0(cls, n) for n in el.iterfind('{http://www.diverza.com/ns/addenda/diverza/1}domicilioDestinoR')]
    if (a := node.attrib.get('comprador')) is not None:
        self['Comprador'] = a
    if (a := node.attrib.get('numCliente')) is not None:
        self['NumCliente'] = a
    return self
def conceptos0(cls, node):
    self = ScalarMap()
    self['Concepto'] = [concepto0(cls, n) for n in node.iterfind('{http://www.diverza.com/ns/addenda/diverza/1}concepto')]
    if (a := node.attrib.get('numeroConceptos')) is not None:
        self['NumeroConceptos'] = Xint(a)
    return self
def concepto0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.diverza.com/ns/addenda/diverza/1}datosExtraC')
    if el is not None:
        self['DatosExtraC'] = [extra0(cls, n) for n in node.iterfind('{http://www.diverza.com/ns/addenda/diverza/1}datosExtraC')]
    if (a := node.attrib.get('indicador')) is not None:
        self['Indicador'] = a
    if (a := node.attrib.get('identificador1')) is not None:
        self['Identificador1'] = a
    if (a := node.attrib.get('identificador2')) is not None:
        self['Identificador2'] = a
    if (a := node.attrib.get('descripcionExtranjera')) is not None:
        self['DescripcionExtranjera'] = a
    if (a := node.attrib.get('valorUnitarioMonedaExtranjera')) is not None:
        self['ValorUnitarioMonedaExtranjera'] = Decimal(a)
    if (a := node.attrib.get('importeMonedaExtranjera')) is not None:
        self['ImporteMonedaExtranjera'] = Decimal(a)
    if (a := node.attrib.get('mensaje')) is not None:
        self['Mensaje'] = a
    if (a := node.attrib.get('unidadMedida')) is not None:
        self['UnidadMedida'] = a
    if (a := node.attrib.get('codigoEAN')) is not None:
        self['CodigoEAN'] = a
    if (a := node.attrib.get('sku')) is not None:
        self['Sku'] = a
    if (a := node.attrib.get('nombreTransportistaC')) is not None:
        self['NombreTransportistaC'] = a
    if (a := node.attrib.get('numeroEntregaC')) is not None:
        self['NumeroEntregaC'] = a
    if (a := node.attrib.get('fechaEntregaC')) is not None:
        self['FechaEntregaC'] = date.fromisoformat(a)
    return self
def auxiliar_ctas0(cls, node):
    self = cls()
    self.tag = node.tag
    self['Cuenta'] = [cuenta0(cls, n) for n in node.iterfind('{www.sat.gob.mx/esquemas/ContabilidadE/1_1/AuxiliarCtas}Cuenta')]
    self['Version'] = node.attrib['Version']
    self['RFC'] = node.attrib['RFC']
    self['Mes'] = node.attrib['Mes']
    self['Anio'] = Xint(node.attrib['Anio'])
    self['TipoSolicitud'] = node.attrib['TipoSolicitud']
    if (a := node.attrib.get('NumOrden')) is not None:
        self['NumOrden'] = a
    if (a := node.attrib.get('NumTramite')) is not None:
        self['NumTramite'] = a
    if (a := node.attrib.get('Sello')) is not None:
        self['Sello'] = a
    if (a := node.attrib.get('noCertificado')) is not None:
        self['NoCertificado'] = a
    if (a := node.attrib.get('Certificado')) is not None:
        self['Certificado'] = a
    return self
def cuenta0(cls, node):
    self = ScalarMap()
    self['DetalleAux'] = [detalle_aux0(cls, n) for n in node.iterfind('{www.sat.gob.mx/esquemas/ContabilidadE/1_1/AuxiliarCtas}DetalleAux')]
    self['NumCta'] = node.attrib['NumCta']
    self['DesCta'] = node.attrib['DesCta']
    self['SaldoIni'] = Decimal(node.attrib['SaldoIni'])
    self['SaldoFin'] = Decimal(node.attrib['SaldoFin'])
    return self
def detalle_aux0(cls, node):
    self = ScalarMap()
    self['Fecha'] = date.fromisoformat(node.attrib['Fecha'])
    self['NumUnIdenPol'] = node.attrib['NumUnIdenPol']
    self['Concepto'] = node.attrib['Concepto']
    self['Debe'] = Decimal(node.attrib['Debe'])
    self['Haber'] = Decimal(node.attrib['Haber'])
    return self
def rep_aux_fol0(cls, node):
    self = cls()
    self.tag = node.tag
    el = node.find('{www.sat.gob.mx/esquemas/ContabilidadE/1_1/AuxiliarFolios}DetAuxFol')
    if el is not None:
        self['DetAuxFol'] = [det_aux_fol0(cls, n) for n in node.iterfind('{www.sat.gob.mx/esquemas/ContabilidadE/1_1/AuxiliarFolios}DetAuxFol')]
    self['Version'] = node.attrib['Version']
    self['RFC'] = node.attrib['RFC']
    self['Mes'] = node.attrib['Mes']
    self['Anio'] = Xint(node.attrib['Anio'])
    self['TipoSolicitud'] = node.attrib['TipoSolicitud']
    if (a := node.attrib.get('NumOrden')) is not None:
        self['NumOrden'] = a
    if (a := node.attrib.get('NumTramite')) is not None:
        self['NumTramite'] = a
    if (a := node.attrib.get('Sello')) is not None:
        self['Sello'] = a
    if (a := node.attrib.get('noCertificado')) is not None:
        self['NoCertificado'] = a
    if (a := node.attrib.get('Certificado')) is not None:
        self['Certificado'] = a
    return self
def det_aux_fol0(cls, node):
    self = ScalarMap()
    el = node.find('{www.sat.gob.mx/esquemas/ContabilidadE/1_1/AuxiliarFolios}ComprNal')
    if el is not None:
        self['ComprNal'] = [compr_nal0(cls, n) for n in node.iterfind('{www.sat.gob.mx/esquemas/ContabilidadE/1_1/AuxiliarFolios}ComprNal')]
    el = node.find('{www.sat.gob.mx/esquemas/ContabilidadE/1_1/AuxiliarFolios}ComprNalOtr')
    if el is not None:
        self['ComprNalOtr'] = [compr_nal_otr0(cls, n) for n in node.iterfind('{www.sat.gob.mx/esquemas/ContabilidadE/1_1/AuxiliarFolios}ComprNalOtr')]
    el = node.find('{www.sat.gob.mx/esquemas/ContabilidadE/1_1/AuxiliarFolios}ComprExt')
    if el is not None:
        self['ComprExt'] = [compr_ext0(cls, n) for n in node.iterfind('{www.sat.gob.mx/esquemas/ContabilidadE/1_1/AuxiliarFolios}ComprExt')]
    self['NumUnIdenPol'] = node.attrib['NumUnIdenPol']
    self['Fecha'] = date.fromisoformat(node.attrib['Fecha'])
    return self
def compr_nal0(cls, node):
    self = ScalarMap()
    self['UUID_CFDI'] = node.attrib['UUID_CFDI']
    self['MontoTotal'] = Decimal(node.attrib['MontoTotal'])
    self['RFC'] = node.attrib['RFC']
    if (a := node.attrib.get('MetPagoAux')) is not None:
        self['MetPagoAux'] = catalog_code('C756_c_FormaPago', a)
    if (a := node.attrib.get('Moneda')) is not None:
        self['Moneda'] = catalog_code('C756_c_Moneda', a, 0)
    if (a := node.attrib.get('TipCamb')) is not None:
        self['TipCamb'] = Decimal(a)
    return self
def compr_nal_otr0(cls, node):
    self = ScalarMap()
    if (a := node.attrib.get('CFD_CBB_Serie')) is not None:
        self['CFD_CBB_Serie'] = a
    self['CFD_CBB_NumFol'] = Xint(node.attrib['CFD_CBB_NumFol'])
    self['MontoTotal'] = Decimal(node.attrib['MontoTotal'])
    self['RFC'] = node.attrib['RFC']
    if (a := node.attrib.get('MetPagoAux')) is not None:
        self['MetPagoAux'] = catalog_code('C756_c_FormaPago', a)
    if (a := node.attrib.get('Moneda')) is not None:
        self['Moneda'] = catalog_code('C756_c_Moneda', a, 0)
    if (a := node.attrib.get('TipCamb')) is not None:
        self['TipCamb'] = Decimal(a)
    return self
def compr_ext0(cls, node):
    self = ScalarMap()
    self['NumFactExt'] = node.attrib['NumFactExt']
    if (a := node.attrib.get('TaxID')) is not None:
        self['TaxID'] = a
    self['MontoTotal'] = Decimal(node.attrib['MontoTotal'])
    if (a := node.attrib.get('MetPagoAux')) is not None:
        self['MetPagoAux'] = catalog_code('C756_c_FormaPago', a)
    if (a := node.attrib.get('Moneda')) is not None:
        self['Moneda'] = catalog_code('C756_c_Moneda', a, 0)
    if (a := node.attrib.get('TipCamb')) is not None:
        self['TipCamb'] = Decimal(a)
    return self
def balanza0(cls, node):
    self = cls()
    self.tag = node.tag
    self['Ctas'] = [ctas0(cls, n) for n in node.iterfind('{www.sat.gob.mx/esquemas/ContabilidadE/1_1/BalanzaComprobacion}Ctas')]
    self['Version'] = node.attrib['Version']
    self['RFC'] = node.attrib['RFC']
    self['Mes'] = node.attrib['Mes']
    self['Anio'] = Xint(node.attrib['Anio'])
    self['TipoEnvio'] = node.attrib['TipoEnvio']
    if (a := node.attrib.get('FechaModBal')) is not None:
        self['FechaModBal'] = date.fromisoformat(a)
    if (a := node.attrib.get('Sello')) is not None:
        self['Sello'] = a
    if (a := node.attrib.get('noCertificado')) is not None:
        self['NoCertificado'] = a
    if (a := node.attrib.get('Certificado')) is not None:
        self['Certificado'] = a
    return self
def ctas0(cls, node):
    self = ScalarMap()
    self['NumCta'] = node.attrib['NumCta']
    self['SaldoIni'] = Decimal(node.attrib['SaldoIni'])
    self['Debe'] = Decimal(node.attrib['Debe'])
    self['Haber'] = Decimal(node.attrib['Haber'])
    self['SaldoFin'] = Decimal(node.attrib['SaldoFin'])
    return self
def catalogo0(cls, node):
    self = cls()
    self.tag = node.tag
    self['Ctas'] = [ctas1(cls, n) for n in node.iterfind('{www.sat.gob.mx/esquemas/ContabilidadE/1_1/CatalogoCuentas}Ctas')]
    self['Version'] = node.attrib['Version']
    self['RFC'] = node.attrib['RFC']
    self['Mes'] = node.attrib['Mes']
    self['Anio'] = Xint(node.attrib['Anio'])
    if (a := node.attrib.get('Sello')) is not None:
        self['Sello'] = a
    if (a := node.attrib.get('noCertificado')) is not None:
        self['NoCertificado'] = a
    if (a := node.attrib.get('Certificado')) is not None:
        self['Certificado'] = a
    return self
def ctas1(cls, node):
    self = ScalarMap()
    self['CodAgrup'] = catalog_code('Cb9f_c_CodAgrup', node.attrib['CodAgrup'])
    self['NumCta'] = node.attrib['NumCta']
    self['Desc'] = node.attrib['Desc']
    if (a := node.attrib.get('SubCtaDe')) is not None:
        self['SubCtaDe'] = a
    self['Nivel'] = Xint(node.attrib['Nivel'])
    self['Natur'] = node.attrib['Natur']
    return self
def polizas0(cls, node):
    self = cls()
    self.tag = node.tag
    self['Poliza'] = [poliza0(cls, n) for n in node.iterfind('{www.sat.gob.mx/esquemas/ContabilidadE/1_1/PolizasPeriodo}Poliza')]
    self['Version'] = node.attrib['Version']
    self['RFC'] = node.attrib['RFC']
    self['Mes'] = node.attrib['Mes']
    self['Anio'] = Xint(node.attrib['Anio'])
    self['TipoSolicitud'] = node.attrib['TipoSolicitud']
    if (a := node.attrib.get('NumOrden')) is not None:
        self['NumOrden'] = a
    if (a := node.attrib.get('NumTramite')) is not None:
        self['NumTramite'] = a
    if (a := node.attrib.get('Sello')) is not None:
        self['Sello'] = a
    if (a := node.attrib.get('noCertificado')) is not None:
        self['NoCertificado'] = a
    if (a := node.attrib.get('Certificado')) is not None:
        self['Certificado'] = a
    return self
def poliza0(cls, node):
    self = ScalarMap()
    self['Transaccion'] = [transaccion0(cls, n) for n in node.iterfind('{www.sat.gob.mx/esquemas/ContabilidadE/1_1/PolizasPeriodo}Transaccion')]
    self['NumUnIdenPol'] = node.attrib['NumUnIdenPol']
    self['Fecha'] = date.fromisoformat(node.attrib['Fecha'])
    self['Concepto'] = node.attrib['Concepto']
    return self
def transaccion0(cls, node):
    self = ScalarMap()
    el = node.find('{www.sat.gob.mx/esquemas/ContabilidadE/1_1/PolizasPeriodo}CompNal')
    if el is not None:
        self['CompNal'] = [comp_nal0(cls, n) for n in node.iterfind('{www.sat.gob.mx/esquemas/ContabilidadE/1_1/PolizasPeriodo}CompNal')]
    el = node.find('{www.sat.gob.mx/esquemas/ContabilidadE/1_1/PolizasPeriodo}CompNalOtr')
    if el is not None:
        self['CompNalOtr'] = [comp_nal_otr0(cls, n) for n in node.iterfind('{www.sat.gob.mx/esquemas/ContabilidadE/1_1/PolizasPeriodo}CompNalOtr')]
    el = node.find('{www.sat.gob.mx/esquemas/ContabilidadE/1_1/PolizasPeriodo}CompExt')
    if el is not None:
        self['CompExt'] = [comp_ext0(cls, n) for n in node.iterfind('{www.sat.gob.mx/esquemas/ContabilidadE/1_1/PolizasPeriodo}CompExt')]
    el = node.find('{www.sat.gob.mx/esquemas/ContabilidadE/1_1/PolizasPeriodo}Cheque')
    if el is not None:
        self['Cheque'] = [cheque0(cls, n) for n in node.iterfind('{www.sat.gob.mx/esquemas/ContabilidadE/1_1/PolizasPeriodo}Cheque')]
    el = node.find('{www.sat.gob.mx/esquemas/ContabilidadE/1_1/PolizasPeriodo}Transferencia')
    if el is not None:
        self['Transferencia'] = [transferencia0(cls, n) for n in node.iterfind('{www.sat.gob.mx/esquemas/ContabilidadE/1_1/PolizasPeriodo}Transferencia')]
    el = node.find('{www.sat.gob.mx/esquemas/ContabilidadE/1_1/PolizasPeriodo}OtrMetodoPago')
    if el is not None:
        self['OtrMetodoPago'] = [otr_metodo_pago0(cls, n) for n in node.iterfind('{www.sat.gob.mx/esquemas/ContabilidadE/1_1/PolizasPeriodo}OtrMetodoPago')]
    self['NumCta'] = node.attrib['NumCta']
    self['DesCta'] = node.attrib['DesCta']
    self['Concepto'] = node.attrib['Concepto']
    self['Debe'] = Decimal(node.attrib['Debe'])
    self['Haber'] = Decimal(node.attrib['Haber'])
    return self
def comp_nal0(cls, node):
    self = ScalarMap()
    self['UUID_CFDI'] = node.attrib['UUID_CFDI']
    self['RFC'] = node.attrib['RFC']
    self['MontoTotal'] = Decimal(node.attrib['MontoTotal'])
    if (a := node.attrib.get('Moneda')) is not None:
        self['Moneda'] = catalog_code('C756_c_Moneda', a, 0)
    if (a := node.attrib.get('TipCamb')) is not None:
        self['TipCamb'] = Decimal(a)
    return self
def comp_nal_otr0(cls, node):
    self = ScalarMap()
    if (a := node.attrib.get('CFD_CBB_Serie')) is not None:
        self['CFD_CBB_Serie'] = a
    self['CFD_CBB_NumFol'] = Xint(node.attrib['CFD_CBB_NumFol'])
    self['RFC'] = node.attrib['RFC']
    self['MontoTotal'] = Decimal(node.attrib['MontoTotal'])
    if (a := node.attrib.get('Moneda')) is not None:
        self['Moneda'] = catalog_code('C756_c_Moneda', a, 0)
    if (a := node.attrib.get('TipCamb')) is not None:
        self['TipCamb'] = Decimal(a)
    return self
def comp_ext0(cls, node):
    self = ScalarMap()
    self['NumFactExt'] = node.attrib['NumFactExt']
    if (a := node.attrib.get('TaxID')) is not None:
        self['TaxID'] = a
    self['MontoTotal'] = Decimal(node.attrib['MontoTotal'])
    if (a := node.attrib.get('Moneda')) is not None:
        self['Moneda'] = catalog_code('C756_c_Moneda', a, 0)
    if (a := node.attrib.get('TipCamb')) is not None:
        self['TipCamb'] = Decimal(a)
    return self
def cheque0(cls, node):
    self = ScalarMap()
    self['Num'] = node.attrib['Num']
    self['BanEmisNal'] = catalog_code('C75b_c_Banco', node.attrib['BanEmisNal'])
    if (a := node.attrib.get('BanEmisExt')) is not None:
        self['BanEmisExt'] = a
    self['CtaOri'] = node.attrib['CtaOri']
    self['Fecha'] = date.fromisoformat(node.attrib['Fecha'])
    self['Benef'] = node.attrib['Benef']
    self['RFC'] = node.attrib['RFC']
    self['Monto'] = Decimal(node.attrib['Monto'])
    if (a := node.attrib.get('Moneda')) is not None:
        self['Moneda'] = catalog_code('C756_c_Moneda', a, 0)
    if (a := node.attrib.get('TipCamb')) is not None:
        self['TipCamb'] = Decimal(a)
    return self
def transferencia0(cls, node):
    self = ScalarMap()
    if (a := node.attrib.get('CtaOri')) is not None:
        self['CtaOri'] = a
    self['BancoOriNal'] = catalog_code('C75b_c_Banco', node.attrib['BancoOriNal'])
    if (a := node.attrib.get('BancoOriExt')) is not None:
        self['BancoOriExt'] = a
    self['CtaDest'] = node.attrib['CtaDest']
    self['BancoDestNal'] = catalog_code('C75b_c_Banco', node.attrib['BancoDestNal'])
    if (a := node.attrib.get('BancoDestExt')) is not None:
        self['BancoDestExt'] = a
    self['Fecha'] = date.fromisoformat(node.attrib['Fecha'])
    self['Benef'] = node.attrib['Benef']
    self['RFC'] = node.attrib['RFC']
    self['Monto'] = Decimal(node.attrib['Monto'])
    if (a := node.attrib.get('Moneda')) is not None:
        self['Moneda'] = catalog_code('C756_c_Moneda', a, 0)
    if (a := node.attrib.get('TipCamb')) is not None:
        self['TipCamb'] = Decimal(a)
    return self
def otr_metodo_pago0(cls, node):
    self = ScalarMap()
    self['MetPagoPol'] = catalog_code('C756_c_FormaPago', node.attrib['MetPagoPol'])
    self['Fecha'] = date.fromisoformat(node.attrib['Fecha'])
    self['Benef'] = node.attrib['Benef']
    self['RFC'] = node.attrib['RFC']
    self['Monto'] = Decimal(node.attrib['Monto'])
    if (a := node.attrib.get('Moneda')) is not None:
        self['Moneda'] = catalog_code('C756_c_Moneda', a, 0)
    if (a := node.attrib.get('TipCamb')) is not None:
        self['TipCamb'] = Decimal(a)
    return self
def auxiliar_ctas1(cls, node):
    self = cls()
    self.tag = node.tag
    self['Cuenta'] = [cuenta1(cls, n) for n in node.iterfind('{http://www.sat.gob.mx/esquemas/ContabilidadE/1_3/AuxiliarCtas}Cuenta')]
    self['Version'] = node.attrib['Version']
    self['RFC'] = node.attrib['RFC']
    self['Mes'] = node.attrib['Mes']
    self['Anio'] = Xint(node.attrib['Anio'])
    self['TipoSolicitud'] = node.attrib['TipoSolicitud']
    if (a := node.attrib.get('NumOrden')) is not None:
        self['NumOrden'] = a
    if (a := node.attrib.get('NumTramite')) is not None:
        self['NumTramite'] = a
    if (a := node.attrib.get('Sello')) is not None:
        self['Sello'] = a
    if (a := node.attrib.get('noCertificado')) is not None:
        self['NoCertificado'] = a
    if (a := node.attrib.get('Certificado')) is not None:
        self['Certificado'] = a
    return self
def cuenta1(cls, node):
    self = ScalarMap()
    self['DetalleAux'] = [detalle_aux1(cls, n) for n in node.iterfind('{http://www.sat.gob.mx/esquemas/ContabilidadE/1_3/AuxiliarCtas}DetalleAux')]
    self['NumCta'] = node.attrib['NumCta']
    self['DesCta'] = node.attrib['DesCta']
    self['SaldoIni'] = Decimal(node.attrib['SaldoIni'])
    self['SaldoFin'] = Decimal(node.attrib['SaldoFin'])
    return self
def detalle_aux1(cls, node):
    self = ScalarMap()
    self['Fecha'] = date.fromisoformat(node.attrib['Fecha'])
    self['NumUnIdenPol'] = node.attrib['NumUnIdenPol']
    self['Concepto'] = node.attrib['Concepto']
    self['Debe'] = Decimal(node.attrib['Debe'])
    self['Haber'] = Decimal(node.attrib['Haber'])
    return self
def rep_aux_fol1(cls, node):
    self = cls()
    self.tag = node.tag
    el = node.find('{http://www.sat.gob.mx/esquemas/ContabilidadE/1_3/AuxiliarFolios}DetAuxFol')
    if el is not None:
        self['DetAuxFol'] = [det_aux_fol1(cls, n) for n in node.iterfind('{http://www.sat.gob.mx/esquemas/ContabilidadE/1_3/AuxiliarFolios}DetAuxFol')]
    self['Version'] = node.attrib['Version']
    self['RFC'] = node.attrib['RFC']
    self['Mes'] = node.attrib['Mes']
    self['Anio'] = Xint(node.attrib['Anio'])
    self['TipoSolicitud'] = node.attrib['TipoSolicitud']
    if (a := node.attrib.get('NumOrden')) is not None:
        self['NumOrden'] = a
    if (a := node.attrib.get('NumTramite')) is not None:
        self['NumTramite'] = a
    if (a := node.attrib.get('Sello')) is not None:
        self['Sello'] = a
    if (a := node.attrib.get('noCertificado')) is not None:
        self['NoCertificado'] = a
    if (a := node.attrib.get('Certificado')) is not None:
        self['Certificado'] = a
    return self
def det_aux_fol1(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.sat.gob.mx/esquemas/ContabilidadE/1_3/AuxiliarFolios}ComprNal')
    if el is not None:
        self['ComprNal'] = [compr_nal1(cls, n) for n in node.iterfind('{http://www.sat.gob.mx/esquemas/ContabilidadE/1_3/AuxiliarFolios}ComprNal')]
    el = node.find('{http://www.sat.gob.mx/esquemas/ContabilidadE/1_3/AuxiliarFolios}ComprNalOtr')
    if el is not None:
        self['ComprNalOtr'] = [compr_nal_otr1(cls, n) for n in node.iterfind('{http://www.sat.gob.mx/esquemas/ContabilidadE/1_3/AuxiliarFolios}ComprNalOtr')]
    el = node.find('{http://www.sat.gob.mx/esquemas/ContabilidadE/1_3/AuxiliarFolios}ComprExt')
    if el is not None:
        self['ComprExt'] = [compr_ext1(cls, n) for n in node.iterfind('{http://www.sat.gob.mx/esquemas/ContabilidadE/1_3/AuxiliarFolios}ComprExt')]
    self['NumUnIdenPol'] = node.attrib['NumUnIdenPol']
    self['Fecha'] = date.fromisoformat(node.attrib['Fecha'])
    return self
def compr_nal1(cls, node):
    self = ScalarMap()
    self['UUID_CFDI'] = node.attrib['UUID_CFDI']
    self['MontoTotal'] = Decimal(node.attrib['MontoTotal'])
    self['RFC'] = node.attrib['RFC']
    if (a := node.attrib.get('MetPagoAux')) is not None:
        self['MetPagoAux'] = catalog_code('C756_c_FormaPago', a)
    if (a := node.attrib.get('Moneda')) is not None:
        self['Moneda'] = catalog_code('C756_c_Moneda', a, 0)
    if (a := node.attrib.get('TipCamb')) is not None:
        self['TipCamb'] = Decimal(a)
    return self
def compr_nal_otr1(cls, node):
    self = ScalarMap()
    if (a := node.attrib.get('CFD_CBB_Serie')) is not None:
        self['CFD_CBB_Serie'] = a
    self['CFD_CBB_NumFol'] = Xint(node.attrib['CFD_CBB_NumFol'])
    self['MontoTotal'] = Decimal(node.attrib['MontoTotal'])
    self['RFC'] = node.attrib['RFC']
    if (a := node.attrib.get('MetPagoAux')) is not None:
        self['MetPagoAux'] = catalog_code('C756_c_FormaPago', a)
    if (a := node.attrib.get('Moneda')) is not None:
        self['Moneda'] = catalog_code('C756_c_Moneda', a, 0)
    if (a := node.attrib.get('TipCamb')) is not None:
        self['TipCamb'] = Decimal(a)
    return self
def compr_ext1(cls, node):
    self = ScalarMap()
    self['NumFactExt'] = node.attrib['NumFactExt']
    if (a := node.attrib.get('TaxID')) is not None:
        self['TaxID'] = a
    self['MontoTotal'] = Decimal(node.attrib['MontoTotal'])
    if (a := node.attrib.get('MetPagoAux')) is not None:
        self['MetPagoAux'] = catalog_code('C756_c_FormaPago', a)
    if (a := node.attrib.get('Moneda')) is not None:
        self['Moneda'] = catalog_code('C756_c_Moneda', a, 0)
    if (a := node.attrib.get('TipCamb')) is not None:
        self['TipCamb'] = Decimal(a)
    return self
def balanza1(cls, node):
    self = cls()
    self.tag = node.tag
    self['Ctas'] = [ctas2(cls, n) for n in node.iterfind('{http://www.sat.gob.mx/esquemas/ContabilidadE/1_3/BalanzaComprobacion}Ctas')]
    self['Version'] = node.attrib['Version']
    self['RFC'] = node.attrib['RFC']
    self['Mes'] = node.attrib['Mes']
    self['Anio'] = Xint(node.attrib['Anio'])
    self['TipoEnvio'] = node.attrib['TipoEnvio']
    if (a := node.attrib.get('FechaModBal')) is not None:
        self['FechaModBal'] = date.fromisoformat(a)
    if (a := node.attrib.get('Sello')) is not None:
        self['Sello'] = a
    if (a := node.attrib.get('noCertificado')) is not None:
        self['NoCertificado'] = a
    if (a := node.attrib.get('Certificado')) is not None:
        self['Certificado'] = a
    return self
def ctas2(cls, node):
    self = ScalarMap()
    self['NumCta'] = node.attrib['NumCta']
    self['SaldoIni'] = Decimal(node.attrib['SaldoIni'])
    self['Debe'] = Decimal(node.attrib['Debe'])
    self['Haber'] = Decimal(node.attrib['Haber'])
    self['SaldoFin'] = Decimal(node.attrib['SaldoFin'])
    return self
def catalogo1(cls, node):
    self = cls()
    self.tag = node.tag
    self['Ctas'] = [ctas3(cls, n) for n in node.iterfind('{http://www.sat.gob.mx/esquemas/ContabilidadE/1_3/CatalogoCuentas}Ctas')]
    self['Version'] = node.attrib['Version']
    self['RFC'] = node.attrib['RFC']
    self['Mes'] = node.attrib['Mes']
    self['Anio'] = Xint(node.attrib['Anio'])
    if (a := node.attrib.get('Sello')) is not None:
        self['Sello'] = a
    if (a := node.attrib.get('noCertificado')) is not None:
        self['NoCertificado'] = a
    if (a := node.attrib.get('Certificado')) is not None:
        self['Certificado'] = a
    return self
def ctas3(cls, node):
    self = ScalarMap()
    self['CodAgrup'] = catalog_code('Cb9f_c_CodAgrup', node.attrib['CodAgrup'])
    self['NumCta'] = node.attrib['NumCta']
    self['Desc'] = node.attrib['Desc']
    if (a := node.attrib.get('SubCtaDe')) is not None:
        self['SubCtaDe'] = a
    self['Nivel'] = Xint(node.attrib['Nivel'])
    self['Natur'] = node.attrib['Natur']
    return self
def polizas1(cls, node):
    self = cls()
    self.tag = node.tag
    self['Poliza'] = [poliza1(cls, n) for n in node.iterfind('{http://www.sat.gob.mx/esquemas/ContabilidadE/1_3/PolizasPeriodo}Poliza')]
    self['Version'] = node.attrib['Version']
    self['RFC'] = node.attrib['RFC']
    self['Mes'] = node.attrib['Mes']
    self['Anio'] = Xint(node.attrib['Anio'])
    self['TipoSolicitud'] = node.attrib['TipoSolicitud']
    if (a := node.attrib.get('NumOrden')) is not None:
        self['NumOrden'] = a
    if (a := node.attrib.get('NumTramite')) is not None:
        self['NumTramite'] = a
    if (a := node.attrib.get('Sello')) is not None:
        self['Sello'] = a
    if (a := node.attrib.get('noCertificado')) is not None:
        self['NoCertificado'] = a
    if (a := node.attrib.get('Certificado')) is not None:
        self['Certificado'] = a
    return self
def poliza1(cls, node):
    self = ScalarMap()
    self['Transaccion'] = [transaccion1(cls, n) for n in node.iterfind('{http://www.sat.gob.mx/esquemas/ContabilidadE/1_3/PolizasPeriodo}Transaccion')]
    self['NumUnIdenPol'] = node.attrib['NumUnIdenPol']
    self['Fecha'] = date.fromisoformat(node.attrib['Fecha'])
    self['Concepto'] = node.attrib['Concepto']
    return self
def transaccion1(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.sat.gob.mx/esquemas/ContabilidadE/1_3/PolizasPeriodo}CompNal')
    if el is not None:
        self['CompNal'] = [comp_nal1(cls, n) for n in node.iterfind('{http://www.sat.gob.mx/esquemas/ContabilidadE/1_3/PolizasPeriodo}CompNal')]
    el = node.find('{http://www.sat.gob.mx/esquemas/ContabilidadE/1_3/PolizasPeriodo}CompNalOtr')
    if el is not None:
        self['CompNalOtr'] = [comp_nal_otr1(cls, n) for n in node.iterfind('{http://www.sat.gob.mx/esquemas/ContabilidadE/1_3/PolizasPeriodo}CompNalOtr')]
    el = node.find('{http://www.sat.gob.mx/esquemas/ContabilidadE/1_3/PolizasPeriodo}CompExt')
    if el is not None:
        self['CompExt'] = [comp_ext1(cls, n) for n in node.iterfind('{http://www.sat.gob.mx/esquemas/ContabilidadE/1_3/PolizasPeriodo}CompExt')]
    el = node.find('{http://www.sat.gob.mx/esquemas/ContabilidadE/1_3/PolizasPeriodo}Cheque')
    if el is not None:
        self['Cheque'] = [cheque1(cls, n) for n in node.iterfind('{http://www.sat.gob.mx/esquemas/ContabilidadE/1_3/PolizasPeriodo}Cheque')]
    el = node.find('{http://www.sat.gob.mx/esquemas/ContabilidadE/1_3/PolizasPeriodo}Transferencia')
    if el is not None:
        self['Transferencia'] = [transferencia1(cls, n) for n in node.iterfind('{http://www.sat.gob.mx/esquemas/ContabilidadE/1_3/PolizasPeriodo}Transferencia')]
    el = node.find('{http://www.sat.gob.mx/esquemas/ContabilidadE/1_3/PolizasPeriodo}OtrMetodoPago')
    if el is not None:
        self['OtrMetodoPago'] = [otr_metodo_pago1(cls, n) for n in node.iterfind('{http://www.sat.gob.mx/esquemas/ContabilidadE/1_3/PolizasPeriodo}OtrMetodoPago')]
    self['NumCta'] = node.attrib['NumCta']
    self['DesCta'] = node.attrib['DesCta']
    self['Concepto'] = node.attrib['Concepto']
    self['Debe'] = Decimal(node.attrib['Debe'])
    self['Haber'] = Decimal(node.attrib['Haber'])
    return self
def comp_nal1(cls, node):
    self = ScalarMap()
    self['UUID_CFDI'] = node.attrib['UUID_CFDI']
    self['RFC'] = node.attrib['RFC']
    self['MontoTotal'] = Decimal(node.attrib['MontoTotal'])
    if (a := node.attrib.get('Moneda')) is not None:
        self['Moneda'] = catalog_code('C756_c_Moneda', a, 0)
    if (a := node.attrib.get('TipCamb')) is not None:
        self['TipCamb'] = Decimal(a)
    return self
def comp_nal_otr1(cls, node):
    self = ScalarMap()
    if (a := node.attrib.get('CFD_CBB_Serie')) is not None:
        self['CFD_CBB_Serie'] = a
    self['CFD_CBB_NumFol'] = Xint(node.attrib['CFD_CBB_NumFol'])
    self['RFC'] = node.attrib['RFC']
    self['MontoTotal'] = Decimal(node.attrib['MontoTotal'])
    if (a := node.attrib.get('Moneda')) is not None:
        self['Moneda'] = catalog_code('C756_c_Moneda', a, 0)
    if (a := node.attrib.get('TipCamb')) is not None:
        self['TipCamb'] = Decimal(a)
    return self
def comp_ext1(cls, node):
    self = ScalarMap()
    self['NumFactExt'] = node.attrib['NumFactExt']
    if (a := node.attrib.get('TaxID')) is not None:
        self['TaxID'] = a
    self['MontoTotal'] = Decimal(node.attrib['MontoTotal'])
    if (a := node.attrib.get('Moneda')) is not None:
        self['Moneda'] = catalog_code('C756_c_Moneda', a, 0)
    if (a := node.attrib.get('TipCamb')) is not None:
        self['TipCamb'] = Decimal(a)
    return self
def cheque1(cls, node):
    self = ScalarMap()
    self['Num'] = node.attrib['Num']
    self['BanEmisNal'] = catalog_code('C75b_c_Banco', node.attrib['BanEmisNal'])
    if (a := node.attrib.get('BanEmisExt')) is not None:
        self['BanEmisExt'] = a
    self['CtaOri'] = node.attrib['CtaOri']
    self['Fecha'] = date.fromisoformat(node.attrib['Fecha'])
    self['Benef'] = node.attrib['Benef']
    self['RFC'] = node.attrib['RFC']
    self['Monto'] = Decimal(node.attrib['Monto'])
    if (a := node.attrib.get('Moneda')) is not None:
        self['Moneda'] = catalog_code('C756_c_Moneda', a, 0)
    if (a := node.attrib.get('TipCamb')) is not None:
        self['TipCamb'] = Decimal(a)
    return self
def transferencia1(cls, node):
    self = ScalarMap()
    if (a := node.attrib.get('CtaOri')) is not None:
        self['CtaOri'] = a
    self['BancoOriNal'] = catalog_code('C75b_c_Banco', node.attrib['BancoOriNal'])
    if (a := node.attrib.get('BancoOriExt')) is not None:
        self['BancoOriExt'] = a
    self['CtaDest'] = node.attrib['CtaDest']
    self['BancoDestNal'] = catalog_code('C75b_c_Banco', node.attrib['BancoDestNal'])
    if (a := node.attrib.get('BancoDestExt')) is not None:
        self['BancoDestExt'] = a
    self['Fecha'] = date.fromisoformat(node.attrib['Fecha'])
    self['Benef'] = node.attrib['Benef']
    self['RFC'] = node.attrib['RFC']
    self['Monto'] = Decimal(node.attrib['Monto'])
    if (a := node.attrib.get('Moneda')) is not None:
        self['Moneda'] = catalog_code('C756_c_Moneda', a, 0)
    if (a := node.attrib.get('TipCamb')) is not None:
        self['TipCamb'] = Decimal(a)
    return self
def otr_metodo_pago1(cls, node):
    self = ScalarMap()
    self['MetPagoPol'] = catalog_code('C756_c_FormaPago', node.attrib['MetPagoPol'])
    self['Fecha'] = date.fromisoformat(node.attrib['Fecha'])
    self['Benef'] = node.attrib['Benef']
    self['RFC'] = node.attrib['RFC']
    self['Monto'] = Decimal(node.attrib['Monto'])
    if (a := node.attrib.get('Moneda')) is not None:
        self['Moneda'] = catalog_code('C756_c_Moneda', a, 0)
    if (a := node.attrib.get('TipCamb')) is not None:
        self['TipCamb'] = Decimal(a)
    return self
def sello_digital_cont_elec0(cls, node):
    self = cls()
    self.tag = node.tag
    self['Version'] = node.attrib['Version']
    self['Folio'] = node.attrib['Folio']
    self['RFC'] = node.attrib['RFC']
    self['FechadeSello'] = datetime.fromisoformat(node.attrib['FechadeSello'])
    if (a := node.attrib.get('sello')) is not None:
        self['Sello'] = a
    self['NoCertificadoSAT'] = node.attrib['noCertificadoSAT']
    self['SelloSAT'] = node.attrib['selloSAT']
    return self
def servicios_plataformas_tecnologicas0(cls, node):
    self = cls()
    self.tag = node.tag
    el = node.find('{http://www.sat.gob.mx/esquemas/retencionpago/1/PlataformasTecnologicas10}Servicios')
    self['Servicios'] = [detalles_del_servicio0(cls, n) for n in el.iterfind('{http://www.sat.gob.mx/esquemas/retencionpago/1/PlataformasTecnologicas10}DetallesDelServicio')]
    self['Version'] = node.attrib['Version']
    self['Periodicidad'] = catalog_code('Ccb0_c_Periodicidad', node.attrib['Periodicidad'])
    self['NumServ'] = Xint(node.attrib['NumServ'])
    self['MonTotServSIVA'] = Decimal(node.attrib['MonTotServSIVA'])
    self['TotalIVATrasladado'] = Decimal(node.attrib['TotalIVATrasladado'])
    self['TotalIVARetenido'] = Decimal(node.attrib['TotalIVARetenido'])
    self['TotalISRRetenido'] = Decimal(node.attrib['TotalISRRetenido'])
    self['DifIVAEntregadoPrestServ'] = Decimal(node.attrib['DifIVAEntregadoPrestServ'])
    self['MonTotalporUsoPlataforma'] = Decimal(node.attrib['MonTotalporUsoPlataforma'])
    if (a := node.attrib.get('MonTotalContribucionGubernamental')) is not None:
        self['MonTotalContribucionGubernamental'] = Decimal(a)
    return self
def detalles_del_servicio0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.sat.gob.mx/esquemas/retencionpago/1/PlataformasTecnologicas10}ImpuestosTrasladadosdelServicio')
    if el is not None:
        self['ImpuestosTrasladadosdelServicio'] = impuestos_trasladadosdel_servicio0(cls, el)
    el = node.find('{http://www.sat.gob.mx/esquemas/retencionpago/1/PlataformasTecnologicas10}ContribucionGubernamental')
    if el is not None:
        self['ContribucionGubernamental'] = contribucion_gubernamental0(cls, el)
    el = node.find('{http://www.sat.gob.mx/esquemas/retencionpago/1/PlataformasTecnologicas10}ComisionDelServicio')
    if el is not None:
        self['ComisionDelServicio'] = comision_del_servicio0(cls, el)
    self['FormaPagoServ'] = catalog_code('Cfc6_c_FormaPagoServ', node.attrib['FormaPagoServ'])
    self['TipoDeServ'] = catalog_code('Cfc6_c_TipoDeServ', node.attrib['TipoDeServ'])
    if (a := node.attrib.get('SubTipServ')) is not None:
        self['SubTipServ'] = catalog_code('Cfc6_c_SubTipoServ', a)
    if (a := node.attrib.get('RFCTerceroAutorizado')) is not None:
        self['RFCTerceroAutorizado'] = a
    self['FechaServ'] = date.fromisoformat(node.attrib['FechaServ'])
    self['PrecioServSinIVA'] = Decimal(node.attrib['PrecioServSinIVA'])
    return self
def impuestos_trasladadosdel_servicio0(cls, node):
    self = ScalarMap()
    self['Base'] = Decimal(node.attrib['Base'])
    self['Impuesto'] = catalog_code('Ccb0_c_TipoImpuesto', node.attrib['Impuesto'])
    self['TipoFactor'] = node.attrib['TipoFactor']
    self['TasaCuota'] = Decimal(node.attrib['TasaCuota'])
    self['Importe'] = Decimal(node.attrib['Importe'])
    return self
def contribucion_gubernamental0(cls, node):
    self = ScalarMap()
    self['ImpContrib'] = Decimal(node.attrib['ImpContrib'])
    self['EntidadDondePagaLaContribucion'] = catalog_code('Ccb0_c_EntidadesFederativas', node.attrib['EntidadDondePagaLaContribucion'])
    return self
def comision_del_servicio0(cls, node):
    self = ScalarMap()
    if (a := node.attrib.get('Base')) is not None:
        self['Base'] = Decimal(a)
    if (a := node.attrib.get('Porcentaje')) is not None:
        self['Porcentaje'] = Decimal(a)
    self['Importe'] = Decimal(node.attrib['Importe'])
    return self
def arrendamientoenfideicomiso0(cls, node):
    self = cls()
    self.tag = node.tag
    self['Version'] = node.attrib['Version']
    self['PagProvEfecPorFiduc'] = Decimal(node.attrib['PagProvEfecPorFiduc'])
    self['RendimFideicom'] = Decimal(node.attrib['RendimFideicom'])
    self['DeduccCorresp'] = Decimal(node.attrib['DeduccCorresp'])
    if (a := node.attrib.get('MontTotRet')) is not None:
        self['MontTotRet'] = Decimal(a)
    if (a := node.attrib.get('MontResFiscDistFibras')) is not None:
        self['MontResFiscDistFibras'] = Decimal(a)
    if (a := node.attrib.get('MontOtrosConceptDistr')) is not None:
        self['MontOtrosConceptDistr'] = Decimal(a)
    if (a := node.attrib.get('DescrMontOtrosConceptDistr')) is not None:
        self['DescrMontOtrosConceptDistr'] = a
    return self
def dividendos0(cls, node):
    self = cls()
    self.tag = node.tag
    el = node.find('{http://www.sat.gob.mx/esquemas/retencionpago/1/dividendos}DividOUtil')
    if el is not None:
        self['DividOUtil'] = divid_o_util0(cls, el)
    el = node.find('{http://www.sat.gob.mx/esquemas/retencionpago/1/dividendos}Remanente')
    if el is not None:
        self['Remanente'] = remanente0(cls, el)
    self['Version'] = node.attrib['Version']
    return self
def divid_o_util0(cls, node):
    self = ScalarMap()
    self['CveTipDivOUtil'] = catalog_code('Ccb0_c_TipoDividendoOUtilidadDistribuida', node.attrib['CveTipDivOUtil'])
    self['MontISRAcredRetMexico'] = Decimal(node.attrib['MontISRAcredRetMexico'])
    self['MontISRAcredRetExtranjero'] = Decimal(node.attrib['MontISRAcredRetExtranjero'])
    if (a := node.attrib.get('MontRetExtDivExt')) is not None:
        self['MontRetExtDivExt'] = Decimal(a)
    self['TipoSocDistrDiv'] = node.attrib['TipoSocDistrDiv']
    if (a := node.attrib.get('MontISRAcredNal')) is not None:
        self['MontISRAcredNal'] = Decimal(a)
    if (a := node.attrib.get('MontDivAcumNal')) is not None:
        self['MontDivAcumNal'] = Decimal(a)
    if (a := node.attrib.get('MontDivAcumExt')) is not None:
        self['MontDivAcumExt'] = Decimal(a)
    return self
def remanente0(cls, node):
    self = ScalarMap()
    if (a := node.attrib.get('ProporcionRem')) is not None:
        self['ProporcionRem'] = Decimal(a)
    return self
def enajenacionde_acciones0(cls, node):
    self = cls()
    self.tag = node.tag
    self['Version'] = node.attrib['Version']
    self['ContratoIntermediacion'] = node.attrib['ContratoIntermediacion']
    self['Ganancia'] = Decimal(node.attrib['Ganancia'])
    self['Perdida'] = Decimal(node.attrib['Perdida'])
    return self
def fideicomisonoempresarial0(cls, node):
    self = cls()
    self.tag = node.tag
    el = node.find('{http://www.sat.gob.mx/esquemas/retencionpago/1/fideicomisonoempresarial}IngresosOEntradas')
    self['IngresosOEntradas'] = ingresos_oentradas0(cls, el)
    el = node.find('{http://www.sat.gob.mx/esquemas/retencionpago/1/fideicomisonoempresarial}DeduccOSalidas')
    self['DeduccOSalidas'] = deducc_osalidas0(cls, el)
    el = node.find('{http://www.sat.gob.mx/esquemas/retencionpago/1/fideicomisonoempresarial}RetEfectFideicomiso')
    self['RetEfectFideicomiso'] = ret_efect_fideicomiso0(cls, el)
    self['Version'] = node.attrib['Version']
    return self
def ingresos_oentradas0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.sat.gob.mx/esquemas/retencionpago/1/fideicomisonoempresarial}IntegracIngresos')
    self['IntegracIngresos'] = integrac_ingresos0(cls, el)
    self['MontTotEntradasPeriodo'] = Decimal(node.attrib['MontTotEntradasPeriodo'])
    self['PartPropAcumDelFideicom'] = Decimal(node.attrib['PartPropAcumDelFideicom'])
    self['PropDelMontTot'] = Decimal(node.attrib['PropDelMontTot'])
    return self
def integrac_ingresos0(cls, node):
    return node.attrib['Concepto']
def deducc_osalidas0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.sat.gob.mx/esquemas/retencionpago/1/fideicomisonoempresarial}IntegracEgresos')
    self['IntegracEgresos'] = integrac_egresos0(cls, el)
    self['MontTotEgresPeriodo'] = Decimal(node.attrib['MontTotEgresPeriodo'])
    self['PartPropDelFideicom'] = Decimal(node.attrib['PartPropDelFideicom'])
    self['PropDelMontTot'] = Decimal(node.attrib['PropDelMontTot'])
    return self
def integrac_egresos0(cls, node):
    return node.attrib['ConceptoS']
def ret_efect_fideicomiso0(cls, node):
    self = ScalarMap()
    self['MontRetRelPagFideic'] = Decimal(node.attrib['MontRetRelPagFideic'])
    self['DescRetRelPagFideic'] = node.attrib['DescRetRelPagFideic']
    return self
def intereses0(cls, node):
    self = cls()
    self.tag = node.tag
    self['Version'] = node.attrib['Version']
    self['SistFinanciero'] = node.attrib['SistFinanciero']
    self['RetiroAORESRetInt'] = node.attrib['RetiroAORESRetInt']
    self['OperFinancDerivad'] = node.attrib['OperFinancDerivad']
    self['MontIntNominal'] = Decimal(node.attrib['MontIntNominal'])
    self['MontIntReal'] = Decimal(node.attrib['MontIntReal'])
    self['Perdida'] = Decimal(node.attrib['Perdida'])
    return self
def intereseshipotecarios0(cls, node):
    self = cls()
    self.tag = node.tag
    self['Version'] = node.attrib['Version']
    self['CreditoDeInstFinanc'] = node.attrib['CreditoDeInstFinanc']
    self['SaldoInsoluto'] = Decimal(node.attrib['SaldoInsoluto'])
    if (a := node.attrib.get('PropDeducDelCredit')) is not None:
        self['PropDeducDelCredit'] = Decimal(a)
    if (a := node.attrib.get('MontTotIntNominalesDev')) is not None:
        self['MontTotIntNominalesDev'] = Decimal(a)
    if (a := node.attrib.get('MontTotIntNominalesDevYPag')) is not None:
        self['MontTotIntNominalesDevYPag'] = Decimal(a)
    if (a := node.attrib.get('MontTotIntRealPagDeduc')) is not None:
        self['MontTotIntRealPagDeduc'] = Decimal(a)
    if (a := node.attrib.get('NumContrato')) is not None:
        self['NumContrato'] = a
    return self
def operacionesconderivados0(cls, node):
    self = cls()
    self.tag = node.tag
    self['Version'] = node.attrib['Version']
    self['MontGanAcum'] = Decimal(node.attrib['MontGanAcum'])
    self['MontPerdDed'] = Decimal(node.attrib['MontPerdDed'])
    return self
def pagosaextranjeros0(cls, node):
    self = cls()
    self.tag = node.tag
    el = node.find('{http://www.sat.gob.mx/esquemas/retencionpago/1/pagosaextranjeros}NoBeneficiario')
    if el is not None:
        self['NoBeneficiario'] = no_beneficiario0(cls, el)
    el = node.find('{http://www.sat.gob.mx/esquemas/retencionpago/1/pagosaextranjeros}Beneficiario')
    if el is not None:
        self['Beneficiario'] = beneficiario1(cls, el)
    self['Version'] = node.attrib['Version']
    self['EsBenefEfectDelCobro'] = node.attrib['EsBenefEfectDelCobro']
    return self
def no_beneficiario0(cls, node):
    self = ScalarMap()
    self['PaisDeResidParaEfecFisc'] = catalog_code('Ccb0_c_Pais', node.attrib['PaisDeResidParaEfecFisc'])
    self['ConceptoPago'] = catalog_code('Ccb0_c_TipoContribuyenteSujetoRetencion', node.attrib['ConceptoPago'])
    self['DescripcionConcepto'] = node.attrib['DescripcionConcepto']
    return self
def beneficiario1(cls, node):
    self = ScalarMap()
    self['RFC'] = node.attrib['RFC']
    self['CURP'] = node.attrib['CURP']
    self['NomDenRazSocB'] = node.attrib['NomDenRazSocB']
    self['ConceptoPago'] = catalog_code('Ccb0_c_TipoContribuyenteSujetoRetencion', node.attrib['ConceptoPago'])
    self['DescripcionConcepto'] = node.attrib['DescripcionConcepto']
    return self
def planesderetiro0(cls, node):
    self = cls()
    self.tag = node.tag
    el = node.find('{http://www.sat.gob.mx/esquemas/retencionpago/1/planesderetiro11}AportacionesODepositos')
    if el is not None:
        self['AportacionesODepositos'] = [aportaciones_odepositos0(cls, n) for n in node.iterfind('{http://www.sat.gob.mx/esquemas/retencionpago/1/planesderetiro11}AportacionesODepositos')]
    self['Version'] = node.attrib['Version']
    self['SistemaFinanc'] = node.attrib['SistemaFinanc']
    if (a := node.attrib.get('MontTotAportAnioInmAnterior')) is not None:
        self['MontTotAportAnioInmAnterior'] = Decimal(a)
    self['MontIntRealesDevengAniooInmAnt'] = Decimal(node.attrib['MontIntRealesDevengAniooInmAnt'])
    self['HuboRetirosAnioInmAntPer'] = node.attrib['HuboRetirosAnioInmAntPer']
    if (a := node.attrib.get('MontTotRetiradoAnioInmAntPer')) is not None:
        self['MontTotRetiradoAnioInmAntPer'] = Decimal(a)
    if (a := node.attrib.get('MontTotExentRetiradoAnioInmAnt')) is not None:
        self['MontTotExentRetiradoAnioInmAnt'] = Decimal(a)
    if (a := node.attrib.get('MontTotExedenteAnioInmAnt')) is not None:
        self['MontTotExedenteAnioInmAnt'] = Decimal(a)
    self['HuboRetirosAnioInmAnt'] = node.attrib['HuboRetirosAnioInmAnt']
    if (a := node.attrib.get('MontTotRetiradoAnioInmAnt')) is not None:
        self['MontTotRetiradoAnioInmAnt'] = Decimal(a)
    if (a := node.attrib.get('NumReferencia')) is not None:
        self['NumReferencia'] = a
    return self
def aportaciones_odepositos0(cls, node):
    self = ScalarMap()
    self['TipoAportacionODeposito'] = catalog_code('Cb58_c_TipoAportODep', node.attrib['TipoAportacionODeposito'])
    self['MontAportODep'] = Decimal(node.attrib['MontAportODep'])
    if (a := node.attrib.get('RFCFiduciaria')) is not None:
        self['RFCFiduciaria'] = a
    return self
def planesderetiro1(cls, node):
    self = cls()
    self.tag = node.tag
    self['Version'] = node.attrib['Version']
    self['SistemaFinanc'] = node.attrib['SistemaFinanc']
    if (a := node.attrib.get('MontTotAportAnioInmAnterior')) is not None:
        self['MontTotAportAnioInmAnterior'] = Decimal(a)
    self['MontIntRealesDevengAniooInmAnt'] = Decimal(node.attrib['MontIntRealesDevengAniooInmAnt'])
    self['HuboRetirosAnioInmAntPer'] = node.attrib['HuboRetirosAnioInmAntPer']
    if (a := node.attrib.get('MontTotRetiradoAnioInmAntPer')) is not None:
        self['MontTotRetiradoAnioInmAntPer'] = Decimal(a)
    if (a := node.attrib.get('MontTotExentRetiradoAnioInmAnt')) is not None:
        self['MontTotExentRetiradoAnioInmAnt'] = Decimal(a)
    if (a := node.attrib.get('MontTotExedenteAnioInmAnt')) is not None:
        self['MontTotExedenteAnioInmAnt'] = Decimal(a)
    self['HuboRetirosAnioInmAnt'] = node.attrib['HuboRetirosAnioInmAnt']
    if (a := node.attrib.get('MontTotRetiradoAnioInmAnt')) is not None:
        self['MontTotRetiradoAnioInmAnt'] = Decimal(a)
    return self
def premios0(cls, node):
    self = cls()
    self.tag = node.tag
    self['Version'] = node.attrib['Version']
    self['EntidadFederativa'] = catalog_code('Ccb0_c_EntidadesFederativas', node.attrib['EntidadFederativa'])
    self['MontTotPago'] = Decimal(node.attrib['MontTotPago'])
    self['MontTotPagoGrav'] = Decimal(node.attrib['MontTotPagoGrav'])
    self['MontTotPagoExent'] = Decimal(node.attrib['MontTotPagoExent'])
    return self
def retenciones0(cls, node):
    self = cls()
    self.tag = node.tag
    el = node.find('{http://www.sat.gob.mx/esquemas/retencionpago/1}Emisor')
    self['Emisor'] = emisor1(cls, el)
    el = node.find('{http://www.sat.gob.mx/esquemas/retencionpago/1}Receptor')
    self['Receptor'] = receptor1(cls, el)
    el = node.find('{http://www.sat.gob.mx/esquemas/retencionpago/1}Periodo')
    self['Periodo'] = periodo0(cls, el)
    el = node.find('{http://www.sat.gob.mx/esquemas/retencionpago/1}Totales')
    self['Totales'] = totales0(cls, el)
    el = node.find('{http://www.sat.gob.mx/esquemas/retencionpago/1}Complemento')
    if el is not None:
        self['Complemento'] = complemento0(cls, el)
    el = node.find('{http://www.sat.gob.mx/esquemas/retencionpago/1}Addenda')
    if el is not None:
        self['Addenda'] = addenda0(cls, el)
    self['Version'] = node.attrib['Version']
    if (a := node.attrib.get('FolioInt')) is not None:
        self['FolioInt'] = a
    self['Sello'] = node.attrib['Sello']
    self['NumCert'] = node.attrib['NumCert']
    self['Cert'] = node.attrib['Cert']
    self['FechaExp'] = datetime.fromisoformat(node.attrib['FechaExp'])
    self['CveRetenc'] = catalog_code('Ccb0_c_Retenciones', node.attrib['CveRetenc'])
    if (a := node.attrib.get('DescRetenc')) is not None:
        self['DescRetenc'] = a
    return self
def emisor1(cls, node):
    self = ScalarMap()
    self['RFCEmisor'] = node.attrib['RFCEmisor']
    if (a := node.attrib.get('NomDenRazSocE')) is not None:
        self['NomDenRazSocE'] = a
    if (a := node.attrib.get('CURPE')) is not None:
        self['CURPE'] = a
    return self
def receptor1(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.sat.gob.mx/esquemas/retencionpago/1}Nacional')
    if el is not None:
        self['Nacional'] = nacional14(cls, el)
    el = node.find('{http://www.sat.gob.mx/esquemas/retencionpago/1}Extranjero')
    if el is not None:
        self['Extranjero'] = extranjero14(cls, el)
    self['Nacionalidad'] = node.attrib['Nacionalidad']
    return self
def nacional14(cls, node):
    self = ScalarMap()
    self['RFCRecep'] = node.attrib['RFCRecep']
    if (a := node.attrib.get('NomDenRazSocR')) is not None:
        self['NomDenRazSocR'] = a
    if (a := node.attrib.get('CURPR')) is not None:
        self['CURPR'] = a
    return self
def extranjero14(cls, node):
    self = ScalarMap()
    if (a := node.attrib.get('NumRegIdTrib')) is not None:
        self['NumRegIdTrib'] = a
    self['NomDenRazSocR'] = node.attrib['NomDenRazSocR']
    return self
def periodo0(cls, node):
    self = ScalarMap()
    self['MesIni'] = Xint(node.attrib['MesIni'])
    self['MesFin'] = Xint(node.attrib['MesFin'])
    self['Ejerc'] = Xint(node.attrib['Ejerc'])
    return self
def totales0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.sat.gob.mx/esquemas/retencionpago/1}ImpRetenidos')
    if el is not None:
        self['ImpRetenidos'] = [imp_retenidos0(cls, n) for n in node.iterfind('{http://www.sat.gob.mx/esquemas/retencionpago/1}ImpRetenidos')]
    self['MontoTotOperacion'] = Decimal(node.attrib['montoTotOperacion'])
    self['MontoTotGrav'] = Decimal(node.attrib['montoTotGrav'])
    self['MontoTotExent'] = Decimal(node.attrib['montoTotExent'])
    self['MontoTotRet'] = Decimal(node.attrib['montoTotRet'])
    return self
def imp_retenidos0(cls, node):
    self = ScalarMap()
    if (a := node.attrib.get('BaseRet')) is not None:
        self['BaseRet'] = Decimal(a)
    if (a := node.attrib.get('Impuesto')) is not None:
        self['Impuesto'] = catalog_code('Ccb0_c_TipoImpuesto', a)
    self['MontoRet'] = Decimal(node.attrib['montoRet'])
    self['TipoPagoRet'] = node.attrib['TipoPagoRet']
    return self
def complemento0(cls, node):
    self = {n.tag.rsplit('}', 1)[-1]: cfdi_objectify.get(n.tag, default_objectify)(cls, n) for n in node}
    return self
def addenda0(cls, node):
    self = {n.tag.rsplit('}', 1)[-1]: cfdi_objectify.get(n.tag, default_objectify)(cls, n) for n in node}
    return self
def sector_financiero0(cls, node):
    self = cls()
    self.tag = node.tag
    self['Version'] = node.attrib['Version']
    self['IdFideicom'] = node.attrib['IdFideicom']
    if (a := node.attrib.get('NomFideicom')) is not None:
        self['NomFideicom'] = a
    self['DescripFideicom'] = node.attrib['DescripFideicom']
    return self
def retenciones1(cls, node):
    self = cls()
    self.tag = node.tag
    el = node.find('{http://www.sat.gob.mx/esquemas/retencionpago/2}CfdiRetenRelacionados')
    if el is not None:
        self['CfdiRetenRelacionados'] = cfdi_reten_relacionados0(cls, el)
    el = node.find('{http://www.sat.gob.mx/esquemas/retencionpago/2}Emisor')
    self['Emisor'] = emisor2(cls, el)
    el = node.find('{http://www.sat.gob.mx/esquemas/retencionpago/2}Receptor')
    self['Receptor'] = receptor2(cls, el)
    el = node.find('{http://www.sat.gob.mx/esquemas/retencionpago/2}Periodo')
    self['Periodo'] = periodo1(cls, el)
    el = node.find('{http://www.sat.gob.mx/esquemas/retencionpago/2}Totales')
    self['Totales'] = totales1(cls, el)
    el = node.find('{http://www.sat.gob.mx/esquemas/retencionpago/2}Complemento')
    if el is not None:
        self['Complemento'] = complemento1(cls, el)
    el = node.find('{http://www.sat.gob.mx/esquemas/retencionpago/2}Addenda')
    if el is not None:
        self['Addenda'] = addenda1(cls, el)
    self['Version'] = node.attrib['Version']
    if (a := node.attrib.get('FolioInt')) is not None:
        self['FolioInt'] = a
    self['Sello'] = node.attrib['Sello']
    self['NoCertificado'] = node.attrib['NoCertificado']
    self['Certificado'] = node.attrib['Certificado']
    self['FechaExp'] = datetime.fromisoformat(node.attrib['FechaExp'])
    self['LugarExpRetenc'] = node.attrib['LugarExpRetenc']
    self['CveRetenc'] = catalog_code('Ccb0_c_CveRetenc', node.attrib['CveRetenc'])
    if (a := node.attrib.get('DescRetenc')) is not None:
        self['DescRetenc'] = a
    return self
def cfdi_reten_relacionados0(cls, node):
    self = ScalarMap()
    self['TipoRelacion'] = catalog_code('C756_c_TipoRelacion', node.attrib['TipoRelacion'])
    self['UUID'] = node.attrib['UUID']
    return self
def emisor2(cls, node):
    self = ScalarMap()
    self['RfcE'] = node.attrib['RfcE']
    self['NomDenRazSocE'] = node.attrib['NomDenRazSocE']
    self['RegimenFiscalE'] = catalog_code('C756_c_RegimenFiscal', node.attrib['RegimenFiscalE'])
    return self
def receptor2(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.sat.gob.mx/esquemas/retencionpago/2}Nacional')
    if el is not None:
        self['Nacional'] = nacional15(cls, el)
    el = node.find('{http://www.sat.gob.mx/esquemas/retencionpago/2}Extranjero')
    if el is not None:
        self['Extranjero'] = extranjero15(cls, el)
    self['NacionalidadR'] = node.attrib['NacionalidadR']
    return self
def nacional15(cls, node):
    self = ScalarMap()
    self['RfcR'] = node.attrib['RfcR']
    self['NomDenRazSocR'] = node.attrib['NomDenRazSocR']
    if (a := node.attrib.get('CurpR')) is not None:
        self['CurpR'] = a
    self['DomicilioFiscalR'] = node.attrib['DomicilioFiscalR']
    return self
def extranjero15(cls, node):
    self = ScalarMap()
    if (a := node.attrib.get('NumRegIdTribR')) is not None:
        self['NumRegIdTribR'] = a
    self['NomDenRazSocR'] = node.attrib['NomDenRazSocR']
    return self
def periodo1(cls, node):
    self = ScalarMap()
    self['MesIni'] = catalog_code('Ccb0_c_Periodo', node.attrib['MesIni'])
    self['MesFin'] = catalog_code('Ccb0_c_Periodo', node.attrib['MesFin'])
    self['Ejercicio'] = node.attrib['Ejercicio']
    return self
def totales1(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.sat.gob.mx/esquemas/retencionpago/2}ImpRetenidos')
    if el is not None:
        self['ImpRetenidos'] = [imp_retenidos1(cls, n) for n in node.iterfind('{http://www.sat.gob.mx/esquemas/retencionpago/2}ImpRetenidos')]
    self['MontoTotOperacion'] = Decimal(node.attrib['MontoTotOperacion'])
    self['MontoTotGrav'] = Decimal(node.attrib['MontoTotGrav'])
    self['MontoTotExent'] = Decimal(node.attrib['MontoTotExent'])
    self['MontoTotRet'] = Decimal(node.attrib['MontoTotRet'])
    if (a := node.attrib.get('UtilidadBimestral')) is not None:
        self['UtilidadBimestral'] = Decimal(a)
    if (a := node.attrib.get('ISRCorrespondiente')) is not None:
        self['ISRCorrespondiente'] = Decimal(a)
    return self
def imp_retenidos1(cls, node):
    self = ScalarMap()
    if (a := node.attrib.get('BaseRet')) is not None:
        self['BaseRet'] = Decimal(a)
    if (a := node.attrib.get('ImpuestoRet')) is not None:
        self['ImpuestoRet'] = catalog_code('C756_c_Impuesto', a)
    self['MontoRet'] = Decimal(node.attrib['MontoRet'])
    self['TipoPagoRet'] = catalog_code('Ccb0_c_TipoPagoRet', node.attrib['TipoPagoRet'])
    return self
def complemento1(cls, node):
    self = {n.tag.rsplit('}', 1)[-1]: cfdi_objectify.get(n.tag, default_objectify)(cls, n) for n in node}
    return self
def addenda1(cls, node):
    self = {n.tag.rsplit('}', 1)[-1]: cfdi_objectify.get(n.tag, default_objectify)(cls, n) for n in node}
    return self
def comprobante0(cls, node):
    self = cls()
    self.tag = node.tag
    el = node.find('{http://www.sat.gob.mx/cfd/3}Emisor')
    self['Emisor'] = emisor3(cls, el)
    el = node.find('{http://www.sat.gob.mx/cfd/3}Receptor')
    self['Receptor'] = receptor3(cls, el)
    el = node.find('{http://www.sat.gob.mx/cfd/3}Conceptos')
    self['Conceptos'] = [concepto1(cls, n) for n in el.iterfind('{http://www.sat.gob.mx/cfd/3}Concepto')]
    el = node.find('{http://www.sat.gob.mx/cfd/3}Impuestos')
    self['Impuestos'] = impuestos0(cls, el)
    el = node.find('{http://www.sat.gob.mx/cfd/3}Complemento')
    if el is not None:
        self['Complemento'] = complemento2(cls, el)
    el = node.find('{http://www.sat.gob.mx/cfd/3}Addenda')
    if el is not None:
        self['Addenda'] = addenda2(cls, el)
    self['Version'] = node.attrib['version']
    if (a := node.attrib.get('serie')) is not None:
        self['Serie'] = a
    if (a := node.attrib.get('folio')) is not None:
        self['Folio'] = a
    self['Fecha'] = datetime.fromisoformat(node.attrib['fecha'])
    self['Sello'] = node.attrib['sello']
    self['FormaDePago'] = node.attrib['formaDePago']
    self['NoCertificado'] = node.attrib['noCertificado']
    self['Certificado'] = node.attrib['certificado']
    if (a := node.attrib.get('condicionesDePago')) is not None:
        self['CondicionesDePago'] = a
    self['SubTotal'] = Decimal(node.attrib['subTotal'])
    if (a := node.attrib.get('descuento')) is not None:
        self['Descuento'] = Decimal(a)
    if (a := node.attrib.get('motivoDescuento')) is not None:
        self['MotivoDescuento'] = a
    if (a := node.attrib.get('TipoCambio')) is not None:
        self['TipoCambio'] = a
    if (a := node.attrib.get('Moneda')) is not None:
        self['Moneda'] = a
    self['Total'] = Decimal(node.attrib['total'])
    self['TipoDeComprobante'] = node.attrib['tipoDeComprobante']
    self['MetodoDePago'] = node.attrib['metodoDePago']
    self['LugarExpedicion'] = node.attrib['LugarExpedicion']
    if (a := node.attrib.get('NumCtaPago')) is not None:
        self['NumCtaPago'] = a
    if (a := node.attrib.get('FolioFiscalOrig')) is not None:
        self['FolioFiscalOrig'] = a
    if (a := node.attrib.get('SerieFolioFiscalOrig')) is not None:
        self['SerieFolioFiscalOrig'] = a
    if (a := node.attrib.get('FechaFolioFiscalOrig')) is not None:
        self['FechaFolioFiscalOrig'] = datetime.fromisoformat(a)
    if (a := node.attrib.get('MontoFolioFiscalOrig')) is not None:
        self['MontoFolioFiscalOrig'] = Decimal(a)
    return self
def emisor3(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.sat.gob.mx/cfd/3}DomicilioFiscal')
    if el is not None:
        self['DomicilioFiscal'] = t_ubicacion_fiscal0(cls, el)
    el = node.find('{http://www.sat.gob.mx/cfd/3}ExpedidoEn')
    if el is not None:
        self['ExpedidoEn'] = t_ubicacion0(cls, el)
    self['RegimenFiscal'] = [regimen_fiscal0(cls, n) for n in node.iterfind('{http://www.sat.gob.mx/cfd/3}RegimenFiscal')]
    self['Rfc'] = node.attrib['rfc']
    if (a := node.attrib.get('nombre')) is not None:
        self['Nombre'] = a
    return self
def regimen_fiscal0(cls, node):
    return node.attrib['Regimen']
def receptor3(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.sat.gob.mx/cfd/3}Domicilio')
    if el is not None:
        self['Domicilio'] = t_ubicacion0(cls, el)
    self['Rfc'] = node.attrib['rfc']
    if (a := node.attrib.get('nombre')) is not None:
        self['Nombre'] = a
    return self
def concepto1(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.sat.gob.mx/cfd/3}InformacionAduanera')
    if el is not None:
        self['InformacionAduanera'] = [t_informacion_aduanera0(cls, n) for n in node.iterfind('{http://www.sat.gob.mx/cfd/3}InformacionAduanera')]
    el = node.find('{http://www.sat.gob.mx/cfd/3}CuentaPredial')
    if el is not None:
        self['CuentaPredial'] = cuenta_predial0(cls, el)
    el = node.find('{http://www.sat.gob.mx/cfd/3}ComplementoConcepto')
    if el is not None:
        self['ComplementoConcepto'] = complemento_concepto0(cls, el)
    el = node.find('{http://www.sat.gob.mx/cfd/3}Parte')
    if el is not None:
        self['Parte'] = [parte0(cls, n) for n in node.iterfind('{http://www.sat.gob.mx/cfd/3}Parte')]
    self['Cantidad'] = Decimal(node.attrib['cantidad'])
    self['Unidad'] = node.attrib['unidad']
    if (a := node.attrib.get('noIdentificacion')) is not None:
        self['NoIdentificacion'] = a
    self['Descripcion'] = node.attrib['descripcion']
    self['ValorUnitario'] = Decimal(node.attrib['valorUnitario'])
    self['Importe'] = Decimal(node.attrib['importe'])
    return self
def cuenta_predial0(cls, node):
    return node.attrib['numero']
def complemento_concepto0(cls, node):
    self = {n.tag.rsplit('}', 1)[-1]: cfdi_objectify.get(n.tag, default_objectify)(cls, n) for n in node}
    return self
def parte0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.sat.gob.mx/cfd/3}InformacionAduanera')
    if el is not None:
        self['InformacionAduanera'] = [t_informacion_aduanera0(cls, n) for n in node.iterfind('{http://www.sat.gob.mx/cfd/3}InformacionAduanera')]
    self['Cantidad'] = Decimal(node.attrib['cantidad'])
    if (a := node.attrib.get('unidad')) is not None:
        self['Unidad'] = a
    if (a := node.attrib.get('noIdentificacion')) is not None:
        self['NoIdentificacion'] = a
    self['Descripcion'] = node.attrib['descripcion']
    if (a := node.attrib.get('valorUnitario')) is not None:
        self['ValorUnitario'] = Decimal(a)
    if (a := node.attrib.get('importe')) is not None:
        self['Importe'] = Decimal(a)
    return self
def impuestos0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.sat.gob.mx/cfd/3}Retenciones')
    if el is not None:
        self['Retenciones'] = [retencion0(cls, n) for n in el.iterfind('{http://www.sat.gob.mx/cfd/3}Retencion')]
    el = node.find('{http://www.sat.gob.mx/cfd/3}Traslados')
    if el is not None:
        self['Traslados'] = [traslado0(cls, n) for n in el.iterfind('{http://www.sat.gob.mx/cfd/3}Traslado')]
    if (a := node.attrib.get('totalImpuestosRetenidos')) is not None:
        self['TotalImpuestosRetenidos'] = Decimal(a)
    if (a := node.attrib.get('totalImpuestosTrasladados')) is not None:
        self['TotalImpuestosTrasladados'] = Decimal(a)
    return self
def retencion0(cls, node):
    self = ScalarMap()
    self['Impuesto'] = node.attrib['impuesto']
    self['Importe'] = Decimal(node.attrib['importe'])
    return self
def traslado0(cls, node):
    self = ScalarMap()
    self['Impuesto'] = node.attrib['impuesto']
    self['Tasa'] = Decimal(node.attrib['tasa'])
    self['Importe'] = Decimal(node.attrib['importe'])
    return self
def complemento2(cls, node):
    self = {n.tag.rsplit('}', 1)[-1]: cfdi_objectify.get(n.tag, default_objectify)(cls, n) for n in node}
    return self
def addenda2(cls, node):
    self = {n.tag.rsplit('}', 1)[-1]: cfdi_objectify.get(n.tag, default_objectify)(cls, n) for n in node}
    return self
def comprobante1(cls, node):
    self = cls()
    self.tag = node.tag
    el = node.find('{http://www.sat.gob.mx/cfd/3}CfdiRelacionados')
    if el is not None:
        self['CfdiRelacionados'] = cfdi_relacionados0(cls, el)
    el = node.find('{http://www.sat.gob.mx/cfd/3}Emisor')
    self['Emisor'] = emisor4(cls, el)
    el = node.find('{http://www.sat.gob.mx/cfd/3}Receptor')
    self['Receptor'] = receptor4(cls, el)
    el = node.find('{http://www.sat.gob.mx/cfd/3}Conceptos')
    self['Conceptos'] = [concepto2(cls, n) for n in el.iterfind('{http://www.sat.gob.mx/cfd/3}Concepto')]
    el = node.find('{http://www.sat.gob.mx/cfd/3}Impuestos')
    if el is not None:
        self['Impuestos'] = impuestos2(cls, el)
    el = node.find('{http://www.sat.gob.mx/cfd/3}Complemento')
    if el is not None:
        self['Complemento'] = complemento3(cls, el)
    el = node.find('{http://www.sat.gob.mx/cfd/3}Addenda')
    if el is not None:
        self['Addenda'] = addenda3(cls, el)
    self['Version'] = node.attrib['Version']
    if (a := node.attrib.get('Serie')) is not None:
        self['Serie'] = a
    if (a := node.attrib.get('Folio')) is not None:
        self['Folio'] = a
    self['Fecha'] = datetime.fromisoformat(node.attrib['Fecha'])
    self['Sello'] = node.attrib['Sello']
    if (a := node.attrib.get('FormaPago')) is not None:
        self['FormaPago'] = catalog_code('C756_c_FormaPago', a)
    self['NoCertificado'] = node.attrib['NoCertificado']
    self['Certificado'] = node.attrib['Certificado']
    if (a := node.attrib.get('CondicionesDePago')) is not None:
        self['CondicionesDePago'] = a
    self['SubTotal'] = Decimal(node.attrib['SubTotal'])
    if (a := node.attrib.get('Descuento')) is not None:
        self['Descuento'] = Decimal(a)
    self['Moneda'] = catalog_code('C756_c_Moneda', node.attrib['Moneda'], 0)
    if (a := node.attrib.get('TipoCambio')) is not None:
        self['TipoCambio'] = Decimal(a)
    self['Total'] = Decimal(node.attrib['Total'])
    self['TipoDeComprobante'] = catalog_code('C756_c_TipoDeComprobante', node.attrib['TipoDeComprobante'])
    if (a := node.attrib.get('MetodoPago')) is not None:
        self['MetodoPago'] = catalog_code('C756_c_MetodoPago', a)
    self['LugarExpedicion'] = node.attrib['LugarExpedicion']
    if (a := node.attrib.get('Confirmacion')) is not None:
        self['Confirmacion'] = a
    return self
def cfdi_relacionados0(cls, node):
    self = ScalarMap()
    self['CfdiRelacionado'] = [cfdi_relacionado0(cls, n) for n in node.iterfind('{http://www.sat.gob.mx/cfd/3}CfdiRelacionado')]
    self['TipoRelacion'] = catalog_code('C756_c_TipoRelacion', node.attrib['TipoRelacion'])
    return self
def cfdi_relacionado0(cls, node):
    return node.attrib['UUID']
def emisor4(cls, node):
    self = ScalarMap()
    self['Rfc'] = node.attrib['Rfc']
    if (a := node.attrib.get('Nombre')) is not None:
        self['Nombre'] = a
    self['RegimenFiscal'] = catalog_code('C756_c_RegimenFiscal', node.attrib['RegimenFiscal'])
    return self
def receptor4(cls, node):
    self = ScalarMap()
    self['Rfc'] = node.attrib['Rfc']
    if (a := node.attrib.get('Nombre')) is not None:
        self['Nombre'] = a
    if (a := node.attrib.get('ResidenciaFiscal')) is not None:
        self['ResidenciaFiscal'] = catalog_code('C756_c_Pais', a)
    if (a := node.attrib.get('NumRegIdTrib')) is not None:
        self['NumRegIdTrib'] = a
    self['UsoCFDI'] = catalog_code('C756_c_UsoCFDI', node.attrib['UsoCFDI'])
    return self
def concepto2(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.sat.gob.mx/cfd/3}Impuestos')
    if el is not None:
        self['Impuestos'] = impuestos1(cls, el)
    el = node.find('{http://www.sat.gob.mx/cfd/3}InformacionAduanera')
    if el is not None:
        self['InformacionAduanera'] = [informacion_aduanera0(cls, n) for n in node.iterfind('{http://www.sat.gob.mx/cfd/3}InformacionAduanera')]
    el = node.find('{http://www.sat.gob.mx/cfd/3}CuentaPredial')
    if el is not None:
        self['CuentaPredial'] = cuenta_predial1(cls, el)
    el = node.find('{http://www.sat.gob.mx/cfd/3}ComplementoConcepto')
    if el is not None:
        self['ComplementoConcepto'] = complemento_concepto1(cls, el)
    el = node.find('{http://www.sat.gob.mx/cfd/3}Parte')
    if el is not None:
        self['Parte'] = [parte1(cls, n) for n in node.iterfind('{http://www.sat.gob.mx/cfd/3}Parte')]
    self['ClaveProdServ'] = catalog_code('C756_c_ClaveProdServ', node.attrib['ClaveProdServ'])
    if (a := node.attrib.get('NoIdentificacion')) is not None:
        self['NoIdentificacion'] = a
    self['Cantidad'] = Decimal(node.attrib['Cantidad'])
    self['ClaveUnidad'] = catalog_code('C756_c_ClaveUnidad', node.attrib['ClaveUnidad'])
    if (a := node.attrib.get('Unidad')) is not None:
        self['Unidad'] = a
    self['Descripcion'] = node.attrib['Descripcion']
    self['ValorUnitario'] = Decimal(node.attrib['ValorUnitario'])
    self['Importe'] = Decimal(node.attrib['Importe'])
    if (a := node.attrib.get('Descuento')) is not None:
        self['Descuento'] = Decimal(a)
    return self
def impuestos1(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.sat.gob.mx/cfd/3}Traslados')
    if el is not None:
        self['Traslados'] = {impuesto_index(n.attrib, 'Impuesto'): traslado1(cls, n) for n in el.iterfind('{http://www.sat.gob.mx/cfd/3}Traslado')}
    el = node.find('{http://www.sat.gob.mx/cfd/3}Retenciones')
    if el is not None:
        self['Retenciones'] = {impuesto_index(n.attrib, 'Impuesto'): retencion1(cls, n) for n in el.iterfind('{http://www.sat.gob.mx/cfd/3}Retencion')}
    return self
def traslado1(cls, node):
    self = ScalarMap()
    self['Base'] = Decimal(node.attrib['Base'])
    self['Impuesto'] = catalog_code('C756_c_Impuesto', node.attrib['Impuesto'])
    self['TipoFactor'] = catalog_code('C756_c_TipoFactor', node.attrib['TipoFactor'])
    if (a := node.attrib.get('TasaOCuota')) is not None:
        self['TasaOCuota'] = Decimal(a)
    if (a := node.attrib.get('Importe')) is not None:
        self['Importe'] = Decimal(a)
    return self
def retencion1(cls, node):
    self = ScalarMap()
    self['Base'] = Decimal(node.attrib['Base'])
    self['Impuesto'] = catalog_code('C756_c_Impuesto', node.attrib['Impuesto'])
    self['TipoFactor'] = catalog_code('C756_c_TipoFactor', node.attrib['TipoFactor'])
    self['TasaOCuota'] = Decimal(node.attrib['TasaOCuota'])
    self['Importe'] = Decimal(node.attrib['Importe'])
    return self
def informacion_aduanera0(cls, node):
    return node.attrib['NumeroPedimento']
def cuenta_predial1(cls, node):
    return node.attrib['Numero']
def complemento_concepto1(cls, node):
    self = {n.tag.rsplit('}', 1)[-1]: cfdi_objectify.get(n.tag, default_objectify)(cls, n) for n in node}
    return self
def parte1(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.sat.gob.mx/cfd/3}InformacionAduanera')
    if el is not None:
        self['InformacionAduanera'] = [informacion_aduanera1(cls, n) for n in node.iterfind('{http://www.sat.gob.mx/cfd/3}InformacionAduanera')]
    self['ClaveProdServ'] = catalog_code('C756_c_ClaveProdServ', node.attrib['ClaveProdServ'])
    if (a := node.attrib.get('NoIdentificacion')) is not None:
        self['NoIdentificacion'] = a
    self['Cantidad'] = Decimal(node.attrib['Cantidad'])
    if (a := node.attrib.get('Unidad')) is not None:
        self['Unidad'] = a
    self['Descripcion'] = node.attrib['Descripcion']
    if (a := node.attrib.get('ValorUnitario')) is not None:
        self['ValorUnitario'] = Decimal(a)
    if (a := node.attrib.get('Importe')) is not None:
        self['Importe'] = Decimal(a)
    return self
def informacion_aduanera1(cls, node):
    return node.attrib['NumeroPedimento']
def impuestos2(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.sat.gob.mx/cfd/3}Retenciones')
    if el is not None:
        self['Retenciones'] = {impuesto_index(n.attrib, 'Impuesto'): retencion2(cls, n) for n in el.iterfind('{http://www.sat.gob.mx/cfd/3}Retencion')}
    el = node.find('{http://www.sat.gob.mx/cfd/3}Traslados')
    if el is not None:
        self['Traslados'] = {impuesto_index(n.attrib, 'Impuesto'): traslado2(cls, n) for n in el.iterfind('{http://www.sat.gob.mx/cfd/3}Traslado')}
    if (a := node.attrib.get('TotalImpuestosRetenidos')) is not None:
        self['TotalImpuestosRetenidos'] = Decimal(a)
    if (a := node.attrib.get('TotalImpuestosTrasladados')) is not None:
        self['TotalImpuestosTrasladados'] = Decimal(a)
    return self
def retencion2(cls, node):
    self = ScalarMap()
    self['Impuesto'] = catalog_code('C756_c_Impuesto', node.attrib['Impuesto'])
    self['Importe'] = Decimal(node.attrib['Importe'])
    return self
def traslado2(cls, node):
    self = ScalarMap()
    self['Impuesto'] = catalog_code('C756_c_Impuesto', node.attrib['Impuesto'])
    self['TipoFactor'] = catalog_code('C756_c_TipoFactor', node.attrib['TipoFactor'])
    self['TasaOCuota'] = Decimal(node.attrib['TasaOCuota'])
    self['Importe'] = Decimal(node.attrib['Importe'])
    return self
def complemento3(cls, node):
    self = {n.tag.rsplit('}', 1)[-1]: cfdi_objectify.get(n.tag, default_objectify)(cls, n) for n in node}
    return self
def addenda3(cls, node):
    self = {n.tag.rsplit('}', 1)[-1]: cfdi_objectify.get(n.tag, default_objectify)(cls, n) for n in node}
    return self
def comprobante2(cls, node):
    self = cls()
    self.tag = node.tag
    el = node.find('{http://www.sat.gob.mx/cfd/4}InformacionGlobal')
    if el is not None:
        self['InformacionGlobal'] = informacion_global0(cls, el)
    el = node.find('{http://www.sat.gob.mx/cfd/4}CfdiRelacionados')
    if el is not None:
        self['CfdiRelacionados'] = [cfdi_relacionados1(cls, n) for n in node.iterfind('{http://www.sat.gob.mx/cfd/4}CfdiRelacionados')]
    el = node.find('{http://www.sat.gob.mx/cfd/4}Emisor')
    self['Emisor'] = emisor5(cls, el)
    el = node.find('{http://www.sat.gob.mx/cfd/4}Receptor')
    self['Receptor'] = receptor5(cls, el)
    el = node.find('{http://www.sat.gob.mx/cfd/4}Conceptos')
    self['Conceptos'] = [concepto3(cls, n) for n in el.iterfind('{http://www.sat.gob.mx/cfd/4}Concepto')]
    el = node.find('{http://www.sat.gob.mx/cfd/4}Impuestos')
    if el is not None:
        self['Impuestos'] = impuestos4(cls, el)
    el = node.find('{http://www.sat.gob.mx/cfd/4}Complemento')
    if el is not None:
        self['Complemento'] = complemento4(cls, el)
    el = node.find('{http://www.sat.gob.mx/cfd/4}Addenda')
    if el is not None:
        self['Addenda'] = addenda4(cls, el)
    self['Version'] = node.attrib['Version']
    if (a := node.attrib.get('Serie')) is not None:
        self['Serie'] = a
    if (a := node.attrib.get('Folio')) is not None:
        self['Folio'] = a
    self['Fecha'] = datetime.fromisoformat(node.attrib['Fecha'])
    self['Sello'] = node.attrib['Sello']
    if (a := node.attrib.get('FormaPago')) is not None:
        self['FormaPago'] = catalog_code('C756_c_FormaPago', a)
    self['NoCertificado'] = node.attrib['NoCertificado']
    self['Certificado'] = node.attrib['Certificado']
    if (a := node.attrib.get('CondicionesDePago')) is not None:
        self['CondicionesDePago'] = a
    self['SubTotal'] = Decimal(node.attrib['SubTotal'])
    if (a := node.attrib.get('Descuento')) is not None:
        self['Descuento'] = Decimal(a)
    self['Moneda'] = catalog_code('C756_c_Moneda', node.attrib['Moneda'], 0)
    if (a := node.attrib.get('TipoCambio')) is not None:
        self['TipoCambio'] = Decimal(a)
    self['Total'] = Decimal(node.attrib['Total'])
    self['TipoDeComprobante'] = catalog_code('C756_c_TipoDeComprobante', node.attrib['TipoDeComprobante'])
    self['Exportacion'] = catalog_code('C756_c_Exportacion', node.attrib['Exportacion'])
    if (a := node.attrib.get('MetodoPago')) is not None:
        self['MetodoPago'] = catalog_code('C756_c_MetodoPago', a)
    self['LugarExpedicion'] = node.attrib['LugarExpedicion']
    if (a := node.attrib.get('Confirmacion')) is not None:
        self['Confirmacion'] = a
    return self
def informacion_global0(cls, node):
    self = ScalarMap()
    self['Periodicidad'] = catalog_code('C756_c_Periodicidad', node.attrib['Periodicidad'])
    self['Meses'] = catalog_code('C756_c_Meses', node.attrib['Meses'])
    self['Año'] = Xint(node.attrib['Año'])
    return self
def cfdi_relacionados1(cls, node):
    self = ScalarMap()
    self['CfdiRelacionado'] = [cfdi_relacionado1(cls, n) for n in node.iterfind('{http://www.sat.gob.mx/cfd/4}CfdiRelacionado')]
    self['TipoRelacion'] = catalog_code('C756_c_TipoRelacion', node.attrib['TipoRelacion'])
    return self
def cfdi_relacionado1(cls, node):
    return node.attrib['UUID']
def emisor5(cls, node):
    self = ScalarMap()
    self['Rfc'] = node.attrib['Rfc']
    self['Nombre'] = node.attrib['Nombre']
    self['RegimenFiscal'] = catalog_code('C756_c_RegimenFiscal', node.attrib['RegimenFiscal'])
    if (a := node.attrib.get('FacAtrAdquirente')) is not None:
        self['FacAtrAdquirente'] = a
    return self
def receptor5(cls, node):
    self = ScalarMap()
    self['Rfc'] = node.attrib['Rfc']
    self['Nombre'] = node.attrib['Nombre']
    self['DomicilioFiscalReceptor'] = node.attrib['DomicilioFiscalReceptor']
    if (a := node.attrib.get('ResidenciaFiscal')) is not None:
        self['ResidenciaFiscal'] = catalog_code('C756_c_Pais', a)
    if (a := node.attrib.get('NumRegIdTrib')) is not None:
        self['NumRegIdTrib'] = a
    self['RegimenFiscalReceptor'] = catalog_code('C756_c_RegimenFiscal', node.attrib['RegimenFiscalReceptor'])
    self['UsoCFDI'] = catalog_code('C756_c_UsoCFDI', node.attrib['UsoCFDI'])
    return self
def concepto3(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.sat.gob.mx/cfd/4}Impuestos')
    if el is not None:
        self['Impuestos'] = impuestos3(cls, el)
    el = node.find('{http://www.sat.gob.mx/cfd/4}ACuentaTerceros')
    if el is not None:
        self['ACuentaTerceros'] = a_cuenta_terceros0(cls, el)
    el = node.find('{http://www.sat.gob.mx/cfd/4}InformacionAduanera')
    if el is not None:
        self['InformacionAduanera'] = [informacion_aduanera2(cls, n) for n in node.iterfind('{http://www.sat.gob.mx/cfd/4}InformacionAduanera')]
    el = node.find('{http://www.sat.gob.mx/cfd/4}CuentaPredial')
    if el is not None:
        self['CuentaPredial'] = [cuenta_predial2(cls, n) for n in node.iterfind('{http://www.sat.gob.mx/cfd/4}CuentaPredial')]
    el = node.find('{http://www.sat.gob.mx/cfd/4}ComplementoConcepto')
    if el is not None:
        self['ComplementoConcepto'] = complemento_concepto2(cls, el)
    el = node.find('{http://www.sat.gob.mx/cfd/4}Parte')
    if el is not None:
        self['Parte'] = [parte2(cls, n) for n in node.iterfind('{http://www.sat.gob.mx/cfd/4}Parte')]
    self['ClaveProdServ'] = catalog_code('C756_c_ClaveProdServ', node.attrib['ClaveProdServ'])
    if (a := node.attrib.get('NoIdentificacion')) is not None:
        self['NoIdentificacion'] = a
    self['Cantidad'] = Decimal(node.attrib['Cantidad'])
    self['ClaveUnidad'] = catalog_code('C756_c_ClaveUnidad', node.attrib['ClaveUnidad'])
    if (a := node.attrib.get('Unidad')) is not None:
        self['Unidad'] = a
    self['Descripcion'] = node.attrib['Descripcion']
    self['ValorUnitario'] = Decimal(node.attrib['ValorUnitario'])
    self['Importe'] = Decimal(node.attrib['Importe'])
    if (a := node.attrib.get('Descuento')) is not None:
        self['Descuento'] = Decimal(a)
    self['ObjetoImp'] = catalog_code('C756_c_ObjetoImp', node.attrib['ObjetoImp'])
    return self
def impuestos3(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.sat.gob.mx/cfd/4}Traslados')
    if el is not None:
        self['Traslados'] = {impuesto_index(n.attrib, 'Impuesto'): traslado3(cls, n) for n in el.iterfind('{http://www.sat.gob.mx/cfd/4}Traslado')}
    el = node.find('{http://www.sat.gob.mx/cfd/4}Retenciones')
    if el is not None:
        self['Retenciones'] = {impuesto_index(n.attrib, 'Impuesto'): retencion3(cls, n) for n in el.iterfind('{http://www.sat.gob.mx/cfd/4}Retencion')}
    return self
def traslado3(cls, node):
    self = ScalarMap()
    self['Base'] = Decimal(node.attrib['Base'])
    self['Impuesto'] = catalog_code('C756_c_Impuesto', node.attrib['Impuesto'])
    self['TipoFactor'] = catalog_code('C756_c_TipoFactor', node.attrib['TipoFactor'])
    if (a := node.attrib.get('TasaOCuota')) is not None:
        self['TasaOCuota'] = Decimal(a)
    if (a := node.attrib.get('Importe')) is not None:
        self['Importe'] = Decimal(a)
    return self
def retencion3(cls, node):
    self = ScalarMap()
    self['Base'] = Decimal(node.attrib['Base'])
    self['Impuesto'] = catalog_code('C756_c_Impuesto', node.attrib['Impuesto'])
    self['TipoFactor'] = catalog_code('C756_c_TipoFactor', node.attrib['TipoFactor'])
    self['TasaOCuota'] = Decimal(node.attrib['TasaOCuota'])
    self['Importe'] = Decimal(node.attrib['Importe'])
    return self
def a_cuenta_terceros0(cls, node):
    self = ScalarMap()
    self['RfcACuentaTerceros'] = node.attrib['RfcACuentaTerceros']
    self['NombreACuentaTerceros'] = node.attrib['NombreACuentaTerceros']
    self['RegimenFiscalACuentaTerceros'] = catalog_code('C756_c_RegimenFiscal', node.attrib['RegimenFiscalACuentaTerceros'])
    self['DomicilioFiscalACuentaTerceros'] = node.attrib['DomicilioFiscalACuentaTerceros']
    return self
def informacion_aduanera2(cls, node):
    return node.attrib['NumeroPedimento']
def cuenta_predial2(cls, node):
    return node.attrib['Numero']
def complemento_concepto2(cls, node):
    self = {n.tag.rsplit('}', 1)[-1]: cfdi_objectify.get(n.tag, default_objectify)(cls, n) for n in node}
    return self
def parte2(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.sat.gob.mx/cfd/4}InformacionAduanera')
    if el is not None:
        self['InformacionAduanera'] = [informacion_aduanera3(cls, n) for n in node.iterfind('{http://www.sat.gob.mx/cfd/4}InformacionAduanera')]
    self['ClaveProdServ'] = catalog_code('C756_c_ClaveProdServ', node.attrib['ClaveProdServ'])
    if (a := node.attrib.get('NoIdentificacion')) is not None:
        self['NoIdentificacion'] = a
    self['Cantidad'] = Decimal(node.attrib['Cantidad'])
    if (a := node.attrib.get('Unidad')) is not None:
        self['Unidad'] = a
    self['Descripcion'] = node.attrib['Descripcion']
    if (a := node.attrib.get('ValorUnitario')) is not None:
        self['ValorUnitario'] = Decimal(a)
    if (a := node.attrib.get('Importe')) is not None:
        self['Importe'] = Decimal(a)
    return self
def informacion_aduanera3(cls, node):
    return node.attrib['NumeroPedimento']
def impuestos4(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.sat.gob.mx/cfd/4}Retenciones')
    if el is not None:
        self['Retenciones'] = {impuesto_index(n.attrib, 'Impuesto'): retencion4(cls, n) for n in el.iterfind('{http://www.sat.gob.mx/cfd/4}Retencion')}
    el = node.find('{http://www.sat.gob.mx/cfd/4}Traslados')
    if el is not None:
        self['Traslados'] = {impuesto_index(n.attrib, 'Impuesto'): traslado4(cls, n) for n in el.iterfind('{http://www.sat.gob.mx/cfd/4}Traslado')}
    if (a := node.attrib.get('TotalImpuestosRetenidos')) is not None:
        self['TotalImpuestosRetenidos'] = Decimal(a)
    if (a := node.attrib.get('TotalImpuestosTrasladados')) is not None:
        self['TotalImpuestosTrasladados'] = Decimal(a)
    return self
def retencion4(cls, node):
    self = ScalarMap()
    self['Impuesto'] = catalog_code('C756_c_Impuesto', node.attrib['Impuesto'])
    self['Importe'] = Decimal(node.attrib['Importe'])
    return self
def traslado4(cls, node):
    self = ScalarMap()
    self['Base'] = Decimal(node.attrib['Base'])
    self['Impuesto'] = catalog_code('C756_c_Impuesto', node.attrib['Impuesto'])
    self['TipoFactor'] = catalog_code('C756_c_TipoFactor', node.attrib['TipoFactor'])
    if (a := node.attrib.get('TasaOCuota')) is not None:
        self['TasaOCuota'] = Decimal(a)
    if (a := node.attrib.get('Importe')) is not None:
        self['Importe'] = Decimal(a)
    return self
def complemento4(cls, node):
    self = {n.tag.rsplit('}', 1)[-1]: cfdi_objectify.get(n.tag, default_objectify)(cls, n) for n in node}
    return self
def addenda4(cls, node):
    self = {n.tag.rsplit('}', 1)[-1]: cfdi_objectify.get(n.tag, default_objectify)(cls, n) for n in node}
    return self
def carta_porte0(cls, node):
    self = cls()
    self.tag = node.tag
    el = node.find('{http://www.sat.gob.mx/CartaPorte}Ubicaciones')
    self['Ubicaciones'] = [ubicacion1(cls, n) for n in el.iterfind('{http://www.sat.gob.mx/CartaPorte}Ubicacion')]
    el = node.find('{http://www.sat.gob.mx/CartaPorte}Mercancias')
    self['Mercancias'] = mercancias0(cls, el)
    el = node.find('{http://www.sat.gob.mx/CartaPorte}FiguraTransporte')
    if el is not None:
        self['FiguraTransporte'] = figura_transporte0(cls, el)
    self['Version'] = node.attrib['Version']
    self['TranspInternac'] = node.attrib['TranspInternac']
    if (a := node.attrib.get('EntradaSalidaMerc')) is not None:
        self['EntradaSalidaMerc'] = a
    if (a := node.attrib.get('ViaEntradaSalida')) is not None:
        self['ViaEntradaSalida'] = catalog_code('C592_c_CveTransporte', a)
    if (a := node.attrib.get('TotalDistRec')) is not None:
        self['TotalDistRec'] = Decimal(a)
    return self
def ubicacion1(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.sat.gob.mx/CartaPorte}Origen')
    if el is not None:
        self['Origen'] = origen0(cls, el)
    el = node.find('{http://www.sat.gob.mx/CartaPorte}Destino')
    if el is not None:
        self['Destino'] = destino0(cls, el)
    el = node.find('{http://www.sat.gob.mx/CartaPorte}Domicilio')
    if el is not None:
        self['Domicilio'] = domicilio0(cls, el)
    if (a := node.attrib.get('TipoEstacion')) is not None:
        self['TipoEstacion'] = catalog_code('C592_c_TipoEstacion', a)
    if (a := node.attrib.get('DistanciaRecorrida')) is not None:
        self['DistanciaRecorrida'] = Decimal(a)
    return self
def origen0(cls, node):
    self = ScalarMap()
    if (a := node.attrib.get('IDOrigen')) is not None:
        self['IDOrigen'] = a
    if (a := node.attrib.get('RFCRemitente')) is not None:
        self['RFCRemitente'] = a
    if (a := node.attrib.get('NombreRemitente')) is not None:
        self['NombreRemitente'] = a
    if (a := node.attrib.get('NumRegIdTrib')) is not None:
        self['NumRegIdTrib'] = a
    if (a := node.attrib.get('ResidenciaFiscal')) is not None:
        self['ResidenciaFiscal'] = catalog_code('C756_c_Pais', a)
    if (a := node.attrib.get('NumEstacion')) is not None:
        self['NumEstacion'] = catalog_code('C592_c_Estaciones', a)
    if (a := node.attrib.get('NombreEstacion')) is not None:
        self['NombreEstacion'] = a
    if (a := node.attrib.get('NavegacionTrafico')) is not None:
        self['NavegacionTrafico'] = a
    self['FechaHoraSalida'] = datetime.fromisoformat(node.attrib['FechaHoraSalida'])
    return self
def destino0(cls, node):
    self = ScalarMap()
    if (a := node.attrib.get('IDDestino')) is not None:
        self['IDDestino'] = a
    if (a := node.attrib.get('RFCDestinatario')) is not None:
        self['RFCDestinatario'] = a
    if (a := node.attrib.get('NombreDestinatario')) is not None:
        self['NombreDestinatario'] = a
    if (a := node.attrib.get('NumRegIdTrib')) is not None:
        self['NumRegIdTrib'] = a
    if (a := node.attrib.get('ResidenciaFiscal')) is not None:
        self['ResidenciaFiscal'] = catalog_code('C756_c_Pais', a)
    if (a := node.attrib.get('NumEstacion')) is not None:
        self['NumEstacion'] = catalog_code('C592_c_Estaciones', a)
    if (a := node.attrib.get('NombreEstacion')) is not None:
        self['NombreEstacion'] = a
    if (a := node.attrib.get('NavegacionTrafico')) is not None:
        self['NavegacionTrafico'] = a
    self['FechaHoraProgLlegada'] = datetime.fromisoformat(node.attrib['FechaHoraProgLlegada'])
    return self
def domicilio0(cls, node):
    self = ScalarMap()
    self['Calle'] = node.attrib['Calle']
    if (a := node.attrib.get('NumeroExterior')) is not None:
        self['NumeroExterior'] = a
    if (a := node.attrib.get('NumeroInterior')) is not None:
        self['NumeroInterior'] = a
    if (a := node.attrib.get('Colonia')) is not None:
        self['Colonia'] = a
    if (a := node.attrib.get('Localidad')) is not None:
        self['Localidad'] = a
    if (a := node.attrib.get('Referencia')) is not None:
        self['Referencia'] = a
    if (a := node.attrib.get('Municipio')) is not None:
        self['Municipio'] = a
    self['Estado'] = node.attrib['Estado']
    self['Pais'] = catalog_code('C756_c_Pais', node.attrib['Pais'])
    self['CodigoPostal'] = node.attrib['CodigoPostal']
    return self
def mercancias0(cls, node):
    self = ScalarMap()
    self['Mercancia'] = [mercancia0(cls, n) for n in node.iterfind('{http://www.sat.gob.mx/CartaPorte}Mercancia')]
    el = node.find('{http://www.sat.gob.mx/CartaPorte}AutotransporteFederal')
    if el is not None:
        self['AutotransporteFederal'] = autotransporte_federal0(cls, el)
    el = node.find('{http://www.sat.gob.mx/CartaPorte}TransporteMaritimo')
    if el is not None:
        self['TransporteMaritimo'] = transporte_maritimo0(cls, el)
    el = node.find('{http://www.sat.gob.mx/CartaPorte}TransporteAereo')
    if el is not None:
        self['TransporteAereo'] = transporte_aereo0(cls, el)
    el = node.find('{http://www.sat.gob.mx/CartaPorte}TransporteFerroviario')
    if el is not None:
        self['TransporteFerroviario'] = transporte_ferroviario0(cls, el)
    if (a := node.attrib.get('PesoBrutoTotal')) is not None:
        self['PesoBrutoTotal'] = Decimal(a)
    if (a := node.attrib.get('UnidadPeso')) is not None:
        self['UnidadPeso'] = catalog_code('C592_c_ClaveUnidadPeso', a)
    if (a := node.attrib.get('PesoNetoTotal')) is not None:
        self['PesoNetoTotal'] = Decimal(a)
    self['NumTotalMercancias'] = Xint(node.attrib['NumTotalMercancias'])
    if (a := node.attrib.get('CargoPorTasacion')) is not None:
        self['CargoPorTasacion'] = Decimal(a)
    return self
def mercancia0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.sat.gob.mx/CartaPorte}CantidadTransporta')
    if el is not None:
        self['CantidadTransporta'] = [cantidad_transporta0(cls, n) for n in node.iterfind('{http://www.sat.gob.mx/CartaPorte}CantidadTransporta')]
    el = node.find('{http://www.sat.gob.mx/CartaPorte}DetalleMercancia')
    if el is not None:
        self['DetalleMercancia'] = detalle_mercancia0(cls, el)
    if (a := node.attrib.get('BienesTransp')) is not None:
        self['BienesTransp'] = catalog_code('C592_c_ClaveProdServCP', a)
    if (a := node.attrib.get('ClaveSTCC')) is not None:
        self['ClaveSTCC'] = a
    if (a := node.attrib.get('Descripcion')) is not None:
        self['Descripcion'] = a
    if (a := node.attrib.get('Cantidad')) is not None:
        self['Cantidad'] = Decimal(a)
    if (a := node.attrib.get('ClaveUnidad')) is not None:
        self['ClaveUnidad'] = catalog_code('C756_c_ClaveUnidad', a)
    if (a := node.attrib.get('Unidad')) is not None:
        self['Unidad'] = a
    if (a := node.attrib.get('Dimensiones')) is not None:
        self['Dimensiones'] = a
    if (a := node.attrib.get('MaterialPeligroso')) is not None:
        self['MaterialPeligroso'] = a
    if (a := node.attrib.get('CveMaterialPeligroso')) is not None:
        self['CveMaterialPeligroso'] = catalog_code('C592_c_MaterialPeligroso', a)
    if (a := node.attrib.get('Embalaje')) is not None:
        self['Embalaje'] = catalog_code('C592_c_TipoEmbalaje', a)
    if (a := node.attrib.get('DescripEmbalaje')) is not None:
        self['DescripEmbalaje'] = a
    self['PesoEnKg'] = Decimal(node.attrib['PesoEnKg'])
    if (a := node.attrib.get('ValorMercancia')) is not None:
        self['ValorMercancia'] = Decimal(a)
    if (a := node.attrib.get('Moneda')) is not None:
        self['Moneda'] = catalog_code('C756_c_Moneda', a, 0)
    if (a := node.attrib.get('FraccionArancelaria')) is not None:
        self['FraccionArancelaria'] = catalog_code('C5bc_c_FraccionArancelaria', a)
    if (a := node.attrib.get('UUIDComercioExt')) is not None:
        self['UUIDComercioExt'] = a
    return self
def cantidad_transporta0(cls, node):
    self = ScalarMap()
    self['Cantidad'] = Decimal(node.attrib['Cantidad'])
    self['IDOrigen'] = node.attrib['IDOrigen']
    self['IDDestino'] = node.attrib['IDDestino']
    if (a := node.attrib.get('CvesTransporte')) is not None:
        self['CvesTransporte'] = catalog_code('C592_c_CveTransporte', a)
    return self
def detalle_mercancia0(cls, node):
    self = ScalarMap()
    self['UnidadPeso'] = catalog_code('C592_c_ClaveUnidadPeso', node.attrib['UnidadPeso'])
    self['PesoBruto'] = Decimal(node.attrib['PesoBruto'])
    self['PesoNeto'] = Decimal(node.attrib['PesoNeto'])
    self['PesoTara'] = Decimal(node.attrib['PesoTara'])
    if (a := node.attrib.get('NumPiezas')) is not None:
        self['NumPiezas'] = Xint(a)
    return self
def autotransporte_federal0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.sat.gob.mx/CartaPorte}IdentificacionVehicular')
    self['IdentificacionVehicular'] = identificacion_vehicular0(cls, el)
    el = node.find('{http://www.sat.gob.mx/CartaPorte}Remolques')
    if el is not None:
        self['Remolques'] = [remolque0(cls, n) for n in el.iterfind('{http://www.sat.gob.mx/CartaPorte}Remolque')]
    self['PermSCT'] = catalog_code('C592_c_TipoPermiso', node.attrib['PermSCT'])
    self['NumPermisoSCT'] = node.attrib['NumPermisoSCT']
    self['NombreAseg'] = node.attrib['NombreAseg']
    self['NumPolizaSeguro'] = node.attrib['NumPolizaSeguro']
    return self
def identificacion_vehicular0(cls, node):
    self = ScalarMap()
    self['ConfigVehicular'] = catalog_code('C592_c_ConfigAutotransporte', node.attrib['ConfigVehicular'])
    self['PlacaVM'] = node.attrib['PlacaVM']
    self['AnioModeloVM'] = Xint(node.attrib['AnioModeloVM'])
    return self
def remolque0(cls, node):
    self = ScalarMap()
    self['SubTipoRem'] = catalog_code('C592_c_SubTipoRem', node.attrib['SubTipoRem'])
    self['Placa'] = node.attrib['Placa']
    return self
def transporte_maritimo0(cls, node):
    self = ScalarMap()
    self['Contenedor'] = [contenedor0(cls, n) for n in node.iterfind('{http://www.sat.gob.mx/CartaPorte}Contenedor')]
    if (a := node.attrib.get('PermSCT')) is not None:
        self['PermSCT'] = catalog_code('C592_c_TipoPermiso', a)
    if (a := node.attrib.get('NumPermisoSCT')) is not None:
        self['NumPermisoSCT'] = a
    if (a := node.attrib.get('NombreAseg')) is not None:
        self['NombreAseg'] = a
    if (a := node.attrib.get('NumPolizaSeguro')) is not None:
        self['NumPolizaSeguro'] = a
    self['TipoEmbarcacion'] = catalog_code('C592_c_ConfigMaritima', node.attrib['TipoEmbarcacion'])
    self['Matricula'] = node.attrib['Matricula']
    self['NumeroOMI'] = node.attrib['NumeroOMI']
    if (a := node.attrib.get('AnioEmbarcacion')) is not None:
        self['AnioEmbarcacion'] = Xint(a)
    if (a := node.attrib.get('NombreEmbarc')) is not None:
        self['NombreEmbarc'] = a
    self['NacionalidadEmbarc'] = catalog_code('C756_c_Pais', node.attrib['NacionalidadEmbarc'])
    self['UnidadesDeArqBruto'] = Decimal(node.attrib['UnidadesDeArqBruto'])
    self['TipoCarga'] = catalog_code('C592_c_ClaveTipoCarga', node.attrib['TipoCarga'])
    self['NumCertITC'] = node.attrib['NumCertITC']
    if (a := node.attrib.get('Eslora')) is not None:
        self['Eslora'] = Decimal(a)
    if (a := node.attrib.get('Manga')) is not None:
        self['Manga'] = Decimal(a)
    if (a := node.attrib.get('Calado')) is not None:
        self['Calado'] = Decimal(a)
    if (a := node.attrib.get('LineaNaviera')) is not None:
        self['LineaNaviera'] = a
    self['NombreAgenteNaviero'] = node.attrib['NombreAgenteNaviero']
    self['NumAutorizacionNaviero'] = node.attrib['NumAutorizacionNaviero']
    if (a := node.attrib.get('NumViaje')) is not None:
        self['NumViaje'] = a
    if (a := node.attrib.get('NumConocEmbarc')) is not None:
        self['NumConocEmbarc'] = a
    return self
def contenedor0(cls, node):
    self = ScalarMap()
    self['MatriculaContenedor'] = node.attrib['MatriculaContenedor']
    self['TipoContenedor'] = catalog_code('C592_c_ContenedorMaritimo', node.attrib['TipoContenedor'])
    if (a := node.attrib.get('NumPrecinto')) is not None:
        self['NumPrecinto'] = a
    return self
def transporte_aereo0(cls, node):
    self = ScalarMap()
    self['PermSCT'] = catalog_code('C592_c_TipoPermiso', node.attrib['PermSCT'])
    self['NumPermisoSCT'] = node.attrib['NumPermisoSCT']
    self['MatriculaAeronave'] = node.attrib['MatriculaAeronave']
    if (a := node.attrib.get('NombreAseg')) is not None:
        self['NombreAseg'] = a
    if (a := node.attrib.get('NumPolizaSeguro')) is not None:
        self['NumPolizaSeguro'] = a
    self['NumeroGuia'] = node.attrib['NumeroGuia']
    if (a := node.attrib.get('LugarContrato')) is not None:
        self['LugarContrato'] = a
    if (a := node.attrib.get('RFCTransportista')) is not None:
        self['RFCTransportista'] = a
    self['CodigoTransportista'] = catalog_code('C592_c_CodigoTransporteAereo', node.attrib['CodigoTransportista'])
    if (a := node.attrib.get('NumRegIdTribTranspor')) is not None:
        self['NumRegIdTribTranspor'] = a
    if (a := node.attrib.get('ResidenciaFiscalTranspor')) is not None:
        self['ResidenciaFiscalTranspor'] = catalog_code('C756_c_Pais', a)
    if (a := node.attrib.get('NombreTransportista')) is not None:
        self['NombreTransportista'] = a
    if (a := node.attrib.get('RFCEmbarcador')) is not None:
        self['RFCEmbarcador'] = a
    if (a := node.attrib.get('NumRegIdTribEmbarc')) is not None:
        self['NumRegIdTribEmbarc'] = a
    if (a := node.attrib.get('ResidenciaFiscalEmbarc')) is not None:
        self['ResidenciaFiscalEmbarc'] = catalog_code('C756_c_Pais', a)
    if (a := node.attrib.get('NombreEmbarcador')) is not None:
        self['NombreEmbarcador'] = a
    return self
def transporte_ferroviario0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.sat.gob.mx/CartaPorte}DerechosDePaso')
    if el is not None:
        self['DerechosDePaso'] = [derechos_de_paso0(cls, n) for n in node.iterfind('{http://www.sat.gob.mx/CartaPorte}DerechosDePaso')]
    self['Carro'] = [carro0(cls, n) for n in node.iterfind('{http://www.sat.gob.mx/CartaPorte}Carro')]
    self['TipoDeServicio'] = catalog_code('C592_c_TipoDeServicio', node.attrib['TipoDeServicio'])
    if (a := node.attrib.get('NombreAseg')) is not None:
        self['NombreAseg'] = a
    if (a := node.attrib.get('NumPolizaSeguro')) is not None:
        self['NumPolizaSeguro'] = a
    if (a := node.attrib.get('Concesionario')) is not None:
        self['Concesionario'] = a
    return self
def derechos_de_paso0(cls, node):
    self = ScalarMap()
    self['TipoDerechoDePaso'] = catalog_code('C592_c_DerechosDePaso', node.attrib['TipoDerechoDePaso'])
    self['KilometrajePagado'] = Decimal(node.attrib['KilometrajePagado'])
    return self
def carro0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.sat.gob.mx/CartaPorte}Contenedor')
    if el is not None:
        self['Contenedor'] = [contenedor1(cls, n) for n in node.iterfind('{http://www.sat.gob.mx/CartaPorte}Contenedor')]
    self['TipoCarro'] = catalog_code('C592_c_TipoCarro', node.attrib['TipoCarro'])
    self['MatriculaCarro'] = node.attrib['MatriculaCarro']
    self['GuiaCarro'] = node.attrib['GuiaCarro']
    self['ToneladasNetasCarro'] = Decimal(node.attrib['ToneladasNetasCarro'])
    return self
def contenedor1(cls, node):
    self = ScalarMap()
    self['TipoContenedor'] = catalog_code('C592_c_Contenedor', node.attrib['TipoContenedor'])
    self['PesoContenedorVacio'] = Decimal(node.attrib['PesoContenedorVacio'])
    self['PesoNetoMercancia'] = Decimal(node.attrib['PesoNetoMercancia'])
    return self
def figura_transporte0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.sat.gob.mx/CartaPorte}Operadores')
    if el is not None:
        self['Operadores'] = [operadores0(cls, n) for n in node.iterfind('{http://www.sat.gob.mx/CartaPorte}Operadores')]
    el = node.find('{http://www.sat.gob.mx/CartaPorte}Propietario')
    if el is not None:
        self['Propietario'] = [propietario0(cls, n) for n in node.iterfind('{http://www.sat.gob.mx/CartaPorte}Propietario')]
    el = node.find('{http://www.sat.gob.mx/CartaPorte}Arrendatario')
    if el is not None:
        self['Arrendatario'] = [arrendatario0(cls, n) for n in node.iterfind('{http://www.sat.gob.mx/CartaPorte}Arrendatario')]
    el = node.find('{http://www.sat.gob.mx/CartaPorte}Notificado')
    if el is not None:
        self['Notificado'] = [notificado0(cls, n) for n in node.iterfind('{http://www.sat.gob.mx/CartaPorte}Notificado')]
    self['CveTransporte'] = catalog_code('C592_c_CveTransporte', node.attrib['CveTransporte'])
    return self
def operadores0(cls, node):
    self = ScalarMap()
    self['Operador'] = [operador0(cls, n) for n in node.iterfind('{http://www.sat.gob.mx/CartaPorte}Operador')]
    return self
def operador0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.sat.gob.mx/CartaPorte}Domicilio')
    if el is not None:
        self['Domicilio'] = domicilio1(cls, el)
    if (a := node.attrib.get('RFCOperador')) is not None:
        self['RFCOperador'] = a
    if (a := node.attrib.get('NumLicencia')) is not None:
        self['NumLicencia'] = a
    if (a := node.attrib.get('NombreOperador')) is not None:
        self['NombreOperador'] = a
    if (a := node.attrib.get('NumRegIdTribOperador')) is not None:
        self['NumRegIdTribOperador'] = a
    if (a := node.attrib.get('ResidenciaFiscalOperador')) is not None:
        self['ResidenciaFiscalOperador'] = catalog_code('C756_c_Pais', a)
    return self
def domicilio1(cls, node):
    self = ScalarMap()
    self['Calle'] = node.attrib['Calle']
    if (a := node.attrib.get('NumeroExterior')) is not None:
        self['NumeroExterior'] = a
    if (a := node.attrib.get('NumeroInterior')) is not None:
        self['NumeroInterior'] = a
    if (a := node.attrib.get('Colonia')) is not None:
        self['Colonia'] = a
    if (a := node.attrib.get('Localidad')) is not None:
        self['Localidad'] = a
    if (a := node.attrib.get('Referencia')) is not None:
        self['Referencia'] = a
    if (a := node.attrib.get('Municipio')) is not None:
        self['Municipio'] = a
    self['Estado'] = node.attrib['Estado']
    self['Pais'] = catalog_code('C756_c_Pais', node.attrib['Pais'])
    self['CodigoPostal'] = node.attrib['CodigoPostal']
    return self
def propietario0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.sat.gob.mx/CartaPorte}Domicilio')
    if el is not None:
        self['Domicilio'] = domicilio2(cls, el)
    if (a := node.attrib.get('RFCPropietario')) is not None:
        self['RFCPropietario'] = a
    if (a := node.attrib.get('NombrePropietario')) is not None:
        self['NombrePropietario'] = a
    if (a := node.attrib.get('NumRegIdTribPropietario')) is not None:
        self['NumRegIdTribPropietario'] = a
    if (a := node.attrib.get('ResidenciaFiscalPropietario')) is not None:
        self['ResidenciaFiscalPropietario'] = catalog_code('C756_c_Pais', a)
    return self
def domicilio2(cls, node):
    self = ScalarMap()
    self['Calle'] = node.attrib['Calle']
    if (a := node.attrib.get('NumeroExterior')) is not None:
        self['NumeroExterior'] = a
    if (a := node.attrib.get('NumeroInterior')) is not None:
        self['NumeroInterior'] = a
    if (a := node.attrib.get('Colonia')) is not None:
        self['Colonia'] = a
    if (a := node.attrib.get('Localidad')) is not None:
        self['Localidad'] = a
    if (a := node.attrib.get('Referencia')) is not None:
        self['Referencia'] = a
    if (a := node.attrib.get('Municipio')) is not None:
        self['Municipio'] = a
    self['Estado'] = node.attrib['Estado']
    self['Pais'] = catalog_code('C756_c_Pais', node.attrib['Pais'])
    self['CodigoPostal'] = node.attrib['CodigoPostal']
    return self
def arrendatario0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.sat.gob.mx/CartaPorte}Domicilio')
    if el is not None:
        self['Domicilio'] = domicilio3(cls, el)
    if (a := node.attrib.get('RFCArrendatario')) is not None:
        self['RFCArrendatario'] = a
    if (a := node.attrib.get('NombreArrendatario')) is not None:
        self['NombreArrendatario'] = a
    if (a := node.attrib.get('NumRegIdTribArrendatario')) is not None:
        self['NumRegIdTribArrendatario'] = a
    if (a := node.attrib.get('ResidenciaFiscalArrendatario')) is not None:
        self['ResidenciaFiscalArrendatario'] = catalog_code('C756_c_Pais', a)
    return self
def domicilio3(cls, node):
    self = ScalarMap()
    self['Calle'] = node.attrib['Calle']
    if (a := node.attrib.get('NumeroExterior')) is not None:
        self['NumeroExterior'] = a
    if (a := node.attrib.get('NumeroInterior')) is not None:
        self['NumeroInterior'] = a
    if (a := node.attrib.get('Colonia')) is not None:
        self['Colonia'] = a
    if (a := node.attrib.get('Localidad')) is not None:
        self['Localidad'] = a
    if (a := node.attrib.get('Referencia')) is not None:
        self['Referencia'] = a
    if (a := node.attrib.get('Municipio')) is not None:
        self['Municipio'] = a
    self['Estado'] = node.attrib['Estado']
    self['Pais'] = catalog_code('C756_c_Pais', node.attrib['Pais'])
    self['CodigoPostal'] = node.attrib['CodigoPostal']
    return self
def notificado0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.sat.gob.mx/CartaPorte}Domicilio')
    if el is not None:
        self['Domicilio'] = domicilio4(cls, el)
    if (a := node.attrib.get('RFCNotificado')) is not None:
        self['RFCNotificado'] = a
    if (a := node.attrib.get('NombreNotificado')) is not None:
        self['NombreNotificado'] = a
    if (a := node.attrib.get('NumRegIdTribNotificado')) is not None:
        self['NumRegIdTribNotificado'] = a
    if (a := node.attrib.get('ResidenciaFiscalNotificado')) is not None:
        self['ResidenciaFiscalNotificado'] = catalog_code('C756_c_Pais', a)
    return self
def domicilio4(cls, node):
    self = ScalarMap()
    self['Calle'] = node.attrib['Calle']
    if (a := node.attrib.get('NumeroExterior')) is not None:
        self['NumeroExterior'] = a
    if (a := node.attrib.get('NumeroInterior')) is not None:
        self['NumeroInterior'] = a
    if (a := node.attrib.get('Colonia')) is not None:
        self['Colonia'] = a
    if (a := node.attrib.get('Localidad')) is not None:
        self['Localidad'] = a
    if (a := node.attrib.get('Referencia')) is not None:
        self['Referencia'] = a
    if (a := node.attrib.get('Municipio')) is not None:
        self['Municipio'] = a
    self['Estado'] = node.attrib['Estado']
    self['Pais'] = catalog_code('C756_c_Pais', node.attrib['Pais'])
    self['CodigoPostal'] = node.attrib['CodigoPostal']
    return self
def carta_porte1(cls, node):
    self = cls()
    self.tag = node.tag
    el = node.find('{http://www.sat.gob.mx/CartaPorte20}Ubicaciones')
    self['Ubicaciones'] = [ubicacion2(cls, n) for n in el.iterfind('{http://www.sat.gob.mx/CartaPorte20}Ubicacion')]
    el = node.find('{http://www.sat.gob.mx/CartaPorte20}Mercancias')
    self['Mercancias'] = mercancias1(cls, el)
    el = node.find('{http://www.sat.gob.mx/CartaPorte20}FiguraTransporte')
    if el is not None:
        self['FiguraTransporte'] = [tipos_figura0(cls, n) for n in el.iterfind('{http://www.sat.gob.mx/CartaPorte20}TiposFigura')]
    self['Version'] = node.attrib['Version']
    self['TranspInternac'] = node.attrib['TranspInternac']
    if (a := node.attrib.get('EntradaSalidaMerc')) is not None:
        self['EntradaSalidaMerc'] = a
    if (a := node.attrib.get('PaisOrigenDestino')) is not None:
        self['PaisOrigenDestino'] = catalog_code('C756_c_Pais', a)
    if (a := node.attrib.get('ViaEntradaSalida')) is not None:
        self['ViaEntradaSalida'] = catalog_code('C592_c_CveTransporte', a)
    if (a := node.attrib.get('TotalDistRec')) is not None:
        self['TotalDistRec'] = Decimal(a)
    return self
def ubicacion2(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.sat.gob.mx/CartaPorte20}Domicilio')
    if el is not None:
        self['Domicilio'] = domicilio5(cls, el)
    self['TipoUbicacion'] = node.attrib['TipoUbicacion']
    if (a := node.attrib.get('IDUbicacion')) is not None:
        self['IDUbicacion'] = a
    self['RFCRemitenteDestinatario'] = node.attrib['RFCRemitenteDestinatario']
    if (a := node.attrib.get('NombreRemitenteDestinatario')) is not None:
        self['NombreRemitenteDestinatario'] = a
    if (a := node.attrib.get('NumRegIdTrib')) is not None:
        self['NumRegIdTrib'] = a
    if (a := node.attrib.get('ResidenciaFiscal')) is not None:
        self['ResidenciaFiscal'] = catalog_code('C756_c_Pais', a)
    if (a := node.attrib.get('NumEstacion')) is not None:
        self['NumEstacion'] = catalog_code('C592_c_Estaciones', a)
    if (a := node.attrib.get('NombreEstacion')) is not None:
        self['NombreEstacion'] = a
    if (a := node.attrib.get('NavegacionTrafico')) is not None:
        self['NavegacionTrafico'] = a
    self['FechaHoraSalidaLlegada'] = datetime.fromisoformat(node.attrib['FechaHoraSalidaLlegada'])
    if (a := node.attrib.get('TipoEstacion')) is not None:
        self['TipoEstacion'] = catalog_code('C592_c_TipoEstacion', a)
    if (a := node.attrib.get('DistanciaRecorrida')) is not None:
        self['DistanciaRecorrida'] = Decimal(a)
    return self
def domicilio5(cls, node):
    self = ScalarMap()
    if (a := node.attrib.get('Calle')) is not None:
        self['Calle'] = a
    if (a := node.attrib.get('NumeroExterior')) is not None:
        self['NumeroExterior'] = a
    if (a := node.attrib.get('NumeroInterior')) is not None:
        self['NumeroInterior'] = a
    if (a := node.attrib.get('Colonia')) is not None:
        self['Colonia'] = a
    if (a := node.attrib.get('Localidad')) is not None:
        self['Localidad'] = a
    if (a := node.attrib.get('Referencia')) is not None:
        self['Referencia'] = a
    if (a := node.attrib.get('Municipio')) is not None:
        self['Municipio'] = a
    self['Estado'] = node.attrib['Estado']
    self['Pais'] = catalog_code('C756_c_Pais', node.attrib['Pais'])
    self['CodigoPostal'] = node.attrib['CodigoPostal']
    return self
def mercancias1(cls, node):
    self = ScalarMap()
    self['Mercancia'] = [mercancia1(cls, n) for n in node.iterfind('{http://www.sat.gob.mx/CartaPorte20}Mercancia')]
    el = node.find('{http://www.sat.gob.mx/CartaPorte20}Autotransporte')
    if el is not None:
        self['Autotransporte'] = autotransporte0(cls, el)
    el = node.find('{http://www.sat.gob.mx/CartaPorte20}TransporteMaritimo')
    if el is not None:
        self['TransporteMaritimo'] = transporte_maritimo1(cls, el)
    el = node.find('{http://www.sat.gob.mx/CartaPorte20}TransporteAereo')
    if el is not None:
        self['TransporteAereo'] = transporte_aereo1(cls, el)
    el = node.find('{http://www.sat.gob.mx/CartaPorte20}TransporteFerroviario')
    if el is not None:
        self['TransporteFerroviario'] = transporte_ferroviario1(cls, el)
    self['PesoBrutoTotal'] = Decimal(node.attrib['PesoBrutoTotal'])
    self['UnidadPeso'] = catalog_code('C592_c_ClaveUnidadPeso', node.attrib['UnidadPeso'])
    if (a := node.attrib.get('PesoNetoTotal')) is not None:
        self['PesoNetoTotal'] = Decimal(a)
    self['NumTotalMercancias'] = Xint(node.attrib['NumTotalMercancias'])
    if (a := node.attrib.get('CargoPorTasacion')) is not None:
        self['CargoPorTasacion'] = Decimal(a)
    return self
def mercancia1(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.sat.gob.mx/CartaPorte20}Pedimentos')
    if el is not None:
        self['Pedimentos'] = [pedimentos0(cls, n) for n in node.iterfind('{http://www.sat.gob.mx/CartaPorte20}Pedimentos')]
    el = node.find('{http://www.sat.gob.mx/CartaPorte20}GuiasIdentificacion')
    if el is not None:
        self['GuiasIdentificacion'] = [guias_identificacion0(cls, n) for n in node.iterfind('{http://www.sat.gob.mx/CartaPorte20}GuiasIdentificacion')]
    el = node.find('{http://www.sat.gob.mx/CartaPorte20}CantidadTransporta')
    if el is not None:
        self['CantidadTransporta'] = [cantidad_transporta1(cls, n) for n in node.iterfind('{http://www.sat.gob.mx/CartaPorte20}CantidadTransporta')]
    el = node.find('{http://www.sat.gob.mx/CartaPorte20}DetalleMercancia')
    if el is not None:
        self['DetalleMercancia'] = detalle_mercancia1(cls, el)
    self['BienesTransp'] = catalog_code('C592_c_ClaveProdServCP', node.attrib['BienesTransp'])
    if (a := node.attrib.get('ClaveSTCC')) is not None:
        self['ClaveSTCC'] = a
    self['Descripcion'] = node.attrib['Descripcion']
    self['Cantidad'] = Decimal(node.attrib['Cantidad'])
    self['ClaveUnidad'] = catalog_code('C756_c_ClaveUnidad', node.attrib['ClaveUnidad'])
    if (a := node.attrib.get('Unidad')) is not None:
        self['Unidad'] = a
    if (a := node.attrib.get('Dimensiones')) is not None:
        self['Dimensiones'] = a
    if (a := node.attrib.get('MaterialPeligroso')) is not None:
        self['MaterialPeligroso'] = a
    if (a := node.attrib.get('CveMaterialPeligroso')) is not None:
        self['CveMaterialPeligroso'] = catalog_code('C592_c_MaterialPeligroso', a)
    if (a := node.attrib.get('Embalaje')) is not None:
        self['Embalaje'] = catalog_code('C592_c_TipoEmbalaje', a)
    if (a := node.attrib.get('DescripEmbalaje')) is not None:
        self['DescripEmbalaje'] = a
    self['PesoEnKg'] = Decimal(node.attrib['PesoEnKg'])
    if (a := node.attrib.get('ValorMercancia')) is not None:
        self['ValorMercancia'] = Decimal(a)
    if (a := node.attrib.get('Moneda')) is not None:
        self['Moneda'] = catalog_code('C756_c_Moneda', a, 0)
    if (a := node.attrib.get('FraccionArancelaria')) is not None:
        self['FraccionArancelaria'] = catalog_code('C5bc_c_FraccionArancelaria', a)
    if (a := node.attrib.get('UUIDComercioExt')) is not None:
        self['UUIDComercioExt'] = a
    return self
def pedimentos0(cls, node):
    return node.attrib['Pedimento']
def guias_identificacion0(cls, node):
    self = ScalarMap()
    self['NumeroGuiaIdentificacion'] = node.attrib['NumeroGuiaIdentificacion']
    self['DescripGuiaIdentificacion'] = node.attrib['DescripGuiaIdentificacion']
    self['PesoGuiaIdentificacion'] = Decimal(node.attrib['PesoGuiaIdentificacion'])
    return self
def cantidad_transporta1(cls, node):
    self = ScalarMap()
    self['Cantidad'] = Decimal(node.attrib['Cantidad'])
    self['IDOrigen'] = node.attrib['IDOrigen']
    self['IDDestino'] = node.attrib['IDDestino']
    if (a := node.attrib.get('CvesTransporte')) is not None:
        self['CvesTransporte'] = catalog_code('C592_c_CveTransporte', a)
    return self
def detalle_mercancia1(cls, node):
    self = ScalarMap()
    self['UnidadPesoMerc'] = catalog_code('C592_c_ClaveUnidadPeso', node.attrib['UnidadPesoMerc'])
    self['PesoBruto'] = Decimal(node.attrib['PesoBruto'])
    self['PesoNeto'] = Decimal(node.attrib['PesoNeto'])
    self['PesoTara'] = Decimal(node.attrib['PesoTara'])
    if (a := node.attrib.get('NumPiezas')) is not None:
        self['NumPiezas'] = Xint(a)
    return self
def autotransporte0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.sat.gob.mx/CartaPorte20}IdentificacionVehicular')
    self['IdentificacionVehicular'] = identificacion_vehicular1(cls, el)
    el = node.find('{http://www.sat.gob.mx/CartaPorte20}Seguros')
    self['Seguros'] = seguros0(cls, el)
    el = node.find('{http://www.sat.gob.mx/CartaPorte20}Remolques')
    if el is not None:
        self['Remolques'] = [remolque1(cls, n) for n in el.iterfind('{http://www.sat.gob.mx/CartaPorte20}Remolque')]
    self['PermSCT'] = catalog_code('C592_c_TipoPermiso', node.attrib['PermSCT'])
    self['NumPermisoSCT'] = node.attrib['NumPermisoSCT']
    return self
def identificacion_vehicular1(cls, node):
    self = ScalarMap()
    self['ConfigVehicular'] = catalog_code('C592_c_ConfigAutotransporte', node.attrib['ConfigVehicular'])
    self['PlacaVM'] = node.attrib['PlacaVM']
    self['AnioModeloVM'] = Xint(node.attrib['AnioModeloVM'])
    return self
def seguros0(cls, node):
    self = ScalarMap()
    self['AseguraRespCivil'] = node.attrib['AseguraRespCivil']
    self['PolizaRespCivil'] = node.attrib['PolizaRespCivil']
    if (a := node.attrib.get('AseguraMedAmbiente')) is not None:
        self['AseguraMedAmbiente'] = a
    if (a := node.attrib.get('PolizaMedAmbiente')) is not None:
        self['PolizaMedAmbiente'] = a
    if (a := node.attrib.get('AseguraCarga')) is not None:
        self['AseguraCarga'] = a
    if (a := node.attrib.get('PolizaCarga')) is not None:
        self['PolizaCarga'] = a
    if (a := node.attrib.get('PrimaSeguro')) is not None:
        self['PrimaSeguro'] = Decimal(a)
    return self
def remolque1(cls, node):
    self = ScalarMap()
    self['SubTipoRem'] = catalog_code('C592_c_SubTipoRem', node.attrib['SubTipoRem'])
    self['Placa'] = node.attrib['Placa']
    return self
def transporte_maritimo1(cls, node):
    self = ScalarMap()
    self['Contenedor'] = [contenedor2(cls, n) for n in node.iterfind('{http://www.sat.gob.mx/CartaPorte20}Contenedor')]
    if (a := node.attrib.get('PermSCT')) is not None:
        self['PermSCT'] = catalog_code('C592_c_TipoPermiso', a)
    if (a := node.attrib.get('NumPermisoSCT')) is not None:
        self['NumPermisoSCT'] = a
    if (a := node.attrib.get('NombreAseg')) is not None:
        self['NombreAseg'] = a
    if (a := node.attrib.get('NumPolizaSeguro')) is not None:
        self['NumPolizaSeguro'] = a
    self['TipoEmbarcacion'] = catalog_code('C592_c_ConfigMaritima', node.attrib['TipoEmbarcacion'])
    self['Matricula'] = node.attrib['Matricula']
    self['NumeroOMI'] = node.attrib['NumeroOMI']
    if (a := node.attrib.get('AnioEmbarcacion')) is not None:
        self['AnioEmbarcacion'] = Xint(a)
    if (a := node.attrib.get('NombreEmbarc')) is not None:
        self['NombreEmbarc'] = a
    self['NacionalidadEmbarc'] = catalog_code('C756_c_Pais', node.attrib['NacionalidadEmbarc'])
    self['UnidadesDeArqBruto'] = Decimal(node.attrib['UnidadesDeArqBruto'])
    self['TipoCarga'] = catalog_code('C592_c_ClaveTipoCarga', node.attrib['TipoCarga'])
    self['NumCertITC'] = node.attrib['NumCertITC']
    if (a := node.attrib.get('Eslora')) is not None:
        self['Eslora'] = Decimal(a)
    if (a := node.attrib.get('Manga')) is not None:
        self['Manga'] = Decimal(a)
    if (a := node.attrib.get('Calado')) is not None:
        self['Calado'] = Decimal(a)
    if (a := node.attrib.get('LineaNaviera')) is not None:
        self['LineaNaviera'] = a
    self['NombreAgenteNaviero'] = node.attrib['NombreAgenteNaviero']
    self['NumAutorizacionNaviero'] = node.attrib['NumAutorizacionNaviero']
    if (a := node.attrib.get('NumViaje')) is not None:
        self['NumViaje'] = a
    if (a := node.attrib.get('NumConocEmbarc')) is not None:
        self['NumConocEmbarc'] = a
    return self
def contenedor2(cls, node):
    self = ScalarMap()
    self['MatriculaContenedor'] = node.attrib['MatriculaContenedor']
    self['TipoContenedor'] = catalog_code('C592_c_ContenedorMaritimo', node.attrib['TipoContenedor'])
    if (a := node.attrib.get('NumPrecinto')) is not None:
        self['NumPrecinto'] = a
    return self
def transporte_aereo1(cls, node):
    self = ScalarMap()
    self['PermSCT'] = catalog_code('C592_c_TipoPermiso', node.attrib['PermSCT'])
    self['NumPermisoSCT'] = node.attrib['NumPermisoSCT']
    if (a := node.attrib.get('MatriculaAeronave')) is not None:
        self['MatriculaAeronave'] = a
    if (a := node.attrib.get('NombreAseg')) is not None:
        self['NombreAseg'] = a
    if (a := node.attrib.get('NumPolizaSeguro')) is not None:
        self['NumPolizaSeguro'] = a
    self['NumeroGuia'] = node.attrib['NumeroGuia']
    if (a := node.attrib.get('LugarContrato')) is not None:
        self['LugarContrato'] = a
    self['CodigoTransportista'] = catalog_code('C592_c_CodigoTransporteAereo', node.attrib['CodigoTransportista'])
    if (a := node.attrib.get('RFCEmbarcador')) is not None:
        self['RFCEmbarcador'] = a
    if (a := node.attrib.get('NumRegIdTribEmbarc')) is not None:
        self['NumRegIdTribEmbarc'] = a
    if (a := node.attrib.get('ResidenciaFiscalEmbarc')) is not None:
        self['ResidenciaFiscalEmbarc'] = catalog_code('C756_c_Pais', a)
    if (a := node.attrib.get('NombreEmbarcador')) is not None:
        self['NombreEmbarcador'] = a
    return self
def transporte_ferroviario1(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.sat.gob.mx/CartaPorte20}DerechosDePaso')
    if el is not None:
        self['DerechosDePaso'] = [derechos_de_paso1(cls, n) for n in node.iterfind('{http://www.sat.gob.mx/CartaPorte20}DerechosDePaso')]
    self['Carro'] = [carro1(cls, n) for n in node.iterfind('{http://www.sat.gob.mx/CartaPorte20}Carro')]
    self['TipoDeServicio'] = catalog_code('C592_c_TipoDeServicio', node.attrib['TipoDeServicio'])
    self['TipoDeTrafico'] = catalog_code('C592_c_TipoDeTrafico', node.attrib['TipoDeTrafico'])
    if (a := node.attrib.get('NombreAseg')) is not None:
        self['NombreAseg'] = a
    if (a := node.attrib.get('NumPolizaSeguro')) is not None:
        self['NumPolizaSeguro'] = a
    return self
def derechos_de_paso1(cls, node):
    self = ScalarMap()
    self['TipoDerechoDePaso'] = catalog_code('C592_c_DerechosDePaso', node.attrib['TipoDerechoDePaso'])
    self['KilometrajePagado'] = Decimal(node.attrib['KilometrajePagado'])
    return self
def carro1(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.sat.gob.mx/CartaPorte20}Contenedor')
    if el is not None:
        self['Contenedor'] = [contenedor3(cls, n) for n in node.iterfind('{http://www.sat.gob.mx/CartaPorte20}Contenedor')]
    self['TipoCarro'] = catalog_code('C592_c_TipoCarro', node.attrib['TipoCarro'])
    self['MatriculaCarro'] = node.attrib['MatriculaCarro']
    self['GuiaCarro'] = node.attrib['GuiaCarro']
    self['ToneladasNetasCarro'] = Decimal(node.attrib['ToneladasNetasCarro'])
    return self
def contenedor3(cls, node):
    self = ScalarMap()
    self['TipoContenedor'] = catalog_code('C592_c_Contenedor', node.attrib['TipoContenedor'])
    self['PesoContenedorVacio'] = Decimal(node.attrib['PesoContenedorVacio'])
    self['PesoNetoMercancia'] = Decimal(node.attrib['PesoNetoMercancia'])
    return self
def tipos_figura0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.sat.gob.mx/CartaPorte20}PartesTransporte')
    if el is not None:
        self['PartesTransporte'] = [partes_transporte0(cls, n) for n in node.iterfind('{http://www.sat.gob.mx/CartaPorte20}PartesTransporte')]
    el = node.find('{http://www.sat.gob.mx/CartaPorte20}Domicilio')
    if el is not None:
        self['Domicilio'] = domicilio6(cls, el)
    self['TipoFigura'] = catalog_code('C592_c_FiguraTransporte', node.attrib['TipoFigura'])
    if (a := node.attrib.get('RFCFigura')) is not None:
        self['RFCFigura'] = a
    if (a := node.attrib.get('NumLicencia')) is not None:
        self['NumLicencia'] = a
    if (a := node.attrib.get('NombreFigura')) is not None:
        self['NombreFigura'] = a
    if (a := node.attrib.get('NumRegIdTribFigura')) is not None:
        self['NumRegIdTribFigura'] = a
    if (a := node.attrib.get('ResidenciaFiscalFigura')) is not None:
        self['ResidenciaFiscalFigura'] = catalog_code('C756_c_Pais', a)
    return self
def partes_transporte0(cls, node):
    return catalog_code('C592_c_ParteTransporte', node.attrib['ParteTransporte'])
def domicilio6(cls, node):
    self = ScalarMap()
    if (a := node.attrib.get('Calle')) is not None:
        self['Calle'] = a
    if (a := node.attrib.get('NumeroExterior')) is not None:
        self['NumeroExterior'] = a
    if (a := node.attrib.get('NumeroInterior')) is not None:
        self['NumeroInterior'] = a
    if (a := node.attrib.get('Colonia')) is not None:
        self['Colonia'] = a
    if (a := node.attrib.get('Localidad')) is not None:
        self['Localidad'] = a
    if (a := node.attrib.get('Referencia')) is not None:
        self['Referencia'] = a
    if (a := node.attrib.get('Municipio')) is not None:
        self['Municipio'] = a
    self['Estado'] = node.attrib['Estado']
    self['Pais'] = catalog_code('C756_c_Pais', node.attrib['Pais'])
    self['CodigoPostal'] = node.attrib['CodigoPostal']
    return self
def carta_porte2(cls, node):
    self = cls()
    self.tag = node.tag
    el = node.find('{http://www.sat.gob.mx/CartaPorte30}Ubicaciones')
    self['Ubicaciones'] = [ubicacion3(cls, n) for n in el.iterfind('{http://www.sat.gob.mx/CartaPorte30}Ubicacion')]
    el = node.find('{http://www.sat.gob.mx/CartaPorte30}Mercancias')
    self['Mercancias'] = mercancias2(cls, el)
    el = node.find('{http://www.sat.gob.mx/CartaPorte30}FiguraTransporte')
    if el is not None:
        self['FiguraTransporte'] = [tipos_figura1(cls, n) for n in el.iterfind('{http://www.sat.gob.mx/CartaPorte30}TiposFigura')]
    self['Version'] = node.attrib['Version']
    self['IdCCP'] = node.attrib['IdCCP']
    self['TranspInternac'] = node.attrib['TranspInternac']
    if (a := node.attrib.get('RegimenAduanero')) is not None:
        self['RegimenAduanero'] = catalog_code('C592_c_RegimenAduanero', a)
    if (a := node.attrib.get('EntradaSalidaMerc')) is not None:
        self['EntradaSalidaMerc'] = a
    if (a := node.attrib.get('PaisOrigenDestino')) is not None:
        self['PaisOrigenDestino'] = catalog_code('C756_c_Pais', a)
    if (a := node.attrib.get('ViaEntradaSalida')) is not None:
        self['ViaEntradaSalida'] = catalog_code('C592_c_CveTransporte', a)
    if (a := node.attrib.get('TotalDistRec')) is not None:
        self['TotalDistRec'] = Decimal(a)
    if (a := node.attrib.get('RegistroISTMO')) is not None:
        self['RegistroISTMO'] = a
    if (a := node.attrib.get('UbicacionPoloOrigen')) is not None:
        self['UbicacionPoloOrigen'] = catalog_code('C592_c_RegistroISTMO', a)
    if (a := node.attrib.get('UbicacionPoloDestino')) is not None:
        self['UbicacionPoloDestino'] = catalog_code('C592_c_RegistroISTMO', a)
    return self
def ubicacion3(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.sat.gob.mx/CartaPorte30}Domicilio')
    if el is not None:
        self['Domicilio'] = domicilio7(cls, el)
    self['TipoUbicacion'] = node.attrib['TipoUbicacion']
    if (a := node.attrib.get('IDUbicacion')) is not None:
        self['IDUbicacion'] = a
    self['RFCRemitenteDestinatario'] = node.attrib['RFCRemitenteDestinatario']
    if (a := node.attrib.get('NombreRemitenteDestinatario')) is not None:
        self['NombreRemitenteDestinatario'] = a
    if (a := node.attrib.get('NumRegIdTrib')) is not None:
        self['NumRegIdTrib'] = a
    if (a := node.attrib.get('ResidenciaFiscal')) is not None:
        self['ResidenciaFiscal'] = catalog_code('C756_c_Pais', a)
    if (a := node.attrib.get('NumEstacion')) is not None:
        self['NumEstacion'] = catalog_code('C592_c_Estaciones', a)
    if (a := node.attrib.get('NombreEstacion')) is not None:
        self['NombreEstacion'] = a
    if (a := node.attrib.get('NavegacionTrafico')) is not None:
        self['NavegacionTrafico'] = a
    self['FechaHoraSalidaLlegada'] = datetime.fromisoformat(node.attrib['FechaHoraSalidaLlegada'])
    if (a := node.attrib.get('TipoEstacion')) is not None:
        self['TipoEstacion'] = catalog_code('C592_c_TipoEstacion', a)
    if (a := node.attrib.get('DistanciaRecorrida')) is not None:
        self['DistanciaRecorrida'] = Decimal(a)
    return self
def domicilio7(cls, node):
    self = ScalarMap()
    if (a := node.attrib.get('Calle')) is not None:
        self['Calle'] = a
    if (a := node.attrib.get('NumeroExterior')) is not None:
        self['NumeroExterior'] = a
    if (a := node.attrib.get('NumeroInterior')) is not None:
        self['NumeroInterior'] = a
    if (a := node.attrib.get('Colonia')) is not None:
        self['Colonia'] = a
    if (a := node.attrib.get('Localidad')) is not None:
        self['Localidad'] = a
    if (a := node.attrib.get('Referencia')) is not None:
        self['Referencia'] = a
    if (a := node.attrib.get('Municipio')) is not None:
        self['Municipio'] = a
    self['Estado'] = node.attrib['Estado']
    self['Pais'] = catalog_code('C756_c_Pais', node.attrib['Pais'])
    self['CodigoPostal'] = node.attrib['CodigoPostal']
    return self
def mercancias2(cls, node):
    self = ScalarMap()
    self['Mercancia'] = [mercancia2(cls, n) for n in node.iterfind('{http://www.sat.gob.mx/CartaPorte30}Mercancia')]
    el = node.find('{http://www.sat.gob.mx/CartaPorte30}Autotransporte')
    if el is not None:
        self['Autotransporte'] = autotransporte1(cls, el)
    el = node.find('{http://www.sat.gob.mx/CartaPorte30}TransporteMaritimo')
    if el is not None:
        self['TransporteMaritimo'] = transporte_maritimo2(cls, el)
    el = node.find('{http://www.sat.gob.mx/CartaPorte30}TransporteAereo')
    if el is not None:
        self['TransporteAereo'] = transporte_aereo2(cls, el)
    el = node.find('{http://www.sat.gob.mx/CartaPorte30}TransporteFerroviario')
    if el is not None:
        self['TransporteFerroviario'] = transporte_ferroviario2(cls, el)
    self['PesoBrutoTotal'] = Decimal(node.attrib['PesoBrutoTotal'])
    self['UnidadPeso'] = catalog_code('C592_c_ClaveUnidadPeso', node.attrib['UnidadPeso'])
    if (a := node.attrib.get('PesoNetoTotal')) is not None:
        self['PesoNetoTotal'] = Decimal(a)
    self['NumTotalMercancias'] = Xint(node.attrib['NumTotalMercancias'])
    if (a := node.attrib.get('CargoPorTasacion')) is not None:
        self['CargoPorTasacion'] = Decimal(a)
    if (a := node.attrib.get('LogisticaInversaRecoleccionDevolucion')) is not None:
        self['LogisticaInversaRecoleccionDevolucion'] = a
    return self
def mercancia2(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.sat.gob.mx/CartaPorte30}DocumentacionAduanera')
    if el is not None:
        self['DocumentacionAduanera'] = [documentacion_aduanera0(cls, n) for n in node.iterfind('{http://www.sat.gob.mx/CartaPorte30}DocumentacionAduanera')]
    el = node.find('{http://www.sat.gob.mx/CartaPorte30}GuiasIdentificacion')
    if el is not None:
        self['GuiasIdentificacion'] = [guias_identificacion1(cls, n) for n in node.iterfind('{http://www.sat.gob.mx/CartaPorte30}GuiasIdentificacion')]
    el = node.find('{http://www.sat.gob.mx/CartaPorte30}CantidadTransporta')
    if el is not None:
        self['CantidadTransporta'] = [cantidad_transporta2(cls, n) for n in node.iterfind('{http://www.sat.gob.mx/CartaPorte30}CantidadTransporta')]
    el = node.find('{http://www.sat.gob.mx/CartaPorte30}DetalleMercancia')
    if el is not None:
        self['DetalleMercancia'] = detalle_mercancia2(cls, el)
    self['BienesTransp'] = catalog_code('C592_c_ClaveProdServCP', node.attrib['BienesTransp'])
    if (a := node.attrib.get('ClaveSTCC')) is not None:
        self['ClaveSTCC'] = a
    self['Descripcion'] = node.attrib['Descripcion']
    self['Cantidad'] = Decimal(node.attrib['Cantidad'])
    self['ClaveUnidad'] = catalog_code('C756_c_ClaveUnidad', node.attrib['ClaveUnidad'])
    if (a := node.attrib.get('Unidad')) is not None:
        self['Unidad'] = a
    if (a := node.attrib.get('Dimensiones')) is not None:
        self['Dimensiones'] = a
    if (a := node.attrib.get('MaterialPeligroso')) is not None:
        self['MaterialPeligroso'] = a
    if (a := node.attrib.get('CveMaterialPeligroso')) is not None:
        self['CveMaterialPeligroso'] = catalog_code('C592_c_MaterialPeligroso', a)
    if (a := node.attrib.get('Embalaje')) is not None:
        self['Embalaje'] = catalog_code('C592_c_TipoEmbalaje', a)
    if (a := node.attrib.get('DescripEmbalaje')) is not None:
        self['DescripEmbalaje'] = a
    if (a := node.attrib.get('SectorCOFEPRIS')) is not None:
        self['SectorCOFEPRIS'] = catalog_code('C592_c_SectorCOFEPRIS', a)
    if (a := node.attrib.get('NombreIngredienteActivo')) is not None:
        self['NombreIngredienteActivo'] = a
    if (a := node.attrib.get('NomQuimico')) is not None:
        self['NomQuimico'] = a
    if (a := node.attrib.get('DenominacionGenericaProd')) is not None:
        self['DenominacionGenericaProd'] = a
    if (a := node.attrib.get('DenominacionDistintivaProd')) is not None:
        self['DenominacionDistintivaProd'] = a
    if (a := node.attrib.get('Fabricante')) is not None:
        self['Fabricante'] = a
    if (a := node.attrib.get('FechaCaducidad')) is not None:
        self['FechaCaducidad'] = date.fromisoformat(a)
    if (a := node.attrib.get('LoteMedicamento')) is not None:
        self['LoteMedicamento'] = a
    if (a := node.attrib.get('FormaFarmaceutica')) is not None:
        self['FormaFarmaceutica'] = catalog_code('C592_c_FormaFarmaceutica', a)
    if (a := node.attrib.get('CondicionesEspTransp')) is not None:
        self['CondicionesEspTransp'] = catalog_code('C592_c_CondicionesEspeciales', a)
    if (a := node.attrib.get('RegistroSanitarioFolioAutorizacion')) is not None:
        self['RegistroSanitarioFolioAutorizacion'] = a
    if (a := node.attrib.get('PermisoImportacion')) is not None:
        self['PermisoImportacion'] = a
    if (a := node.attrib.get('FolioImpoVUCEM')) is not None:
        self['FolioImpoVUCEM'] = a
    if (a := node.attrib.get('NumCAS')) is not None:
        self['NumCAS'] = a
    if (a := node.attrib.get('RazonSocialEmpImp')) is not None:
        self['RazonSocialEmpImp'] = a
    if (a := node.attrib.get('NumRegSanPlagCOFEPRIS')) is not None:
        self['NumRegSanPlagCOFEPRIS'] = a
    if (a := node.attrib.get('DatosFabricante')) is not None:
        self['DatosFabricante'] = a
    if (a := node.attrib.get('DatosFormulador')) is not None:
        self['DatosFormulador'] = a
    if (a := node.attrib.get('DatosMaquilador')) is not None:
        self['DatosMaquilador'] = a
    if (a := node.attrib.get('UsoAutorizado')) is not None:
        self['UsoAutorizado'] = a
    self['PesoEnKg'] = Decimal(node.attrib['PesoEnKg'])
    if (a := node.attrib.get('ValorMercancia')) is not None:
        self['ValorMercancia'] = Decimal(a)
    if (a := node.attrib.get('Moneda')) is not None:
        self['Moneda'] = catalog_code('C756_c_Moneda', a, 0)
    if (a := node.attrib.get('FraccionArancelaria')) is not None:
        self['FraccionArancelaria'] = catalog_code('C5bc_c_FraccionArancelaria', a)
    if (a := node.attrib.get('UUIDComercioExt')) is not None:
        self['UUIDComercioExt'] = a
    if (a := node.attrib.get('TipoMateria')) is not None:
        self['TipoMateria'] = catalog_code('C592_c_TipoMateria', a)
    if (a := node.attrib.get('DescripcionMateria')) is not None:
        self['DescripcionMateria'] = a
    return self
def documentacion_aduanera0(cls, node):
    self = ScalarMap()
    self['TipoDocumento'] = catalog_code('C592_c_DocumentoAduanero', node.attrib['TipoDocumento'])
    if (a := node.attrib.get('NumPedimento')) is not None:
        self['NumPedimento'] = a
    if (a := node.attrib.get('IdentDocAduanero')) is not None:
        self['IdentDocAduanero'] = a
    if (a := node.attrib.get('RFCImpo')) is not None:
        self['RFCImpo'] = a
    return self
def guias_identificacion1(cls, node):
    self = ScalarMap()
    self['NumeroGuiaIdentificacion'] = node.attrib['NumeroGuiaIdentificacion']
    self['DescripGuiaIdentificacion'] = node.attrib['DescripGuiaIdentificacion']
    self['PesoGuiaIdentificacion'] = Decimal(node.attrib['PesoGuiaIdentificacion'])
    return self
def cantidad_transporta2(cls, node):
    self = ScalarMap()
    self['Cantidad'] = Decimal(node.attrib['Cantidad'])
    self['IDOrigen'] = node.attrib['IDOrigen']
    self['IDDestino'] = node.attrib['IDDestino']
    if (a := node.attrib.get('CvesTransporte')) is not None:
        self['CvesTransporte'] = catalog_code('C592_c_CveTransporte', a)
    return self
def detalle_mercancia2(cls, node):
    self = ScalarMap()
    self['UnidadPesoMerc'] = catalog_code('C592_c_ClaveUnidadPeso', node.attrib['UnidadPesoMerc'])
    self['PesoBruto'] = Decimal(node.attrib['PesoBruto'])
    self['PesoNeto'] = Decimal(node.attrib['PesoNeto'])
    self['PesoTara'] = Decimal(node.attrib['PesoTara'])
    if (a := node.attrib.get('NumPiezas')) is not None:
        self['NumPiezas'] = Xint(a)
    return self
def autotransporte1(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.sat.gob.mx/CartaPorte30}IdentificacionVehicular')
    self['IdentificacionVehicular'] = identificacion_vehicular2(cls, el)
    el = node.find('{http://www.sat.gob.mx/CartaPorte30}Seguros')
    self['Seguros'] = seguros1(cls, el)
    el = node.find('{http://www.sat.gob.mx/CartaPorte30}Remolques')
    if el is not None:
        self['Remolques'] = [remolque2(cls, n) for n in el.iterfind('{http://www.sat.gob.mx/CartaPorte30}Remolque')]
    self['PermSCT'] = catalog_code('C592_c_TipoPermiso', node.attrib['PermSCT'])
    self['NumPermisoSCT'] = node.attrib['NumPermisoSCT']
    return self
def identificacion_vehicular2(cls, node):
    self = ScalarMap()
    self['ConfigVehicular'] = catalog_code('C592_c_ConfigAutotransporte', node.attrib['ConfigVehicular'])
    self['PesoBrutoVehicular'] = Decimal(node.attrib['PesoBrutoVehicular'])
    self['PlacaVM'] = node.attrib['PlacaVM']
    self['AnioModeloVM'] = Xint(node.attrib['AnioModeloVM'])
    return self
def seguros1(cls, node):
    self = ScalarMap()
    self['AseguraRespCivil'] = node.attrib['AseguraRespCivil']
    self['PolizaRespCivil'] = node.attrib['PolizaRespCivil']
    if (a := node.attrib.get('AseguraMedAmbiente')) is not None:
        self['AseguraMedAmbiente'] = a
    if (a := node.attrib.get('PolizaMedAmbiente')) is not None:
        self['PolizaMedAmbiente'] = a
    if (a := node.attrib.get('AseguraCarga')) is not None:
        self['AseguraCarga'] = a
    if (a := node.attrib.get('PolizaCarga')) is not None:
        self['PolizaCarga'] = a
    if (a := node.attrib.get('PrimaSeguro')) is not None:
        self['PrimaSeguro'] = Decimal(a)
    return self
def remolque2(cls, node):
    self = ScalarMap()
    self['SubTipoRem'] = catalog_code('C592_c_SubTipoRem', node.attrib['SubTipoRem'])
    self['Placa'] = node.attrib['Placa']
    return self
def transporte_maritimo2(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.sat.gob.mx/CartaPorte30}Contenedor')
    if el is not None:
        self['Contenedor'] = [contenedor4(cls, n) for n in node.iterfind('{http://www.sat.gob.mx/CartaPorte30}Contenedor')]
    el = node.find('{http://www.sat.gob.mx/CartaPorte30}RemolquesCCP')
    if el is not None:
        self['RemolquesCCP'] = [remolque_ccp0(cls, n) for n in el.iterfind('{http://www.sat.gob.mx/CartaPorte30}RemolqueCCP')]
    if (a := node.attrib.get('PermSCT')) is not None:
        self['PermSCT'] = catalog_code('C592_c_TipoPermiso', a)
    if (a := node.attrib.get('NumPermisoSCT')) is not None:
        self['NumPermisoSCT'] = a
    if (a := node.attrib.get('NombreAseg')) is not None:
        self['NombreAseg'] = a
    if (a := node.attrib.get('NumPolizaSeguro')) is not None:
        self['NumPolizaSeguro'] = a
    self['TipoEmbarcacion'] = catalog_code('C592_c_ConfigMaritima', node.attrib['TipoEmbarcacion'])
    self['Matricula'] = node.attrib['Matricula']
    self['NumeroOMI'] = node.attrib['NumeroOMI']
    if (a := node.attrib.get('AnioEmbarcacion')) is not None:
        self['AnioEmbarcacion'] = Xint(a)
    if (a := node.attrib.get('NombreEmbarc')) is not None:
        self['NombreEmbarc'] = a
    self['NacionalidadEmbarc'] = catalog_code('C756_c_Pais', node.attrib['NacionalidadEmbarc'])
    self['UnidadesDeArqBruto'] = Decimal(node.attrib['UnidadesDeArqBruto'])
    self['TipoCarga'] = catalog_code('C592_c_ClaveTipoCarga', node.attrib['TipoCarga'])
    if (a := node.attrib.get('Eslora')) is not None:
        self['Eslora'] = Decimal(a)
    if (a := node.attrib.get('Manga')) is not None:
        self['Manga'] = Decimal(a)
    if (a := node.attrib.get('Calado')) is not None:
        self['Calado'] = Decimal(a)
    if (a := node.attrib.get('Puntal')) is not None:
        self['Puntal'] = Decimal(a)
    if (a := node.attrib.get('LineaNaviera')) is not None:
        self['LineaNaviera'] = a
    self['NombreAgenteNaviero'] = node.attrib['NombreAgenteNaviero']
    self['NumAutorizacionNaviero'] = node.attrib['NumAutorizacionNaviero']
    if (a := node.attrib.get('NumViaje')) is not None:
        self['NumViaje'] = a
    if (a := node.attrib.get('NumConocEmbarc')) is not None:
        self['NumConocEmbarc'] = a
    if (a := node.attrib.get('PermisoTempNavegacion')) is not None:
        self['PermisoTempNavegacion'] = a
    return self
def contenedor4(cls, node):
    self = ScalarMap()
    self['TipoContenedor'] = catalog_code('C592_c_ContenedorMaritimo', node.attrib['TipoContenedor'])
    if (a := node.attrib.get('MatriculaContenedor')) is not None:
        self['MatriculaContenedor'] = a
    if (a := node.attrib.get('NumPrecinto')) is not None:
        self['NumPrecinto'] = a
    if (a := node.attrib.get('IdCCPRelacionado')) is not None:
        self['IdCCPRelacionado'] = a
    if (a := node.attrib.get('PlacaVMCCP')) is not None:
        self['PlacaVMCCP'] = a
    if (a := node.attrib.get('FechaCertificacionCCP')) is not None:
        self['FechaCertificacionCCP'] = datetime.fromisoformat(a)
    return self
def remolque_ccp0(cls, node):
    self = ScalarMap()
    self['SubTipoRemCCP'] = catalog_code('C592_c_SubTipoRem', node.attrib['SubTipoRemCCP'])
    self['PlacaCCP'] = node.attrib['PlacaCCP']
    return self
def transporte_aereo2(cls, node):
    self = ScalarMap()
    self['PermSCT'] = catalog_code('C592_c_TipoPermiso', node.attrib['PermSCT'])
    self['NumPermisoSCT'] = node.attrib['NumPermisoSCT']
    if (a := node.attrib.get('MatriculaAeronave')) is not None:
        self['MatriculaAeronave'] = a
    if (a := node.attrib.get('NombreAseg')) is not None:
        self['NombreAseg'] = a
    if (a := node.attrib.get('NumPolizaSeguro')) is not None:
        self['NumPolizaSeguro'] = a
    self['NumeroGuia'] = node.attrib['NumeroGuia']
    if (a := node.attrib.get('LugarContrato')) is not None:
        self['LugarContrato'] = a
    self['CodigoTransportista'] = catalog_code('C592_c_CodigoTransporteAereo', node.attrib['CodigoTransportista'])
    if (a := node.attrib.get('RFCEmbarcador')) is not None:
        self['RFCEmbarcador'] = a
    if (a := node.attrib.get('NumRegIdTribEmbarc')) is not None:
        self['NumRegIdTribEmbarc'] = a
    if (a := node.attrib.get('ResidenciaFiscalEmbarc')) is not None:
        self['ResidenciaFiscalEmbarc'] = catalog_code('C756_c_Pais', a)
    if (a := node.attrib.get('NombreEmbarcador')) is not None:
        self['NombreEmbarcador'] = a
    return self
def transporte_ferroviario2(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.sat.gob.mx/CartaPorte30}DerechosDePaso')
    if el is not None:
        self['DerechosDePaso'] = [derechos_de_paso2(cls, n) for n in node.iterfind('{http://www.sat.gob.mx/CartaPorte30}DerechosDePaso')]
    self['Carro'] = [carro2(cls, n) for n in node.iterfind('{http://www.sat.gob.mx/CartaPorte30}Carro')]
    self['TipoDeServicio'] = catalog_code('C592_c_TipoDeServicio', node.attrib['TipoDeServicio'])
    self['TipoDeTrafico'] = catalog_code('C592_c_TipoDeTrafico', node.attrib['TipoDeTrafico'])
    if (a := node.attrib.get('NombreAseg')) is not None:
        self['NombreAseg'] = a
    if (a := node.attrib.get('NumPolizaSeguro')) is not None:
        self['NumPolizaSeguro'] = a
    return self
def derechos_de_paso2(cls, node):
    self = ScalarMap()
    self['TipoDerechoDePaso'] = catalog_code('C592_c_DerechosDePaso', node.attrib['TipoDerechoDePaso'])
    self['KilometrajePagado'] = Decimal(node.attrib['KilometrajePagado'])
    return self
def carro2(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.sat.gob.mx/CartaPorte30}Contenedor')
    if el is not None:
        self['Contenedor'] = [contenedor5(cls, n) for n in node.iterfind('{http://www.sat.gob.mx/CartaPorte30}Contenedor')]
    self['TipoCarro'] = catalog_code('C592_c_TipoCarro', node.attrib['TipoCarro'])
    self['MatriculaCarro'] = node.attrib['MatriculaCarro']
    self['GuiaCarro'] = node.attrib['GuiaCarro']
    self['ToneladasNetasCarro'] = Decimal(node.attrib['ToneladasNetasCarro'])
    return self
def contenedor5(cls, node):
    self = ScalarMap()
    self['TipoContenedor'] = catalog_code('C592_c_Contenedor', node.attrib['TipoContenedor'])
    self['PesoContenedorVacio'] = Decimal(node.attrib['PesoContenedorVacio'])
    self['PesoNetoMercancia'] = Decimal(node.attrib['PesoNetoMercancia'])
    return self
def tipos_figura1(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.sat.gob.mx/CartaPorte30}PartesTransporte')
    if el is not None:
        self['PartesTransporte'] = [partes_transporte1(cls, n) for n in node.iterfind('{http://www.sat.gob.mx/CartaPorte30}PartesTransporte')]
    el = node.find('{http://www.sat.gob.mx/CartaPorte30}Domicilio')
    if el is not None:
        self['Domicilio'] = domicilio8(cls, el)
    self['TipoFigura'] = catalog_code('C592_c_FiguraTransporte', node.attrib['TipoFigura'])
    if (a := node.attrib.get('RFCFigura')) is not None:
        self['RFCFigura'] = a
    if (a := node.attrib.get('NumLicencia')) is not None:
        self['NumLicencia'] = a
    self['NombreFigura'] = node.attrib['NombreFigura']
    if (a := node.attrib.get('NumRegIdTribFigura')) is not None:
        self['NumRegIdTribFigura'] = a
    if (a := node.attrib.get('ResidenciaFiscalFigura')) is not None:
        self['ResidenciaFiscalFigura'] = catalog_code('C756_c_Pais', a)
    return self
def partes_transporte1(cls, node):
    return catalog_code('C592_c_ParteTransporte', node.attrib['ParteTransporte'])
def domicilio8(cls, node):
    self = ScalarMap()
    if (a := node.attrib.get('Calle')) is not None:
        self['Calle'] = a
    if (a := node.attrib.get('NumeroExterior')) is not None:
        self['NumeroExterior'] = a
    if (a := node.attrib.get('NumeroInterior')) is not None:
        self['NumeroInterior'] = a
    if (a := node.attrib.get('Colonia')) is not None:
        self['Colonia'] = a
    if (a := node.attrib.get('Localidad')) is not None:
        self['Localidad'] = a
    if (a := node.attrib.get('Referencia')) is not None:
        self['Referencia'] = a
    if (a := node.attrib.get('Municipio')) is not None:
        self['Municipio'] = a
    self['Estado'] = node.attrib['Estado']
    self['Pais'] = catalog_code('C756_c_Pais', node.attrib['Pais'])
    self['CodigoPostal'] = node.attrib['CodigoPostal']
    return self
def carta_porte3(cls, node):
    self = cls()
    self.tag = node.tag
    el = node.find('{http://www.sat.gob.mx/CartaPorte31}RegimenesAduaneros')
    if el is not None:
        self['RegimenesAduaneros'] = [regimen_aduanero_ccp0(cls, n) for n in el.iterfind('{http://www.sat.gob.mx/CartaPorte31}RegimenAduaneroCCP')]
    el = node.find('{http://www.sat.gob.mx/CartaPorte31}Ubicaciones')
    self['Ubicaciones'] = [ubicacion4(cls, n) for n in el.iterfind('{http://www.sat.gob.mx/CartaPorte31}Ubicacion')]
    el = node.find('{http://www.sat.gob.mx/CartaPorte31}Mercancias')
    self['Mercancias'] = mercancias3(cls, el)
    el = node.find('{http://www.sat.gob.mx/CartaPorte31}FiguraTransporte')
    if el is not None:
        self['FiguraTransporte'] = [tipos_figura2(cls, n) for n in el.iterfind('{http://www.sat.gob.mx/CartaPorte31}TiposFigura')]
    self['Version'] = node.attrib['Version']
    self['IdCCP'] = node.attrib['IdCCP']
    self['TranspInternac'] = node.attrib['TranspInternac']
    if (a := node.attrib.get('EntradaSalidaMerc')) is not None:
        self['EntradaSalidaMerc'] = a
    if (a := node.attrib.get('PaisOrigenDestino')) is not None:
        self['PaisOrigenDestino'] = catalog_code('C756_c_Pais', a)
    if (a := node.attrib.get('ViaEntradaSalida')) is not None:
        self['ViaEntradaSalida'] = catalog_code('C592_c_CveTransporte', a)
    if (a := node.attrib.get('TotalDistRec')) is not None:
        self['TotalDistRec'] = Decimal(a)
    if (a := node.attrib.get('RegistroISTMO')) is not None:
        self['RegistroISTMO'] = a
    if (a := node.attrib.get('UbicacionPoloOrigen')) is not None:
        self['UbicacionPoloOrigen'] = catalog_code('C592_c_RegistroISTMO', a)
    if (a := node.attrib.get('UbicacionPoloDestino')) is not None:
        self['UbicacionPoloDestino'] = catalog_code('C592_c_RegistroISTMO', a)
    return self
def regimen_aduanero_ccp0(cls, node):
    return catalog_code('C592_c_RegimenAduanero', node.attrib['RegimenAduanero'])
def ubicacion4(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.sat.gob.mx/CartaPorte31}Domicilio')
    if el is not None:
        self['Domicilio'] = domicilio9(cls, el)
    self['TipoUbicacion'] = node.attrib['TipoUbicacion']
    if (a := node.attrib.get('IDUbicacion')) is not None:
        self['IDUbicacion'] = a
    self['RFCRemitenteDestinatario'] = node.attrib['RFCRemitenteDestinatario']
    if (a := node.attrib.get('NombreRemitenteDestinatario')) is not None:
        self['NombreRemitenteDestinatario'] = a
    if (a := node.attrib.get('NumRegIdTrib')) is not None:
        self['NumRegIdTrib'] = a
    if (a := node.attrib.get('ResidenciaFiscal')) is not None:
        self['ResidenciaFiscal'] = catalog_code('C756_c_Pais', a)
    if (a := node.attrib.get('NumEstacion')) is not None:
        self['NumEstacion'] = catalog_code('C592_c_Estaciones', a)
    if (a := node.attrib.get('NombreEstacion')) is not None:
        self['NombreEstacion'] = a
    if (a := node.attrib.get('NavegacionTrafico')) is not None:
        self['NavegacionTrafico'] = a
    self['FechaHoraSalidaLlegada'] = datetime.fromisoformat(node.attrib['FechaHoraSalidaLlegada'])
    if (a := node.attrib.get('TipoEstacion')) is not None:
        self['TipoEstacion'] = catalog_code('C592_c_TipoEstacion', a)
    if (a := node.attrib.get('DistanciaRecorrida')) is not None:
        self['DistanciaRecorrida'] = Decimal(a)
    return self
def domicilio9(cls, node):
    self = ScalarMap()
    if (a := node.attrib.get('Calle')) is not None:
        self['Calle'] = a
    if (a := node.attrib.get('NumeroExterior')) is not None:
        self['NumeroExterior'] = a
    if (a := node.attrib.get('NumeroInterior')) is not None:
        self['NumeroInterior'] = a
    if (a := node.attrib.get('Colonia')) is not None:
        self['Colonia'] = a
    if (a := node.attrib.get('Localidad')) is not None:
        self['Localidad'] = a
    if (a := node.attrib.get('Referencia')) is not None:
        self['Referencia'] = a
    if (a := node.attrib.get('Municipio')) is not None:
        self['Municipio'] = a
    self['Estado'] = node.attrib['Estado']
    self['Pais'] = catalog_code('C756_c_Pais', node.attrib['Pais'])
    self['CodigoPostal'] = node.attrib['CodigoPostal']
    return self
def mercancias3(cls, node):
    self = ScalarMap()
    self['Mercancia'] = [mercancia3(cls, n) for n in node.iterfind('{http://www.sat.gob.mx/CartaPorte31}Mercancia')]
    el = node.find('{http://www.sat.gob.mx/CartaPorte31}Autotransporte')
    if el is not None:
        self['Autotransporte'] = autotransporte2(cls, el)
    el = node.find('{http://www.sat.gob.mx/CartaPorte31}TransporteMaritimo')
    if el is not None:
        self['TransporteMaritimo'] = transporte_maritimo3(cls, el)
    el = node.find('{http://www.sat.gob.mx/CartaPorte31}TransporteAereo')
    if el is not None:
        self['TransporteAereo'] = transporte_aereo3(cls, el)
    el = node.find('{http://www.sat.gob.mx/CartaPorte31}TransporteFerroviario')
    if el is not None:
        self['TransporteFerroviario'] = transporte_ferroviario3(cls, el)
    self['PesoBrutoTotal'] = Decimal(node.attrib['PesoBrutoTotal'])
    self['UnidadPeso'] = catalog_code('C592_c_ClaveUnidadPeso', node.attrib['UnidadPeso'])
    if (a := node.attrib.get('PesoNetoTotal')) is not None:
        self['PesoNetoTotal'] = Decimal(a)
    self['NumTotalMercancias'] = Xint(node.attrib['NumTotalMercancias'])
    if (a := node.attrib.get('CargoPorTasacion')) is not None:
        self['CargoPorTasacion'] = Decimal(a)
    if (a := node.attrib.get('LogisticaInversaRecoleccionDevolucion')) is not None:
        self['LogisticaInversaRecoleccionDevolucion'] = a
    return self
def mercancia3(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.sat.gob.mx/CartaPorte31}DocumentacionAduanera')
    if el is not None:
        self['DocumentacionAduanera'] = [documentacion_aduanera1(cls, n) for n in node.iterfind('{http://www.sat.gob.mx/CartaPorte31}DocumentacionAduanera')]
    el = node.find('{http://www.sat.gob.mx/CartaPorte31}GuiasIdentificacion')
    if el is not None:
        self['GuiasIdentificacion'] = [guias_identificacion2(cls, n) for n in node.iterfind('{http://www.sat.gob.mx/CartaPorte31}GuiasIdentificacion')]
    el = node.find('{http://www.sat.gob.mx/CartaPorte31}CantidadTransporta')
    if el is not None:
        self['CantidadTransporta'] = [cantidad_transporta3(cls, n) for n in node.iterfind('{http://www.sat.gob.mx/CartaPorte31}CantidadTransporta')]
    el = node.find('{http://www.sat.gob.mx/CartaPorte31}DetalleMercancia')
    if el is not None:
        self['DetalleMercancia'] = detalle_mercancia3(cls, el)
    self['BienesTransp'] = catalog_code('C592_c_ClaveProdServCP', node.attrib['BienesTransp'])
    if (a := node.attrib.get('ClaveSTCC')) is not None:
        self['ClaveSTCC'] = a
    self['Descripcion'] = node.attrib['Descripcion']
    self['Cantidad'] = Decimal(node.attrib['Cantidad'])
    self['ClaveUnidad'] = catalog_code('C756_c_ClaveUnidad', node.attrib['ClaveUnidad'])
    if (a := node.attrib.get('Unidad')) is not None:
        self['Unidad'] = a
    if (a := node.attrib.get('Dimensiones')) is not None:
        self['Dimensiones'] = a
    if (a := node.attrib.get('MaterialPeligroso')) is not None:
        self['MaterialPeligroso'] = a
    if (a := node.attrib.get('CveMaterialPeligroso')) is not None:
        self['CveMaterialPeligroso'] = catalog_code('C592_c_MaterialPeligroso', a)
    if (a := node.attrib.get('Embalaje')) is not None:
        self['Embalaje'] = catalog_code('C592_c_TipoEmbalaje', a)
    if (a := node.attrib.get('DescripEmbalaje')) is not None:
        self['DescripEmbalaje'] = a
    if (a := node.attrib.get('SectorCOFEPRIS')) is not None:
        self['SectorCOFEPRIS'] = catalog_code('C592_c_SectorCOFEPRIS', a)
    if (a := node.attrib.get('NombreIngredienteActivo')) is not None:
        self['NombreIngredienteActivo'] = a
    if (a := node.attrib.get('NomQuimico')) is not None:
        self['NomQuimico'] = a
    if (a := node.attrib.get('DenominacionGenericaProd')) is not None:
        self['DenominacionGenericaProd'] = a
    if (a := node.attrib.get('DenominacionDistintivaProd')) is not None:
        self['DenominacionDistintivaProd'] = a
    if (a := node.attrib.get('Fabricante')) is not None:
        self['Fabricante'] = a
    if (a := node.attrib.get('FechaCaducidad')) is not None:
        self['FechaCaducidad'] = date.fromisoformat(a)
    if (a := node.attrib.get('LoteMedicamento')) is not None:
        self['LoteMedicamento'] = a
    if (a := node.attrib.get('FormaFarmaceutica')) is not None:
        self['FormaFarmaceutica'] = catalog_code('C592_c_FormaFarmaceutica', a)
    if (a := node.attrib.get('CondicionesEspTransp')) is not None:
        self['CondicionesEspTransp'] = catalog_code('C592_c_CondicionesEspeciales', a)
    if (a := node.attrib.get('RegistroSanitarioFolioAutorizacion')) is not None:
        self['RegistroSanitarioFolioAutorizacion'] = a
    if (a := node.attrib.get('PermisoImportacion')) is not None:
        self['PermisoImportacion'] = a
    if (a := node.attrib.get('FolioImpoVUCEM')) is not None:
        self['FolioImpoVUCEM'] = a
    if (a := node.attrib.get('NumCAS')) is not None:
        self['NumCAS'] = a
    if (a := node.attrib.get('RazonSocialEmpImp')) is not None:
        self['RazonSocialEmpImp'] = a
    if (a := node.attrib.get('NumRegSanPlagCOFEPRIS')) is not None:
        self['NumRegSanPlagCOFEPRIS'] = a
    if (a := node.attrib.get('DatosFabricante')) is not None:
        self['DatosFabricante'] = a
    if (a := node.attrib.get('DatosFormulador')) is not None:
        self['DatosFormulador'] = a
    if (a := node.attrib.get('DatosMaquilador')) is not None:
        self['DatosMaquilador'] = a
    if (a := node.attrib.get('UsoAutorizado')) is not None:
        self['UsoAutorizado'] = a
    self['PesoEnKg'] = Decimal(node.attrib['PesoEnKg'])
    if (a := node.attrib.get('ValorMercancia')) is not None:
        self['ValorMercancia'] = Decimal(a)
    if (a := node.attrib.get('Moneda')) is not None:
        self['Moneda'] = catalog_code('C756_c_Moneda', a, 0)
    if (a := node.attrib.get('FraccionArancelaria')) is not None:
        self['FraccionArancelaria'] = catalog_code('C5bc_c_FraccionArancelaria', a)
    if (a := node.attrib.get('UUIDComercioExt')) is not None:
        self['UUIDComercioExt'] = a
    if (a := node.attrib.get('TipoMateria')) is not None:
        self['TipoMateria'] = catalog_code('C592_c_TipoMateria', a)
    if (a := node.attrib.get('DescripcionMateria')) is not None:
        self['DescripcionMateria'] = a
    return self
def documentacion_aduanera1(cls, node):
    self = ScalarMap()
    self['TipoDocumento'] = catalog_code('C592_c_DocumentoAduanero', node.attrib['TipoDocumento'])
    if (a := node.attrib.get('NumPedimento')) is not None:
        self['NumPedimento'] = a
    if (a := node.attrib.get('IdentDocAduanero')) is not None:
        self['IdentDocAduanero'] = a
    if (a := node.attrib.get('RFCImpo')) is not None:
        self['RFCImpo'] = a
    return self
def guias_identificacion2(cls, node):
    self = ScalarMap()
    self['NumeroGuiaIdentificacion'] = node.attrib['NumeroGuiaIdentificacion']
    self['DescripGuiaIdentificacion'] = node.attrib['DescripGuiaIdentificacion']
    self['PesoGuiaIdentificacion'] = Decimal(node.attrib['PesoGuiaIdentificacion'])
    return self
def cantidad_transporta3(cls, node):
    self = ScalarMap()
    self['Cantidad'] = Decimal(node.attrib['Cantidad'])
    self['IDOrigen'] = node.attrib['IDOrigen']
    self['IDDestino'] = node.attrib['IDDestino']
    if (a := node.attrib.get('CvesTransporte')) is not None:
        self['CvesTransporte'] = catalog_code('C592_c_CveTransporte', a)
    return self
def detalle_mercancia3(cls, node):
    self = ScalarMap()
    self['UnidadPesoMerc'] = catalog_code('C592_c_ClaveUnidadPeso', node.attrib['UnidadPesoMerc'])
    self['PesoBruto'] = Decimal(node.attrib['PesoBruto'])
    self['PesoNeto'] = Decimal(node.attrib['PesoNeto'])
    self['PesoTara'] = Decimal(node.attrib['PesoTara'])
    if (a := node.attrib.get('NumPiezas')) is not None:
        self['NumPiezas'] = Xint(a)
    return self
def autotransporte2(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.sat.gob.mx/CartaPorte31}IdentificacionVehicular')
    self['IdentificacionVehicular'] = identificacion_vehicular3(cls, el)
    el = node.find('{http://www.sat.gob.mx/CartaPorte31}Seguros')
    self['Seguros'] = seguros2(cls, el)
    el = node.find('{http://www.sat.gob.mx/CartaPorte31}Remolques')
    if el is not None:
        self['Remolques'] = [remolque3(cls, n) for n in el.iterfind('{http://www.sat.gob.mx/CartaPorte31}Remolque')]
    self['PermSCT'] = catalog_code('C592_c_TipoPermiso', node.attrib['PermSCT'])
    self['NumPermisoSCT'] = node.attrib['NumPermisoSCT']
    return self
def identificacion_vehicular3(cls, node):
    self = ScalarMap()
    self['ConfigVehicular'] = catalog_code('C592_c_ConfigAutotransporte', node.attrib['ConfigVehicular'])
    self['PesoBrutoVehicular'] = Decimal(node.attrib['PesoBrutoVehicular'])
    self['PlacaVM'] = node.attrib['PlacaVM']
    self['AnioModeloVM'] = Xint(node.attrib['AnioModeloVM'])
    return self
def seguros2(cls, node):
    self = ScalarMap()
    self['AseguraRespCivil'] = node.attrib['AseguraRespCivil']
    self['PolizaRespCivil'] = node.attrib['PolizaRespCivil']
    if (a := node.attrib.get('AseguraMedAmbiente')) is not None:
        self['AseguraMedAmbiente'] = a
    if (a := node.attrib.get('PolizaMedAmbiente')) is not None:
        self['PolizaMedAmbiente'] = a
    if (a := node.attrib.get('AseguraCarga')) is not None:
        self['AseguraCarga'] = a
    if (a := node.attrib.get('PolizaCarga')) is not None:
        self['PolizaCarga'] = a
    if (a := node.attrib.get('PrimaSeguro')) is not None:
        self['PrimaSeguro'] = Decimal(a)
    return self
def remolque3(cls, node):
    self = ScalarMap()
    self['SubTipoRem'] = catalog_code('C592_c_SubTipoRem', node.attrib['SubTipoRem'])
    self['Placa'] = node.attrib['Placa']
    return self
def transporte_maritimo3(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.sat.gob.mx/CartaPorte31}Contenedor')
    if el is not None:
        self['Contenedor'] = [contenedor6(cls, n) for n in node.iterfind('{http://www.sat.gob.mx/CartaPorte31}Contenedor')]
    if (a := node.attrib.get('PermSCT')) is not None:
        self['PermSCT'] = catalog_code('C592_c_TipoPermiso', a)
    if (a := node.attrib.get('NumPermisoSCT')) is not None:
        self['NumPermisoSCT'] = a
    if (a := node.attrib.get('NombreAseg')) is not None:
        self['NombreAseg'] = a
    if (a := node.attrib.get('NumPolizaSeguro')) is not None:
        self['NumPolizaSeguro'] = a
    self['TipoEmbarcacion'] = catalog_code('C592_c_ConfigMaritima', node.attrib['TipoEmbarcacion'])
    self['Matricula'] = node.attrib['Matricula']
    self['NumeroOMI'] = node.attrib['NumeroOMI']
    if (a := node.attrib.get('AnioEmbarcacion')) is not None:
        self['AnioEmbarcacion'] = Xint(a)
    if (a := node.attrib.get('NombreEmbarc')) is not None:
        self['NombreEmbarc'] = a
    self['NacionalidadEmbarc'] = catalog_code('C756_c_Pais', node.attrib['NacionalidadEmbarc'])
    self['UnidadesDeArqBruto'] = Decimal(node.attrib['UnidadesDeArqBruto'])
    self['TipoCarga'] = catalog_code('C592_c_ClaveTipoCarga', node.attrib['TipoCarga'])
    if (a := node.attrib.get('Eslora')) is not None:
        self['Eslora'] = Decimal(a)
    if (a := node.attrib.get('Manga')) is not None:
        self['Manga'] = Decimal(a)
    if (a := node.attrib.get('Calado')) is not None:
        self['Calado'] = Decimal(a)
    if (a := node.attrib.get('Puntal')) is not None:
        self['Puntal'] = Decimal(a)
    if (a := node.attrib.get('LineaNaviera')) is not None:
        self['LineaNaviera'] = a
    self['NombreAgenteNaviero'] = node.attrib['NombreAgenteNaviero']
    self['NumAutorizacionNaviero'] = node.attrib['NumAutorizacionNaviero']
    if (a := node.attrib.get('NumViaje')) is not None:
        self['NumViaje'] = a
    if (a := node.attrib.get('NumConocEmbarc')) is not None:
        self['NumConocEmbarc'] = a
    if (a := node.attrib.get('PermisoTempNavegacion')) is not None:
        self['PermisoTempNavegacion'] = a
    return self
def contenedor6(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.sat.gob.mx/CartaPorte31}RemolquesCCP')
    if el is not None:
        self['RemolquesCCP'] = [remolque_ccp1(cls, n) for n in el.iterfind('{http://www.sat.gob.mx/CartaPorte31}RemolqueCCP')]
    self['TipoContenedor'] = catalog_code('C592_c_ContenedorMaritimo', node.attrib['TipoContenedor'])
    if (a := node.attrib.get('MatriculaContenedor')) is not None:
        self['MatriculaContenedor'] = a
    if (a := node.attrib.get('NumPrecinto')) is not None:
        self['NumPrecinto'] = a
    if (a := node.attrib.get('IdCCPRelacionado')) is not None:
        self['IdCCPRelacionado'] = a
    if (a := node.attrib.get('PlacaVMCCP')) is not None:
        self['PlacaVMCCP'] = a
    if (a := node.attrib.get('FechaCertificacionCCP')) is not None:
        self['FechaCertificacionCCP'] = datetime.fromisoformat(a)
    return self
def remolque_ccp1(cls, node):
    self = ScalarMap()
    self['SubTipoRemCCP'] = catalog_code('C592_c_SubTipoRem', node.attrib['SubTipoRemCCP'])
    self['PlacaCCP'] = node.attrib['PlacaCCP']
    return self
def transporte_aereo3(cls, node):
    self = ScalarMap()
    self['PermSCT'] = catalog_code('C592_c_TipoPermiso', node.attrib['PermSCT'])
    self['NumPermisoSCT'] = node.attrib['NumPermisoSCT']
    if (a := node.attrib.get('MatriculaAeronave')) is not None:
        self['MatriculaAeronave'] = a
    if (a := node.attrib.get('NombreAseg')) is not None:
        self['NombreAseg'] = a
    if (a := node.attrib.get('NumPolizaSeguro')) is not None:
        self['NumPolizaSeguro'] = a
    self['NumeroGuia'] = node.attrib['NumeroGuia']
    if (a := node.attrib.get('LugarContrato')) is not None:
        self['LugarContrato'] = a
    self['CodigoTransportista'] = catalog_code('C592_c_CodigoTransporteAereo', node.attrib['CodigoTransportista'])
    if (a := node.attrib.get('RFCEmbarcador')) is not None:
        self['RFCEmbarcador'] = a
    if (a := node.attrib.get('NumRegIdTribEmbarc')) is not None:
        self['NumRegIdTribEmbarc'] = a
    if (a := node.attrib.get('ResidenciaFiscalEmbarc')) is not None:
        self['ResidenciaFiscalEmbarc'] = catalog_code('C756_c_Pais', a)
    if (a := node.attrib.get('NombreEmbarcador')) is not None:
        self['NombreEmbarcador'] = a
    return self
def transporte_ferroviario3(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.sat.gob.mx/CartaPorte31}DerechosDePaso')
    if el is not None:
        self['DerechosDePaso'] = [derechos_de_paso3(cls, n) for n in node.iterfind('{http://www.sat.gob.mx/CartaPorte31}DerechosDePaso')]
    self['Carro'] = [carro3(cls, n) for n in node.iterfind('{http://www.sat.gob.mx/CartaPorte31}Carro')]
    self['TipoDeServicio'] = catalog_code('C592_c_TipoDeServicio', node.attrib['TipoDeServicio'])
    self['TipoDeTrafico'] = catalog_code('C592_c_TipoDeTrafico', node.attrib['TipoDeTrafico'])
    if (a := node.attrib.get('NombreAseg')) is not None:
        self['NombreAseg'] = a
    if (a := node.attrib.get('NumPolizaSeguro')) is not None:
        self['NumPolizaSeguro'] = a
    return self
def derechos_de_paso3(cls, node):
    self = ScalarMap()
    self['TipoDerechoDePaso'] = catalog_code('C592_c_DerechosDePaso', node.attrib['TipoDerechoDePaso'])
    self['KilometrajePagado'] = Decimal(node.attrib['KilometrajePagado'])
    return self
def carro3(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.sat.gob.mx/CartaPorte31}Contenedor')
    if el is not None:
        self['Contenedor'] = [contenedor7(cls, n) for n in node.iterfind('{http://www.sat.gob.mx/CartaPorte31}Contenedor')]
    self['TipoCarro'] = catalog_code('C592_c_TipoCarro', node.attrib['TipoCarro'])
    self['MatriculaCarro'] = node.attrib['MatriculaCarro']
    self['GuiaCarro'] = node.attrib['GuiaCarro']
    self['ToneladasNetasCarro'] = Decimal(node.attrib['ToneladasNetasCarro'])
    return self
def contenedor7(cls, node):
    self = ScalarMap()
    self['TipoContenedor'] = catalog_code('C592_c_Contenedor', node.attrib['TipoContenedor'])
    self['PesoContenedorVacio'] = Decimal(node.attrib['PesoContenedorVacio'])
    self['PesoNetoMercancia'] = Decimal(node.attrib['PesoNetoMercancia'])
    return self
def tipos_figura2(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.sat.gob.mx/CartaPorte31}PartesTransporte')
    if el is not None:
        self['PartesTransporte'] = [partes_transporte2(cls, n) for n in node.iterfind('{http://www.sat.gob.mx/CartaPorte31}PartesTransporte')]
    el = node.find('{http://www.sat.gob.mx/CartaPorte31}Domicilio')
    if el is not None:
        self['Domicilio'] = domicilioa(cls, el)
    self['TipoFigura'] = catalog_code('C592_c_FiguraTransporte', node.attrib['TipoFigura'])
    if (a := node.attrib.get('RFCFigura')) is not None:
        self['RFCFigura'] = a
    if (a := node.attrib.get('NumLicencia')) is not None:
        self['NumLicencia'] = a
    self['NombreFigura'] = node.attrib['NombreFigura']
    if (a := node.attrib.get('NumRegIdTribFigura')) is not None:
        self['NumRegIdTribFigura'] = a
    if (a := node.attrib.get('ResidenciaFiscalFigura')) is not None:
        self['ResidenciaFiscalFigura'] = catalog_code('C756_c_Pais', a)
    return self
def partes_transporte2(cls, node):
    return catalog_code('C592_c_ParteTransporte', node.attrib['ParteTransporte'])
def domicilioa(cls, node):
    self = ScalarMap()
    if (a := node.attrib.get('Calle')) is not None:
        self['Calle'] = a
    if (a := node.attrib.get('NumeroExterior')) is not None:
        self['NumeroExterior'] = a
    if (a := node.attrib.get('NumeroInterior')) is not None:
        self['NumeroInterior'] = a
    if (a := node.attrib.get('Colonia')) is not None:
        self['Colonia'] = a
    if (a := node.attrib.get('Localidad')) is not None:
        self['Localidad'] = a
    if (a := node.attrib.get('Referencia')) is not None:
        self['Referencia'] = a
    if (a := node.attrib.get('Municipio')) is not None:
        self['Municipio'] = a
    self['Estado'] = node.attrib['Estado']
    self['Pais'] = catalog_code('C756_c_Pais', node.attrib['Pais'])
    self['CodigoPostal'] = node.attrib['CodigoPostal']
    return self
def comercio_exterior0(cls, node):
    self = cls()
    self.tag = node.tag
    el = node.find('{http://www.sat.gob.mx/ComercioExterior11}Emisor')
    if el is not None:
        self['Emisor'] = emisor6(cls, el)
    el = node.find('{http://www.sat.gob.mx/ComercioExterior11}Propietario')
    if el is not None:
        self['Propietario'] = [propietario1(cls, n) for n in node.iterfind('{http://www.sat.gob.mx/ComercioExterior11}Propietario')]
    el = node.find('{http://www.sat.gob.mx/ComercioExterior11}Receptor')
    if el is not None:
        self['Receptor'] = receptor6(cls, el)
    el = node.find('{http://www.sat.gob.mx/ComercioExterior11}Destinatario')
    if el is not None:
        self['Destinatario'] = [destinatario1(cls, n) for n in node.iterfind('{http://www.sat.gob.mx/ComercioExterior11}Destinatario')]
    el = node.find('{http://www.sat.gob.mx/ComercioExterior11}Mercancias')
    if el is not None:
        self['Mercancias'] = [mercancia4(cls, n) for n in el.iterfind('{http://www.sat.gob.mx/ComercioExterior11}Mercancia')]
    self['Version'] = node.attrib['Version']
    if (a := node.attrib.get('MotivoTraslado')) is not None:
        self['MotivoTraslado'] = catalog_code('C5bc_c_MotivoTraslado', a)
    self['TipoOperacion'] = catalog_code('C5bc_c_TipoOperacion', node.attrib['TipoOperacion'])
    if (a := node.attrib.get('ClaveDePedimento')) is not None:
        self['ClaveDePedimento'] = catalog_code('C5bc_c_ClavePedimento', a)
    if (a := node.attrib.get('CertificadoOrigen')) is not None:
        self['CertificadoOrigen'] = Xint(a)
    if (a := node.attrib.get('NumCertificadoOrigen')) is not None:
        self['NumCertificadoOrigen'] = a
    if (a := node.attrib.get('NumeroExportadorConfiable')) is not None:
        self['NumeroExportadorConfiable'] = a
    if (a := node.attrib.get('Incoterm')) is not None:
        self['Incoterm'] = catalog_code('C5bc_c_INCOTERM', a)
    if (a := node.attrib.get('Subdivision')) is not None:
        self['Subdivision'] = Xint(a)
    if (a := node.attrib.get('Observaciones')) is not None:
        self['Observaciones'] = a
    if (a := node.attrib.get('TipoCambioUSD')) is not None:
        self['TipoCambioUSD'] = Decimal(a)
    if (a := node.attrib.get('TotalUSD')) is not None:
        self['TotalUSD'] = Decimal(a)
    return self
def emisor6(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.sat.gob.mx/ComercioExterior11}Domicilio')
    if el is not None:
        self['Domicilio'] = domiciliob(cls, el)
    if (a := node.attrib.get('Curp')) is not None:
        self['Curp'] = a
    return self
def domiciliob(cls, node):
    self = ScalarMap()
    self['Calle'] = node.attrib['Calle']
    if (a := node.attrib.get('NumeroExterior')) is not None:
        self['NumeroExterior'] = a
    if (a := node.attrib.get('NumeroInterior')) is not None:
        self['NumeroInterior'] = a
    if (a := node.attrib.get('Colonia')) is not None:
        self['Colonia'] = catalog_code('C756_c_Colonia', (a, node.attrib['CodigoPostal']))
    if (a := node.attrib.get('Localidad')) is not None:
        self['Localidad'] = catalog_code('C756_c_Localidad', (a, node.attrib['Estado']))
    if (a := node.attrib.get('Referencia')) is not None:
        self['Referencia'] = a
    if (a := node.attrib.get('Municipio')) is not None:
        self['Municipio'] = catalog_code('C756_c_Municipio', (a, node.attrib['Estado']))
    self['Estado'] = catalog_code('C756_c_Estado', node.attrib['Estado'], 1)
    self['Pais'] = catalog_code('C756_c_Pais', node.attrib['Pais'])
    self['CodigoPostal'] = node.attrib['CodigoPostal']
    return self
def propietario1(cls, node):
    self = ScalarMap()
    self['NumRegIdTrib'] = node.attrib['NumRegIdTrib']
    self['ResidenciaFiscal'] = catalog_code('C756_c_Pais', node.attrib['ResidenciaFiscal'])
    return self
def receptor6(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.sat.gob.mx/ComercioExterior11}Domicilio')
    if el is not None:
        self['Domicilio'] = domicilioc(cls, el)
    if (a := node.attrib.get('NumRegIdTrib')) is not None:
        self['NumRegIdTrib'] = a
    return self
def domicilioc(cls, node):
    self = ScalarMap()
    self['Calle'] = node.attrib['Calle']
    if (a := node.attrib.get('NumeroExterior')) is not None:
        self['NumeroExterior'] = a
    if (a := node.attrib.get('NumeroInterior')) is not None:
        self['NumeroInterior'] = a
    if (a := node.attrib.get('Colonia')) is not None:
        self['Colonia'] = a
    if (a := node.attrib.get('Localidad')) is not None:
        self['Localidad'] = a
    if (a := node.attrib.get('Referencia')) is not None:
        self['Referencia'] = a
    if (a := node.attrib.get('Municipio')) is not None:
        self['Municipio'] = a
    self['Estado'] = node.attrib['Estado']
    self['Pais'] = catalog_code('C756_c_Pais', node.attrib['Pais'])
    self['CodigoPostal'] = node.attrib['CodigoPostal']
    return self
def destinatario1(cls, node):
    self = ScalarMap()
    self['Domicilio'] = [domiciliod(cls, n) for n in node.iterfind('{http://www.sat.gob.mx/ComercioExterior11}Domicilio')]
    if (a := node.attrib.get('NumRegIdTrib')) is not None:
        self['NumRegIdTrib'] = a
    if (a := node.attrib.get('Nombre')) is not None:
        self['Nombre'] = a
    return self
def domiciliod(cls, node):
    self = ScalarMap()
    self['Calle'] = node.attrib['Calle']
    if (a := node.attrib.get('NumeroExterior')) is not None:
        self['NumeroExterior'] = a
    if (a := node.attrib.get('NumeroInterior')) is not None:
        self['NumeroInterior'] = a
    if (a := node.attrib.get('Colonia')) is not None:
        self['Colonia'] = a
    if (a := node.attrib.get('Localidad')) is not None:
        self['Localidad'] = a
    if (a := node.attrib.get('Referencia')) is not None:
        self['Referencia'] = a
    if (a := node.attrib.get('Municipio')) is not None:
        self['Municipio'] = a
    self['Estado'] = node.attrib['Estado']
    self['Pais'] = catalog_code('C756_c_Pais', node.attrib['Pais'])
    self['CodigoPostal'] = node.attrib['CodigoPostal']
    return self
def mercancia4(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.sat.gob.mx/ComercioExterior11}DescripcionesEspecificas')
    if el is not None:
        self['DescripcionesEspecificas'] = [descripciones_especificas0(cls, n) for n in node.iterfind('{http://www.sat.gob.mx/ComercioExterior11}DescripcionesEspecificas')]
    self['NoIdentificacion'] = node.attrib['NoIdentificacion']
    if (a := node.attrib.get('FraccionArancelaria')) is not None:
        self['FraccionArancelaria'] = catalog_code('C5bc_c_FraccionArancelaria', a)
    if (a := node.attrib.get('CantidadAduana')) is not None:
        self['CantidadAduana'] = Decimal(a)
    if (a := node.attrib.get('UnidadAduana')) is not None:
        self['UnidadAduana'] = catalog_code('C5bc_c_UnidadAduana', a)
    if (a := node.attrib.get('ValorUnitarioAduana')) is not None:
        self['ValorUnitarioAduana'] = Decimal(a)
    self['ValorDolares'] = Decimal(node.attrib['ValorDolares'])
    return self
def descripciones_especificas0(cls, node):
    self = ScalarMap()
    self['Marca'] = node.attrib['Marca']
    if (a := node.attrib.get('Modelo')) is not None:
        self['Modelo'] = a
    if (a := node.attrib.get('SubModelo')) is not None:
        self['SubModelo'] = a
    if (a := node.attrib.get('NumeroSerie')) is not None:
        self['NumeroSerie'] = a
    return self
def comercio_exterior1(cls, node):
    self = cls()
    self.tag = node.tag
    el = node.find('{http://www.sat.gob.mx/ComercioExterior20}Emisor')
    if el is not None:
        self['Emisor'] = emisor7(cls, el)
    el = node.find('{http://www.sat.gob.mx/ComercioExterior20}Propietario')
    if el is not None:
        self['Propietario'] = [propietario2(cls, n) for n in node.iterfind('{http://www.sat.gob.mx/ComercioExterior20}Propietario')]
    el = node.find('{http://www.sat.gob.mx/ComercioExterior20}Receptor')
    if el is not None:
        self['Receptor'] = receptor7(cls, el)
    el = node.find('{http://www.sat.gob.mx/ComercioExterior20}Destinatario')
    if el is not None:
        self['Destinatario'] = [destinatario2(cls, n) for n in node.iterfind('{http://www.sat.gob.mx/ComercioExterior20}Destinatario')]
    el = node.find('{http://www.sat.gob.mx/ComercioExterior20}Mercancias')
    self['Mercancias'] = [mercancia5(cls, n) for n in el.iterfind('{http://www.sat.gob.mx/ComercioExterior20}Mercancia')]
    self['Version'] = node.attrib['Version']
    if (a := node.attrib.get('MotivoTraslado')) is not None:
        self['MotivoTraslado'] = catalog_code('C5bc_c_MotivoTraslado', a)
    self['ClaveDePedimento'] = catalog_code('C5bc_c_ClavePedimento', node.attrib['ClaveDePedimento'])
    self['CertificadoOrigen'] = Xint(node.attrib['CertificadoOrigen'])
    if (a := node.attrib.get('NumCertificadoOrigen')) is not None:
        self['NumCertificadoOrigen'] = a
    if (a := node.attrib.get('NumeroExportadorConfiable')) is not None:
        self['NumeroExportadorConfiable'] = a
    if (a := node.attrib.get('Incoterm')) is not None:
        self['Incoterm'] = catalog_code('C5bc_c_INCOTERM', a)
    if (a := node.attrib.get('Observaciones')) is not None:
        self['Observaciones'] = a
    self['TipoCambioUSD'] = Decimal(node.attrib['TipoCambioUSD'])
    self['TotalUSD'] = Decimal(node.attrib['TotalUSD'])
    return self
def emisor7(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.sat.gob.mx/ComercioExterior20}Domicilio')
    self['Domicilio'] = domicilioe(cls, el)
    if (a := node.attrib.get('Curp')) is not None:
        self['Curp'] = a
    return self
def domicilioe(cls, node):
    self = ScalarMap()
    self['Calle'] = node.attrib['Calle']
    if (a := node.attrib.get('NumeroExterior')) is not None:
        self['NumeroExterior'] = a
    if (a := node.attrib.get('NumeroInterior')) is not None:
        self['NumeroInterior'] = a
    if (a := node.attrib.get('Colonia')) is not None:
        self['Colonia'] = catalog_code('C756_c_Colonia', (a, node.attrib['CodigoPostal']))
    if (a := node.attrib.get('Localidad')) is not None:
        self['Localidad'] = catalog_code('C756_c_Localidad', (a, node.attrib['Estado']))
    if (a := node.attrib.get('Referencia')) is not None:
        self['Referencia'] = a
    if (a := node.attrib.get('Municipio')) is not None:
        self['Municipio'] = catalog_code('C756_c_Municipio', (a, node.attrib['Estado']))
    self['Estado'] = catalog_code('C756_c_Estado', node.attrib['Estado'], 1)
    self['Pais'] = catalog_code('C756_c_Pais', node.attrib['Pais'])
    self['CodigoPostal'] = node.attrib['CodigoPostal']
    return self
def propietario2(cls, node):
    self = ScalarMap()
    self['NumRegIdTrib'] = node.attrib['NumRegIdTrib']
    self['ResidenciaFiscal'] = catalog_code('C756_c_Pais', node.attrib['ResidenciaFiscal'])
    return self
def receptor7(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.sat.gob.mx/ComercioExterior20}Domicilio')
    if el is not None:
        self['Domicilio'] = domiciliof(cls, el)
    if (a := node.attrib.get('NumRegIdTrib')) is not None:
        self['NumRegIdTrib'] = a
    return self
def domiciliof(cls, node):
    self = ScalarMap()
    self['Calle'] = node.attrib['Calle']
    if (a := node.attrib.get('NumeroExterior')) is not None:
        self['NumeroExterior'] = a
    if (a := node.attrib.get('NumeroInterior')) is not None:
        self['NumeroInterior'] = a
    if (a := node.attrib.get('Colonia')) is not None:
        self['Colonia'] = a
    if (a := node.attrib.get('Localidad')) is not None:
        self['Localidad'] = a
    if (a := node.attrib.get('Referencia')) is not None:
        self['Referencia'] = a
    if (a := node.attrib.get('Municipio')) is not None:
        self['Municipio'] = a
    self['Estado'] = node.attrib['Estado']
    self['Pais'] = catalog_code('C756_c_Pais', node.attrib['Pais'])
    self['CodigoPostal'] = node.attrib['CodigoPostal']
    return self
def destinatario2(cls, node):
    self = ScalarMap()
    self['Domicilio'] = [domicilio10(cls, n) for n in node.iterfind('{http://www.sat.gob.mx/ComercioExterior20}Domicilio')]
    if (a := node.attrib.get('NumRegIdTrib')) is not None:
        self['NumRegIdTrib'] = a
    if (a := node.attrib.get('Nombre')) is not None:
        self['Nombre'] = a
    return self
def domicilio10(cls, node):
    self = ScalarMap()
    self['Calle'] = node.attrib['Calle']
    if (a := node.attrib.get('NumeroExterior')) is not None:
        self['NumeroExterior'] = a
    if (a := node.attrib.get('NumeroInterior')) is not None:
        self['NumeroInterior'] = a
    if (a := node.attrib.get('Colonia')) is not None:
        self['Colonia'] = a
    if (a := node.attrib.get('Localidad')) is not None:
        self['Localidad'] = a
    if (a := node.attrib.get('Referencia')) is not None:
        self['Referencia'] = a
    if (a := node.attrib.get('Municipio')) is not None:
        self['Municipio'] = a
    self['Estado'] = node.attrib['Estado']
    self['Pais'] = catalog_code('C756_c_Pais', node.attrib['Pais'])
    self['CodigoPostal'] = node.attrib['CodigoPostal']
    return self
def mercancia5(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.sat.gob.mx/ComercioExterior20}DescripcionesEspecificas')
    if el is not None:
        self['DescripcionesEspecificas'] = [descripciones_especificas1(cls, n) for n in node.iterfind('{http://www.sat.gob.mx/ComercioExterior20}DescripcionesEspecificas')]
    self['NoIdentificacion'] = node.attrib['NoIdentificacion']
    if (a := node.attrib.get('FraccionArancelaria')) is not None:
        self['FraccionArancelaria'] = catalog_code('C5bc_c_FraccionArancelaria', a)
    if (a := node.attrib.get('CantidadAduana')) is not None:
        self['CantidadAduana'] = Decimal(a)
    if (a := node.attrib.get('UnidadAduana')) is not None:
        self['UnidadAduana'] = catalog_code('C5bc_c_UnidadAduana', a)
    if (a := node.attrib.get('ValorUnitarioAduana')) is not None:
        self['ValorUnitarioAduana'] = Decimal(a)
    self['ValorDolares'] = Decimal(node.attrib['ValorDolares'])
    return self
def descripciones_especificas1(cls, node):
    self = ScalarMap()
    self['Marca'] = node.attrib['Marca']
    if (a := node.attrib.get('Modelo')) is not None:
        self['Modelo'] = a
    if (a := node.attrib.get('SubModelo')) is not None:
        self['SubModelo'] = a
    if (a := node.attrib.get('NumeroSerie')) is not None:
        self['NumeroSerie'] = a
    return self
def comercio_exterior2(cls, node):
    self = cls()
    self.tag = node.tag
    el = node.find('{http://www.sat.gob.mx/ComercioExterior}Emisor')
    if el is not None:
        self['Emisor'] = emisor8(cls, el)
    el = node.find('{http://www.sat.gob.mx/ComercioExterior}Receptor')
    self['Receptor'] = receptor8(cls, el)
    el = node.find('{http://www.sat.gob.mx/ComercioExterior}Destinatario')
    if el is not None:
        self['Destinatario'] = destinatario3(cls, el)
    el = node.find('{http://www.sat.gob.mx/ComercioExterior}Mercancias')
    if el is not None:
        self['Mercancias'] = [mercancia6(cls, n) for n in el.iterfind('{http://www.sat.gob.mx/ComercioExterior}Mercancia')]
    self['Version'] = node.attrib['Version']
    self['TipoOperacion'] = catalog_code('C5bc_c_TipoOperacion', node.attrib['TipoOperacion'])
    if (a := node.attrib.get('ClaveDePedimento')) is not None:
        self['ClaveDePedimento'] = catalog_code('C5bc_c_ClavePedimento', a)
    if (a := node.attrib.get('CertificadoOrigen')) is not None:
        self['CertificadoOrigen'] = Xint(a)
    if (a := node.attrib.get('NumCertificadoOrigen')) is not None:
        self['NumCertificadoOrigen'] = a
    if (a := node.attrib.get('NumeroExportadorConfiable')) is not None:
        self['NumeroExportadorConfiable'] = a
    if (a := node.attrib.get('Incoterm')) is not None:
        self['Incoterm'] = catalog_code('C5bc_c_INCOTERM', a)
    if (a := node.attrib.get('Subdivision')) is not None:
        self['Subdivision'] = Xint(a)
    if (a := node.attrib.get('Observaciones')) is not None:
        self['Observaciones'] = a
    if (a := node.attrib.get('TipoCambioUSD')) is not None:
        self['TipoCambioUSD'] = Decimal(a)
    if (a := node.attrib.get('TotalUSD')) is not None:
        self['TotalUSD'] = Decimal(a)
    return self
def emisor8(cls, node):
    self = ScalarMap()
    if (a := node.attrib.get('Curp')) is not None:
        self['Curp'] = a
    return self
def receptor8(cls, node):
    self = ScalarMap()
    if (a := node.attrib.get('Curp')) is not None:
        self['Curp'] = a
    self['NumRegIdTrib'] = node.attrib['NumRegIdTrib']
    return self
def destinatario3(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.sat.gob.mx/ComercioExterior}Domicilio')
    self['Domicilio'] = domicilio11(cls, el)
    if (a := node.attrib.get('NumRegIdTrib')) is not None:
        self['NumRegIdTrib'] = a
    if (a := node.attrib.get('Rfc')) is not None:
        self['Rfc'] = a
    if (a := node.attrib.get('Curp')) is not None:
        self['Curp'] = a
    if (a := node.attrib.get('Nombre')) is not None:
        self['Nombre'] = a
    return self
def domicilio11(cls, node):
    self = ScalarMap()
    self['Calle'] = node.attrib['Calle']
    if (a := node.attrib.get('NumeroExterior')) is not None:
        self['NumeroExterior'] = a
    if (a := node.attrib.get('NumeroInterior')) is not None:
        self['NumeroInterior'] = a
    if (a := node.attrib.get('Colonia')) is not None:
        self['Colonia'] = a
    if (a := node.attrib.get('Localidad')) is not None:
        self['Localidad'] = a
    if (a := node.attrib.get('Referencia')) is not None:
        self['Referencia'] = a
    if (a := node.attrib.get('Municipio')) is not None:
        self['Municipio'] = a
    self['Estado'] = node.attrib['Estado']
    self['Pais'] = catalog_code('C756_c_Pais', node.attrib['Pais'])
    self['CodigoPostal'] = node.attrib['CodigoPostal']
    return self
def mercancia6(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.sat.gob.mx/ComercioExterior}DescripcionesEspecificas')
    if el is not None:
        self['DescripcionesEspecificas'] = [descripciones_especificas2(cls, n) for n in node.iterfind('{http://www.sat.gob.mx/ComercioExterior}DescripcionesEspecificas')]
    self['NoIdentificacion'] = node.attrib['NoIdentificacion']
    if (a := node.attrib.get('FraccionArancelaria')) is not None:
        self['FraccionArancelaria'] = catalog_code('C5bc_c_FraccionArancelaria', a)
    if (a := node.attrib.get('CantidadAduana')) is not None:
        self['CantidadAduana'] = Decimal(a)
    if (a := node.attrib.get('UnidadAduana')) is not None:
        self['UnidadAduana'] = catalog_code('C5bc_c_UnidadAduana', a)
    if (a := node.attrib.get('ValorUnitarioAduana')) is not None:
        self['ValorUnitarioAduana'] = Decimal(a)
    self['ValorDolares'] = Decimal(node.attrib['ValorDolares'])
    return self
def descripciones_especificas2(cls, node):
    self = ScalarMap()
    self['Marca'] = node.attrib['Marca']
    if (a := node.attrib.get('Modelo')) is not None:
        self['Modelo'] = a
    if (a := node.attrib.get('SubModelo')) is not None:
        self['SubModelo'] = a
    if (a := node.attrib.get('NumeroSerie')) is not None:
        self['NumeroSerie'] = a
    return self
def estado_de_cuenta_combustible0(cls, node):
    self = cls()
    self.tag = node.tag
    el = node.find('{http://www.sat.gob.mx/EstadoDeCuentaCombustible}Conceptos')
    self['Conceptos'] = [concepto_estado_de_cuenta_combustible0(cls, n) for n in el.iterfind('{http://www.sat.gob.mx/EstadoDeCuentaCombustible}ConceptoEstadoDeCuentaCombustible')]
    self['Version'] = node.attrib['Version']
    self['TipoOperacion'] = node.attrib['TipoOperacion']
    self['NumeroDeCuenta'] = node.attrib['NumeroDeCuenta']
    self['SubTotal'] = Decimal(node.attrib['SubTotal'])
    self['Total'] = Decimal(node.attrib['Total'])
    return self
def concepto_estado_de_cuenta_combustible0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.sat.gob.mx/EstadoDeCuentaCombustible}Traslados')
    self['Traslados'] = [traslado5(cls, n) for n in el.iterfind('{http://www.sat.gob.mx/EstadoDeCuentaCombustible}Traslado')]
    self['Identificador'] = node.attrib['Identificador']
    self['Fecha'] = datetime.fromisoformat(node.attrib['Fecha'])
    self['Rfc'] = node.attrib['Rfc']
    self['ClaveEstacion'] = node.attrib['ClaveEstacion']
    if (a := node.attrib.get('TAR')) is not None:
        self['TAR'] = catalog_code('C40c_c_TAR', a)
    self['Cantidad'] = Decimal(node.attrib['Cantidad'])
    self['NoIdentificacion'] = catalog_code('C40c_c_claveProducto', node.attrib['NoIdentificacion'])
    if (a := node.attrib.get('Unidad')) is not None:
        self['Unidad'] = a
    self['NombreCombustible'] = node.attrib['NombreCombustible']
    self['FolioOperacion'] = node.attrib['FolioOperacion']
    self['ValorUnitario'] = Decimal(node.attrib['ValorUnitario'])
    self['Importe'] = Decimal(node.attrib['Importe'])
    return self
def traslado5(cls, node):
    self = ScalarMap()
    self['Impuesto'] = node.attrib['Impuesto']
    self['TasaoCuota'] = Decimal(node.attrib['TasaoCuota'])
    self['Importe'] = Decimal(node.attrib['Importe'])
    return self
def estado_de_cuenta_combustible1(cls, node):
    self = cls()
    self.tag = node.tag
    el = node.find('{http://www.sat.gob.mx/EstadoDeCuentaCombustible12}Conceptos')
    self['Conceptos'] = [concepto_estado_de_cuenta_combustible1(cls, n) for n in el.iterfind('{http://www.sat.gob.mx/EstadoDeCuentaCombustible12}ConceptoEstadoDeCuentaCombustible')]
    self['Version'] = node.attrib['Version']
    self['TipoOperacion'] = node.attrib['TipoOperacion']
    self['NumeroDeCuenta'] = node.attrib['NumeroDeCuenta']
    self['SubTotal'] = Decimal(node.attrib['SubTotal'])
    self['Total'] = Decimal(node.attrib['Total'])
    return self
def concepto_estado_de_cuenta_combustible1(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.sat.gob.mx/EstadoDeCuentaCombustible12}Traslados')
    self['Traslados'] = [traslado6(cls, n) for n in el.iterfind('{http://www.sat.gob.mx/EstadoDeCuentaCombustible12}Traslado')]
    self['Identificador'] = node.attrib['Identificador']
    self['Fecha'] = datetime.fromisoformat(node.attrib['Fecha'])
    self['Rfc'] = node.attrib['Rfc']
    self['ClaveEstacion'] = node.attrib['ClaveEstacion']
    self['Cantidad'] = Decimal(node.attrib['Cantidad'])
    self['TipoCombustible'] = catalog_code('C23d_c_ClaveTipoCombustible', node.attrib['TipoCombustible'])
    if (a := node.attrib.get('Unidad')) is not None:
        self['Unidad'] = a
    self['NombreCombustible'] = node.attrib['NombreCombustible']
    self['FolioOperacion'] = node.attrib['FolioOperacion']
    self['ValorUnitario'] = Decimal(node.attrib['ValorUnitario'])
    self['Importe'] = Decimal(node.attrib['Importe'])
    return self
def traslado6(cls, node):
    self = ScalarMap()
    self['Impuesto'] = node.attrib['Impuesto']
    self['TasaOCuota'] = Decimal(node.attrib['TasaOCuota'])
    self['Importe'] = Decimal(node.attrib['Importe'])
    return self
def gastos_hidrocarburos0(cls, node):
    self = cls()
    self.tag = node.tag
    self['Erogacion'] = [erogacion0(cls, n) for n in node.iterfind('{http://www.sat.gob.mx/GastosHidrocarburos10}Erogacion')]
    self['Version'] = node.attrib['Version']
    self['NumeroContrato'] = node.attrib['NumeroContrato']
    if (a := node.attrib.get('AreaContractual')) is not None:
        self['AreaContractual'] = a
    return self
def erogacion0(cls, node):
    self = ScalarMap()
    self['DocumentoRelacionado'] = [documento_relacionado0(cls, n) for n in node.iterfind('{http://www.sat.gob.mx/GastosHidrocarburos10}DocumentoRelacionado')]
    el = node.find('{http://www.sat.gob.mx/GastosHidrocarburos10}Actividades')
    if el is not None:
        self['Actividades'] = [actividades0(cls, n) for n in node.iterfind('{http://www.sat.gob.mx/GastosHidrocarburos10}Actividades')]
    el = node.find('{http://www.sat.gob.mx/GastosHidrocarburos10}CentroCostos')
    if el is not None:
        self['CentroCostos'] = [centro_costos0(cls, n) for n in node.iterfind('{http://www.sat.gob.mx/GastosHidrocarburos10}CentroCostos')]
    self['TipoErogacion'] = node.attrib['TipoErogacion']
    self['MontocuErogacion'] = Decimal(node.attrib['MontocuErogacion'])
    self['Porcentaje'] = Decimal(node.attrib['Porcentaje'])
    return self
def documento_relacionado0(cls, node):
    self = ScalarMap()
    self['OrigenErogacion'] = node.attrib['OrigenErogacion']
    if (a := node.attrib.get('FolioFiscalVinculado')) is not None:
        self['FolioFiscalVinculado'] = a
    if (a := node.attrib.get('RFCProveedor')) is not None:
        self['RFCProveedor'] = a
    if (a := node.attrib.get('MontoTotalIVA')) is not None:
        self['MontoTotalIVA'] = Decimal(a)
    if (a := node.attrib.get('MontoRetencionISR')) is not None:
        self['MontoRetencionISR'] = Decimal(a)
    if (a := node.attrib.get('MontoRetencionIVA')) is not None:
        self['MontoRetencionIVA'] = Decimal(a)
    if (a := node.attrib.get('MontoRetencionOtrosImpuestos')) is not None:
        self['MontoRetencionOtrosImpuestos'] = Decimal(a)
    if (a := node.attrib.get('NumeroPedimentoVinculado')) is not None:
        self['NumeroPedimentoVinculado'] = a
    if (a := node.attrib.get('ClavePedimentoVinculado')) is not None:
        self['ClavePedimentoVinculado'] = catalog_code('C1b7_ClavePedimento', a)
    if (a := node.attrib.get('ClavePagoPedimentoVinculado')) is not None:
        self['ClavePagoPedimentoVinculado'] = catalog_code('C1b7_ClavePagoPedimento', a)
    if (a := node.attrib.get('MontoIVAPedimento')) is not None:
        self['MontoIVAPedimento'] = Decimal(a)
    if (a := node.attrib.get('OtrosImpuestosPagadosPedimento')) is not None:
        self['OtrosImpuestosPagadosPedimento'] = Decimal(a)
    if (a := node.attrib.get('FechaFolioFiscalVinculado')) is not None:
        self['FechaFolioFiscalVinculado'] = date.fromisoformat(a)
    self['Mes'] = catalog_code('C1b7_Meses', node.attrib['Mes'])
    self['MontoTotalErogaciones'] = Decimal(node.attrib['MontoTotalErogaciones'])
    return self
def actividades0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.sat.gob.mx/GastosHidrocarburos10}SubActividades')
    if el is not None:
        self['SubActividades'] = [sub_actividades0(cls, n) for n in node.iterfind('{http://www.sat.gob.mx/GastosHidrocarburos10}SubActividades')]
    if (a := node.attrib.get('ActividadRelacionada')) is not None:
        self['ActividadRelacionada'] = catalog_code('C1b7_Actividades', a)
    return self
def sub_actividades0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.sat.gob.mx/GastosHidrocarburos10}Tareas')
    if el is not None:
        self['Tareas'] = [tareas0(cls, n) for n in node.iterfind('{http://www.sat.gob.mx/GastosHidrocarburos10}Tareas')]
    if (a := node.attrib.get('SubActividadRelacionada')) is not None:
        self['SubActividadRelacionada'] = catalog_code('C1b7_SubActividad', a)
    return self
def tareas0(cls, node):
    self = ScalarMap()
    if (a := node.attrib.get('TareaRelacionada')) is not None:
        self['TareaRelacionada'] = catalog_code('C1b7_Tareas', a)
    return self
def centro_costos0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.sat.gob.mx/GastosHidrocarburos10}Yacimientos')
    if el is not None:
        self['Yacimientos'] = [yacimientos0(cls, n) for n in node.iterfind('{http://www.sat.gob.mx/GastosHidrocarburos10}Yacimientos')]
    if (a := node.attrib.get('Campo')) is not None:
        self['Campo'] = a
    return self
def yacimientos0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.sat.gob.mx/GastosHidrocarburos10}Pozos')
    if el is not None:
        self['Pozos'] = [pozos0(cls, n) for n in node.iterfind('{http://www.sat.gob.mx/GastosHidrocarburos10}Pozos')]
    if (a := node.attrib.get('Yacimiento')) is not None:
        self['Yacimiento'] = a
    return self
def pozos0(cls, node):
    self = ScalarMap()
    if (a := node.attrib.get('Pozo')) is not None:
        self['Pozo'] = a
    return self
def ingresos_hidrocarburos0(cls, node):
    self = cls()
    self.tag = node.tag
    self['DocumentoRelacionado'] = [documento_relacionado1(cls, n) for n in node.iterfind('{http://www.sat.gob.mx/IngresosHidrocarburos10}DocumentoRelacionado')]
    self['Version'] = node.attrib['Version']
    self['NumeroContrato'] = node.attrib['NumeroContrato']
    self['ContraprestacionPagadaOperador'] = Decimal(node.attrib['ContraprestacionPagadaOperador'])
    self['Porcentaje'] = Decimal(node.attrib['Porcentaje'])
    return self
def documento_relacionado1(cls, node):
    self = ScalarMap()
    self['FolioFiscalVinculado'] = node.attrib['FolioFiscalVinculado']
    self['FechaFolioFiscalVinculado'] = date.fromisoformat(node.attrib['FechaFolioFiscalVinculado'])
    self['Mes'] = catalog_code('C1b7_Meses', node.attrib['Mes'])
    return self
def pagos0(cls, node):
    self = cls()
    self.tag = node.tag
    self['Pago'] = [pago0(cls, n) for n in node.iterfind('{http://www.sat.gob.mx/Pagos}Pago')]
    self['Version'] = node.attrib['Version']
    return self
def pago0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.sat.gob.mx/Pagos}DoctoRelacionado')
    if el is not None:
        self['DoctoRelacionado'] = [docto_relacionado0(cls, n) for n in node.iterfind('{http://www.sat.gob.mx/Pagos}DoctoRelacionado')]
    el = node.find('{http://www.sat.gob.mx/Pagos}Impuestos')
    if el is not None:
        self['Impuestos'] = [impuestos5(cls, n) for n in node.iterfind('{http://www.sat.gob.mx/Pagos}Impuestos')]
    self['FechaPago'] = datetime.fromisoformat(node.attrib['FechaPago'])
    self['FormaDePagoP'] = catalog_code('C756_c_FormaPago', node.attrib['FormaDePagoP'])
    self['MonedaP'] = catalog_code('C756_c_Moneda', node.attrib['MonedaP'], 0)
    if (a := node.attrib.get('TipoCambioP')) is not None:
        self['TipoCambioP'] = Decimal(a)
    self['Monto'] = Decimal(node.attrib['Monto'])
    if (a := node.attrib.get('NumOperacion')) is not None:
        self['NumOperacion'] = a
    if (a := node.attrib.get('RfcEmisorCtaOrd')) is not None:
        self['RfcEmisorCtaOrd'] = a
    if (a := node.attrib.get('NomBancoOrdExt')) is not None:
        self['NomBancoOrdExt'] = a
    if (a := node.attrib.get('CtaOrdenante')) is not None:
        self['CtaOrdenante'] = a
    if (a := node.attrib.get('RfcEmisorCtaBen')) is not None:
        self['RfcEmisorCtaBen'] = a
    if (a := node.attrib.get('CtaBeneficiario')) is not None:
        self['CtaBeneficiario'] = a
    if (a := node.attrib.get('TipoCadPago')) is not None:
        self['TipoCadPago'] = catalog_code('C004_c_TipoCadenaPago', a)
    if (a := node.attrib.get('CertPago')) is not None:
        self['CertPago'] = a
    if (a := node.attrib.get('CadPago')) is not None:
        self['CadPago'] = a
    if (a := node.attrib.get('SelloPago')) is not None:
        self['SelloPago'] = a
    return self
def docto_relacionado0(cls, node):
    self = ScalarMap()
    self['IdDocumento'] = node.attrib['IdDocumento']
    if (a := node.attrib.get('Serie')) is not None:
        self['Serie'] = a
    if (a := node.attrib.get('Folio')) is not None:
        self['Folio'] = a
    self['MonedaDR'] = catalog_code('C756_c_Moneda', node.attrib['MonedaDR'], 0)
    if (a := node.attrib.get('TipoCambioDR')) is not None:
        self['TipoCambioDR'] = Decimal(a)
    self['MetodoDePagoDR'] = catalog_code('C756_c_MetodoPago', node.attrib['MetodoDePagoDR'])
    if (a := node.attrib.get('NumParcialidad')) is not None:
        self['NumParcialidad'] = Xint(a)
    if (a := node.attrib.get('ImpSaldoAnt')) is not None:
        self['ImpSaldoAnt'] = Decimal(a)
    if (a := node.attrib.get('ImpPagado')) is not None:
        self['ImpPagado'] = Decimal(a)
    if (a := node.attrib.get('ImpSaldoInsoluto')) is not None:
        self['ImpSaldoInsoluto'] = Decimal(a)
    return self
def impuestos5(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.sat.gob.mx/Pagos}Retenciones')
    if el is not None:
        self['Retenciones'] = {impuesto_index(n.attrib, 'Impuesto'): retencion5(cls, n) for n in el.iterfind('{http://www.sat.gob.mx/Pagos}Retencion')}
    el = node.find('{http://www.sat.gob.mx/Pagos}Traslados')
    if el is not None:
        self['Traslados'] = {impuesto_index(n.attrib, 'Impuesto'): traslado7(cls, n) for n in el.iterfind('{http://www.sat.gob.mx/Pagos}Traslado')}
    if (a := node.attrib.get('TotalImpuestosRetenidos')) is not None:
        self['TotalImpuestosRetenidos'] = Decimal(a)
    if (a := node.attrib.get('TotalImpuestosTrasladados')) is not None:
        self['TotalImpuestosTrasladados'] = Decimal(a)
    return self
def retencion5(cls, node):
    self = ScalarMap()
    self['Impuesto'] = catalog_code('C756_c_Impuesto', node.attrib['Impuesto'])
    self['Importe'] = Decimal(node.attrib['Importe'])
    return self
def traslado7(cls, node):
    self = ScalarMap()
    self['Impuesto'] = catalog_code('C756_c_Impuesto', node.attrib['Impuesto'])
    self['TipoFactor'] = catalog_code('C756_c_TipoFactor', node.attrib['TipoFactor'])
    self['TasaOCuota'] = Decimal(node.attrib['TasaOCuota'])
    self['Importe'] = Decimal(node.attrib['Importe'])
    return self
def pagos1(cls, node):
    self = cls()
    self.tag = node.tag
    el = node.find('{http://www.sat.gob.mx/Pagos20}Totales')
    self['Totales'] = totales2(cls, el)
    self['Pago'] = [pago1(cls, n) for n in node.iterfind('{http://www.sat.gob.mx/Pagos20}Pago')]
    self['Version'] = node.attrib['Version']
    return self
def totales2(cls, node):
    self = ScalarMap()
    if (a := node.attrib.get('TotalRetencionesIVA')) is not None:
        self['TotalRetencionesIVA'] = Decimal(a)
    if (a := node.attrib.get('TotalRetencionesISR')) is not None:
        self['TotalRetencionesISR'] = Decimal(a)
    if (a := node.attrib.get('TotalRetencionesIEPS')) is not None:
        self['TotalRetencionesIEPS'] = Decimal(a)
    if (a := node.attrib.get('TotalTrasladosBaseIVA16')) is not None:
        self['TotalTrasladosBaseIVA16'] = Decimal(a)
    if (a := node.attrib.get('TotalTrasladosImpuestoIVA16')) is not None:
        self['TotalTrasladosImpuestoIVA16'] = Decimal(a)
    if (a := node.attrib.get('TotalTrasladosBaseIVA8')) is not None:
        self['TotalTrasladosBaseIVA8'] = Decimal(a)
    if (a := node.attrib.get('TotalTrasladosImpuestoIVA8')) is not None:
        self['TotalTrasladosImpuestoIVA8'] = Decimal(a)
    if (a := node.attrib.get('TotalTrasladosBaseIVA0')) is not None:
        self['TotalTrasladosBaseIVA0'] = Decimal(a)
    if (a := node.attrib.get('TotalTrasladosImpuestoIVA0')) is not None:
        self['TotalTrasladosImpuestoIVA0'] = Decimal(a)
    if (a := node.attrib.get('TotalTrasladosBaseIVAExento')) is not None:
        self['TotalTrasladosBaseIVAExento'] = Decimal(a)
    self['MontoTotalPagos'] = Decimal(node.attrib['MontoTotalPagos'])
    return self
def pago1(cls, node):
    self = ScalarMap()
    self['DoctoRelacionado'] = [docto_relacionado1(cls, n) for n in node.iterfind('{http://www.sat.gob.mx/Pagos20}DoctoRelacionado')]
    el = node.find('{http://www.sat.gob.mx/Pagos20}ImpuestosP')
    if el is not None:
        self['ImpuestosP'] = impuestos_p0(cls, el)
    self['FechaPago'] = datetime.fromisoformat(node.attrib['FechaPago'])
    self['FormaDePagoP'] = catalog_code('C756_c_FormaPago', node.attrib['FormaDePagoP'])
    self['MonedaP'] = catalog_code('C756_c_Moneda', node.attrib['MonedaP'], 0)
    if (a := node.attrib.get('TipoCambioP')) is not None:
        self['TipoCambioP'] = Decimal(a)
    self['Monto'] = Decimal(node.attrib['Monto'])
    if (a := node.attrib.get('NumOperacion')) is not None:
        self['NumOperacion'] = a
    if (a := node.attrib.get('RfcEmisorCtaOrd')) is not None:
        self['RfcEmisorCtaOrd'] = a
    if (a := node.attrib.get('NomBancoOrdExt')) is not None:
        self['NomBancoOrdExt'] = a
    if (a := node.attrib.get('CtaOrdenante')) is not None:
        self['CtaOrdenante'] = a
    if (a := node.attrib.get('RfcEmisorCtaBen')) is not None:
        self['RfcEmisorCtaBen'] = a
    if (a := node.attrib.get('CtaBeneficiario')) is not None:
        self['CtaBeneficiario'] = a
    if (a := node.attrib.get('TipoCadPago')) is not None:
        self['TipoCadPago'] = catalog_code('C004_c_TipoCadenaPago', a)
    if (a := node.attrib.get('CertPago')) is not None:
        self['CertPago'] = a
    if (a := node.attrib.get('CadPago')) is not None:
        self['CadPago'] = a
    if (a := node.attrib.get('SelloPago')) is not None:
        self['SelloPago'] = a
    return self
def docto_relacionado1(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.sat.gob.mx/Pagos20}ImpuestosDR')
    if el is not None:
        self['ImpuestosDR'] = impuestos_dr0(cls, el)
    self['IdDocumento'] = node.attrib['IdDocumento']
    if (a := node.attrib.get('Serie')) is not None:
        self['Serie'] = a
    if (a := node.attrib.get('Folio')) is not None:
        self['Folio'] = a
    self['MonedaDR'] = catalog_code('C756_c_Moneda', node.attrib['MonedaDR'], 0)
    if (a := node.attrib.get('EquivalenciaDR')) is not None:
        self['EquivalenciaDR'] = Decimal(a)
    self['NumParcialidad'] = Xint(node.attrib['NumParcialidad'])
    self['ImpSaldoAnt'] = Decimal(node.attrib['ImpSaldoAnt'])
    self['ImpPagado'] = Decimal(node.attrib['ImpPagado'])
    self['ImpSaldoInsoluto'] = Decimal(node.attrib['ImpSaldoInsoluto'])
    self['ObjetoImpDR'] = catalog_code('C756_c_ObjetoImp', node.attrib['ObjetoImpDR'])
    return self
def impuestos_dr0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.sat.gob.mx/Pagos20}RetencionesDR')
    if el is not None:
        self['RetencionesDR'] = {impuesto_index(n.attrib, 'ImpuestoDR'): retencion_dr0(cls, n) for n in el.iterfind('{http://www.sat.gob.mx/Pagos20}RetencionDR')}
    el = node.find('{http://www.sat.gob.mx/Pagos20}TrasladosDR')
    if el is not None:
        self['TrasladosDR'] = {impuesto_index(n.attrib, 'ImpuestoDR'): traslado_dr0(cls, n) for n in el.iterfind('{http://www.sat.gob.mx/Pagos20}TrasladoDR')}
    return self
def retencion_dr0(cls, node):
    self = ScalarMap()
    self['BaseDR'] = Decimal(node.attrib['BaseDR'])
    self['ImpuestoDR'] = catalog_code('C756_c_Impuesto', node.attrib['ImpuestoDR'])
    self['TipoFactorDR'] = catalog_code('C756_c_TipoFactor', node.attrib['TipoFactorDR'])
    self['TasaOCuotaDR'] = Decimal(node.attrib['TasaOCuotaDR'])
    self['ImporteDR'] = Decimal(node.attrib['ImporteDR'])
    return self
def traslado_dr0(cls, node):
    self = ScalarMap()
    self['BaseDR'] = Decimal(node.attrib['BaseDR'])
    self['ImpuestoDR'] = catalog_code('C756_c_Impuesto', node.attrib['ImpuestoDR'])
    self['TipoFactorDR'] = catalog_code('C756_c_TipoFactor', node.attrib['TipoFactorDR'])
    if (a := node.attrib.get('TasaOCuotaDR')) is not None:
        self['TasaOCuotaDR'] = Decimal(a)
    if (a := node.attrib.get('ImporteDR')) is not None:
        self['ImporteDR'] = Decimal(a)
    return self
def impuestos_p0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.sat.gob.mx/Pagos20}RetencionesP')
    if el is not None:
        self['RetencionesP'] = {impuesto_index(n.attrib, 'ImpuestoP'): retencion_p0(cls, n) for n in el.iterfind('{http://www.sat.gob.mx/Pagos20}RetencionP')}
    el = node.find('{http://www.sat.gob.mx/Pagos20}TrasladosP')
    if el is not None:
        self['TrasladosP'] = {impuesto_index(n.attrib, 'ImpuestoP'): traslado_p0(cls, n) for n in el.iterfind('{http://www.sat.gob.mx/Pagos20}TrasladoP')}
    return self
def retencion_p0(cls, node):
    self = ScalarMap()
    self['ImpuestoP'] = catalog_code('C756_c_Impuesto', node.attrib['ImpuestoP'])
    self['ImporteP'] = Decimal(node.attrib['ImporteP'])
    return self
def traslado_p0(cls, node):
    self = ScalarMap()
    self['BaseP'] = Decimal(node.attrib['BaseP'])
    self['ImpuestoP'] = catalog_code('C756_c_Impuesto', node.attrib['ImpuestoP'])
    self['TipoFactorP'] = catalog_code('C756_c_TipoFactor', node.attrib['TipoFactorP'])
    if (a := node.attrib.get('TasaOCuotaP')) is not None:
        self['TasaOCuotaP'] = Decimal(a)
    if (a := node.attrib.get('ImporteP')) is not None:
        self['ImporteP'] = Decimal(a)
    return self
def timbre_fiscal_digital0(cls, node):
    self = cls()
    self.tag = node.tag
    self['Version'] = node.attrib['version']
    self['UUID'] = node.attrib['UUID']
    self['FechaTimbrado'] = datetime.fromisoformat(node.attrib['FechaTimbrado'])
    self['SelloCFD'] = node.attrib['selloCFD']
    self['NoCertificadoSAT'] = node.attrib['noCertificadoSAT']
    self['SelloSAT'] = node.attrib['selloSAT']
    return self
def timbre_fiscal_digital1(cls, node):
    self = cls()
    self.tag = node.tag
    self['Version'] = node.attrib['Version']
    self['UUID'] = node.attrib['UUID']
    self['FechaTimbrado'] = datetime.fromisoformat(node.attrib['FechaTimbrado'])
    self['RfcProvCertif'] = node.attrib['RfcProvCertif']
    if (a := node.attrib.get('Leyenda')) is not None:
        self['Leyenda'] = a
    self['SelloCFD'] = node.attrib['SelloCFD']
    self['NoCertificadoSAT'] = node.attrib['NoCertificadoSAT']
    self['SelloSAT'] = node.attrib['SelloSAT']
    return self
def turista_pasajero_extranjero0(cls, node):
    self = cls()
    self.tag = node.tag
    el = node.find('{http://www.sat.gob.mx/TuristaPasajeroExtranjero}datosTransito')
    self['DatosTransito'] = datos_transito0(cls, el)
    self['Version'] = node.attrib['version']
    self['FechadeTransito'] = datetime.fromisoformat(node.attrib['fechadeTransito'])
    self['TipoTransito'] = node.attrib['tipoTransito']
    return self
def datos_transito0(cls, node):
    self = ScalarMap()
    self['Via'] = node.attrib['Via']
    self['TipoId'] = node.attrib['TipoId']
    self['NumeroId'] = node.attrib['NumeroId']
    self['Nacionalidad'] = node.attrib['Nacionalidad']
    self['EmpresaTransporte'] = node.attrib['EmpresaTransporte']
    if (a := node.attrib.get('IdTransporte')) is not None:
        self['IdTransporte'] = a
    return self
def acreditamiento_ieps0(cls, node):
    self = cls()
    self.tag = node.tag
    self['Version'] = node.attrib['Version']
    self['TAR'] = catalog_code('C40c_c_TAR', node.attrib['TAR'])
    return self
def aerolineas0(cls, node):
    self = cls()
    self.tag = node.tag
    el = node.find('{http://www.sat.gob.mx/aerolineas}OtrosCargos')
    if el is not None:
        self['OtrosCargos'] = otros_cargos0(cls, el)
    self['Version'] = node.attrib['Version']
    self['TUA'] = Decimal(node.attrib['TUA'])
    return self
def otros_cargos0(cls, node):
    self = ScalarMap()
    self['Cargo'] = [cargo0(cls, n) for n in node.iterfind('{http://www.sat.gob.mx/aerolineas}Cargo')]
    self['TotalCargos'] = Decimal(node.attrib['TotalCargos'])
    return self
def cargo0(cls, node):
    self = ScalarMap()
    self['CodigoCargo'] = node.attrib['CodigoCargo']
    self['Importe'] = Decimal(node.attrib['Importe'])
    return self
def obrasarteantiguedades0(cls, node):
    self = cls()
    self.tag = node.tag
    self['Version'] = node.attrib['Version']
    self['TipoBien'] = catalog_code('Cc50_c_TipoBien', node.attrib['TipoBien'])
    if (a := node.attrib.get('OtrosTipoBien')) is not None:
        self['OtrosTipoBien'] = a
    self['TituloAdquirido'] = catalog_code('Cc50_c_Tituloadquirido', node.attrib['TituloAdquirido'])
    if (a := node.attrib.get('OtrosTituloAdquirido')) is not None:
        self['OtrosTituloAdquirido'] = a
    if (a := node.attrib.get('Subtotal')) is not None:
        self['Subtotal'] = Decimal(a)
    if (a := node.attrib.get('IVA')) is not None:
        self['IVA'] = Decimal(a)
    self['FechaAdquisicion'] = date.fromisoformat(node.attrib['FechaAdquisicion'])
    self['CaracterísticasDeObraoPieza'] = catalog_code('Cc50_c_CaracterísticasDeObraoPieza', node.attrib['CaracterísticasDeObraoPieza'])
    return self
def certificadodedestruccion0(cls, node):
    self = cls()
    self.tag = node.tag
    el = node.find('{http://www.sat.gob.mx/certificadodestruccion}VehiculoDestruido')
    self['VehiculoDestruido'] = vehiculo_destruido0(cls, el)
    el = node.find('{http://www.sat.gob.mx/certificadodestruccion}InformacionAduanera')
    if el is not None:
        self['InformacionAduanera'] = informacion_aduanera4(cls, el)
    self['Version'] = node.attrib['Version']
    self['Serie'] = catalog_code('Cc31_c_TipoSerie', node.attrib['Serie'])
    self['NumFolDesVeh'] = node.attrib['NumFolDesVeh']
    return self
def vehiculo_destruido0(cls, node):
    self = ScalarMap()
    self['Marca'] = node.attrib['Marca']
    self['TipooClase'] = node.attrib['TipooClase']
    self['Año'] = Xint(node.attrib['Año'])
    if (a := node.attrib.get('Modelo')) is not None:
        self['Modelo'] = a
    if (a := node.attrib.get('NIV')) is not None:
        self['NIV'] = a
    if (a := node.attrib.get('NumSerie')) is not None:
        self['NumSerie'] = a
    self['NumPlacas'] = node.attrib['NumPlacas']
    if (a := node.attrib.get('NumMotor')) is not None:
        self['NumMotor'] = a
    self['NumFolTarjCir'] = node.attrib['NumFolTarjCir']
    return self
def informacion_aduanera4(cls, node):
    self = ScalarMap()
    self['NumPedImp'] = node.attrib['NumPedImp']
    self['Fecha'] = date.fromisoformat(node.attrib['Fecha'])
    self['Aduana'] = node.attrib['Aduana']
    return self
def cfdiregistro_fiscal0(cls, node):
    self = cls()
    self.tag = node.tag
    self['Version'] = node.attrib['Version']
    self['Folio'] = node.attrib['Folio']
    return self
def consumo_de_combustibles0(cls, node):
    self = cls()
    self.tag = node.tag
    el = node.find('{http://www.sat.gob.mx/ConsumoDeCombustibles11}Conceptos')
    self['Conceptos'] = [concepto_consumo_de_combustibles0(cls, n) for n in el.iterfind('{http://www.sat.gob.mx/ConsumoDeCombustibles11}ConceptoConsumoDeCombustibles')]
    self['Version'] = node.attrib['version']
    self['TipoOperacion'] = node.attrib['tipoOperacion']
    self['NumeroDeCuenta'] = node.attrib['numeroDeCuenta']
    if (a := node.attrib.get('subTotal')) is not None:
        self['SubTotal'] = Decimal(a)
    self['Total'] = Decimal(node.attrib['total'])
    return self
def concepto_consumo_de_combustibles0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.sat.gob.mx/ConsumoDeCombustibles11}Determinados')
    self['Determinados'] = [determinado0(cls, n) for n in el.iterfind('{http://www.sat.gob.mx/ConsumoDeCombustibles11}Determinado')]
    self['Identificador'] = node.attrib['identificador']
    self['Fecha'] = datetime.fromisoformat(node.attrib['fecha'])
    self['Rfc'] = node.attrib['rfc']
    self['ClaveEstacion'] = node.attrib['claveEstacion']
    self['TipoCombustible'] = catalog_code('C23d_c_ClaveTipoCombustible', node.attrib['tipoCombustible'])
    self['Cantidad'] = Decimal(node.attrib['cantidad'])
    self['NombreCombustible'] = node.attrib['nombreCombustible']
    self['FolioOperacion'] = node.attrib['folioOperacion']
    self['ValorUnitario'] = Decimal(node.attrib['valorUnitario'])
    self['Importe'] = Decimal(node.attrib['importe'])
    return self
def determinado0(cls, node):
    self = ScalarMap()
    self['Impuesto'] = node.attrib['impuesto']
    self['TasaOCuota'] = Decimal(node.attrib['tasaOCuota'])
    self['Importe'] = Decimal(node.attrib['importe'])
    return self
def consumo_de_combustibles1(cls, node):
    self = cls()
    self.tag = node.tag
    el = node.find('{http://www.sat.gob.mx/consumodecombustibles}Conceptos')
    self['Conceptos'] = [concepto_consumo_de_combustibles1(cls, n) for n in el.iterfind('{http://www.sat.gob.mx/consumodecombustibles}ConceptoConsumoDeCombustibles')]
    self['Version'] = node.attrib['version']
    self['TipoOperacion'] = node.attrib['tipoOperacion']
    self['NumeroDeCuenta'] = node.attrib['numeroDeCuenta']
    if (a := node.attrib.get('subTotal')) is not None:
        self['SubTotal'] = Decimal(a)
    self['Total'] = Decimal(node.attrib['total'])
    return self
def concepto_consumo_de_combustibles1(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.sat.gob.mx/consumodecombustibles}Determinados')
    self['Determinados'] = [determinado1(cls, n) for n in el.iterfind('{http://www.sat.gob.mx/consumodecombustibles}Determinado')]
    self['Identificador'] = node.attrib['identificador']
    self['Fecha'] = datetime.fromisoformat(node.attrib['fecha'])
    self['Rfc'] = node.attrib['rfc']
    self['ClaveEstacion'] = node.attrib['claveEstacion']
    self['Cantidad'] = Decimal(node.attrib['cantidad'])
    self['NombreCombustible'] = node.attrib['nombreCombustible']
    self['FolioOperacion'] = node.attrib['folioOperacion']
    self['ValorUnitario'] = Decimal(node.attrib['valorUnitario'])
    self['Importe'] = Decimal(node.attrib['importe'])
    return self
def determinado1(cls, node):
    self = ScalarMap()
    self['Impuesto'] = node.attrib['impuesto']
    self['Tasa'] = Decimal(node.attrib['tasa'])
    self['Importe'] = Decimal(node.attrib['importe'])
    return self
def detallista0(cls, node):
    self = cls()
    self.tag = node.tag
    el = node.find('{http://www.sat.gob.mx/detallista}requestForPaymentIdentification')
    self['RequestForPaymentIdentification'] = request_for_payment_identification0(cls, el)
    el = node.find('{http://www.sat.gob.mx/detallista}specialInstruction')
    if el is not None:
        self['SpecialInstruction'] = [special_instruction0(cls, n) for n in node.iterfind('{http://www.sat.gob.mx/detallista}specialInstruction')]
    el = node.find('{http://www.sat.gob.mx/detallista}orderIdentification')
    self['OrderIdentification'] = order_identification0(cls, el)
    el = node.find('{http://www.sat.gob.mx/detallista}AdditionalInformation')
    self['AdditionalInformation'] = [reference_identification1(cls, n) for n in el.iterfind('{http://www.sat.gob.mx/detallista}referenceIdentification')]
    el = node.find('{http://www.sat.gob.mx/detallista}DeliveryNote')
    if el is not None:
        self['DeliveryNote'] = delivery_note0(cls, el)
    el = node.find('{http://www.sat.gob.mx/detallista}buyer')
    self['Buyer'] = buyer0(cls, el)
    el = node.find('{http://www.sat.gob.mx/detallista}seller')
    if el is not None:
        self['Seller'] = seller0(cls, el)
    el = node.find('{http://www.sat.gob.mx/detallista}shipTo')
    if el is not None:
        self['ShipTo'] = ship_to0(cls, el)
    el = node.find('{http://www.sat.gob.mx/detallista}InvoiceCreator')
    if el is not None:
        self['InvoiceCreator'] = invoice_creator0(cls, el)
    el = node.find('{http://www.sat.gob.mx/detallista}Customs')
    if el is not None:
        self['Customs'] = [n.text for n in el.iterfind('{http://www.sat.gob.mx/detallista}gln')]
    el = node.find('{http://www.sat.gob.mx/detallista}currency')
    if el is not None:
        self['Currency'] = [currency0(cls, n) for n in node.iterfind('{http://www.sat.gob.mx/detallista}currency')]
    el = node.find('{http://www.sat.gob.mx/detallista}paymentTerms')
    if el is not None:
        self['PaymentTerms'] = payment_terms0(cls, el)
    el = node.find('{http://www.sat.gob.mx/detallista}shipmentDetail')
    if el is not None:
        self['ShipmentDetail'] = shipment_detail0(cls, el)
    el = node.find('{http://www.sat.gob.mx/detallista}allowanceCharge')
    if el is not None:
        self['AllowanceCharge'] = [allowance_charge0(cls, n) for n in node.iterfind('{http://www.sat.gob.mx/detallista}allowanceCharge')]
    el = node.find('{http://www.sat.gob.mx/detallista}lineItem')
    if el is not None:
        self['LineItem'] = [line_item0(cls, n) for n in node.iterfind('{http://www.sat.gob.mx/detallista}lineItem')]
    el = node.find('{http://www.sat.gob.mx/detallista}totalAmount')
    if el is not None:
        self['TotalAmount'] = total_amount0(cls, el)
    el = node.find('{http://www.sat.gob.mx/detallista}TotalAllowanceCharge')
    if el is not None:
        self['TotalAllowanceCharge'] = [total_allowance_charge0(cls, n) for n in node.iterfind('{http://www.sat.gob.mx/detallista}TotalAllowanceCharge')]
    if (a := node.attrib.get('type')) is not None:
        self['Type'] = a
    if (a := node.attrib.get('contentVersion')) is not None:
        self['ContentVersion'] = a
    self['DocumentStructureVersion'] = node.attrib['documentStructureVersion']
    self['DocumentStatus'] = node.attrib['documentStatus']
    return self
def request_for_payment_identification0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.sat.gob.mx/detallista}entityType')
    self['EntityType'] = el.text
    return self
def special_instruction0(cls, node):
    self = ScalarMap()
    self['Text'] = [n.text for n in node.iterfind('{http://www.sat.gob.mx/detallista}text')]
    self['Code'] = node.attrib['code']
    return self
def order_identification0(cls, node):
    self = ScalarMap()
    self['ReferenceIdentification'] = [reference_identification0(cls, n) for n in node.iterfind('{http://www.sat.gob.mx/detallista}referenceIdentification')]
    el = node.find('{http://www.sat.gob.mx/detallista}ReferenceDate')
    if el is not None:
        self['ReferenceDate'] = date.fromisoformat(el.text)
    return self
def reference_identification0(cls, node):
    self = ScalarMap()
    self['_text'] = node.text
    self['Type'] = node.attrib['type']
    return self
def reference_identification1(cls, node):
    self = ScalarMap()
    self['_text'] = node.text
    self['Type'] = node.attrib['type']
    return self
def delivery_note0(cls, node):
    self = ScalarMap()
    self['ReferenceIdentification'] = [n.text for n in node.iterfind('{http://www.sat.gob.mx/detallista}referenceIdentification')]
    el = node.find('{http://www.sat.gob.mx/detallista}ReferenceDate')
    if el is not None:
        self['ReferenceDate'] = date.fromisoformat(el.text)
    return self
def buyer0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.sat.gob.mx/detallista}gln')
    self['Gln'] = el.text
    el = node.find('{http://www.sat.gob.mx/detallista}contactInformation')
    if el is not None:
        self['ContactInformation'] = contact_information0(cls, el)
    return self
def contact_information0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.sat.gob.mx/detallista}personOrDepartmentName')
    self['PersonOrDepartmentName'] = person_or_department_name0(cls, el)
    return self
def person_or_department_name0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.sat.gob.mx/detallista}text')
    self['Text'] = el.text
    return self
def seller0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.sat.gob.mx/detallista}gln')
    self['Gln'] = el.text
    el = node.find('{http://www.sat.gob.mx/detallista}alternatePartyIdentification')
    self['AlternatePartyIdentification'] = alternate_party_identification0(cls, el)
    return self
def alternate_party_identification0(cls, node):
    self = ScalarMap()
    self['_text'] = node.text
    self['Type'] = node.attrib['type']
    return self
def ship_to0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.sat.gob.mx/detallista}gln')
    if el is not None:
        self['Gln'] = el.text
    el = node.find('{http://www.sat.gob.mx/detallista}nameAndAddress')
    if el is not None:
        self['NameAndAddress'] = name_and_address0(cls, el)
    return self
def name_and_address0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.sat.gob.mx/detallista}name')
    if el is not None:
        self['Name'] = el.text
    el = node.find('{http://www.sat.gob.mx/detallista}streetAddressOne')
    if el is not None:
        self['StreetAddressOne'] = el.text
    el = node.find('{http://www.sat.gob.mx/detallista}city')
    if el is not None:
        self['City'] = el.text
    el = node.find('{http://www.sat.gob.mx/detallista}postalCode')
    if el is not None:
        self['PostalCode'] = el.text
    return self
def invoice_creator0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.sat.gob.mx/detallista}gln')
    if el is not None:
        self['Gln'] = el.text
    el = node.find('{http://www.sat.gob.mx/detallista}alternatePartyIdentification')
    if el is not None:
        self['AlternatePartyIdentification'] = alternate_party_identification1(cls, el)
    el = node.find('{http://www.sat.gob.mx/detallista}nameAndAddress')
    if el is not None:
        self['NameAndAddress'] = name_and_address1(cls, el)
    return self
def alternate_party_identification1(cls, node):
    self = ScalarMap()
    self['_text'] = node.text
    self['Type'] = node.attrib['type']
    return self
def name_and_address1(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.sat.gob.mx/detallista}name')
    if el is not None:
        self['Name'] = el.text
    el = node.find('{http://www.sat.gob.mx/detallista}streetAddressOne')
    if el is not None:
        self['StreetAddressOne'] = el.text
    el = node.find('{http://www.sat.gob.mx/detallista}city')
    if el is not None:
        self['City'] = el.text
    el = node.find('{http://www.sat.gob.mx/detallista}postalCode')
    if el is not None:
        self['PostalCode'] = el.text
    return self
def currency0(cls, node):
    self = ScalarMap()
    self['CurrencyFunction'] = [n.text for n in node.iterfind('{http://www.sat.gob.mx/detallista}currencyFunction')]
    el = node.find('{http://www.sat.gob.mx/detallista}rateOfChange')
    if el is not None:
        self['RateOfChange'] = Decimal(el.text)
    self['CurrencyISOCode'] = node.attrib['currencyISOCode']
    return self
def payment_terms0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.sat.gob.mx/detallista}netPayment')
    if el is not None:
        self['NetPayment'] = net_payment0(cls, el)
    el = node.find('{http://www.sat.gob.mx/detallista}discountPayment')
    if el is not None:
        self['DiscountPayment'] = discount_payment0(cls, el)
    if (a := node.attrib.get('paymentTermsEvent')) is not None:
        self['PaymentTermsEvent'] = a
    if (a := node.attrib.get('PaymentTermsRelationTime')) is not None:
        self['PaymentTermsRelationTime'] = a
    return self
def net_payment0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.sat.gob.mx/detallista}paymentTimePeriod')
    if el is not None:
        self['PaymentTimePeriod'] = payment_time_period0(cls, el)
    self['NetPaymentTermsType'] = node.attrib['netPaymentTermsType']
    return self
def payment_time_period0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.sat.gob.mx/detallista}timePeriodDue')
    self['TimePeriodDue'] = time_period_due0(cls, el)
    return self
def time_period_due0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.sat.gob.mx/detallista}value')
    self['Value'] = el.text
    self['TimePeriod'] = node.attrib['timePeriod']
    return self
def discount_payment0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.sat.gob.mx/detallista}percentage')
    self['Percentage'] = el.text
    self['DiscountType'] = node.attrib['discountType']
    return self
def shipment_detail0(cls, node):
    self = ScalarMap()
    return self
def allowance_charge0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.sat.gob.mx/detallista}specialServicesType')
    if el is not None:
        self['SpecialServicesType'] = el.text
    el = node.find('{http://www.sat.gob.mx/detallista}monetaryAmountOrPercentage')
    if el is not None:
        self['MonetaryAmountOrPercentage'] = monetary_amount_or_percentage0(cls, el)
    self['AllowanceChargeType'] = node.attrib['allowanceChargeType']
    self['SettlementType'] = node.attrib['settlementType']
    if (a := node.attrib.get('sequenceNumber')) is not None:
        self['SequenceNumber'] = a
    return self
def monetary_amount_or_percentage0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.sat.gob.mx/detallista}rate')
    if el is not None:
        self['Rate'] = rate0(cls, el)
    return self
def rate0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.sat.gob.mx/detallista}percentage')
    self['Percentage'] = Decimal(el.text)
    self['Base'] = node.attrib['base']
    return self
def line_item0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.sat.gob.mx/detallista}tradeItemIdentification')
    self['TradeItemIdentification'] = trade_item_identification0(cls, el)
    el = node.find('{http://www.sat.gob.mx/detallista}alternateTradeItemIdentification')
    if el is not None:
        self['AlternateTradeItemIdentification'] = [alternate_trade_item_identification0(cls, n) for n in node.iterfind('{http://www.sat.gob.mx/detallista}alternateTradeItemIdentification')]
    el = node.find('{http://www.sat.gob.mx/detallista}tradeItemDescriptionInformation')
    if el is not None:
        self['TradeItemDescriptionInformation'] = trade_item_description_information0(cls, el)
    el = node.find('{http://www.sat.gob.mx/detallista}invoicedQuantity')
    self['InvoicedQuantity'] = invoiced_quantity0(cls, el)
    el = node.find('{http://www.sat.gob.mx/detallista}aditionalQuantity')
    if el is not None:
        self['AditionalQuantity'] = [aditional_quantity0(cls, n) for n in node.iterfind('{http://www.sat.gob.mx/detallista}aditionalQuantity')]
    el = node.find('{http://www.sat.gob.mx/detallista}grossPrice')
    if el is not None:
        self['GrossPrice'] = gross_price0(cls, el)
    el = node.find('{http://www.sat.gob.mx/detallista}netPrice')
    if el is not None:
        self['NetPrice'] = net_price0(cls, el)
    el = node.find('{http://www.sat.gob.mx/detallista}AdditionalInformation')
    if el is not None:
        self['AdditionalInformation'] = additional_information0(cls, el)
    el = node.find('{http://www.sat.gob.mx/detallista}Customs')
    if el is not None:
        self['Customs'] = [customs0(cls, n) for n in node.iterfind('{http://www.sat.gob.mx/detallista}Customs')]
    el = node.find('{http://www.sat.gob.mx/detallista}LogisticUnits')
    if el is not None:
        self['LogisticUnits'] = logistic_units0(cls, el)
    el = node.find('{http://www.sat.gob.mx/detallista}palletInformation')
    if el is not None:
        self['PalletInformation'] = pallet_information0(cls, el)
    el = node.find('{http://www.sat.gob.mx/detallista}extendedAttributes')
    if el is not None:
        self['ExtendedAttributes'] = [lot_number0(cls, n) for n in el.iterfind('{http://www.sat.gob.mx/detallista}lotNumber')]
    el = node.find('{http://www.sat.gob.mx/detallista}allowanceCharge')
    if el is not None:
        self['AllowanceCharge'] = [allowance_charge1(cls, n) for n in node.iterfind('{http://www.sat.gob.mx/detallista}allowanceCharge')]
    el = node.find('{http://www.sat.gob.mx/detallista}tradeItemTaxInformation')
    if el is not None:
        self['TradeItemTaxInformation'] = [trade_item_tax_information0(cls, n) for n in node.iterfind('{http://www.sat.gob.mx/detallista}tradeItemTaxInformation')]
    el = node.find('{http://www.sat.gob.mx/detallista}totalLineAmount')
    self['TotalLineAmount'] = total_line_amount0(cls, el)
    if (a := node.attrib.get('type')) is not None:
        self['Type'] = a
    if (a := node.attrib.get('number')) is not None:
        self['Number'] = Xint(a)
    return self
def trade_item_identification0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.sat.gob.mx/detallista}gtin')
    self['Gtin'] = el.text
    return self
def alternate_trade_item_identification0(cls, node):
    self = ScalarMap()
    self['_text'] = node.text
    self['Type'] = node.attrib['type']
    return self
def trade_item_description_information0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.sat.gob.mx/detallista}longText')
    self['LongText'] = el.text
    if (a := node.attrib.get('language')) is not None:
        self['Language'] = a
    return self
def invoiced_quantity0(cls, node):
    self = ScalarMap()
    self['_text'] = Decimal(node.text)
    self['UnitOfMeasure'] = node.attrib['unitOfMeasure']
    return self
def aditional_quantity0(cls, node):
    self = ScalarMap()
    self['_text'] = Decimal(node.text)
    self['QuantityType'] = node.attrib['QuantityType']
    return self
def gross_price0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.sat.gob.mx/detallista}Amount')
    self['Amount'] = Decimal(el.text)
    return self
def net_price0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.sat.gob.mx/detallista}Amount')
    self['Amount'] = Decimal(el.text)
    return self
def additional_information0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.sat.gob.mx/detallista}referenceIdentification')
    if el is not None:
        self['ReferenceIdentification'] = reference_identification2(cls, el)
    return self
def reference_identification2(cls, node):
    self = ScalarMap()
    self['_text'] = node.text
    self['Type'] = node.attrib['type']
    return self
def customs0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.sat.gob.mx/detallista}gln')
    if el is not None:
        self['Gln'] = el.text
    el = node.find('{http://www.sat.gob.mx/detallista}alternatePartyIdentification')
    self['AlternatePartyIdentification'] = alternate_party_identification2(cls, el)
    el = node.find('{http://www.sat.gob.mx/detallista}ReferenceDate')
    self['ReferenceDate'] = date.fromisoformat(el.text)
    el = node.find('{http://www.sat.gob.mx/detallista}nameAndAddress')
    self['NameAndAddress'] = name_and_address2(cls, el)
    return self
def alternate_party_identification2(cls, node):
    self = ScalarMap()
    self['_text'] = node.text
    self['Type'] = node.attrib['type']
    return self
def name_and_address2(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.sat.gob.mx/detallista}name')
    self['Name'] = el.text
    return self
def logistic_units0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.sat.gob.mx/detallista}serialShippingContainerCode')
    self['SerialShippingContainerCode'] = serial_shipping_container_code0(cls, el)
    return self
def serial_shipping_container_code0(cls, node):
    self = ScalarMap()
    self['_text'] = node.text
    self['Type'] = node.attrib['type']
    return self
def pallet_information0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.sat.gob.mx/detallista}palletQuantity')
    self['PalletQuantity'] = el.text
    el = node.find('{http://www.sat.gob.mx/detallista}description')
    self['Description'] = description0(cls, el)
    el = node.find('{http://www.sat.gob.mx/detallista}transport')
    self['Transport'] = transport0(cls, el)
    return self
def description0(cls, node):
    self = ScalarMap()
    self['_text'] = node.text
    self['Type'] = node.attrib['type']
    return self
def transport0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.sat.gob.mx/detallista}methodOfPayment')
    self['MethodOfPayment'] = el.text
    return self
def lot_number0(cls, node):
    self = ScalarMap()
    self['_text'] = node.text
    if (a := node.attrib.get('productionDate')) is not None:
        self['ProductionDate'] = date.fromisoformat(a)
    return self
def allowance_charge1(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.sat.gob.mx/detallista}specialServicesType')
    if el is not None:
        self['SpecialServicesType'] = el.text
    el = node.find('{http://www.sat.gob.mx/detallista}monetaryAmountOrPercentage')
    self['MonetaryAmountOrPercentage'] = monetary_amount_or_percentage1(cls, el)
    self['AllowanceChargeType'] = node.attrib['allowanceChargeType']
    if (a := node.attrib.get('settlementType')) is not None:
        self['SettlementType'] = a
    if (a := node.attrib.get('sequenceNumber')) is not None:
        self['SequenceNumber'] = a
    return self
def monetary_amount_or_percentage1(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.sat.gob.mx/detallista}percentagePerUnit')
    self['PercentagePerUnit'] = el.text
    el = node.find('{http://www.sat.gob.mx/detallista}ratePerUnit')
    if el is not None:
        self['RatePerUnit'] = rate_per_unit0(cls, el)
    return self
def rate_per_unit0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.sat.gob.mx/detallista}amountPerUnit')
    self['AmountPerUnit'] = el.text
    return self
def trade_item_tax_information0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.sat.gob.mx/detallista}taxTypeDescription')
    self['TaxTypeDescription'] = el.text
    el = node.find('{http://www.sat.gob.mx/detallista}referenceNumber')
    if el is not None:
        self['ReferenceNumber'] = el.text
    el = node.find('{http://www.sat.gob.mx/detallista}tradeItemTaxAmount')
    if el is not None:
        self['TradeItemTaxAmount'] = trade_item_tax_amount0(cls, el)
    el = node.find('{http://www.sat.gob.mx/detallista}taxCategory')
    if el is not None:
        self['TaxCategory'] = el.text
    return self
def trade_item_tax_amount0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.sat.gob.mx/detallista}taxPercentage')
    self['TaxPercentage'] = Decimal(el.text)
    el = node.find('{http://www.sat.gob.mx/detallista}taxAmount')
    self['TaxAmount'] = Decimal(el.text)
    return self
def total_line_amount0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.sat.gob.mx/detallista}grossAmount')
    if el is not None:
        self['GrossAmount'] = gross_amount0(cls, el)
    el = node.find('{http://www.sat.gob.mx/detallista}netAmount')
    self['NetAmount'] = net_amount0(cls, el)
    return self
def gross_amount0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.sat.gob.mx/detallista}Amount')
    self['Amount'] = Decimal(el.text)
    return self
def net_amount0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.sat.gob.mx/detallista}Amount')
    self['Amount'] = Decimal(el.text)
    return self
def total_amount0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.sat.gob.mx/detallista}Amount')
    self['Amount'] = Decimal(el.text)
    return self
def total_allowance_charge0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.sat.gob.mx/detallista}specialServicesType')
    if el is not None:
        self['SpecialServicesType'] = el.text
    el = node.find('{http://www.sat.gob.mx/detallista}Amount')
    if el is not None:
        self['Amount'] = Decimal(el.text)
    self['AllowanceOrChargeType'] = node.attrib['allowanceOrChargeType']
    return self
def divisas0(cls, node):
    self = cls()
    self.tag = node.tag
    self['Version'] = node.attrib['version']
    self['TipoOperacion'] = node.attrib['tipoOperacion']
    return self
def donatarias0(cls, node):
    self = cls()
    self.tag = node.tag
    self['Version'] = node.attrib['version']
    self['NoAutorizacion'] = node.attrib['noAutorizacion']
    self['FechaAutorizacion'] = date.fromisoformat(node.attrib['fechaAutorizacion'])
    self['Leyenda'] = node.attrib['leyenda']
    return self
def estado_de_cuenta_bancario0(cls, node):
    self = cls()
    self.tag = node.tag
    el = node.find('{http://www.sat.gob.mx/ecb}Movimientos')
    self['Movimientos'] = movimientos0(cls, el)
    self['Version'] = node.attrib['version']
    self['NumeroCuenta'] = Xint(node.attrib['numeroCuenta'])
    self['NombreCliente'] = node.attrib['nombreCliente']
    self['Periodo'] = node.attrib['periodo']
    if (a := node.attrib.get('sucursal')) is not None:
        self['Sucursal'] = a
    return self
def movimientos0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.sat.gob.mx/ecb}MovimientoECB')
    if el is not None:
        self['MovimientoECB'] = movimiento_ecb0(cls, el)
    el = node.find('{http://www.sat.gob.mx/ecb}MovimientoECBFiscal')
    if el is not None:
        self['MovimientoECBFiscal'] = movimiento_ecbfiscal0(cls, el)
    return self
def movimiento_ecb0(cls, node):
    self = ScalarMap()
    self['Fecha'] = datetime.fromisoformat(node.attrib['fecha'])
    if (a := node.attrib.get('referencia')) is not None:
        self['Referencia'] = a
    self['Descripcion'] = node.attrib['descripcion']
    self['Importe'] = Decimal(node.attrib['importe'])
    if (a := node.attrib.get('moneda')) is not None:
        self['Moneda'] = a
    if (a := node.attrib.get('saldoInicial')) is not None:
        self['SaldoInicial'] = Decimal(a)
    if (a := node.attrib.get('saldoAlCorte')) is not None:
        self['SaldoAlCorte'] = Decimal(a)
    return self
def movimiento_ecbfiscal0(cls, node):
    self = ScalarMap()
    self['Fecha'] = datetime.fromisoformat(node.attrib['fecha'])
    if (a := node.attrib.get('referencia')) is not None:
        self['Referencia'] = a
    self['Descripcion'] = node.attrib['descripcion']
    self['RFCenajenante'] = node.attrib['RFCenajenante']
    self['Importe'] = Decimal(node.attrib['Importe'])
    if (a := node.attrib.get('moneda')) is not None:
        self['Moneda'] = a
    if (a := node.attrib.get('saldoInicial')) is not None:
        self['SaldoInicial'] = Decimal(a)
    if (a := node.attrib.get('saldoAlCorte')) is not None:
        self['SaldoAlCorte'] = Decimal(a)
    return self
def estado_de_cuenta_combustible2(cls, node):
    self = cls()
    self.tag = node.tag
    el = node.find('{http://www.sat.gob.mx/ecc}Conceptos')
    self['Conceptos'] = [concepto_estado_de_cuenta_combustible2(cls, n) for n in el.iterfind('{http://www.sat.gob.mx/ecc}ConceptoEstadoDeCuentaCombustible')]
    self['TipoOperacion'] = node.attrib['tipoOperacion']
    self['NumeroDeCuenta'] = node.attrib['numeroDeCuenta']
    if (a := node.attrib.get('subTotal')) is not None:
        self['SubTotal'] = Decimal(a)
    self['Total'] = Decimal(node.attrib['total'])
    return self
def concepto_estado_de_cuenta_combustible2(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.sat.gob.mx/ecc}Traslados')
    self['Traslados'] = [traslado8(cls, n) for n in el.iterfind('{http://www.sat.gob.mx/ecc}Traslado')]
    self['Identificador'] = node.attrib['identificador']
    self['Fecha'] = datetime.fromisoformat(node.attrib['fecha'])
    self['Rfc'] = node.attrib['rfc']
    self['ClaveEstacion'] = node.attrib['claveEstacion']
    self['Cantidad'] = Decimal(node.attrib['cantidad'])
    self['NombreCombustible'] = node.attrib['nombreCombustible']
    self['FolioOperacion'] = node.attrib['folioOperacion']
    self['ValorUnitario'] = Decimal(node.attrib['valorUnitario'])
    self['Importe'] = Decimal(node.attrib['importe'])
    return self
def traslado8(cls, node):
    self = ScalarMap()
    self['Impuesto'] = node.attrib['impuesto']
    self['Tasa'] = Decimal(node.attrib['tasa'])
    self['Importe'] = Decimal(node.attrib['importe'])
    return self
def inst_educativas0(cls, node):
    self = cls()
    self.tag = node.tag
    self['Version'] = node.attrib['version']
    self['NombreAlumno'] = node.attrib['nombreAlumno']
    self['CURP'] = node.attrib['CURP']
    self['NivelEducativo'] = node.attrib['nivelEducativo']
    self['AutRVOE'] = node.attrib['autRVOE']
    if (a := node.attrib.get('rfcPago')) is not None:
        self['RfcPago'] = a
    return self
def impuestos_locales0(cls, node):
    self = cls()
    self.tag = node.tag
    el = node.find('{http://www.sat.gob.mx/implocal}RetencionesLocales')
    if el is not None:
        self['RetencionesLocales'] = retenciones_locales0(cls, el)
    el = node.find('{http://www.sat.gob.mx/implocal}TrasladosLocales')
    if el is not None:
        self['TrasladosLocales'] = traslados_locales0(cls, el)
    self['Version'] = node.attrib['version']
    self['TotaldeRetenciones'] = Decimal(node.attrib['TotaldeRetenciones'])
    self['TotaldeTraslados'] = Decimal(node.attrib['TotaldeTraslados'])
    return self
def retenciones_locales0(cls, node):
    self = ScalarMap()
    self['ImpLocRetenido'] = node.attrib['ImpLocRetenido']
    self['TasadeRetencion'] = Decimal(node.attrib['TasadeRetencion'])
    self['Importe'] = Decimal(node.attrib['Importe'])
    return self
def traslados_locales0(cls, node):
    self = ScalarMap()
    self['ImpLocTrasladado'] = node.attrib['ImpLocTrasladado']
    self['TasadeTraslado'] = Decimal(node.attrib['TasadeTraslado'])
    self['Importe'] = Decimal(node.attrib['Importe'])
    return self
def ine0(cls, node):
    self = cls()
    self.tag = node.tag
    el = node.find('{http://www.sat.gob.mx/ine}Entidad')
    if el is not None:
        self['Entidad'] = [entidad0(cls, n) for n in node.iterfind('{http://www.sat.gob.mx/ine}Entidad')]
    self['Version'] = node.attrib['Version']
    self['TipoProceso'] = node.attrib['TipoProceso']
    if (a := node.attrib.get('TipoComite')) is not None:
        self['TipoComite'] = a
    if (a := node.attrib.get('IdContabilidad')) is not None:
        self['IdContabilidad'] = Xint(a)
    return self
def entidad0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.sat.gob.mx/ine}Contabilidad')
    if el is not None:
        self['Contabilidad'] = [contabilidad0(cls, n) for n in node.iterfind('{http://www.sat.gob.mx/ine}Contabilidad')]
    self['ClaveEntidad'] = catalog_code('Ca37_t_ClaveEntidad', node.attrib['ClaveEntidad'])
    if (a := node.attrib.get('Ambito')) is not None:
        self['Ambito'] = a
    return self
def contabilidad0(cls, node):
    return Xint(node.attrib['IdContabilidad'])
def ine1(cls, node):
    self = cls()
    self.tag = node.tag
    el = node.find('{http://www.sat.gob.mx/ine}Entidad')
    if el is not None:
        self['Entidad'] = [entidad1(cls, n) for n in node.iterfind('{http://www.sat.gob.mx/ine}Entidad')]
    self['Version'] = node.attrib['Version']
    self['TipoProceso'] = node.attrib['TipoProceso']
    if (a := node.attrib.get('TipoComite')) is not None:
        self['TipoComite'] = a
    if (a := node.attrib.get('IdContabilidad')) is not None:
        self['IdContabilidad'] = Xint(a)
    return self
def entidad1(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.sat.gob.mx/ine}Contabilidad')
    if el is not None:
        self['Contabilidad'] = [contabilidad1(cls, n) for n in node.iterfind('{http://www.sat.gob.mx/ine}Contabilidad')]
    self['ClaveEntidad'] = catalog_code('Ca37_t_ClaveEntidad', node.attrib['ClaveEntidad'])
    if (a := node.attrib.get('Ambito')) is not None:
        self['Ambito'] = a
    return self
def contabilidad1(cls, node):
    return Xint(node.attrib['IdContabilidad'])
def leyendas_fiscales0(cls, node):
    self = cls()
    self.tag = node.tag
    self['Leyenda'] = [leyenda0(cls, n) for n in node.iterfind('{http://www.sat.gob.mx/leyendasFiscales}Leyenda')]
    self['Version'] = node.attrib['version']
    return self
def leyenda0(cls, node):
    self = ScalarMap()
    if (a := node.attrib.get('disposicionFiscal')) is not None:
        self['DisposicionFiscal'] = a
    if (a := node.attrib.get('norma')) is not None:
        self['Norma'] = a
    self['TextoLeyenda'] = node.attrib['textoLeyenda']
    return self
def nomina0(cls, node):
    self = cls()
    self.tag = node.tag
    el = node.find('{http://www.sat.gob.mx/nomina}Percepciones')
    if el is not None:
        self['Percepciones'] = percepciones0(cls, el)
    el = node.find('{http://www.sat.gob.mx/nomina}Deducciones')
    if el is not None:
        self['Deducciones'] = deducciones0(cls, el)
    el = node.find('{http://www.sat.gob.mx/nomina}Incapacidades')
    if el is not None:
        self['Incapacidades'] = [incapacidad0(cls, n) for n in el.iterfind('{http://www.sat.gob.mx/nomina}Incapacidad')]
    el = node.find('{http://www.sat.gob.mx/nomina}HorasExtras')
    if el is not None:
        self['HorasExtras'] = [horas_extra0(cls, n) for n in el.iterfind('{http://www.sat.gob.mx/nomina}HorasExtra')]
    self['Version'] = node.attrib['Version']
    if (a := node.attrib.get('RegistroPatronal')) is not None:
        self['RegistroPatronal'] = a
    self['NumEmpleado'] = node.attrib['NumEmpleado']
    self['CURP'] = node.attrib['CURP']
    self['TipoRegimen'] = Xint(node.attrib['TipoRegimen'])
    if (a := node.attrib.get('NumSeguridadSocial')) is not None:
        self['NumSeguridadSocial'] = a
    self['FechaPago'] = date.fromisoformat(node.attrib['FechaPago'])
    self['FechaInicialPago'] = date.fromisoformat(node.attrib['FechaInicialPago'])
    self['FechaFinalPago'] = date.fromisoformat(node.attrib['FechaFinalPago'])
    self['NumDiasPagados'] = Decimal(node.attrib['NumDiasPagados'])
    if (a := node.attrib.get('Departamento')) is not None:
        self['Departamento'] = a
    if (a := node.attrib.get('CLABE')) is not None:
        self['CLABE'] = Xint(a)
    if (a := node.attrib.get('Banco')) is not None:
        self['Banco'] = Xint(a)
    if (a := node.attrib.get('FechaInicioRelLaboral')) is not None:
        self['FechaInicioRelLaboral'] = date.fromisoformat(a)
    if (a := node.attrib.get('Antiguedad')) is not None:
        self['Antiguedad'] = Xint(a)
    if (a := node.attrib.get('Puesto')) is not None:
        self['Puesto'] = a
    if (a := node.attrib.get('TipoContrato')) is not None:
        self['TipoContrato'] = a
    if (a := node.attrib.get('TipoJornada')) is not None:
        self['TipoJornada'] = a
    self['PeriodicidadPago'] = node.attrib['PeriodicidadPago']
    if (a := node.attrib.get('SalarioBaseCotApor')) is not None:
        self['SalarioBaseCotApor'] = Decimal(a)
    if (a := node.attrib.get('RiesgoPuesto')) is not None:
        self['RiesgoPuesto'] = Xint(a)
    if (a := node.attrib.get('SalarioDiarioIntegrado')) is not None:
        self['SalarioDiarioIntegrado'] = Decimal(a)
    return self
def percepciones0(cls, node):
    self = ScalarMap()
    self['Percepcion'] = [percepcion0(cls, n) for n in node.iterfind('{http://www.sat.gob.mx/nomina}Percepcion')]
    self['TotalGravado'] = Decimal(node.attrib['TotalGravado'])
    self['TotalExento'] = Decimal(node.attrib['TotalExento'])
    return self
def percepcion0(cls, node):
    self = ScalarMap()
    self['TipoPercepcion'] = Xint(node.attrib['TipoPercepcion'])
    self['Clave'] = node.attrib['Clave']
    self['Concepto'] = node.attrib['Concepto']
    self['ImporteGravado'] = Decimal(node.attrib['ImporteGravado'])
    self['ImporteExento'] = Decimal(node.attrib['ImporteExento'])
    return self
def deducciones0(cls, node):
    self = ScalarMap()
    self['Deduccion'] = [deduccion0(cls, n) for n in node.iterfind('{http://www.sat.gob.mx/nomina}Deduccion')]
    self['TotalGravado'] = Decimal(node.attrib['TotalGravado'])
    self['TotalExento'] = Decimal(node.attrib['TotalExento'])
    return self
def deduccion0(cls, node):
    self = ScalarMap()
    self['TipoDeduccion'] = Xint(node.attrib['TipoDeduccion'])
    self['Clave'] = node.attrib['Clave']
    self['Concepto'] = node.attrib['Concepto']
    self['ImporteGravado'] = Decimal(node.attrib['ImporteGravado'])
    self['ImporteExento'] = Decimal(node.attrib['ImporteExento'])
    return self
def incapacidad0(cls, node):
    self = ScalarMap()
    self['DiasIncapacidad'] = Decimal(node.attrib['DiasIncapacidad'])
    self['TipoIncapacidad'] = Xint(node.attrib['TipoIncapacidad'])
    self['Descuento'] = Decimal(node.attrib['Descuento'])
    return self
def horas_extra0(cls, node):
    self = ScalarMap()
    self['Dias'] = Xint(node.attrib['Dias'])
    self['TipoHoras'] = node.attrib['TipoHoras']
    self['HorasExtra'] = Xint(node.attrib['HorasExtra'])
    self['ImportePagado'] = Decimal(node.attrib['ImportePagado'])
    return self
def nomina1(cls, node):
    self = cls()
    self.tag = node.tag
    el = node.find('{http://www.sat.gob.mx/nomina12}Emisor')
    if el is not None:
        self['Emisor'] = emisor9(cls, el)
    el = node.find('{http://www.sat.gob.mx/nomina12}Receptor')
    self['Receptor'] = receptor9(cls, el)
    el = node.find('{http://www.sat.gob.mx/nomina12}Percepciones')
    if el is not None:
        self['Percepciones'] = percepciones1(cls, el)
    el = node.find('{http://www.sat.gob.mx/nomina12}Deducciones')
    if el is not None:
        self['Deducciones'] = deducciones1(cls, el)
    el = node.find('{http://www.sat.gob.mx/nomina12}OtrosPagos')
    if el is not None:
        self['OtrosPagos'] = [otro_pago0(cls, n) for n in el.iterfind('{http://www.sat.gob.mx/nomina12}OtroPago')]
    el = node.find('{http://www.sat.gob.mx/nomina12}Incapacidades')
    if el is not None:
        self['Incapacidades'] = [incapacidad1(cls, n) for n in el.iterfind('{http://www.sat.gob.mx/nomina12}Incapacidad')]
    self['Version'] = node.attrib['Version']
    self['TipoNomina'] = catalog_code('C75b_c_TipoNomina', node.attrib['TipoNomina'])
    self['FechaPago'] = date.fromisoformat(node.attrib['FechaPago'])
    self['FechaInicialPago'] = date.fromisoformat(node.attrib['FechaInicialPago'])
    self['FechaFinalPago'] = date.fromisoformat(node.attrib['FechaFinalPago'])
    self['NumDiasPagados'] = Decimal(node.attrib['NumDiasPagados'])
    if (a := node.attrib.get('TotalPercepciones')) is not None:
        self['TotalPercepciones'] = Decimal(a)
    if (a := node.attrib.get('TotalDeducciones')) is not None:
        self['TotalDeducciones'] = Decimal(a)
    if (a := node.attrib.get('TotalOtrosPagos')) is not None:
        self['TotalOtrosPagos'] = Decimal(a)
    return self
def emisor9(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.sat.gob.mx/nomina12}EntidadSNCF')
    if el is not None:
        self['EntidadSNCF'] = entidad_sncf0(cls, el)
    if (a := node.attrib.get('Curp')) is not None:
        self['Curp'] = a
    if (a := node.attrib.get('RegistroPatronal')) is not None:
        self['RegistroPatronal'] = a
    if (a := node.attrib.get('RfcPatronOrigen')) is not None:
        self['RfcPatronOrigen'] = a
    return self
def entidad_sncf0(cls, node):
    self = ScalarMap()
    self['OrigenRecurso'] = catalog_code('C75b_c_OrigenRecurso', node.attrib['OrigenRecurso'])
    if (a := node.attrib.get('MontoRecursoPropio')) is not None:
        self['MontoRecursoPropio'] = Decimal(a)
    return self
def receptor9(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.sat.gob.mx/nomina12}SubContratacion')
    if el is not None:
        self['SubContratacion'] = [sub_contratacion0(cls, n) for n in node.iterfind('{http://www.sat.gob.mx/nomina12}SubContratacion')]
    self['Curp'] = node.attrib['Curp']
    if (a := node.attrib.get('NumSeguridadSocial')) is not None:
        self['NumSeguridadSocial'] = a
    if (a := node.attrib.get('FechaInicioRelLaboral')) is not None:
        self['FechaInicioRelLaboral'] = date.fromisoformat(a)
    if (a := node.attrib.get('Antigüedad')) is not None:
        self['Antigüedad'] = a
    self['TipoContrato'] = catalog_code('C75b_c_TipoContrato', node.attrib['TipoContrato'])
    if (a := node.attrib.get('Sindicalizado')) is not None:
        self['Sindicalizado'] = a
    if (a := node.attrib.get('TipoJornada')) is not None:
        self['TipoJornada'] = catalog_code('C75b_c_TipoJornada', a)
    self['TipoRegimen'] = catalog_code('C75b_c_TipoRegimen', node.attrib['TipoRegimen'])
    self['NumEmpleado'] = node.attrib['NumEmpleado']
    if (a := node.attrib.get('Departamento')) is not None:
        self['Departamento'] = a
    if (a := node.attrib.get('Puesto')) is not None:
        self['Puesto'] = a
    if (a := node.attrib.get('RiesgoPuesto')) is not None:
        self['RiesgoPuesto'] = catalog_code('C75b_c_RiesgoPuesto', a)
    self['PeriodicidadPago'] = catalog_code('C75b_c_PeriodicidadPago', node.attrib['PeriodicidadPago'])
    if (a := node.attrib.get('Banco')) is not None:
        self['Banco'] = catalog_code('C75b_c_Banco', a)
    if (a := node.attrib.get('CuentaBancaria')) is not None:
        self['CuentaBancaria'] = Xint(a)
    if (a := node.attrib.get('SalarioBaseCotApor')) is not None:
        self['SalarioBaseCotApor'] = Decimal(a)
    if (a := node.attrib.get('SalarioDiarioIntegrado')) is not None:
        self['SalarioDiarioIntegrado'] = Decimal(a)
    self['ClaveEntFed'] = catalog_code('C756_c_Estado', node.attrib['ClaveEntFed'], 1)
    return self
def sub_contratacion0(cls, node):
    self = ScalarMap()
    self['RfcLabora'] = node.attrib['RfcLabora']
    self['PorcentajeTiempo'] = Decimal(node.attrib['PorcentajeTiempo'])
    return self
def percepciones1(cls, node):
    self = ScalarMap()
    self['Percepcion'] = [percepcion1(cls, n) for n in node.iterfind('{http://www.sat.gob.mx/nomina12}Percepcion')]
    el = node.find('{http://www.sat.gob.mx/nomina12}JubilacionPensionRetiro')
    if el is not None:
        self['JubilacionPensionRetiro'] = jubilacion_pension_retiro0(cls, el)
    el = node.find('{http://www.sat.gob.mx/nomina12}SeparacionIndemnizacion')
    if el is not None:
        self['SeparacionIndemnizacion'] = separacion_indemnizacion0(cls, el)
    if (a := node.attrib.get('TotalSueldos')) is not None:
        self['TotalSueldos'] = Decimal(a)
    if (a := node.attrib.get('TotalSeparacionIndemnizacion')) is not None:
        self['TotalSeparacionIndemnizacion'] = Decimal(a)
    if (a := node.attrib.get('TotalJubilacionPensionRetiro')) is not None:
        self['TotalJubilacionPensionRetiro'] = Decimal(a)
    self['TotalGravado'] = Decimal(node.attrib['TotalGravado'])
    self['TotalExento'] = Decimal(node.attrib['TotalExento'])
    return self
def percepcion1(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.sat.gob.mx/nomina12}AccionesOTitulos')
    if el is not None:
        self['AccionesOTitulos'] = acciones_o_titulos0(cls, el)
    el = node.find('{http://www.sat.gob.mx/nomina12}HorasExtra')
    if el is not None:
        self['HorasExtra'] = [horas_extra1(cls, n) for n in node.iterfind('{http://www.sat.gob.mx/nomina12}HorasExtra')]
    self['TipoPercepcion'] = catalog_code('C75b_c_TipoPercepcion', node.attrib['TipoPercepcion'])
    self['Clave'] = node.attrib['Clave']
    self['Concepto'] = node.attrib['Concepto']
    self['ImporteGravado'] = Decimal(node.attrib['ImporteGravado'])
    self['ImporteExento'] = Decimal(node.attrib['ImporteExento'])
    return self
def acciones_o_titulos0(cls, node):
    self = ScalarMap()
    self['ValorMercado'] = Decimal(node.attrib['ValorMercado'])
    self['PrecioAlOtorgarse'] = Decimal(node.attrib['PrecioAlOtorgarse'])
    return self
def horas_extra1(cls, node):
    self = ScalarMap()
    self['Dias'] = Xint(node.attrib['Dias'])
    self['TipoHoras'] = catalog_code('C75b_c_TipoHoras', node.attrib['TipoHoras'])
    self['HorasExtra'] = Xint(node.attrib['HorasExtra'])
    self['ImportePagado'] = Decimal(node.attrib['ImportePagado'])
    return self
def jubilacion_pension_retiro0(cls, node):
    self = ScalarMap()
    if (a := node.attrib.get('TotalUnaExhibicion')) is not None:
        self['TotalUnaExhibicion'] = Decimal(a)
    if (a := node.attrib.get('TotalParcialidad')) is not None:
        self['TotalParcialidad'] = Decimal(a)
    if (a := node.attrib.get('MontoDiario')) is not None:
        self['MontoDiario'] = Decimal(a)
    self['IngresoAcumulable'] = Decimal(node.attrib['IngresoAcumulable'])
    self['IngresoNoAcumulable'] = Decimal(node.attrib['IngresoNoAcumulable'])
    return self
def separacion_indemnizacion0(cls, node):
    self = ScalarMap()
    self['TotalPagado'] = Decimal(node.attrib['TotalPagado'])
    self['NumAñosServicio'] = Xint(node.attrib['NumAñosServicio'])
    self['UltimoSueldoMensOrd'] = Decimal(node.attrib['UltimoSueldoMensOrd'])
    self['IngresoAcumulable'] = Decimal(node.attrib['IngresoAcumulable'])
    self['IngresoNoAcumulable'] = Decimal(node.attrib['IngresoNoAcumulable'])
    return self
def deducciones1(cls, node):
    self = ScalarMap()
    self['Deduccion'] = [deduccion1(cls, n) for n in node.iterfind('{http://www.sat.gob.mx/nomina12}Deduccion')]
    if (a := node.attrib.get('TotalOtrasDeducciones')) is not None:
        self['TotalOtrasDeducciones'] = Decimal(a)
    if (a := node.attrib.get('TotalImpuestosRetenidos')) is not None:
        self['TotalImpuestosRetenidos'] = Decimal(a)
    return self
def deduccion1(cls, node):
    self = ScalarMap()
    self['TipoDeduccion'] = catalog_code('C75b_c_TipoDeduccion', node.attrib['TipoDeduccion'])
    self['Clave'] = node.attrib['Clave']
    self['Concepto'] = node.attrib['Concepto']
    self['Importe'] = Decimal(node.attrib['Importe'])
    return self
def otro_pago0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.sat.gob.mx/nomina12}SubsidioAlEmpleo')
    if el is not None:
        self['SubsidioAlEmpleo'] = subsidio_al_empleo0(cls, el)
    el = node.find('{http://www.sat.gob.mx/nomina12}CompensacionSaldosAFavor')
    if el is not None:
        self['CompensacionSaldosAFavor'] = compensacion_saldos_a_favor0(cls, el)
    self['TipoOtroPago'] = catalog_code('C75b_c_TipoOtroPago', node.attrib['TipoOtroPago'])
    self['Clave'] = node.attrib['Clave']
    self['Concepto'] = node.attrib['Concepto']
    self['Importe'] = Decimal(node.attrib['Importe'])
    return self
def subsidio_al_empleo0(cls, node):
    return Decimal(node.attrib['SubsidioCausado'])
def compensacion_saldos_a_favor0(cls, node):
    self = ScalarMap()
    self['SaldoAFavor'] = Decimal(node.attrib['SaldoAFavor'])
    self['Año'] = Xint(node.attrib['Año'])
    self['RemanenteSalFav'] = Decimal(node.attrib['RemanenteSalFav'])
    return self
def incapacidad1(cls, node):
    self = ScalarMap()
    self['DiasIncapacidad'] = Xint(node.attrib['DiasIncapacidad'])
    self['TipoIncapacidad'] = catalog_code('C75b_c_TipoIncapacidad', node.attrib['TipoIncapacidad'])
    if (a := node.attrib.get('ImporteMonetario')) is not None:
        self['ImporteMonetario'] = Decimal(a)
    return self
def notarios_publicos0(cls, node):
    self = cls()
    self.tag = node.tag
    el = node.find('{http://www.sat.gob.mx/notariospublicos}DescInmuebles')
    self['DescInmuebles'] = [desc_inmueble0(cls, n) for n in el.iterfind('{http://www.sat.gob.mx/notariospublicos}DescInmueble')]
    el = node.find('{http://www.sat.gob.mx/notariospublicos}DatosOperacion')
    self['DatosOperacion'] = datos_operacion12(cls, el)
    el = node.find('{http://www.sat.gob.mx/notariospublicos}DatosNotario')
    self['DatosNotario'] = datos_notario0(cls, el)
    el = node.find('{http://www.sat.gob.mx/notariospublicos}DatosEnajenante')
    self['DatosEnajenante'] = datos_enajenante0(cls, el)
    el = node.find('{http://www.sat.gob.mx/notariospublicos}DatosAdquiriente')
    self['DatosAdquiriente'] = datos_adquiriente0(cls, el)
    self['Version'] = node.attrib['Version']
    return self
def desc_inmueble0(cls, node):
    self = ScalarMap()
    self['TipoInmueble'] = node.attrib['TipoInmueble']
    self['Calle'] = node.attrib['Calle']
    if (a := node.attrib.get('NoExterior')) is not None:
        self['NoExterior'] = a
    if (a := node.attrib.get('NoInterior')) is not None:
        self['NoInterior'] = a
    if (a := node.attrib.get('Colonia')) is not None:
        self['Colonia'] = a
    if (a := node.attrib.get('Localidad')) is not None:
        self['Localidad'] = a
    if (a := node.attrib.get('Referencia')) is not None:
        self['Referencia'] = a
    self['Municipio'] = node.attrib['Municipio']
    self['Estado'] = catalog_code('Ccb0_c_EntidadesFederativas', node.attrib['Estado'])
    self['Pais'] = node.attrib['Pais']
    self['CodigoPostal'] = node.attrib['CodigoPostal']
    return self
def datos_operacion12(cls, node):
    self = ScalarMap()
    self['NumInstrumentoNotarial'] = Xint(node.attrib['NumInstrumentoNotarial'])
    self['FechaInstNotarial'] = date.fromisoformat(node.attrib['FechaInstNotarial'])
    self['MontoOperacion'] = Decimal(node.attrib['MontoOperacion'])
    self['Subtotal'] = Decimal(node.attrib['Subtotal'])
    self['IVA'] = Decimal(node.attrib['IVA'])
    return self
def datos_notario0(cls, node):
    self = ScalarMap()
    self['CURP'] = node.attrib['CURP']
    self['NumNotaria'] = Xint(node.attrib['NumNotaria'])
    self['EntidadFederativa'] = catalog_code('Ccb0_c_EntidadesFederativas', node.attrib['EntidadFederativa'])
    if (a := node.attrib.get('Adscripcion')) is not None:
        self['Adscripcion'] = a
    return self
def datos_enajenante0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.sat.gob.mx/notariospublicos}DatosUnEnajenante')
    if el is not None:
        self['DatosUnEnajenante'] = datos_un_enajenante0(cls, el)
    el = node.find('{http://www.sat.gob.mx/notariospublicos}DatosEnajenantesCopSC')
    if el is not None:
        self['DatosEnajenantesCopSC'] = [datos_enajenante_cop_sc0(cls, n) for n in el.iterfind('{http://www.sat.gob.mx/notariospublicos}DatosEnajenanteCopSC')]
    self['CoproSocConyugalE'] = node.attrib['CoproSocConyugalE']
    return self
def datos_un_enajenante0(cls, node):
    self = ScalarMap()
    self['Nombre'] = node.attrib['Nombre']
    self['ApellidoPaterno'] = node.attrib['ApellidoPaterno']
    if (a := node.attrib.get('ApellidoMaterno')) is not None:
        self['ApellidoMaterno'] = a
    self['RFC'] = node.attrib['RFC']
    self['CURP'] = node.attrib['CURP']
    return self
def datos_enajenante_cop_sc0(cls, node):
    self = ScalarMap()
    self['Nombre'] = node.attrib['Nombre']
    if (a := node.attrib.get('ApellidoPaterno')) is not None:
        self['ApellidoPaterno'] = a
    if (a := node.attrib.get('ApellidoMaterno')) is not None:
        self['ApellidoMaterno'] = a
    self['RFC'] = node.attrib['RFC']
    if (a := node.attrib.get('CURP')) is not None:
        self['CURP'] = a
    self['Porcentaje'] = Decimal(node.attrib['Porcentaje'])
    return self
def datos_adquiriente0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.sat.gob.mx/notariospublicos}DatosUnAdquiriente')
    if el is not None:
        self['DatosUnAdquiriente'] = datos_un_adquiriente0(cls, el)
    el = node.find('{http://www.sat.gob.mx/notariospublicos}DatosAdquirientesCopSC')
    if el is not None:
        self['DatosAdquirientesCopSC'] = [datos_adquiriente_cop_sc0(cls, n) for n in el.iterfind('{http://www.sat.gob.mx/notariospublicos}DatosAdquirienteCopSC')]
    self['CoproSocConyugalE'] = node.attrib['CoproSocConyugalE']
    return self
def datos_un_adquiriente0(cls, node):
    self = ScalarMap()
    self['Nombre'] = node.attrib['Nombre']
    if (a := node.attrib.get('ApellidoPaterno')) is not None:
        self['ApellidoPaterno'] = a
    if (a := node.attrib.get('ApellidoMaterno')) is not None:
        self['ApellidoMaterno'] = a
    self['RFC'] = node.attrib['RFC']
    if (a := node.attrib.get('CURP')) is not None:
        self['CURP'] = a
    return self
def datos_adquiriente_cop_sc0(cls, node):
    self = ScalarMap()
    self['Nombre'] = node.attrib['Nombre']
    if (a := node.attrib.get('ApellidoPaterno')) is not None:
        self['ApellidoPaterno'] = a
    if (a := node.attrib.get('ApellidoMaterno')) is not None:
        self['ApellidoMaterno'] = a
    self['RFC'] = node.attrib['RFC']
    if (a := node.attrib.get('CURP')) is not None:
        self['CURP'] = a
    self['Porcentaje'] = Decimal(node.attrib['Porcentaje'])
    return self
def pago_en_especie0(cls, node):
    self = cls()
    self.tag = node.tag
    self['Version'] = node.attrib['Version']
    self['CvePIC'] = node.attrib['CvePIC']
    self['FolioSolDon'] = node.attrib['FolioSolDon']
    self['PzaArtNombre'] = node.attrib['PzaArtNombre']
    self['PzaArtTecn'] = node.attrib['PzaArtTecn']
    self['PzaArtAProd'] = node.attrib['PzaArtAProd']
    self['PzaArtDim'] = node.attrib['PzaArtDim']
    return self
def pfintegrante_coordinado0(cls, node):
    self = cls()
    self.tag = node.tag
    self['Version'] = node.attrib['version']
    self['ClaveVehicular'] = node.attrib['ClaveVehicular']
    self['Placa'] = node.attrib['Placa']
    if (a := node.attrib.get('RFCPF')) is not None:
        self['RFCPF'] = a
    return self
def prestadores_de_servicios_de_cfd0(cls, node):
    self = cls()
    self.tag = node.tag
    self['Nombre'] = node.attrib['nombre']
    self['Rfc'] = node.attrib['rfc']
    self['NoCertificado'] = node.attrib['noCertificado']
    self['FechaAutorizacion'] = datetime.fromisoformat(node.attrib['fechaAutorizacion'])
    self['NoAutorizacion'] = Xint(node.attrib['noAutorizacion'])
    self['SelloDelPSGECFD'] = node.attrib['selloDelPSGECFD']
    return self
def renovacionysustitucionvehiculos0(cls, node):
    self = cls()
    self.tag = node.tag
    el = node.find('{http://www.sat.gob.mx/renovacionysustitucionvehiculos}DecretoRenovVehicular')
    if el is not None:
        self['DecretoRenovVehicular'] = decreto_renov_vehicular0(cls, el)
    el = node.find('{http://www.sat.gob.mx/renovacionysustitucionvehiculos}DecretoSustitVehicular')
    if el is not None:
        self['DecretoSustitVehicular'] = decreto_sustit_vehicular0(cls, el)
    self['Version'] = node.attrib['Version']
    self['TipoDeDecreto'] = catalog_code('C79b_c_TipoDecreto', node.attrib['TipoDeDecreto'])
    return self
def decreto_renov_vehicular0(cls, node):
    self = ScalarMap()
    self['VehiculosUsadosEnajenadoPermAlFab'] = [vehiculos_usados_enajenado_perm_al_fab0(cls, n) for n in node.iterfind('{http://www.sat.gob.mx/renovacionysustitucionvehiculos}VehiculosUsadosEnajenadoPermAlFab')]
    el = node.find('{http://www.sat.gob.mx/renovacionysustitucionvehiculos}VehiculoNuvoSemEnajenadoFabAlPerm')
    self['VehiculoNuvoSemEnajenadoFabAlPerm'] = vehiculo_nuvo_sem_enajenado_fab_al_perm0(cls, el)
    self['VehEnaj'] = catalog_code('C79b_c_VehiculoEnajenado', node.attrib['VehEnaj'])
    return self
def vehiculos_usados_enajenado_perm_al_fab0(cls, node):
    self = ScalarMap()
    self['PrecioVehUsado'] = Decimal(node.attrib['PrecioVehUsado'])
    self['TipoVeh'] = catalog_code('C79b_c_TipoVehiculo_r', node.attrib['TipoVeh'])
    self['Marca'] = node.attrib['Marca']
    self['TipooClase'] = node.attrib['TipooClase']
    self['Año'] = Xint(node.attrib['Año'])
    if (a := node.attrib.get('Modelo')) is not None:
        self['Modelo'] = a
    if (a := node.attrib.get('NIV')) is not None:
        self['NIV'] = a
    if (a := node.attrib.get('NumSerie')) is not None:
        self['NumSerie'] = a
    self['NumPlacas'] = node.attrib['NumPlacas']
    if (a := node.attrib.get('NumMotor')) is not None:
        self['NumMotor'] = a
    self['NumFolTarjCir'] = node.attrib['NumFolTarjCir']
    if (a := node.attrib.get('NumPedIm')) is not None:
        self['NumPedIm'] = a
    if (a := node.attrib.get('Aduana')) is not None:
        self['Aduana'] = a
    if (a := node.attrib.get('FechaRegulVeh')) is not None:
        self['FechaRegulVeh'] = date.fromisoformat(a)
    self['Foliofiscal'] = node.attrib['Foliofiscal']
    return self
def vehiculo_nuvo_sem_enajenado_fab_al_perm0(cls, node):
    self = ScalarMap()
    self['Año'] = Xint(node.attrib['Año'])
    if (a := node.attrib.get('Modelo')) is not None:
        self['Modelo'] = a
    self['NumPlacas'] = node.attrib['NumPlacas']
    if (a := node.attrib.get('RFC')) is not None:
        self['RFC'] = a
    return self
def decreto_sustit_vehicular0(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.sat.gob.mx/renovacionysustitucionvehiculos}VehiculoUsadoEnajenadoPermAlFab')
    self['VehiculoUsadoEnajenadoPermAlFab'] = vehiculo_usado_enajenado_perm_al_fab0(cls, el)
    el = node.find('{http://www.sat.gob.mx/renovacionysustitucionvehiculos}VehiculoNuvoSemEnajenadoFabAlPerm')
    self['VehiculoNuvoSemEnajenadoFabAlPerm'] = vehiculo_nuvo_sem_enajenado_fab_al_perm1(cls, el)
    self['VehEnaj'] = catalog_code('C79b_c_VehiculoEnajenado', node.attrib['VehEnaj'])
    return self
def vehiculo_usado_enajenado_perm_al_fab0(cls, node):
    self = ScalarMap()
    self['PrecioVehUsado'] = Decimal(node.attrib['PrecioVehUsado'])
    self['TipoVeh'] = catalog_code('C79b_c_TipoVehiculo_s', node.attrib['TipoVeh'])
    self['Marca'] = node.attrib['Marca']
    self['TipooClase'] = node.attrib['TipooClase']
    self['Año'] = Xint(node.attrib['Año'])
    if (a := node.attrib.get('Modelo')) is not None:
        self['Modelo'] = a
    if (a := node.attrib.get('NIV')) is not None:
        self['NIV'] = a
    if (a := node.attrib.get('NumSerie')) is not None:
        self['NumSerie'] = a
    self['NumPlacas'] = node.attrib['NumPlacas']
    if (a := node.attrib.get('NumMotor')) is not None:
        self['NumMotor'] = a
    self['NumFolTarjCir'] = node.attrib['NumFolTarjCir']
    self['NumFolAvisoint'] = node.attrib['NumFolAvisoint']
    self['NumPedIm'] = node.attrib['NumPedIm']
    self['Aduana'] = node.attrib['Aduana']
    self['FechaRegulVeh'] = date.fromisoformat(node.attrib['FechaRegulVeh'])
    self['Foliofiscal'] = node.attrib['Foliofiscal']
    return self
def vehiculo_nuvo_sem_enajenado_fab_al_perm1(cls, node):
    self = ScalarMap()
    self['Año'] = Xint(node.attrib['Año'])
    if (a := node.attrib.get('Modelo')) is not None:
        self['Modelo'] = a
    self['NumPlacas'] = node.attrib['NumPlacas']
    if (a := node.attrib.get('RFC')) is not None:
        self['RFC'] = a
    return self
def parcialesconstruccion0(cls, node):
    self = cls()
    self.tag = node.tag
    el = node.find('{http://www.sat.gob.mx/servicioparcialconstruccion}Inmueble')
    self['Inmueble'] = inmueble0(cls, el)
    self['Version'] = node.attrib['Version']
    self['NumPerLicoAut'] = node.attrib['NumPerLicoAut']
    return self
def inmueble0(cls, node):
    self = ScalarMap()
    self['Calle'] = node.attrib['Calle']
    if (a := node.attrib.get('NoExterior')) is not None:
        self['NoExterior'] = a
    if (a := node.attrib.get('NoInterior')) is not None:
        self['NoInterior'] = a
    if (a := node.attrib.get('Colonia')) is not None:
        self['Colonia'] = a
    if (a := node.attrib.get('Localidad')) is not None:
        self['Localidad'] = a
    if (a := node.attrib.get('Referencia')) is not None:
        self['Referencia'] = a
    self['Municipio'] = node.attrib['Municipio']
    self['Estado'] = catalog_code('Ccb0_c_EntidadesFederativas', node.attrib['Estado'])
    self['CodigoPostal'] = node.attrib['CodigoPostal']
    return self
def complemento_spei0(cls, node):
    self = cls()
    self.tag = node.tag
    self['SPEI_Tercero'] = [spei_tercero1(cls, n) for n in node.iterfind('{http://www.sat.gob.mx/spei}SPEI_Tercero')]
    return self
def spei_tercero1(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.sat.gob.mx/spei}Ordenante')
    self['Ordenante'] = ordenante1(cls, el)
    el = node.find('{http://www.sat.gob.mx/spei}Beneficiario')
    self['Beneficiario'] = beneficiario2(cls, el)
    self['FechaOperacion'] = date.fromisoformat(node.attrib['FechaOperacion'])
    self['Hora'] = time.fromisoformat(node.attrib['Hora'])
    self['ClaveSPEI'] = Xint(node.attrib['ClaveSPEI'])
    self['Sello'] = node.attrib['sello']
    self['NumeroCertificado'] = node.attrib['numeroCertificado']
    self['CadenaCDA'] = node.attrib['cadenaCDA']
    return self
def ordenante1(cls, node):
    self = ScalarMap()
    self['BancoEmisor'] = node.attrib['BancoEmisor']
    self['Nombre'] = node.attrib['Nombre']
    self['TipoCuenta'] = Decimal(node.attrib['TipoCuenta'])
    self['Cuenta'] = Decimal(node.attrib['Cuenta'])
    self['RFC'] = node.attrib['RFC']
    return self
def beneficiario2(cls, node):
    self = ScalarMap()
    self['BancoReceptor'] = node.attrib['BancoReceptor']
    self['Nombre'] = node.attrib['Nombre']
    self['TipoCuenta'] = Decimal(node.attrib['TipoCuenta'])
    self['Cuenta'] = Decimal(node.attrib['Cuenta'])
    self['RFC'] = node.attrib['RFC']
    self['Concepto'] = node.attrib['Concepto']
    if (a := node.attrib.get('IVA')) is not None:
        self['IVA'] = Decimal(a)
    self['MontoPago'] = Decimal(node.attrib['MontoPago'])
    return self
def por_cuentade_terceros0(cls, node):
    self = cls()
    self.tag = node.tag
    el = node.find('{http://www.sat.gob.mx/terceros}InformacionFiscalTercero')
    if el is not None:
        self['InformacionFiscalTercero'] = informacion_fiscal_tercero0(cls, el)
    el = node.find('{http://www.sat.gob.mx/terceros}InformacionAduanera')
    if el is not None:
        self['InformacionAduanera'] = informacion_aduanera5(cls, el)
    el = node.find('{http://www.sat.gob.mx/terceros}Parte')
    if el is not None:
        self['Parte'] = [parte3(cls, n) for n in node.iterfind('{http://www.sat.gob.mx/terceros}Parte')]
    el = node.find('{http://www.sat.gob.mx/terceros}CuentaPredial')
    if el is not None:
        self['CuentaPredial'] = cuenta_predial3(cls, el)
    el = node.find('{http://www.sat.gob.mx/terceros}Impuestos')
    self['Impuestos'] = impuestos6(cls, el)
    self['Version'] = node.attrib['version']
    self['Rfc'] = node.attrib['rfc']
    if (a := node.attrib.get('nombre')) is not None:
        self['Nombre'] = a
    return self
def informacion_fiscal_tercero0(cls, node):
    self = t_ubicacion_fiscal1(None, node)
    return self
def informacion_aduanera5(cls, node):
    self = t_informacion_aduanera1(None, node)
    return self
def parte3(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.sat.gob.mx/terceros}InformacionAduanera')
    if el is not None:
        self['InformacionAduanera'] = [t_informacion_aduanera1(cls, n) for n in node.iterfind('{http://www.sat.gob.mx/terceros}InformacionAduanera')]
    self['Cantidad'] = Decimal(node.attrib['cantidad'])
    if (a := node.attrib.get('unidad')) is not None:
        self['Unidad'] = a
    if (a := node.attrib.get('noIdentificacion')) is not None:
        self['NoIdentificacion'] = a
    self['Descripcion'] = node.attrib['descripcion']
    if (a := node.attrib.get('valorUnitario')) is not None:
        self['ValorUnitario'] = Decimal(a)
    if (a := node.attrib.get('importe')) is not None:
        self['Importe'] = Decimal(a)
    return self
def cuenta_predial3(cls, node):
    return node.attrib['numero']
def impuestos6(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.sat.gob.mx/terceros}Retenciones')
    if el is not None:
        self['Retenciones'] = [retencion6(cls, n) for n in el.iterfind('{http://www.sat.gob.mx/terceros}Retencion')]
    el = node.find('{http://www.sat.gob.mx/terceros}Traslados')
    if el is not None:
        self['Traslados'] = [traslado9(cls, n) for n in el.iterfind('{http://www.sat.gob.mx/terceros}Traslado')]
    return self
def retencion6(cls, node):
    self = ScalarMap()
    self['Impuesto'] = node.attrib['impuesto']
    self['Importe'] = Decimal(node.attrib['importe'])
    return self
def traslado9(cls, node):
    self = ScalarMap()
    self['Impuesto'] = node.attrib['impuesto']
    self['Tasa'] = Decimal(node.attrib['tasa'])
    self['Importe'] = Decimal(node.attrib['importe'])
    return self
def vales_de_despensa0(cls, node):
    self = cls()
    self.tag = node.tag
    el = node.find('{http://www.sat.gob.mx/valesdedespensa}Conceptos')
    self['Conceptos'] = [concepto4(cls, n) for n in el.iterfind('{http://www.sat.gob.mx/valesdedespensa}Concepto')]
    self['Version'] = node.attrib['version']
    self['TipoOperacion'] = node.attrib['tipoOperacion']
    if (a := node.attrib.get('registroPatronal')) is not None:
        self['RegistroPatronal'] = a
    self['NumeroDeCuenta'] = node.attrib['numeroDeCuenta']
    self['Total'] = Decimal(node.attrib['total'])
    return self
def concepto4(cls, node):
    self = ScalarMap()
    self['Identificador'] = node.attrib['identificador']
    self['Fecha'] = datetime.fromisoformat(node.attrib['fecha'])
    self['Rfc'] = node.attrib['rfc']
    self['Curp'] = node.attrib['curp']
    self['Nombre'] = node.attrib['nombre']
    if (a := node.attrib.get('numSeguridadSocial')) is not None:
        self['NumSeguridadSocial'] = a
    self['Importe'] = Decimal(node.attrib['importe'])
    return self
def vehiculo_usado0(cls, node):
    self = cls()
    self.tag = node.tag
    el = node.find('{http://www.sat.gob.mx/vehiculousado}InformacionAduanera')
    if el is not None:
        self['InformacionAduanera'] = [t_informacion_aduanera2(cls, n) for n in node.iterfind('{http://www.sat.gob.mx/vehiculousado}InformacionAduanera')]
    self['Version'] = node.attrib['Version']
    self['MontoAdquisicion'] = Decimal(node.attrib['montoAdquisicion'])
    self['MontoEnajenacion'] = Decimal(node.attrib['montoEnajenacion'])
    self['ClaveVehicular'] = node.attrib['claveVehicular']
    self['Marca'] = node.attrib['marca']
    self['Tipo'] = node.attrib['tipo']
    self['Modelo'] = node.attrib['modelo']
    if (a := node.attrib.get('numeroMotor')) is not None:
        self['NumeroMotor'] = a
    if (a := node.attrib.get('numeroSerie')) is not None:
        self['NumeroSerie'] = a
    if (a := node.attrib.get('NIV')) is not None:
        self['NIV'] = a
    self['Valor'] = Decimal(node.attrib['valor'])
    return self
def venta_vehiculos0(cls, node):
    self = cls()
    self.tag = node.tag
    el = node.find('{http://www.sat.gob.mx/ventavehiculos}InformacionAduanera')
    if el is not None:
        self['InformacionAduanera'] = [t_informacion_aduanera3(cls, n) for n in node.iterfind('{http://www.sat.gob.mx/ventavehiculos}InformacionAduanera')]
    el = node.find('{http://www.sat.gob.mx/ventavehiculos}Parte')
    if el is not None:
        self['Parte'] = [parte4(cls, n) for n in node.iterfind('{http://www.sat.gob.mx/ventavehiculos}Parte')]
    self['Version'] = node.attrib['version']
    self['ClaveVehicular'] = node.attrib['ClaveVehicular']
    self['Niv'] = node.attrib['Niv']
    return self
def parte4(cls, node):
    self = ScalarMap()
    el = node.find('{http://www.sat.gob.mx/ventavehiculos}InformacionAduanera')
    if el is not None:
        self['InformacionAduanera'] = [t_informacion_aduanera3(cls, n) for n in node.iterfind('{http://www.sat.gob.mx/ventavehiculos}InformacionAduanera')]
    self['Cantidad'] = Decimal(node.attrib['cantidad'])
    if (a := node.attrib.get('unidad')) is not None:
        self['Unidad'] = a
    if (a := node.attrib.get('noIdentificacion')) is not None:
        self['NoIdentificacion'] = a
    self['Descripcion'] = node.attrib['descripcion']
    if (a := node.attrib.get('valorUnitario')) is not None:
        self['ValorUnitario'] = Decimal(a)
    if (a := node.attrib.get('importe')) is not None:
        self['Importe'] = Decimal(a)
    return self
def s_cancelacion0(cls, node):
    return cancelacion0(cls, node)
def s_cancelacion1(cls, node):
    return cancelacion1(cls, node)
def s_solicitud_aceptacion_rechazo0(cls, node):
    return solicitud_aceptacion_rechazo0(cls, node)
def s_spei_tercero0(cls, node):
    return spei_tercero0(cls, node)
def s_diverza0(cls, node):
    if node.attrib.get('version') == '1.1':
        return diverza0(cls, node)
    raise NamespaceMismatchError(node)
def s_archivo0(cls, node):
    return archivo_type0(cls, node)
def s_archivo1(cls, node):
    return archivo_type1(cls, node)
def s_archivo2(cls, node):
    return archivo_type2(cls, node)
def s_archivo3(cls, node):
    return archivo_type3(cls, node)
def s_archivo4(cls, node):
    return archivo_type4(cls, node)
def s_archivo5(cls, node):
    return archivo_type5(cls, node)
def s_archivo6(cls, node):
    return archivo_type6(cls, node)
def s_archivo7(cls, node):
    return archivo_type7(cls, node)
def s_archivo8(cls, node):
    return archivo_type8(cls, node)
def s_archivo9(cls, node):
    return archivo_type9(cls, node)
def s_archivoa(cls, node):
    return archivo_typea(cls, node)
def s_archivob(cls, node):
    return archivo_typeb(cls, node)
def s_archivoc(cls, node):
    return archivo_typec(cls, node)
def s_archivod(cls, node):
    return archivo_typed(cls, node)
def s_archivoe(cls, node):
    return archivo_typee(cls, node)
def s_archivof(cls, node):
    return archivo_typef(cls, node)
def s_archivo10(cls, node):
    return archivo_type10(cls, node)
def s_archivo11(cls, node):
    return archivo_type11(cls, node)
def s_archivo12(cls, node):
    return archivo_type12(cls, node)
def s_auxiliar_ctas0(cls, node):
    if node.attrib.get('Version') == '1.1':
        return auxiliar_ctas0(cls, node)
    raise NamespaceMismatchError(node)
def s_rep_aux_fol0(cls, node):
    if node.attrib.get('Version') == '1.2':
        return rep_aux_fol0(cls, node)
    raise NamespaceMismatchError(node)
def s_balanza0(cls, node):
    if node.attrib.get('Version') == '1.1':
        return balanza0(cls, node)
    raise NamespaceMismatchError(node)
def s_catalogo0(cls, node):
    if node.attrib.get('Version') == '1.1':
        return catalogo0(cls, node)
    raise NamespaceMismatchError(node)
def s_polizas0(cls, node):
    if node.attrib.get('Version') == '1.1':
        return polizas0(cls, node)
    raise NamespaceMismatchError(node)
def s_auxiliar_ctas1(cls, node):
    if node.attrib.get('Version') == '1.3':
        return auxiliar_ctas1(cls, node)
    raise NamespaceMismatchError(node)
def s_rep_aux_fol1(cls, node):
    if node.attrib.get('Version') == '1.3':
        return rep_aux_fol1(cls, node)
    raise NamespaceMismatchError(node)
def s_balanza1(cls, node):
    if node.attrib.get('Version') == '1.3':
        return balanza1(cls, node)
    raise NamespaceMismatchError(node)
def s_catalogo1(cls, node):
    if node.attrib.get('Version') == '1.3':
        return catalogo1(cls, node)
    raise NamespaceMismatchError(node)
def s_polizas1(cls, node):
    if node.attrib.get('Version') == '1.3':
        return polizas1(cls, node)
    raise NamespaceMismatchError(node)
def s_sello_digital_cont_elec0(cls, node):
    if node.attrib.get('Version') == '1.1':
        return sello_digital_cont_elec0(cls, node)
    raise NamespaceMismatchError(node)
def s_servicios_plataformas_tecnologicas0(cls, node):
    if node.attrib.get('Version') == '1.0':
        return servicios_plataformas_tecnologicas0(cls, node)
    raise NamespaceMismatchError(node)
def s_arrendamientoenfideicomiso0(cls, node):
    if node.attrib.get('Version') == '1.0':
        return arrendamientoenfideicomiso0(cls, node)
    raise NamespaceMismatchError(node)
def s_dividendos0(cls, node):
    if node.attrib.get('Version') == '1.0':
        return dividendos0(cls, node)
    raise NamespaceMismatchError(node)
def s_enajenacionde_acciones0(cls, node):
    if node.attrib.get('Version') == '1.0':
        return enajenacionde_acciones0(cls, node)
    raise NamespaceMismatchError(node)
def s_fideicomisonoempresarial0(cls, node):
    if node.attrib.get('Version') == '1.0':
        return fideicomisonoempresarial0(cls, node)
    raise NamespaceMismatchError(node)
def s_intereses0(cls, node):
    if node.attrib.get('Version') == '1.0':
        return intereses0(cls, node)
    raise NamespaceMismatchError(node)
def s_intereseshipotecarios0(cls, node):
    if node.attrib.get('Version') == '1.0':
        return intereseshipotecarios0(cls, node)
    raise NamespaceMismatchError(node)
def s_operacionesconderivados0(cls, node):
    if node.attrib.get('Version') == '1.0':
        return operacionesconderivados0(cls, node)
    raise NamespaceMismatchError(node)
def s_pagosaextranjeros0(cls, node):
    if node.attrib.get('Version') == '1.0':
        return pagosaextranjeros0(cls, node)
    raise NamespaceMismatchError(node)
def s_planesderetiro0(cls, node):
    if node.attrib.get('Version') == '1.1':
        return planesderetiro0(cls, node)
    raise NamespaceMismatchError(node)
def s_planesderetiro1(cls, node):
    if node.attrib.get('Version') == '1.0':
        return planesderetiro1(cls, node)
    raise NamespaceMismatchError(node)
def s_premios0(cls, node):
    if node.attrib.get('Version') == '1.0':
        return premios0(cls, node)
    raise NamespaceMismatchError(node)
def s_retenciones0(cls, node):
    if node.attrib.get('Version') == '1.0':
        return retenciones0(cls, node)
    raise NamespaceMismatchError(node)
def s_sector_financiero0(cls, node):
    if node.attrib.get('Version') == '1.0':
        return sector_financiero0(cls, node)
    raise NamespaceMismatchError(node)
def s_retenciones1(cls, node):
    if node.attrib.get('Version') == '2.0':
        return retenciones1(cls, node)
    raise NamespaceMismatchError(node)
def s_comprobante0(cls, node):
    if node.attrib.get('version') == '3.2':
        return comprobante0(cls, node)
    if node.attrib.get('Version') == '3.3':
        return comprobante1(cls, node)
    raise NamespaceMismatchError(node)
def s_comprobante1(cls, node):
    if node.attrib.get('Version') == '4.0':
        return comprobante2(cls, node)
    raise NamespaceMismatchError(node)
def s_carta_porte0(cls, node):
    if node.attrib.get('Version') == '1.0':
        return carta_porte0(cls, node)
    raise NamespaceMismatchError(node)
def s_carta_porte1(cls, node):
    if node.attrib.get('Version') == '2.0':
        return carta_porte1(cls, node)
    raise NamespaceMismatchError(node)
def s_carta_porte2(cls, node):
    if node.attrib.get('Version') == '3.0':
        return carta_porte2(cls, node)
    raise NamespaceMismatchError(node)
def s_carta_porte3(cls, node):
    if node.attrib.get('Version') == '3.1':
        return carta_porte3(cls, node)
    raise NamespaceMismatchError(node)
def s_comercio_exterior0(cls, node):
    if node.attrib.get('Version') == '1.1':
        return comercio_exterior0(cls, node)
    raise NamespaceMismatchError(node)
def s_comercio_exterior1(cls, node):
    if node.attrib.get('Version') == '2.0':
        return comercio_exterior1(cls, node)
    raise NamespaceMismatchError(node)
def s_comercio_exterior2(cls, node):
    if node.attrib.get('Version') == '1.0':
        return comercio_exterior2(cls, node)
    raise NamespaceMismatchError(node)
def s_estado_de_cuenta_combustible0(cls, node):
    if node.attrib.get('Version') == '1.1' and node.attrib.get('TipoOperacion') == 'Tarjeta':
        return estado_de_cuenta_combustible0(cls, node)
    raise NamespaceMismatchError(node)
def s_estado_de_cuenta_combustible1(cls, node):
    if node.attrib.get('Version') == '1.2' and node.attrib.get('TipoOperacion') == 'Tarjeta':
        return estado_de_cuenta_combustible1(cls, node)
    raise NamespaceMismatchError(node)
def s_gastos_hidrocarburos0(cls, node):
    if node.attrib.get('Version') == '1.0':
        return gastos_hidrocarburos0(cls, node)
    raise NamespaceMismatchError(node)
def s_ingresos_hidrocarburos0(cls, node):
    if node.attrib.get('Version') == '1.0':
        return ingresos_hidrocarburos0(cls, node)
    raise NamespaceMismatchError(node)
def s_pagos0(cls, node):
    if node.attrib.get('Version') == '1.0':
        return pagos0(cls, node)
    raise NamespaceMismatchError(node)
def s_pagos1(cls, node):
    if node.attrib.get('Version') == '2.0':
        return pagos1(cls, node)
    raise NamespaceMismatchError(node)
def s_timbre_fiscal_digital0(cls, node):
    if node.attrib.get('version') == '1.0':
        return timbre_fiscal_digital0(cls, node)
    if node.attrib.get('Version') == '1.1':
        return timbre_fiscal_digital1(cls, node)
    raise NamespaceMismatchError(node)
def s_turista_pasajero_extranjero0(cls, node):
    if node.attrib.get('version') == '1.0':
        return turista_pasajero_extranjero0(cls, node)
    raise NamespaceMismatchError(node)
def s_acreditamiento_ieps0(cls, node):
    if node.attrib.get('Version') == '1.0':
        return acreditamiento_ieps0(cls, node)
    raise NamespaceMismatchError(node)
def s_aerolineas0(cls, node):
    if node.attrib.get('Version') == '1.0':
        return aerolineas0(cls, node)
    raise NamespaceMismatchError(node)
def s_obrasarteantiguedades0(cls, node):
    if node.attrib.get('Version') == '1.0':
        return obrasarteantiguedades0(cls, node)
    raise NamespaceMismatchError(node)
def s_certificadodedestruccion0(cls, node):
    if node.attrib.get('Version') == '1.0':
        return certificadodedestruccion0(cls, node)
    raise NamespaceMismatchError(node)
def s_cfdiregistro_fiscal0(cls, node):
    if node.attrib.get('Version') == '1.0':
        return cfdiregistro_fiscal0(cls, node)
    raise NamespaceMismatchError(node)
def s_consumo_de_combustibles0(cls, node):
    if node.attrib.get('version') == '1.1' and node.attrib.get('tipoOperacion') == 'monedero electrónico':
        return consumo_de_combustibles0(cls, node)
    raise NamespaceMismatchError(node)
def s_consumo_de_combustibles1(cls, node):
    if node.attrib.get('version') == '1.0' and node.attrib.get('tipoOperacion') == 'monedero electrónico':
        return consumo_de_combustibles1(cls, node)
    raise NamespaceMismatchError(node)
def s_detallista0(cls, node):
    if node.attrib.get('documentStructureVersion') == 'AMC8.1':
        return detallista0(cls, node)
    raise NamespaceMismatchError(node)
def s_divisas0(cls, node):
    if node.attrib.get('version') == '1.0':
        return divisas0(cls, node)
    raise NamespaceMismatchError(node)
def s_donatarias0(cls, node):
    if node.attrib.get('version') == '1.1':
        return donatarias0(cls, node)
    raise NamespaceMismatchError(node)
def s_estado_de_cuenta_bancario0(cls, node):
    if node.attrib.get('version') == '1.0':
        return estado_de_cuenta_bancario0(cls, node)
    raise NamespaceMismatchError(node)
def s_estado_de_cuenta_combustible2(cls, node):
    if node.attrib.get('tipoOperacion') == 'Tarjeta':
        return estado_de_cuenta_combustible2(cls, node)
    raise NamespaceMismatchError(node)
def s_inst_educativas0(cls, node):
    if node.attrib.get('version') == '1.0':
        return inst_educativas0(cls, node)
    raise NamespaceMismatchError(node)
def s_impuestos_locales0(cls, node):
    if node.attrib.get('version') == '1.0':
        return impuestos_locales0(cls, node)
    raise NamespaceMismatchError(node)
def s_ine0(cls, node):
    if node.attrib.get('Version') == '1.0':
        return ine0(cls, node)
    if node.attrib.get('Version') == '1.1':
        return ine1(cls, node)
    raise NamespaceMismatchError(node)
def s_leyendas_fiscales0(cls, node):
    if node.attrib.get('version') == '1.0':
        return leyendas_fiscales0(cls, node)
    raise NamespaceMismatchError(node)
def s_nomina0(cls, node):
    if node.attrib.get('Version') == '1.1':
        return nomina0(cls, node)
    raise NamespaceMismatchError(node)
def s_nomina1(cls, node):
    if node.attrib.get('Version') == '1.2':
        return nomina1(cls, node)
    raise NamespaceMismatchError(node)
def s_notarios_publicos0(cls, node):
    if node.attrib.get('Version') == '1.0':
        return notarios_publicos0(cls, node)
    raise NamespaceMismatchError(node)
def s_pago_en_especie0(cls, node):
    if node.attrib.get('Version') == '1.0':
        return pago_en_especie0(cls, node)
    raise NamespaceMismatchError(node)
def s_pfintegrante_coordinado0(cls, node):
    if node.attrib.get('version') == '1.0':
        return pfintegrante_coordinado0(cls, node)
    raise NamespaceMismatchError(node)
def s_prestadores_de_servicios_de_cfd0(cls, node):
    return prestadores_de_servicios_de_cfd0(cls, node)
def s_renovacionysustitucionvehiculos0(cls, node):
    if node.attrib.get('Version') == '1.0':
        return renovacionysustitucionvehiculos0(cls, node)
    raise NamespaceMismatchError(node)
def s_parcialesconstruccion0(cls, node):
    if node.attrib.get('Version') == '1.0':
        return parcialesconstruccion0(cls, node)
    raise NamespaceMismatchError(node)
def s_complemento_spei0(cls, node):
    return complemento_spei0(cls, node)
def s_por_cuentade_terceros0(cls, node):
    if node.attrib.get('version') == '1.1':
        return por_cuentade_terceros0(cls, node)
    raise NamespaceMismatchError(node)
def s_vales_de_despensa0(cls, node):
    if node.attrib.get('version') == '1.0' and node.attrib.get('tipoOperacion') == 'monedero electrónico':
        return vales_de_despensa0(cls, node)
    raise NamespaceMismatchError(node)
def s_vehiculo_usado0(cls, node):
    if node.attrib.get('Version') == '1.0':
        return vehiculo_usado0(cls, node)
    raise NamespaceMismatchError(node)
def s_venta_vehiculos0(cls, node):
    if node.attrib.get('version') == '1.1':
        return venta_vehiculos0(cls, node)
    raise NamespaceMismatchError(node)
def s_signature0(cls, node):
    return signature_type0(cls, node)
def s_signature_value0(cls, node):
    return signature_value0(cls, node)
def s_signed_info0(cls, node):
    return signed_info0(cls, node)
def s_canonicalization_method0(cls, node):
    return canonicalization_method0(cls, node)
def s_signature_method0(cls, node):
    return signature_method0(cls, node)
def s_reference0(cls, node):
    return reference0(cls, node)
def s_transforms0(cls, node):
    return transforms0(cls, node)
def s_transform0(cls, node):
    return transform0(cls, node)
def s_digest_method0(cls, node):
    return digest_method0(cls, node)
def s_digest_value0(cls, node):
    return node.text
def s_key_info0(cls, node):
    return key_info0(cls, node)
def s_key_name0(cls, node):
    return node.text
def s_mgmt_data0(cls, node):
    return node.text
def s_key_value0(cls, node):
    return key_value0(cls, node)
def s_retrieval_method0(cls, node):
    return retrieval_method0(cls, node)
def s_x509data0(cls, node):
    return x509data0(cls, node)
def s_pgpdata0(cls, node):
    return pgpdata0(cls, node)
def s_spkid_ata0(cls, node):
    return spkid_ata0(cls, node)
def s_object0(cls, node):
    return object0(cls, node)
def s_manifest0(cls, node):
    return manifest_type0(cls, node)
def s_signature_properties0(cls, node):
    return signature_properties_type0(cls, node)
def s_signature_property0(cls, node):
    return signature_property0(cls, node)
def s_dsakey_value0(cls, node):
    return dsakey_value0(cls, node)
def s_rsakey_value0(cls, node):
    return rsakey_value0(cls, node)
cfdi_objectify = {
    '{http://cancelacfd.sat.gob.mx}Cancelacion': s_cancelacion0,
    '{http://www.sat.gob.mx/esquemas/retencionpago/1}Cancelacion': s_cancelacion1,
    '{http://cancelacfd.sat.gob.mx}SolicitudAceptacionRechazo': s_solicitud_aceptacion_rechazo0,
    'SPEI_Tercero': s_spei_tercero0,
    '{http://www.diverza.com/ns/addenda/diverza/1}diverza': s_diverza0,
    '{http://www.uif.shcp.gob.mx/recepcion/ari}archivo': s_archivo0,
    '{http://www.uif.shcp.gob.mx/recepcion/avi}archivo': s_archivo1,
    '{http://www.uif.shcp.gob.mx/recepcion/bli}archivo': s_archivo2,
    '{http://www.uif.shcp.gob.mx/recepcion/chv}archivo': s_archivo3,
    '{http://www.uif.shcp.gob.mx/recepcion/din}archivo': s_archivo4,
    '{http://www.uif.shcp.gob.mx/recepcion/don}archivo': s_archivo5,
    '{http://www.uif.shcp.gob.mx/recepcion/fep}archivo': s_archivo6,
    '{http://www.uif.shcp.gob.mx/recepcion/fes}archivo': s_archivo7,
    '{http://www.uif.shcp.gob.mx/recepcion/inm}archivo': s_archivo8,
    '{http://www.uif.shcp.gob.mx/recepcion/jys}archivo': s_archivo9,
    '{http://www.uif.shcp.gob.mx/recepcion/mjr}archivo': s_archivoa,
    '{http://www.uif.shcp.gob.mx/recepcion/mpc}archivo': s_archivob,
    '{http://www.uif.shcp.gob.mx/recepcion/oba}archivo': s_archivoc,
    '{http://www.uif.shcp.gob.mx/recepcion/spr}archivo': s_archivod,
    '{http://www.uif.shcp.gob.mx/recepcion/tcv}archivo': s_archivoe,
    '{http://www.uif.shcp.gob.mx/recepcion/tdr}archivo': s_archivof,
    '{http://www.uif.shcp.gob.mx/recepcion/tpp}archivo': s_archivo10,
    '{http://www.uif.shcp.gob.mx/recepcion/tsc}archivo': s_archivo11,
    '{http://www.uif.shcp.gob.mx/recepcion/veh}archivo': s_archivo12,
    '{www.sat.gob.mx/esquemas/ContabilidadE/1_1/AuxiliarCtas}AuxiliarCtas': s_auxiliar_ctas0,
    '{www.sat.gob.mx/esquemas/ContabilidadE/1_1/AuxiliarFolios}RepAuxFol': s_rep_aux_fol0,
    '{www.sat.gob.mx/esquemas/ContabilidadE/1_1/BalanzaComprobacion}Balanza': s_balanza0,
    '{www.sat.gob.mx/esquemas/ContabilidadE/1_1/CatalogoCuentas}Catalogo': s_catalogo0,
    '{www.sat.gob.mx/esquemas/ContabilidadE/1_1/PolizasPeriodo}Polizas': s_polizas0,
    '{http://www.sat.gob.mx/esquemas/ContabilidadE/1_3/AuxiliarCtas}AuxiliarCtas': s_auxiliar_ctas1,
    '{http://www.sat.gob.mx/esquemas/ContabilidadE/1_3/AuxiliarFolios}RepAuxFol': s_rep_aux_fol1,
    '{http://www.sat.gob.mx/esquemas/ContabilidadE/1_3/BalanzaComprobacion}Balanza': s_balanza1,
    '{http://www.sat.gob.mx/esquemas/ContabilidadE/1_3/CatalogoCuentas}Catalogo': s_catalogo1,
    '{http://www.sat.gob.mx/esquemas/ContabilidadE/1_3/PolizasPeriodo}Polizas': s_polizas1,
    '{www.sat.gob.mx/esquemas/ContabilidadE/1_1/SelloDigitalContElec}SelloDigitalContElec': s_sello_digital_cont_elec0,
    '{http://www.sat.gob.mx/esquemas/retencionpago/1/PlataformasTecnologicas10}ServiciosPlataformasTecnologicas': s_servicios_plataformas_tecnologicas0,
    '{http://www.sat.gob.mx/esquemas/retencionpago/1/arrendamientoenfideicomiso}Arrendamientoenfideicomiso': s_arrendamientoenfideicomiso0,
    '{http://www.sat.gob.mx/esquemas/retencionpago/1/dividendos}Dividendos': s_dividendos0,
    '{http://www.sat.gob.mx/esquemas/retencionpago/1/enajenaciondeacciones}EnajenaciondeAcciones': s_enajenacionde_acciones0,
    '{http://www.sat.gob.mx/esquemas/retencionpago/1/fideicomisonoempresarial}Fideicomisonoempresarial': s_fideicomisonoempresarial0,
    '{http://www.sat.gob.mx/esquemas/retencionpago/1/intereses}Intereses': s_intereses0,
    '{http://www.sat.gob.mx/esquemas/retencionpago/1/intereseshipotecarios}Intereseshipotecarios': s_intereseshipotecarios0,
    '{http://www.sat.gob.mx/esquemas/retencionpago/1/operacionesconderivados}Operacionesconderivados': s_operacionesconderivados0,
    '{http://www.sat.gob.mx/esquemas/retencionpago/1/pagosaextranjeros}Pagosaextranjeros': s_pagosaextranjeros0,
    '{http://www.sat.gob.mx/esquemas/retencionpago/1/planesderetiro11}Planesderetiro': s_planesderetiro0,
    '{http://www.sat.gob.mx/esquemas/retencionpago/1/planesderetiro}Planesderetiro': s_planesderetiro1,
    '{http://www.sat.gob.mx/esquemas/retencionpago/1/premios}Premios': s_premios0,
    '{http://www.sat.gob.mx/esquemas/retencionpago/1}Retenciones': s_retenciones0,
    '{http://www.sat.gob.mx/esquemas/retencionpago/1/sectorfinanciero}SectorFinanciero': s_sector_financiero0,
    '{http://www.sat.gob.mx/esquemas/retencionpago/2}Retenciones': s_retenciones1,
    '{http://www.sat.gob.mx/cfd/3}Comprobante': s_comprobante0,
    '{http://www.sat.gob.mx/cfd/4}Comprobante': s_comprobante1,
    '{http://www.sat.gob.mx/CartaPorte}CartaPorte': s_carta_porte0,
    '{http://www.sat.gob.mx/CartaPorte20}CartaPorte': s_carta_porte1,
    '{http://www.sat.gob.mx/CartaPorte30}CartaPorte': s_carta_porte2,
    '{http://www.sat.gob.mx/CartaPorte31}CartaPorte': s_carta_porte3,
    '{http://www.sat.gob.mx/ComercioExterior11}ComercioExterior': s_comercio_exterior0,
    '{http://www.sat.gob.mx/ComercioExterior20}ComercioExterior': s_comercio_exterior1,
    '{http://www.sat.gob.mx/ComercioExterior}ComercioExterior': s_comercio_exterior2,
    '{http://www.sat.gob.mx/EstadoDeCuentaCombustible}EstadoDeCuentaCombustible': s_estado_de_cuenta_combustible0,
    '{http://www.sat.gob.mx/EstadoDeCuentaCombustible12}EstadoDeCuentaCombustible': s_estado_de_cuenta_combustible1,
    '{http://www.sat.gob.mx/GastosHidrocarburos10}GastosHidrocarburos': s_gastos_hidrocarburos0,
    '{http://www.sat.gob.mx/IngresosHidrocarburos10}IngresosHidrocarburos': s_ingresos_hidrocarburos0,
    '{http://www.sat.gob.mx/Pagos}Pagos': s_pagos0,
    '{http://www.sat.gob.mx/Pagos20}Pagos': s_pagos1,
    '{http://www.sat.gob.mx/TimbreFiscalDigital}TimbreFiscalDigital': s_timbre_fiscal_digital0,
    '{http://www.sat.gob.mx/TuristaPasajeroExtranjero}TuristaPasajeroExtranjero': s_turista_pasajero_extranjero0,
    '{http://www.sat.gob.mx/acreditamiento}acreditamientoIEPS': s_acreditamiento_ieps0,
    '{http://www.sat.gob.mx/aerolineas}Aerolineas': s_aerolineas0,
    '{http://www.sat.gob.mx/arteantiguedades}obrasarteantiguedades': s_obrasarteantiguedades0,
    '{http://www.sat.gob.mx/certificadodestruccion}certificadodedestruccion': s_certificadodedestruccion0,
    '{http://www.sat.gob.mx/registrofiscal}CFDIRegistroFiscal': s_cfdiregistro_fiscal0,
    '{http://www.sat.gob.mx/ConsumoDeCombustibles11}ConsumoDeCombustibles': s_consumo_de_combustibles0,
    '{http://www.sat.gob.mx/consumodecombustibles}ConsumoDeCombustibles': s_consumo_de_combustibles1,
    '{http://www.sat.gob.mx/detallista}detallista': s_detallista0,
    '{http://www.sat.gob.mx/divisas}Divisas': s_divisas0,
    '{http://www.sat.gob.mx/donat}Donatarias': s_donatarias0,
    '{http://www.sat.gob.mx/ecb}EstadoDeCuentaBancario': s_estado_de_cuenta_bancario0,
    '{http://www.sat.gob.mx/ecc}EstadoDeCuentaCombustible': s_estado_de_cuenta_combustible2,
    '{http://www.sat.gob.mx/iedu}instEducativas': s_inst_educativas0,
    '{http://www.sat.gob.mx/implocal}ImpuestosLocales': s_impuestos_locales0,
    '{http://www.sat.gob.mx/ine}INE': s_ine0,
    '{http://www.sat.gob.mx/leyendasFiscales}LeyendasFiscales': s_leyendas_fiscales0,
    '{http://www.sat.gob.mx/nomina}Nomina': s_nomina0,
    '{http://www.sat.gob.mx/nomina12}Nomina': s_nomina1,
    '{http://www.sat.gob.mx/notariospublicos}NotariosPublicos': s_notarios_publicos0,
    '{http://www.sat.gob.mx/pagoenespecie}PagoEnEspecie': s_pago_en_especie0,
    '{http://www.sat.gob.mx/pfic}PFintegranteCoordinado': s_pfintegrante_coordinado0,
    '{http://www.sat.gob.mx/psgecfd}PrestadoresDeServiciosDeCFD': s_prestadores_de_servicios_de_cfd0,
    '{http://www.sat.gob.mx/renovacionysustitucionvehiculos}renovacionysustitucionvehiculos': s_renovacionysustitucionvehiculos0,
    '{http://www.sat.gob.mx/servicioparcialconstruccion}parcialesconstruccion': s_parcialesconstruccion0,
    '{http://www.sat.gob.mx/spei}Complemento_SPEI': s_complemento_spei0,
    '{http://www.sat.gob.mx/terceros}PorCuentadeTerceros': s_por_cuentade_terceros0,
    '{http://www.sat.gob.mx/valesdedespensa}ValesDeDespensa': s_vales_de_despensa0,
    '{http://www.sat.gob.mx/vehiculousado}VehiculoUsado': s_vehiculo_usado0,
    '{http://www.sat.gob.mx/ventavehiculos}VentaVehiculos': s_venta_vehiculos0,
    '{http://www.w3.org/2000/09/xmldsig#}Signature': s_signature0,
    '{http://www.w3.org/2000/09/xmldsig#}SignatureValue': s_signature_value0,
    '{http://www.w3.org/2000/09/xmldsig#}SignedInfo': s_signed_info0,
    '{http://www.w3.org/2000/09/xmldsig#}CanonicalizationMethod': s_canonicalization_method0,
    '{http://www.w3.org/2000/09/xmldsig#}SignatureMethod': s_signature_method0,
    '{http://www.w3.org/2000/09/xmldsig#}Reference': s_reference0,
    '{http://www.w3.org/2000/09/xmldsig#}Transforms': s_transforms0,
    '{http://www.w3.org/2000/09/xmldsig#}Transform': s_transform0,
    '{http://www.w3.org/2000/09/xmldsig#}DigestMethod': s_digest_method0,
    '{http://www.w3.org/2000/09/xmldsig#}DigestValue': s_digest_value0,
    '{http://www.w3.org/2000/09/xmldsig#}KeyInfo': s_key_info0,
    '{http://www.w3.org/2000/09/xmldsig#}KeyName': s_key_name0,
    '{http://www.w3.org/2000/09/xmldsig#}MgmtData': s_mgmt_data0,
    '{http://www.w3.org/2000/09/xmldsig#}KeyValue': s_key_value0,
    '{http://www.w3.org/2000/09/xmldsig#}RetrievalMethod': s_retrieval_method0,
    '{http://www.w3.org/2000/09/xmldsig#}X509Data': s_x509data0,
    '{http://www.w3.org/2000/09/xmldsig#}PGPData': s_pgpdata0,
    '{http://www.w3.org/2000/09/xmldsig#}SPKIData': s_spkid_ata0,
    '{http://www.w3.org/2000/09/xmldsig#}Object': s_object0,
    '{http://www.w3.org/2000/09/xmldsig#}Manifest': s_manifest0,
    '{http://www.w3.org/2000/09/xmldsig#}SignatureProperties': s_signature_properties0,
    '{http://www.w3.org/2000/09/xmldsig#}SignatureProperty': s_signature_property0,
    '{http://www.w3.org/2000/09/xmldsig#}DSAKeyValue': s_dsakey_value0,
    '{http://www.w3.org/2000/09/xmldsig#}RSAKeyValue': s_rsakey_value0,
}
