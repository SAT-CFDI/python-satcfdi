"""nomina http://www.sat.gob.mx/nomina"""
from decimal import Decimal
from datetime import datetime, date, time
from collections.abc import Sequence
from ...cfdi import CFDI
from ...xelement import XElement
from ...utils import ScalarMap


class HorasExtra(ScalarMap):
    """
    Nodo opcional para expresar información de las horas extras
    
    :param dias: Número de días en que el trabajador realizó horas extra en el periodo
    :param tipo_horas: Tipo de pago de las horas extra: dobles o triples
    :param horas_extra: Número de horas extra trabajadas en el periodo
    :param importe_pagado: Importe pagado por las horas extra
    """
    
    def __init__(
            self,
            dias: int,
            tipo_horas: str,
            horas_extra: int,
            importe_pagado: Decimal | int,
    ): 
        super().__init__({
            'Dias': dias,
            'TipoHoras': tipo_horas,
            'HorasExtra': horas_extra,
            'ImportePagado': importe_pagado,
        })
        

class Incapacidad(ScalarMap):
    """
    Nodo opcional para expresar información de las incapacidades
    
    :param dias_incapacidad: Número de días que el trabajador se incapacitó en el periodo
    :param tipo_incapacidad: Razón de la incapacidad: Catálogo publicado en el portal del SAT en internet
    :param descuento: Monto del descuento por la incapacidad
    """
    
    def __init__(
            self,
            dias_incapacidad: Decimal | int,
            tipo_incapacidad: int,
            descuento: Decimal | int,
    ): 
        super().__init__({
            'DiasIncapacidad': dias_incapacidad,
            'TipoIncapacidad': tipo_incapacidad,
            'Descuento': descuento,
        })
        

class Deduccion(ScalarMap):
    """
    Nodo para expresar la información detallada de una deducción
    
    :param tipo_deduccion: Clave agrupadora. Clasifica la deducción conforme al catálogo publicado en el portal del SAT en internet
    :param clave: Atributo requerido para la clave de deducción de nómina propia de la contabilidad de cada patrón, puede conformarse desde 3 hasta 15 caracteres
    :param concepto: Atributo requerido para la descripción del concepto de deducción
    :param importe_gravado: Atributo requerido, representa el importe gravado de un concepto de deducción
    :param importe_exento: Atributo requerido, representa el importe exento de un concepto de deducción
    """
    
    def __init__(
            self,
            tipo_deduccion: int,
            clave: str,
            concepto: str,
            importe_gravado: Decimal | int,
            importe_exento: Decimal | int,
    ): 
        super().__init__({
            'TipoDeduccion': tipo_deduccion,
            'Clave': clave,
            'Concepto': concepto,
            'ImporteGravado': importe_gravado,
            'ImporteExento': importe_exento,
        })
        

class Deducciones(ScalarMap):
    """
    Nodo opcional para expresar las deducciones aplicables
    
    :param total_gravado: Atributo requerido para expresar el total de deducciones gravadas que se relacionan en el comprobante
    :param total_exento: Atributo requerido para expresar el total de deducciones exentas que se relacionan en el comprobante
    :param deduccion: Nodo para expresar la información detallada de una deducción
    """
    
    def __init__(
            self,
            total_gravado: Decimal | int,
            total_exento: Decimal | int,
            deduccion: Deduccion | dict | Sequence[Deduccion | dict],
    ): 
        super().__init__({
            'TotalGravado': total_gravado,
            'TotalExento': total_exento,
            'Deduccion': deduccion,
        })
        

