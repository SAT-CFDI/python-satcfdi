DIOT
================================================

Sin Operaciones
____________________________________

.. code-block:: python

    from satcfdi.diot import *
    
    diot = DIOT(
        datos_identificacion=DatosIdentificacion(
            rfc="OÑO120726RX3",
            razon_social="ORGANICOS ÑAVEZ OSORIO S.A DE C.V",
            ejercicio=2021,
        ),
        periodo=Periodo.ENERO
    )
    
    package = diot.generate_package()
    print(package)
    

Con Operaciones
_____________________________________

.. code-block:: python

    from datetime import date
    from satcfdi.diot import *
    
    diot = DIOT(
        datos_identificacion=DatosIdentificacion(
            rfc="OÑO120726RX3",
            razon_social="ORGANICOS ÑAVEZ OSORIO S.A DE C.V",
            ejercicio=2021,
        ),
        periodo=Periodo.JULIO_SEPTIEMBRE,
        complementaria=DatosComplementaria(
            folio_anterior="12313",
            fecha_presentacion_anterior=date(2021, 5, 10)
        ),
        proveedores=[
            ProveedorTercero(
                tipo_tercero=TipoTercero.PROVEEDOR_EXTRANJERO,
                tipo_operacion=TipoOperacion.OTROS,
                id_fiscal="1254TAXID",
                nombre_extranjero="NOMBREEXTRANJERO",
                pais=Pais.ANTIGUA_Y_BERMUDA,
                nacionalidad="BERMUDO",
                iva16=456,
                iva16_na=752,
                iva_rfn=782,
                iva_rfn_na=456,
                iva_import16=123,
                iva_import16_na=475,
                iva_import_exento=7575,
                iva0=45213,
                iva_exento=1247,
                retenido=235,
                devoluciones=786
            ),
            ProveedorTercero(
                tipo_tercero=TipoTercero.PROVEEDOR_GLOBAL,
                tipo_operacion=TipoOperacion.ARRENDAMIENTO_DE_INMUEBLES,
                iva16=9874,
                iva16_na=8521,
                iva_rfn=7632,
                iva_rfn_na=6541,
                iva_import16=5241,
                iva_import16_na=4123,
                iva_import_exento=3562,
                iva0=2415,
                iva_exento=1235,
                retenido=985,
                devoluciones=874
            ),
            ProveedorTercero(
                tipo_tercero=TipoTercero.PROVEEDOR_NACIONAL,
                tipo_operacion=TipoOperacion.OTROS,
                rfc="L&O950913MSA",
                iva16=96208900,
                iva16_na=85100,
                iva_rfn=74300,
                iva_rfn_na=67600,
                iva0=58900,
                iva_exento=47700,
                retenido=36400,
                devoluciones=24864
            ),
            ProveedorTercero(
                tipo_tercero=TipoTercero.PROVEEDOR_GLOBAL,
                tipo_operacion=TipoOperacion.PRESTACION_DE_SERVICIOS_PROFESIONALES,
                iva16=77757987856,
            ),
            ProveedorTercero(
                tipo_tercero=TipoTercero.PROVEEDOR_NACIONAL,
                tipo_operacion=TipoOperacion.PRESTACION_DE_SERVICIOS_PROFESIONALES,
                rfc="IXS7607092R5",
                iva16_na=500,
                iva_rfn=0
            )
        ]
    )
    
    package = diot.generate_package()
    print(package)
    
    diot.pdf_write('diot.pdf')
    