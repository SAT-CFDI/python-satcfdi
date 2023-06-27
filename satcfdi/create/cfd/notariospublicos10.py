"""notariospublicos http://www.sat.gob.mx/notariospublicos"""
from decimal import Decimal
from datetime import datetime, date, time
from collections.abc import Sequence
from ...cfdi import CFDI
from ...xelement import XElement
from ...utils import ScalarMap


class DatosAdquirienteCopSC(ScalarMap):
    """
    Nodo para capturar los datos de un adquiriente o de un propietario o poseedor en caso de Copropiedad o Sociedad Conyugal
    
    :param nombre: Atributo requerido para expresar el nombre, denominación o razón social de cada adquiriente o de cada propietario o poseedor en caso de servidumbres de paso.
    :param rfc: Atributo requerido para la Clave del Registro Federal de Contribuyentes sin guiones o espacios, correspondiente a cada adquiriente o de cada propietario o poseedor en caso de servidumbres de paso.
    :param porcentaje: Porcentaje que le corresponde en la copropiedad a cada adquiriente o de cada propietario o poseedor en caso de servidumbres de paso.
    :param apellido_paterno: Atributo opcional para expresar el apellido paterno de cada adquiriente o de cada propietario o poseedor en caso de servidumbres de paso.
    :param apellido_materno: Atributo opcional para expresar el apellido materno de cada adquirientes o de cada propietario o poseedor en caso de servidumbres de paso.
    :param curp: Atributo opcional para expresar la CURP de cada adquiriente o de cada propietario o poseedor en caso de servidumbres de paso.
    """
    
    def __init__(
            self,
            nombre: str,
            rfc: str,
            porcentaje: Decimal | int,
            apellido_paterno: str = None,
            apellido_materno: str = None,
            curp: str = None,
    ): 
        super().__init__({
            'Nombre': nombre,
            'RFC': rfc,
            'Porcentaje': porcentaje,
            'ApellidoPaterno': apellido_paterno,
            'ApellidoMaterno': apellido_materno,
            'CURP': curp,
        })
        

class DatosUnAdquiriente(ScalarMap):
    """
    Nodo para capturar los datos del adquiriente o del propietario o poseedor en caso de ser solo uno.
    
    :param nombre: Atributo requerido para expresar el nombre, denominación o razón social del adquiriente o del propietario o poseedor del bien dominante o del pagador de la indemnización o contraprestación en el caso de servidumbres de paso.
    :param rfc: Atributo requerido para la Clave del Registro Federal de Contribuyentes sin guiones o espacios, del adquiriente o del propietario o poseedor del bien dominante o del pagador de la indemnización o contraprestación en el caso de servidumbres de paso.
    :param apellido_paterno: Atributo opcional para expresar el apellido paterno del adquiriente o del propietario o poseedor del bien dominante o del pagador de la indemnización o contraprestación en el caso de servidumbres de paso.
    :param apellido_materno: Atributo opcional para expresar el apellido materno del adquiriente o del propietario o poseedor del bien dominante o del pagador de la indemnización o contraprestación en el caso de servidumbres de paso.
    :param curp: Atributo opcional para expresar la CURP del adquiriente o del propietario o poseedor del bien dominante o del pagador de la indemnización o contraprestación en el caso de servidumbres de paso.
    """
    
    def __init__(
            self,
            nombre: str,
            rfc: str,
            apellido_paterno: str = None,
            apellido_materno: str = None,
            curp: str = None,
    ): 
        super().__init__({
            'Nombre': nombre,
            'RFC': rfc,
            'ApellidoPaterno': apellido_paterno,
            'ApellidoMaterno': apellido_materno,
            'CURP': curp,
        })
        

class DatosAdquiriente(ScalarMap):
    """
    Nodo para capturar los datos del adquiriente, adquirientes o propietario, o propietarios o poseedores, en caso de servidumbres de paso.
    
    :param copro_soc_conyugal_e: Atributo requerido que expresa si es copropiedad o sociedad conyugal
    :param datos_un_adquiriente: Nodo para capturar los datos del adquiriente o del propietario o poseedor en caso de ser solo uno.
    :param datos_adquirientes_cop_sc: Nodo para capturar los datos de los adquirientes o propietarios o poseedores del bien dominante en caso de Copropiedad o Sociedad Conyugal
    """
    
    def __init__(
            self,
            copro_soc_conyugal_e: str,
            datos_un_adquiriente: DatosUnAdquiriente | dict = None,
            datos_adquirientes_cop_sc: DatosAdquirienteCopSC | dict | Sequence[DatosAdquirienteCopSC | dict] = None,
    ): 
        super().__init__({
            'CoproSocConyugalE': copro_soc_conyugal_e,
            'DatosUnAdquiriente': datos_un_adquiriente,
            'DatosAdquirientesCopSC': datos_adquirientes_cop_sc,
        })
        

