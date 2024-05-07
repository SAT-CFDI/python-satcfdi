import inspect
import os
from datetime import date

import pytest
from satcfdi.xelement import XElement

from satcfdi import render
from satcfdi.exceptions import SchemaValidationError
from satcfdi.create.pld import ari
from tests.utils import verify_result, XElementPrettyPrinter

module = 'satcfdi'
current_dir = os.path.dirname(__file__)


def verify_invoice(invoice, path):
    pp = XElementPrettyPrinter()
    verify = verify_result(data=pp.pformat(invoice), filename=f"{path}.pretty.py")
    assert verify

    verify = verify_result(data=invoice.xml_bytes(pretty_print=True), filename=f"{path}.xml")
    assert verify

    verify = verify_result(data=render.html_str(invoice), filename=f"{path}.html")
    assert verify


def test_ejemplos():
    pld_ejemplos_dir = os.path.join(current_dir, 'pdl', 'ejemplos')

    for file in os.listdir(pld_ejemplos_dir):
        ejemplo = XElement.from_file(os.path.join(pld_ejemplos_dir, file))

        verify_invoice(ejemplo, path=f"ejemplos/{file}")


def test_arrendamiento_de_inmuebles_zeros():
    ari_file = os.path.join(current_dir, 'pdl', 'ejemplo_ari_zeros.xml')
    report_f = XElement.from_file(ari_file)

    report_a = ari.Archivo(
        informe=ari.InformeType(
            mes_reportado='202210',
            sujeto_obligado=ari.SujetoObligadoType(
                clave_sujeto_obligado='OGA751212G56',
                clave_actividad='ARI'
            )
        )
    )

    report_a = report_a.process()
    assert report_a == report_f

    verify = verify_result(data=report_a.xml_bytes(pretty_print=True, include_schema_location=True), filename=f"o_{inspect.stack()[0][3]}.xml")
    assert verify


def test_arrendamiento_de_inmuebles_zeros_invalid():
    with pytest.raises(SchemaValidationError) as excinfo:
        report_a = ari.Archivo(
            informe=ari.InformeType(
                mes_reportado='20221043',  # Mes invalido
                sujeto_obligado=ari.SujetoObligadoType(
                    clave_sujeto_obligado='OGA751212G56',
                    clave_actividad='ARI'
                )
            )
        ).process(validate=True)

    verify = verify_result(data=str(excinfo.value.error_log), filename=f"o_{inspect.stack()[0][3]}.txt")
    assert verify


def test_arrendamiento_de_inmuebles():
    ari_file = os.path.join(current_dir, 'pdl', 'ejemplo_ari.xml')
    report_f = XElement.from_file(ari_file)

    report_a = ari.Archivo(
        informe=ari.InformeType(
            mes_reportado='201407',
            sujeto_obligado=ari.SujetoObligadoType(
                clave_sujeto_obligado='OGA751212G56',
                clave_actividad='ARI'
            ),
            aviso=ari.AvisoType(
                referencia_aviso='REF15454FG454',
                prioridad='1',
                alerta=ari.AlertaType(
                    tipo_alerta='100'
                ),
                persona_aviso=ari.PersonaAvisoType(
                    tipo_persona=ari.TipoPersonaType(
                        persona_fisica=ari.PersonaFisicaType(
                            nombre='NEPOMUCENO',
                            apellido_paterno='ALMONTE',
                            apellido_materno='JUAREZ',
                            fecha_nacimiento=date(1956, 8, 16),
                            pais_nacionalidad='TG',
                            actividad_economica='3130100'
                        )
                    ),
                    tipo_domicilio=ari.TipoDomicilioType(
                        extranjero=ari.ExtranjeroType(
                            pais='TG',
                            estado_provincia='TOGUILLITA',
                            ciudad_poblacion='TOGUIS',
                            colonia='NA',
                            calle='TOGA TOGA',
                            numero_exterior='45',
                            codigo_postal='12448'
                        )
                    ),
                ),
                detalle_operaciones=ari.DetalleOperacionesType(
                    datos_operacion=ari.DatosOperacionType(
                        fecha_operacion=date(2014, 7, 1),
                        tipo_operacion='1501',
                        caracteristicas=ari.CaracteristicasType(
                            fecha_inicio=date(2014, 1, 1),
                            fecha_termino=date(2015, 1, 1),
                            tipo_inmueble='3',
                            valor_referencia='356825.12',
                            colonia='6920',
                            calle='SAN SIMON TOLNAHUAC',
                            numero_exterior='VIOLANTE',
                            numero_interior='45',
                            codigo_postal='01058',
                            folio_real='BG544-FRR-456B-FRR'
                        ),
                        datos_liquidacion=ari.DatosLiquidacionType(
                            fecha_pago=date(2014, 7, 1),
                            forma_pago='4',
                            instrumento_monetario='4',
                            moneda='2',
                            monto_operacion='757897.55'
                        )
                    )
                )
            )
        )
    ).process()

    assert report_a == report_f

    verify_invoice(report_a, path=f"o_{inspect.stack()[0][3]}")
