PLD (Prevencion de Lavado de Dinero)
================================================

Aviso ARI
____________________________________

.. code-block:: python

    from datetime import date
    from satcfdi.create.pld import ari
    
    aviso_ari = ari.Archivo(
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
    
    aviso_ari.xml_write("aviso_ari.xml")