class DatosEnajenanteCopSC(ScalarMap):
    """
    Nodo para capturar los datos de un enajenante o de los propietarios o poseedores tratándose de servidumbres de paso, en caso de Copropiedad o Sociedad Conyugal
    
    :param nombre: Atributo requerido para expresar el nombre (s) de cada enajenante o del propietario o poseedor del predio sirviente, en caso de servidumbres de paso.
    :param rfc: Atributo requerido para la Clave del Registro Federal de Contribuyentes sin guiones o espacios, correspondiente a cada enajenante o del propietario o poseedor del predio sirviente, en caso de servidumbres de paso.
    :param porcentaje: Porcentaje que le corresponde en la copropiedad a cada enajenante o del propietario o poseedor del predio sirviente, en caso de servidumbres de paso.
    :param apellido_paterno: Atributo opcional para expresar el apellido paterno de cada enajenante o del propietario o poseedor del predio sirviente, en caso de servidumbres de paso.
    :param apellido_materno: Atributo opcional para expresar el apellido materno de cada enajenante o del propietario o poseedor del predio sirviente, en caso de servidumbres de paso.
    :param curp: Atributo opcional para expresar la CURP de cada enajenante o del propietario o poseedor del predio sirviente, en caso de servidumbres de paso.
    """
    
    def __init__(
            self,
            nombre: str,
            rfc: str,
            porcentaje: Decimal | int,
            apellido_paterno: str = None,
            apellido_materno: str = None,
            curp: str = None,
    ): 
        super().__init__({
            'Nombre': nombre,
            'RFC': rfc,
            'Porcentaje': porcentaje,
            'ApellidoPaterno': apellido_paterno,
            'ApellidoMaterno': apellido_materno,
            'CURP': curp,
        })
        

class DatosUnEnajenante(ScalarMap):
    """
    Nodo para capturar los datos del enajenante o del propietario o poseedor del predio sirviente en caso de ser solo uno.
    
    :param nombre: Atributo requerido para expresar el nombre del enajenante o del propietario o poseedor del predio sirviente, en caso de servidumbres de paso.
    :param apellido_paterno: Atributo requerido para expresar el apellido paterno del enajenante o del propietario o poseedor del predio sirviente, en caso de servidumbres de paso.
    :param rfc: Atributo requerido para la Clave del Registro Federal de Contribuyentes sin guiones o espacios, del enajenante o del propietario o poseedor del predio sirviente, en caso de servidumbres de paso.
    :param curp: Atributo requerido para expresar la CURP del enajenante o del propietario o poseedor del predio sirviente, en caso de servidumbres de paso.
    :param apellido_materno: Atributo opcional para expresar el apellido materno del enajenante o del propietario o poseedor del predio sirviente, en caso de servidumbres de paso.
    """
    
    def __init__(
            self,
            nombre: str,
            apellido_paterno: str,
            rfc: str,
            curp: str,
            apellido_materno: str = None,
    ): 
        super().__init__({
            'Nombre': nombre,
            'ApellidoPaterno': apellido_paterno,
            'RFC': rfc,
            'CURP': curp,
            'ApellidoMaterno': apellido_materno,
        })
        

class DatosEnajenante(ScalarMap):
    """
    Nodo para capturar los datos del enajenante o enajenantes, o en el caso de servidumbres de paso del propietario o poseedores o propietarios o poseedores del predio sirviente.
    
    :param copro_soc_conyugal_e: Atributo requerido que expresa si es copropiedad o sociedad conyugal
    :param datos_un_enajenante: Nodo para capturar los datos del enajenante o del propietario o poseedor del predio sirviente en caso de ser solo uno.
    :param datos_enajenantes_cop_sc: Nodo para capturar los datos de los enajenantes o de los propietarios o poseedores tratándose de servidumbres de paso, en caso de Copropiedad o Sociedad Conyugal
    """
    
    def __init__(
            self,
            copro_soc_conyugal_e: str,
            datos_un_enajenante: DatosUnEnajenante | dict = None,
            datos_enajenantes_cop_sc: DatosEnajenanteCopSC | dict | Sequence[DatosEnajenanteCopSC | dict] = None,
    ): 
        super().__init__({
            'CoproSocConyugalE': copro_soc_conyugal_e,
            'DatosUnEnajenante': datos_un_enajenante,
            'DatosEnajenantesCopSC': datos_enajenantes_cop_sc,
        })
        

class DatosNotario(ScalarMap):
    """
    
    :param curp: Atributo requerido para expresar la CURP del notario
    :param num_notaria: Atributo requerido para indicar el número de la Notaria que realizar la operación.
    :param entidad_federativa: Entidad Federativa donde se ubica la Notaria conforme al catálogo publicado en el portal del SAT en internet.
    :param adscripcion: Atributo opcional que expresa el señalamiento del notario a la plaza a la que se encuentra adscrito
    """
    
    def __init__(
            self,
            curp: str,
            num_notaria: int,
            entidad_federativa: str,
            adscripcion: str = None,
    ): 
        super().__init__({
            'CURP': curp,
            'NumNotaria': num_notaria,
            'EntidadFederativa': entidad_federativa,
            'Adscripcion': adscripcion,
        })
        