class Percepcion(ScalarMap):
    """
    Nodo para expresar la información detallada de una percepción
    
    :param tipo_percepcion: Clave agrupadora. Clasifica la percepción conforme al catálogo publicado en el portal del SAT en internet
    :param clave: Atributo requerido, representa la clave de percepción de nómina propia de la contabilidad de cada patrón, puede conformarse desde 3 hasta 15 caracteres
    :param concepto: Atributo requerido para la descripción del concepto de percepción
    :param importe_gravado: Atributo requerido, representa el importe gravado de un concepto de percepción
    :param importe_exento: Atributo requerido, representa el importe exento de un concepto de percepción
    """
    
    def __init__(
            self,
            tipo_percepcion: int,
            clave: str,
            concepto: str,
            importe_gravado: Decimal | int,
            importe_exento: Decimal | int,
    ): 
        super().__init__({
            'TipoPercepcion': tipo_percepcion,
            'Clave': clave,
            'Concepto': concepto,
            'ImporteGravado': importe_gravado,
            'ImporteExento': importe_exento,
        })
        

class Percepciones(ScalarMap):
    """
    Nodo opcional para expresar las percepciones aplicables
    
    :param total_gravado: Atributo requerido para expresar el total de percepciones gravadas que se relacionan en el comprobante
    :param total_exento: Atributo requerido para expresar el total de percepciones exentas que se relacionan en el comprobante
    :param percepcion: Nodo para expresar la información detallada de una percepción
    """
    
    def __init__(
            self,
            total_gravado: Decimal | int,
            total_exento: Decimal | int,
            percepcion: Percepcion | dict | Sequence[Percepcion | dict],
    ): 
        super().__init__({
            'TotalGravado': total_gravado,
            'TotalExento': total_exento,
            'Percepcion': percepcion,
        })
        

