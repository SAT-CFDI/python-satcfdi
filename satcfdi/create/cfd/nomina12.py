"""nomina12 http://www.sat.gob.mx/nomina12"""
from collections.abc import *
from datetime import date
from decimal import Decimal

from ...cfdi import CFDI
from ...utils import ScalarMap
from ...utils import iterate


class Incapacidad(ScalarMap):
    """
    Nodo requerido para expresar información de las incapacidades.

    :param dias_incapacidad: Atributo requerido para expresar el número de días enteros que el trabajador se incapacitó en el periodo.
    :param tipo_incapacidad: Atributo requerido para expresar la razón de la incapacidad.
    :param importe_monetario: Atributo condicional para expresar el monto del importe monetario de la incapacidad.
    """

    def __init__(
            self,
            dias_incapacidad: int,
            tipo_incapacidad: str,
            importe_monetario: Decimal | int = None,
    ):
        super().__init__({
            'DiasIncapacidad': dias_incapacidad,
            'TipoIncapacidad': tipo_incapacidad,
            'ImporteMonetario': importe_monetario,
        })


class CompensacionSaldosAFavor(ScalarMap):
    """
    Nodo condicional para expresar la información referente a la compensación de saldos a favor de un trabajador.

    :param saldo_a_favor: Atributo requerido para expresar el saldo a favor determinado por el patrón al trabajador en periodos o ejercicios anteriores.
    :param ano: Atributo requerido para expresar el año en que se determinó el saldo a favor del trabajador por el patrón que se incluye en el campo “RemanenteSalFav”.
    :param remanente_sal_fav: Atributo requerido para expresar el remanente del saldo a favor del trabajador.
    """

    def __init__(
            self,
            saldo_a_favor: Decimal | int,
            ano: int,
            remanente_sal_fav: Decimal | int,
    ):
        super().__init__({
            'SaldoAFavor': saldo_a_favor,
            'Año': ano,
            'RemanenteSalFav': remanente_sal_fav,
        })


class OtroPago(ScalarMap):
    """
    Nodo requerido para expresar la información detallada del otro pago.

    :param tipo_otro_pago: Atributo requerido para expresar la clave agrupadora bajo la cual se clasifica el otro pago.
    :param clave: Atributo requerido, representa la clave de otro pago de nómina propia de la contabilidad de cada patrón, puede conformarse desde 3 hasta 15 caracteres.
    :param concepto: Atributo requerido para la descripción del concepto de otro pago.
    :param importe: Atributo requerido para expresar el importe del concepto de otro pago.
    :param subsidio_al_empleo: Nodo condicional para expresar la información referente al subsidio al empleo del trabajador.
    :param compensacion_saldos_a_favor: Nodo condicional para expresar la información referente a la compensación de saldos a favor de un trabajador.
    """

    def __init__(
            self,
            tipo_otro_pago: str,
            clave: str,
            concepto: str,
            importe: Decimal | int,
            subsidio_al_empleo: Decimal | int = None,
            compensacion_saldos_a_favor: CompensacionSaldosAFavor | dict = None,
    ):
        super().__init__({
            'TipoOtroPago': tipo_otro_pago,
            'Clave': clave,
            'Concepto': concepto,
            'Importe': importe,
            'SubsidioAlEmpleo': subsidio_al_empleo,
            'CompensacionSaldosAFavor': compensacion_saldos_a_favor,
        })


class Deduccion(ScalarMap):
    """
    Nodo requerido para expresar la información detallada de una deducción.

    :param tipo_deduccion: Atributo requerido para registrar la clave agrupadora que clasifica la deducción.
    :param clave: Atributo requerido para la clave de deducción de nómina propia de la contabilidad de cada patrón, puede conformarse desde 3 hasta 15 caracteres.
    :param concepto: Atributo requerido para la descripción del concepto de deducción.
    :param importe: Atributo requerido para registrar el importe del concepto de deducción.
    """

    def __init__(
            self,
            tipo_deduccion: str,
            clave: str,
            concepto: str,
            importe: Decimal | int,
    ):
        super().__init__({
            'TipoDeduccion': tipo_deduccion,
            'Clave': clave,
            'Concepto': concepto,
            'Importe': importe,
        })


class Deducciones(ScalarMap):
    """
    Nodo opcional para expresar las deducciones aplicables.

    :param deduccion: Nodo requerido para expresar la información detallada de una deducción.
    """

    def __init__(
            self,
            deduccion: Deduccion | Sequence[Deduccion | dict],
    ):
        super().__init__({
            'Deduccion': deduccion,
        })