class DatosOperacion(ScalarMap):
    """
    Nodo para definir los detalles de la operación.
    
    :param num_instrumento_notarial: Atributo requerido que indica el número del instrumento Notarial donde consta la operación
    :param fecha_inst_notarial: Atributo requerido que indica la fecha de firma del instrumento Notarial
    :param monto_operacion: Atributo requerido para expresar el monto de la contraprestación, indemnización o valor de la operación.
    :param subtotal: Atributo requerido para expresar el subtotal de la contraprestación, indemnización o su valor en la operación
    :param iva: Atributo requerido para expresar el IVA de la contraprestación, indemnización o su valor en la operación
    """
    
    def __init__(
            self,
            num_instrumento_notarial: int,
            fecha_inst_notarial: date,
            monto_operacion: Decimal | int,
            subtotal: Decimal | int,
            iva: Decimal | int,
    ): 
        super().__init__({
            'NumInstrumentoNotarial': num_instrumento_notarial,
            'FechaInstNotarial': fecha_inst_notarial,
            'MontoOperacion': monto_operacion,
            'Subtotal': subtotal,
            'IVA': iva,
        })
        

class DescInmueble(ScalarMap):
    """
    Nodo para describir el inmueble o inmuebles objeto del acto otorgado.
    
    :param tipo_inmueble: Atributo requerido para la expresión del tipo de inmueble enajenado o sujeto a servidumbre (sirviente) conforme al catálogo publicado en el portal del SAT en internet.
    :param calle: Este atributo requerido sirve para precisar la avenida, calle, camino o carretera donde se ubica el inmueble
    :param municipio: Atributo requerido que sirve para precisar el municipio o delegación (en el caso del Distrito Federal) en donde se da la ubicación del inmueble
    :param estado: Entidad Federativa donde se ubica el inmueble conforme al catálogo publicado en el portal del SAT en internet.
    :param pais: Atributo requerido que sirve para precisar el país donde se da la ubicación, conforme al catálogo publicado en el portal del SAT en internet. En caso de servidumbres de paso, siempre será México.
    :param codigo_postal: Atributo requerido que sirve para asentar el código postal en donde se da la ubicación del inmueble.
    :param no_exterior: Este atributo opcional sirve para expresar el número particular en donde se da la ubicación del inmueble en una calle dada.
    :param no_interior: Este atributo opcional sirve para expresar información adicional para especificar la ubicación cuando calle y número exterior (noExterior) no resulten suficientes para determinar la ubicación precisa del inmueble.
    :param colonia: Este atributo opcional sirve para precisar la colonia en donde se da la ubicación del inmueble cuando se desea ser más específico en casos de ubicaciones urbanas.
    :param localidad: Atributo opcional que sirve para precisar la ciudad o población donde se da la ubicación del inmueble
    :param referencia: Atributo opcional para expresar una referencia adicional de ubicación del inmueble.
    """
    
    def __init__(
            self,
            tipo_inmueble: str,
            calle: str,
            municipio: str,
            estado: str,
            pais: str,
            codigo_postal: str,
            no_exterior: str = None,
            no_interior: str = None,
            colonia: str = None,
            localidad: str = None,
            referencia: str = None,
    ): 
        super().__init__({
            'TipoInmueble': tipo_inmueble,
            'Calle': calle,
            'Municipio': municipio,
            'Estado': estado,
            'Pais': pais,
            'CodigoPostal': codigo_postal,
            'NoExterior': no_exterior,
            'NoInterior': no_interior,
            'Colonia': colonia,
            'Localidad': localidad,
            'Referencia': referencia,
        })
        

class NotariosPublicos(CFDI):
    """
    Complemento al Comprobante Fiscal Digital a través de Internet (CFDI) para el manejo de la enajenación de bienes inmuebles o servidumbres de paso con indemnización o contraprestación en una sola exhibición.
    
    :param desc_inmuebles: Nodo que contiene las descripciones del inmueble o inmuebles objeto del acto otorgado.
    :param datos_operacion: Nodo para definir los detalles de la operación.
    :param datos_notario:
    :param datos_enajenante: Nodo para capturar los datos del enajenante o enajenantes, o en el caso de servidumbres de paso del propietario o poseedores o propietarios o poseedores del predio sirviente.
    :param datos_adquiriente: Nodo para capturar los datos del adquiriente, adquirientes o propietario, o propietarios o poseedores, en caso de servidumbres de paso.
    """
    
    tag = '{http://www.sat.gob.mx/notariospublicos}NotariosPublicos'
    version = '1.0'
    
    def __init__(
            self,
            desc_inmuebles: DescInmueble | dict | Sequence[DescInmueble | dict],
            datos_operacion: DatosOperacion | dict,
            datos_notario: DatosNotario | dict,
            datos_enajenante: DatosEnajenante | dict,
            datos_adquiriente: DatosAdquiriente | dict,
    ): 
        super().__init__({
            'Version': self.version,
            'DescInmuebles': desc_inmuebles,
            'DatosOperacion': datos_operacion,
            'DatosNotario': datos_notario,
            'DatosEnajenante': datos_enajenante,
            'DatosAdquiriente': datos_adquiriente,
        })
        