class Nomina(CFDI):
    """
    Complemento al Comprobante Fiscal Digital a través de Internet (CFDI) para el manejo de datos de Nómina.
    
    :param num_empleado: Atributo requerido para expresar el número de empleado de 1 a 15 posiciones
    :param curp: Atributo requerido para la expresión de la CURP del trabajador
    :param tipo_regimen: Atributo requerido para la expresión de la clave del régimen por el cual se tiene contratado al trabajador, conforme al catálogo publicado en el portal del SAT en internet
    :param fecha_pago: Atributo requerido para la expresión de la fecha efectiva de erogación del gasto. Se expresa en la forma aaaa-mm-dd, de acuerdo con la especificación ISO 8601.
    :param fecha_inicial_pago: Atributo requerido para la expresión de la fecha inicial del pago. Se expresa en la forma aaaa-mm-dd, de acuerdo con la especificación ISO 8601.
    :param fecha_final_pago: Atributo requerido para la expresión de la fecha final del pago. Se expresa en la forma aaaa-mm-dd, de acuerdo con la especificación ISO 8601.
    :param num_dias_pagados: Atributo requerido para la expresión del número de días pagados
    :param periodicidad_pago: Forma en que se establece el pago del salario: diario, semanal, quincenal, catorcenal mensual, bimestral, unidad de obra, comisión, precio alzado, etc.
    :param registro_patronal: Atributo opcional para expresar el registro patronal a 20 posiciones máximo
    :param num_seguridad_social: Atributo opcional para la expresión del número de seguridad social aplicable al trabajador
    :param departamento: Atributo opcional para la expresión del departamento o área a la que pertenece el trabajador
    :param clabe: Atributo opcional para la expresión de la CLABE
    :param banco: Atributo opcional para la expresión del Banco conforme al catálogo, donde se realiza un depósito de nómina
    :param fecha_inicio_rel_laboral: Atributo opcional para expresar la fecha de inicio de la relación laboral entre el empleador y el empleado
    :param antiguedad: Número de semanas que el empleado ha mantenido relación laboral con el empleador
    :param puesto: Puesto asignado al empleado o actividad que realiza
    :param tipo_contrato: Tipo de contrato que tiene el trabajador: Base, Eventual, Confianza, Sindicalizado, a prueba, etc.
    :param tipo_jornada: Tipo de jornada que cubre el trabajador: Diurna, nocturna, mixta, por hora, reducida, continuada, partida, por turnos, etc.
    :param salario_base_cot_apor: Retribución otorgada al trabajador, que se integra por los pagos hechos en efectivo por cuota diaria, gratificaciones, percepciones, alimentación, habitación, primas, comisiones, prestaciones en especie y cualquiera otra cantidad o prestación que se entregue al trabajador por su trabajo, sin considerar los conceptos que se excluyen de conformidad con el Artículo 27 de la Ley del Seguro Social. (Se emplea para pagar las cuotas y aportaciones de Seguridad Social).
    :param riesgo_puesto: Clave conforme a la Clase en que deben inscribirse los patrones, de acuerdo a las actividades que desempeñan sus trabajadores, según lo previsto en el artículo 196 del Reglamento en Materia de Afiliación Clasificación de Empresas, Recaudación y Fiscalización. Catálogo publicado en el portal del SAT en internet
    :param salario_diario_integrado: El salario se integra con los pagos hechos en efectivo por cuota diaria, gratificaciones, percepciones, habitación, primas, comisiones, prestaciones en especie y cualquiera otra cantidad o prestación que se entregue al trabajador por su trabajo, de conformidad con el Art. 84 de la Ley Federal del Trabajo. (Se utiliza para el cálculo de las indemnizaciones).
    :param percepciones: Nodo opcional para expresar las percepciones aplicables
    :param deducciones: Nodo opcional para expresar las deducciones aplicables
    :param incapacidades: Nodo opcional para expresar las incapacidades aplicables
    :param horas_extras: Nodo opcional para expresar las horas extras aplicables
    """
    
    tag = '{http://www.sat.gob.mx/nomina}Nomina'
    version = '1.1'
    
    def __init__(
            self,
            num_empleado: str,
            curp: str,
            tipo_regimen: int,
            fecha_pago: date,
            fecha_inicial_pago: date,
            fecha_final_pago: date,
            num_dias_pagados: Decimal | int,
            periodicidad_pago: str,
            registro_patronal: str = None,
            num_seguridad_social: str = None,
            departamento: str = None,
            clabe: int = None,
            banco: int = None,
            fecha_inicio_rel_laboral: date = None,
            antiguedad: int = None,
            puesto: str = None,
            tipo_contrato: str = None,
            tipo_jornada: str = None,
            salario_base_cot_apor: Decimal | int = None,
            riesgo_puesto: int = None,
            salario_diario_integrado: Decimal | int = None,
            percepciones: Percepciones | dict = None,
            deducciones: Deducciones | dict = None,
            incapacidades: Incapacidad | dict | Sequence[Incapacidad | dict] = None,
            horas_extras: HorasExtra | dict | Sequence[HorasExtra | dict] = None,
    ): 
        super().__init__({
            'Version': self.version,
            'NumEmpleado': num_empleado,
            'CURP': curp,
            'TipoRegimen': tipo_regimen,
            'FechaPago': fecha_pago,
            'FechaInicialPago': fecha_inicial_pago,
            'FechaFinalPago': fecha_final_pago,
            'NumDiasPagados': num_dias_pagados,
            'PeriodicidadPago': periodicidad_pago,
            'RegistroPatronal': registro_patronal,
            'NumSeguridadSocial': num_seguridad_social,
            'Departamento': departamento,
            'CLABE': clabe,
            'Banco': banco,
            'FechaInicioRelLaboral': fecha_inicio_rel_laboral,
            'Antiguedad': antiguedad,
            'Puesto': puesto,
            'TipoContrato': tipo_contrato,
            'TipoJornada': tipo_jornada,
            'SalarioBaseCotApor': salario_base_cot_apor,
            'RiesgoPuesto': riesgo_puesto,
            'SalarioDiarioIntegrado': salario_diario_integrado,
            'Percepciones': percepciones,
            'Deducciones': deducciones,
            'Incapacidades': incapacidades,
            'HorasExtras': horas_extras,
        })
        