class SeparacionIndemnizacion(ScalarMap):
    """
    Nodo condicional para expresar la información detallada de otros pagos por separación.

    :param total_pagado: Atributo requerido que indica el monto total del pago.
    :param num_anos_servicio: Atributo requerido para expresar el número de años de servicio del trabajador. Se redondea al entero superior si la cifra contiene años y meses y hay más de 6 meses.
    :param ultimo_sueldo_mens_ord: Atributo requerido que indica el último sueldo mensual ordinario.
    :param ingreso_acumulable: Atributo requerido para expresar los ingresos acumulables.
    :param ingreso_no_acumulable: Atributo requerido que indica los ingresos no acumulables.
    """

    def __init__(
            self,
            total_pagado: Decimal | int,
            num_anos_servicio: int,
            ultimo_sueldo_mens_ord: Decimal | int,
            ingreso_acumulable: Decimal | int,
            ingreso_no_acumulable: Decimal | int,
    ):
        super().__init__({
            'TotalPagado': total_pagado,
            'NumAñosServicio': num_anos_servicio,
            'UltimoSueldoMensOrd': ultimo_sueldo_mens_ord,
            'IngresoAcumulable': ingreso_acumulable,
            'IngresoNoAcumulable': ingreso_no_acumulable,
        })


class JubilacionPensionRetiro(ScalarMap):
    """
    Nodo condicional para expresar la información detallada de pagos por jubilación, pensiones o haberes de retiro.

    :param ingreso_acumulable: Atributo requerido para expresar los ingresos acumulables.
    :param ingreso_no_acumulable: Atributo requerido para expresar los ingresos no acumulables.
    :param total_una_exhibicion: Atributo condicional que indica el monto total del pago cuando se realiza en una sola exhibición.
    :param total_parcialidad: Atributo condicional para expresar los ingresos totales por pago cuando se hace en parcialidades.
    :param monto_diario: Atributo condicional para expresar el monto diario percibido por jubilación, pensiones o haberes de retiro cuando se realiza en parcialidades.
    """

    def __init__(
            self,
            ingreso_acumulable: Decimal | int,
            ingreso_no_acumulable: Decimal | int,
            total_una_exhibicion: Decimal | int = None,
            total_parcialidad: Decimal | int = None,
            monto_diario: Decimal | int = None,
    ):
        super().__init__({
            'IngresoAcumulable': ingreso_acumulable,
            'IngresoNoAcumulable': ingreso_no_acumulable,
            'TotalUnaExhibicion': total_una_exhibicion,
            'TotalParcialidad': total_parcialidad,
            'MontoDiario': monto_diario,
        })


class HorasExtra(ScalarMap):
    """
    Nodo condicional para expresar las horas extra aplicables.

    :param dias: Atributo requerido para expresar el número de días en que el trabajador realizó horas extra en el periodo.
    :param tipo_horas: Atributo requerido para expresar el tipo de pago de las horas extra.
    :param horas_extra: Atributo requerido para expresar el número de horas extra trabajadas en el periodo.
    :param importe_pagado: Atributo requerido para expresar el importe pagado por las horas extra.
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


class AccionesOTitulos(ScalarMap):
    """
    Nodo condicional para expresar ingresos por acciones o títulos valor que representan bienes. Se vuelve requerido cuando existan ingresos por sueldos derivados de adquisición de acciones o títulos (Art. 94, fracción VII LISR).

    :param valor_mercado: Atributo requerido para expresar el valor de mercado de las Acciones o Títulos valor al ejercer la opción.
    :param precio_al_otorgarse: Atributo requerido para expresar el precio establecido al otorgarse la opción de ingresos en acciones o títulos valor.
    """

    def __init__(
            self,
            valor_mercado: Decimal | int,
            precio_al_otorgarse: Decimal | int,
    ):
        super().__init__({
            'ValorMercado': valor_mercado,
            'PrecioAlOtorgarse': precio_al_otorgarse,
        })


class Percepcion(ScalarMap):
    """
    Nodo requerido para expresar la información detallada de una percepción

    :param tipo_percepcion: Atributo requerido para expresar la Clave agrupadora bajo la cual se clasifica la percepción.
    :param clave: Atributo requerido para expresar la clave de percepción de nómina propia de la contabilidad de cada patrón, puede conformarse desde 3 hasta 15 caracteres.
    :param concepto: Atributo requerido para la descripción del concepto de percepción
    :param importe_gravado: Atributo requerido, representa el importe gravado de un concepto de percepción.
    :param importe_exento: Atributo requerido, representa el importe exento de un concepto de percepción.
    :param acciones_o_titulos: Nodo condicional para expresar ingresos por acciones o títulos valor que representan bienes. Se vuelve requerido cuando existan ingresos por sueldos derivados de adquisición de acciones o títulos (Art. 94, fracción VII LISR).
    :param horas_extra: Nodo condicional para expresar las horas extra aplicables.
    """

    def __init__(
            self,
            tipo_percepcion: str,
            clave: str,
            concepto: str,
            importe_gravado: Decimal | int,
            importe_exento: Decimal | int,
            acciones_o_titulos: AccionesOTitulos | dict = None,
            horas_extra: HorasExtra | Sequence[HorasExtra | dict] = None,
    ):
        super().__init__({
            'TipoPercepcion': tipo_percepcion,
            'Clave': clave,
            'Concepto': concepto,
            'ImporteGravado': importe_gravado,
            'ImporteExento': importe_exento,
            'AccionesOTitulos': acciones_o_titulos,
            'HorasExtra': horas_extra,
        })


class Percepciones(ScalarMap):
    """
    Nodo condicional para expresar las percepciones aplicables.

    :param jubilacion_pension_retiro: Nodo condicional para expresar la información detallada de pagos por jubilación, pensiones o haberes de retiro.
    :param separacion_indemnizacion: Nodo condicional para expresar la información detallada de otros pagos por separación.
    """

    def __init__(
            self,
            percepcion: Percepcion | Sequence[Percepcion | dict],
            jubilacion_pension_retiro: JubilacionPensionRetiro | dict = None,
            separacion_indemnizacion: SeparacionIndemnizacion | dict = None,
    ):
        super().__init__({
            'Percepcion': percepcion,
            'JubilacionPensionRetiro': jubilacion_pension_retiro,
            'SeparacionIndemnizacion': separacion_indemnizacion,
        })


class EntidadSNCF(ScalarMap):
    """
    Nodo condicional para que las entidades adheridas al Sistema Nacional de Coordinación Fiscal realicen la identificación del origen de los recursos utilizados en el pago de nómina del personal que presta o desempeña un servicio personal subordinado en las dependencias de la entidad federativa, del municipio o demarcación territorial de la Ciudad de México, así como en sus respectivos organismos autónomos y entidades paraestatales y paramunicipales

    :param origen_recurso: Atributo requerido para identificar el origen del recurso utilizado para el pago de nómina del personal que presta o desempeña un servicio personal subordinado o asimilado a salarios en las dependencias.
    :param monto_recurso_propio: Atributo condicional para expresar el monto del recurso pagado con cargo a sus participaciones u otros ingresos locales (importe bruto de los ingresos propios, es decir total de gravados y exentos), cuando el origen es mixto.
    """

    def __init__(
            self,
            origen_recurso: str,
            monto_recurso_propio: Decimal | int = None,
    ):
        super().__init__({
            'OrigenRecurso': origen_recurso,
            'MontoRecursoPropio': monto_recurso_propio,
        })


class Emisor(ScalarMap):
    """
    Nodo condicional para expresar la información del contribuyente emisor del comprobante de nómina.

    :param curp: Atributo condicional para expresar la CURP del emisor del comprobante de nómina cuando es una persona física.
    :param registro_patronal: Atributo condicional para expresar el registro patronal, clave de ramo - pagaduría o la que le asigne la institución de seguridad social al patrón, a 20 posiciones máximo. Se debe ingresar cuando se cuente con él, o se esté obligado conforme a otras disposiciones distintas a las fiscales.
    :param rfc_patron_origen: Atributo opcional para expresar el RFC de la persona que fungió como patrón cuando el pago al trabajador se realice a través de un tercero como vehículo o herramienta de pago.
    :param entidad_sncf: Nodo condicional para que las entidades adheridas al Sistema Nacional de Coordinación Fiscal realicen la identificación del origen de los recursos utilizados en el pago de nómina del personal que presta o desempeña un servicio personal subordinado en las dependencias de la entidad federativa, del municipio o demarcación territorial de la Ciudad de México, así como en sus respectivos organismos autónomos y entidades paraestatales y paramunicipales
    """

    def __init__(
            self,
            curp: str = None,
            registro_patronal: str = None,
            rfc_patron_origen: str = None,
            entidad_sncf: EntidadSNCF | dict = None,
    ):
        super().__init__({
            'Curp': curp,
            'RegistroPatronal': registro_patronal,
            'RfcPatronOrigen': rfc_patron_origen,
            'EntidadSNCF': entidad_sncf,
        })


class SubContratacion(ScalarMap):
    """
    Nodo condicional para expresar la lista de las personas que los subcontrataron.

    :param rfc_labora: Atributo requerido para expresar el RFC de la persona que subcontrata.
    :param porcentaje_tiempo: Atributo requerido para expresar el porcentaje del tiempo que prestó sus servicios con el RFC que lo subcontrata.
    """

    def __init__(
            self,
            rfc_labora: str,
            porcentaje_tiempo: Decimal | int,
    ):
        super().__init__({
            'RfcLabora': rfc_labora,
            'PorcentajeTiempo': porcentaje_tiempo,
        })


class Receptor(ScalarMap):
    """
    Nodo requerido para precisar la información del contribuyente receptor del comprobante de nómina.

    :param curp: Atributo requerido para expresar la CURP del receptor del comprobante de nómina.
    :param tipo_contrato: Atributo requerido para expresar el tipo de contrato que tiene el trabajador.
    :param tipo_regimen: Atributo requerido para la expresión de la clave del régimen por el cual se tiene contratado al trabajador.
    :param num_empleado: Atributo requerido para expresar el número de empleado de 1 a 15 posiciones.
    :param periodicidad_pago: Atributo requerido para la forma en que se establece el pago del salario.
    :param clave_ent_fed: Atributo requerido para expresar la clave de la entidad federativa en donde el receptor del recibo prestó el servicio.
    :param num_seguridad_social: Atributo condicional para expresar el número de seguridad social del trabajador. Se debe ingresar cuando se cuente con él, o se esté obligado conforme a otras disposiciones distintas a las fiscales.
    :param fecha_inicio_rel_laboral: Atributo condicional para expresar la fecha de inicio de la relación laboral entre el empleador y el empleado. Se expresa en la forma AAAA-MM-DD, de acuerdo con la especificación ISO 8601. Se debe ingresar cuando se cuente con él, o se esté obligado conforme a otras disposiciones distintas a las fiscales.
    :param antiguedad: Atributo condicional para expresar el número de semanas o el periodo de años, meses y días que el empleado ha mantenido relación laboral con el empleador. Se debe ingresar cuando se cuente con él, o se esté obligado conforme a otras disposiciones distintas a las fiscales.
    :param sindicalizado: Atributo opcional para indicar si el trabajador está asociado a un sindicato. Si se omite se asume que no está asociado a algún sindicato.
    :param tipo_jornada: Atributo condicional para expresar el tipo de jornada que cubre el trabajador. Se debe ingresar cuando se esté obligado conforme a otras disposiciones distintas a las fiscales.
    :param departamento: Atributo opcional para la expresión del departamento o área a la que pertenece el trabajador.
    :param puesto: Atributo opcional para la expresión del puesto asignado al empleado o actividad que realiza.
    :param riesgo_puesto: Atributo opcional para expresar la clave conforme a la Clase en que deben inscribirse los patrones, de acuerdo con las actividades que desempeñan sus trabajadores, según lo previsto en el artículo 196 del Reglamento en Materia de Afiliación Clasificación de Empresas, Recaudación y Fiscalización, o conforme con la normatividad del Instituto de Seguridad Social del trabajador.  Se debe ingresar cuando se cuente con él, o se esté obligado conforme a otras disposiciones distintas a las fiscales.
    :param banco: Atributo condicional para la expresión de la clave del Banco conforme al catálogo, donde se realiza el depósito de nómina.
    :param cuenta_bancaria: Atributo condicional para la expresión de la cuenta bancaria a 11 posiciones o número de teléfono celular a 10 posiciones o número de tarjeta de crédito, débito o servicios a 15 ó 16 posiciones o la CLABE a 18 posiciones o número de monedero electrónico, donde se realiza el depósito de nómina.
    :param salario_base_cot_apor: Atributo opcional para expresar la retribución otorgada al trabajador, que se integra por los pagos hechos en efectivo por cuota diaria, gratificaciones, percepciones, alimentación, habitación, primas, comisiones, prestaciones en especie y cualquiera otra cantidad o prestación que se entregue al trabajador por su trabajo, sin considerar los conceptos que se excluyen de conformidad con el Artículo 27 de la Ley del Seguro Social, o la integración de los pagos conforme la normatividad del Instituto de Seguridad Social del trabajador. (Se emplea para pagar las cuotas y aportaciones de Seguridad Social). Se debe ingresar cuando se esté obligado conforme a otras disposiciones distintas a las fiscales.
    :param salario_diario_integrado: Atributo opcional para expresar el salario que se integra con los pagos hechos en efectivo por cuota diaria, gratificaciones, percepciones, habitación, primas, comisiones, prestaciones en especie y cualquier otra cantidad o prestación que se entregue al trabajador por su trabajo, de conformidad con el Art. 84 de la Ley Federal del Trabajo. (Se utiliza para el cálculo de las indemnizaciones). Se debe ingresar cuando se esté obligado conforme a otras disposiciones distintas a las fiscales.
    :param sub_contratacion: Nodo condicional para expresar la lista de las personas que los subcontrataron.
    """

    def __init__(
            self,
            curp: str,
            tipo_contrato: str,
            tipo_regimen: str,
            num_empleado: str,
            periodicidad_pago: str,
            clave_ent_fed: str,
            num_seguridad_social: str = None,
            fecha_inicio_rel_laboral: date = None,
            antiguedad: str = None,
            sindicalizado: str = None,
            tipo_jornada: str = None,
            departamento: str = None,
            puesto: str = None,
            riesgo_puesto: str = None,
            banco: str = None,
            cuenta_bancaria: int | str = None,
            salario_base_cot_apor: Decimal | int = None,
            salario_diario_integrado: Decimal | int = None,
            sub_contratacion: SubContratacion | Sequence[SubContratacion | dict] = None,
    ):
        super().__init__({
            'Curp': curp,
            'TipoContrato': tipo_contrato,
            'TipoRegimen': tipo_regimen,
            'NumEmpleado': num_empleado,
            'PeriodicidadPago': periodicidad_pago,
            'ClaveEntFed': clave_ent_fed,
            'NumSeguridadSocial': num_seguridad_social,
            'FechaInicioRelLaboral': fecha_inicio_rel_laboral,
            'Antigüedad': antiguedad,
            'Sindicalizado': sindicalizado,
            'TipoJornada': tipo_jornada,
            'Departamento': departamento,
            'Puesto': puesto,
            'RiesgoPuesto': riesgo_puesto,
            'Banco': banco,
            'CuentaBancaria': cuenta_bancaria,
            'SalarioBaseCotApor': salario_base_cot_apor,
            'SalarioDiarioIntegrado': salario_diario_integrado,
            'SubContratacion': sub_contratacion,
        })


# Main #
class Nomina(CFDI):
    """
    Complemento para incorporar al Comprobante Fiscal Digital por Internet (CFDI) la información que ampara conceptos de ingresos por salarios, la prestación de un servicio personal subordinado o conceptos asimilados a salarios (Nómina).

    :param tipo_nomina: Atributo requerido para indicar el tipo de nómina, puede ser O= Nómina ordinaria o E= Nómina extraordinaria.
    :param fecha_pago: Atributo requerido para la expresión de la fecha efectiva de erogación del gasto. Se expresa en la forma AAAA-MM-DD, de acuerdo con la especificación ISO 8601.
    :param fecha_inicial_pago: Atributo requerido para la expresión de la fecha inicial del período de pago. Se expresa en la forma AAAA-MM-DD, de acuerdo con la especificación ISO 8601.
    :param fecha_final_pago: Atributo requerido para la expresión de la fecha final del período de pago. Se expresa en la forma AAAA-MM-DD, de acuerdo con la especificación ISO 8601.
    :param num_dias_pagados: Atributo requerido para la expresión del número o la fracción de días pagados.
    :param receptor: Nodo requerido para precisar la información del contribuyente receptor del comprobante de nómina.
    :param emisor: Nodo condicional para expresar la información del contribuyente emisor del comprobante de nómina.
    :param percepciones: Nodo condicional para expresar las percepciones aplicables.
    :param deducciones: Nodo opcional para expresar las deducciones aplicables.
    :param otros_pagos: Nodo condicional para expresar otros pagos aplicables.
    :param incapacidades: Nodo condicional para expresar información de las incapacidades.
    :return: objeto CFDI
    """

    tag = '{http://www.sat.gob.mx/nomina12}Nomina'
    version = '1.2'

    def __init__(
            self,
            tipo_nomina: str,
            fecha_pago: date,
            fecha_inicial_pago: date,
            fecha_final_pago: date,
            num_dias_pagados: Decimal,
            receptor: Receptor | dict,
            emisor: Emisor | dict = None,
            percepciones: Percepciones | dict = None,
            deducciones: Deducciones | dict = None,
            otros_pagos: OtroPago | Sequence[OtroPago | dict] = None,
            incapacidades: Incapacidad | Sequence[Incapacidad | dict] = None,
    ):
        # total_percepciones: Atributo condicional para representar la suma de las percepciones.
        total_percepciones = None
        if percepciones:
            # TotalGravado: Atributo requerido para expresar el total de percepciones gravadas que se relacionan en el comprobante.
            percepciones['TotalGravado'] = sum(p['ImporteGravado'] for p in iterate(percepciones['Percepcion']))
            # TotalExento: Atributo requerido para expresar el total de percepciones exentas que se relacionan en el comprobante.
            percepciones['TotalExento'] = sum(p['ImporteExento'] for p in iterate(percepciones['Percepcion']))
            # TotalSueldos: Atributo condicional para expresar el total de percepciones brutas (gravadas y exentas) por sueldos y salarios y conceptos asimilados a salarios.
            percepciones['TotalSueldos'] = percepciones['TotalGravado'] + percepciones['TotalExento']

            # TotalSeparacionIndemnizacion: Atributo condicional para expresar el importe exento y gravado de las claves tipo percepción 022 Prima por Antigüedad, 023 Pagos por separación y 025 Indemnizaciones.
            deducciones['TotalSeparacionIndemnizacion'] = sum(
                p['ImporteGravado'] + p['ImporteExento'] for p in iterate(percepciones['Percepcion']) if p['TipoPercepcion'] in ['022', '023', '025'])
            # TotalJubilacionPensionRetiro: Atributo condicional para expresar el importe exento y gravado de las claves tipo percepción 039 Jubilaciones, pensiones o haberes de retiro en una exhibición y 044 Jubilaciones, pensiones o haberes de retiro en parcialidades.
            deducciones['TotalJubilacionPensionRetiro'] = sum(p['ImporteGravado'] + p['ImporteExento'] for p in iterate(percepciones['Percepcion']) if p['TipoPercepcion'] in ['039', '044'])

            total_percepciones = percepciones['TotalSueldos']

        # total_deducciones: Atributo condicional para representar la suma de las deducciones aplicables.
        total_deducciones = None
        if deducciones:
            # TotalOtrasDeducciones: Atributo condicional para expresar el total de deducciones que se relacionan en el comprobante, donde la clave de tipo de deducción sea distinta a la 002 correspondiente a ISR.
            deducciones['TotalOtrasDeducciones'] = sum(p['Importe'] for p in iterate(deducciones['Deduccion']) if p['TipoDeduccion'] != '002')
            # TotalImpuestosRetenidos: Atributo condicional para expresar el total de los impuestos federales retenidos, es decir, donde la clave de tipo de deducción sea 002 correspondiente a ISR.
            deducciones['TotalImpuestosRetenidos'] = sum(p['Importe'] for p in iterate(deducciones['Deduccion']) if p['TipoDeduccion'] == '002')

            total_deducciones = deducciones['TotalImpuestosRetenidos'] + deducciones['TotalOtrasDeducciones']

        # total_otros_pagos: Atributo condicional para representar la suma de otros pagos.
        total_otros_pagos = None
        if otros_pagos:
            total_otros_pagos = sum(p["Importe"] for p in iterate(otros_pagos))

        super().__init__({
            'Version': self.version,
            'TipoNomina': tipo_nomina,
            'FechaPago': fecha_pago,
            'FechaInicialPago': fecha_inicial_pago,
            'FechaFinalPago': fecha_final_pago,
            'NumDiasPagados': num_dias_pagados,
            'Receptor': receptor,
            'TotalPercepciones': total_percepciones,
            'TotalDeducciones': total_deducciones,
            'TotalOtrosPagos': total_otros_pagos,
            'Emisor': emisor,
            'Percepciones': percepciones,
            'Deducciones': deducciones,
            'OtrosPagos': otros_pagos,
            'Incapacidades': incapacidades,
        })
