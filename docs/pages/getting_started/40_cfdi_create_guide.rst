Create CFDI
================================================

Comprobante
______________________

.. code-block:: python

    from decimal import Decimal
    from satcfdi import Signer
    from satcfdi.create.cfd import cfdi40
    from satcfdi.create.cfd.catalogos import RegimenFiscal, UsoCFDI, MetodoPago
    
    
    # Load signing certificate
    signer = Signer.load(
        certificate=open('csd/xiqb891116qe4_csd.cer', 'rb').read(),
        key=open('csd/xiqb891116qe4_csd.key', 'rb').read(),
        password=open('csd/xiqb891116qe4_csd.txt', 'r').read()
    )
    
    # create Comprobante
    invoice = cfdi40.Comprobante(
        emisor=cfdi40.Emisor(
            rfc=signer.rfc,
            nombre=signer.legal_name,
            regimen_fiscal=RegimenFiscal.GENERAL_DE_LEY_PERSONAS_MORALES
        ),
        lugar_expedicion="56820",
        receptor=cfdi40.Receptor(
            rfc='KIJ0906199R1',
            nombre='KIJ, S.A DE C.V.',
            uso_cfdi=UsoCFDI.GASTOS_EN_GENERAL,
            domicilio_fiscal_receptor="59820",
            regimen_fiscal_receptor=RegimenFiscal.GENERAL_DE_LEY_PERSONAS_MORALES
        ),
        metodo_pago=MetodoPago.PAGO_EN_PARCIALIDADES_O_DIFERIDO,
        serie="A",
        folio="123456",
        conceptos=[
            cfdi40.Concepto(
                clave_prod_serv='84111506',
                cantidad=Decimal('1.00'),
                clave_unidad='E48',
                descripcion='SERVICIOS DE FACTURACION',
                valor_unitario=Decimal('1250.30'),
                impuestos=cfdi40.Impuestos(
                    traslados='IVA|Tasa|0.160000',
                    retenciones=['ISR|Tasa|0.100000', 'IVA|Tasa|0.106667'],
                ),
                _traslados_incluidos=False  # indica si el valor unitario incluye los traslados
            )
        ]
    )
    invoice.sign(signer)
    invoice = invoice.process()
    

Nomina
______________________

.. code-block:: python

    from datetime import date
    from decimal import Decimal
    from satcfdi import Signer
    from satcfdi.create.cfd import cfdi40, nomina12
    
    # Load signing certificate
    signer = Signer.load(
        certificate=open('csd/xiqb891116qe4_csd.cer', 'rb').read(),
        key=open('csd/xiqb891116qe4_csd.key', 'rb').read(),
        password=open('csd/xiqb891116qe4_csd.txt', 'r').read()
    )
    
    # create Comprobante
    invoice = cfdi40.Comprobante.nomina(
        emisor=cfdi40.Emisor(
            rfc=signer.rfc,
            nombre=signer.legal_name,
            regimen_fiscal="601"
        ),
        receptor=cfdi40.Receptor(
            rfc='KIJ0906199R1',
            nombre='KIJ, S.A DE C.V.',
            uso_cfdi='G03',
            domicilio_fiscal_receptor="59820",
            regimen_fiscal_receptor="601"
        ),
        lugar_expedicion="56820",
        complemento_nomina=nomina12.Nomina(
            emisor=nomina12.Emisor(
                registro_patronal='Z1234567890'
            ),
            receptor=nomina12.Receptor(
                cuenta_bancaria='0001000200030004',
                curp='XIQB891116MCHZRL72',
                clave_ent_fed='MOR',
                num_empleado='12345678',
                periodicidad_pago='04',
                tipo_contrato='01',
                tipo_regimen='02'
            ),
            percepciones=nomina12.Percepciones(
                percepcion=nomina12.Percepcion(
                    tipo_percepcion='001',
                    clave='001',
                    concepto='SUELDO',
                    importe_gravado=Decimal('1200'),
                    importe_exento=Decimal('400')
                )
            ),
            deducciones=nomina12.Deducciones(
                deduccion=nomina12.Deduccion(
                    tipo_deduccion='002',
                    clave='300',
                    concepto='ISR A CARGO',
                    importe=Decimal('1234.73')
                )
            ),
            tipo_nomina='O',
            fecha_pago=date(2020, 1, 30),
            fecha_final_pago=date(2020, 1, 31),
            fecha_inicial_pago=date(2020, 1, 16),
            num_dias_pagados=Decimal('16.000')
        ),
        serie="A",
        folio="123456"
    )
    invoice.sign(signer)
    invoice = invoice.process()
    

Pago
______________________

.. code-block:: python

    from datetime import date, datetime
    from decimal import Decimal
    
    from satcfdi import Signer
    from satcfdi.create.cfd import cfdi40, pago20
    
    # Load signing certificate
    signer = Signer.load(
        certificate=open('csd/xiqb891116qe4_csd.cer', 'rb').read(),
        key=open('csd/xiqb891116qe4_csd.key', 'rb').read(),
        password=open('csd/xiqb891116qe4_csd.txt', 'r').read()
    )
    
    # create Comprobante
    invoice = cfdi40.Comprobante.pago(
        emisor=cfdi40.Emisor(
            rfc=signer.rfc,
            nombre=signer.legal_name,
            regimen_fiscal="601"
        ),
        receptor=cfdi40.Receptor(
            rfc='KIJ0906199R1',
            nombre='KIJ, S.A DE C.V.',
            uso_cfdi='G03',
            domicilio_fiscal_receptor="59820",
            regimen_fiscal_receptor="601"
        ),
        lugar_expedicion="56820",
        complemento_pago=pago20.Pagos(
            pago=pago20.Pago(
                fecha_pago=datetime(2020, 1, 1),
                forma_de_pago_p='03',
                moneda_p='MXN',
                tipo_cambio_p=1,
                docto_relacionado=pago20.DoctoRelacionado(
                    id_documento='d6042dc8-d525-4e78-8d1b-092c878bd518',
                    imp_pagado=Decimal("100.3"),
                    imp_saldo_ant=Decimal("203.45"),
                    num_parcialidad=3,
                    moneda_dr="MXN",
                    objeto_imp_dr="01"
                )
            )
        ),
        serie="A",
        folio="123456"
    )
    invoice.sign(signer)
    invoice = invoice.process()
    
    

Pago a partir de un Comprobante
__________________________________

.. code-block:: python

    from datetime import datetime
    from satcfdi import Signer, CFDI
    from satcfdi.create.cfd import cfdi40
    
    # Load signing certificate
    signer = Signer.load(
        certificate=open('csd/xiqb891116qe4_csd.cer', 'rb').read(),
        key=open('csd/xiqb891116qe4_csd.key', 'rb').read(),
        password=open('csd/xiqb891116qe4_csd.txt', 'r').read()
    )
    
    # load comprobante
    cfdi = CFDI.from_file('comprobante.xml')
    
    # create Comprobante
    invoice = cfdi40.Comprobante.pago_comprobantes(
        emisor=cfdi40.Emisor(
            rfc=signer.rfc,
            nombre=signer.legal_name,
            regimen_fiscal="601"
        ),
        lugar_expedicion="56820",
        comprobantes=cfdi,
        fecha_pago=datetime.now(),
        forma_pago="03",
        serie="A",
        folio="123456"
    )
    invoice.sign(signer)
    invoice = invoice.process()
    

Addenda
_______________________

.. code-block:: python

    from decimal import Decimal
    from satcfdi import Signer
    from satcfdi.create.addendas import dvz11
    from satcfdi.create.cfd import cfdi40
    
    # Load signing certificate
    signer = Signer.load(
        certificate=open('csd/xiqb891116qe4_csd.cer', 'rb').read(),
        key=open('csd/xiqb891116qe4_csd.key', 'rb').read(),
        password=open('csd/xiqb891116qe4_csd.txt', 'r').read()
    )
    
    # create Comprobante
    invoice = cfdi40.Comprobante(
        emisor=cfdi40.Emisor(
            rfc=signer.rfc,
            nombre=signer.legal_name,
            regimen_fiscal="601"
        ),
        lugar_expedicion="56820",
        receptor=cfdi40.Receptor(
            rfc='KIJ0906199R1',
            nombre='KIJ, S.A DE C.V.',
            uso_cfdi='G03',
            domicilio_fiscal_receptor="59820",
            regimen_fiscal_receptor="601"
        ),
        metodo_pago='PPD',
        serie="A",
        folio="123456",
        conceptos=[
            cfdi40.Concepto(
                clave_prod_serv='84111506',
                cantidad=Decimal('1.00'),
                clave_unidad='E48',
                descripcion='SERVICIOS DE FACTURACION',
                valor_unitario=Decimal('325.30'),
                impuestos=cfdi40.Impuestos(
                    traslados='IVA|Tasa|0.160000',
                    retenciones=['ISR|Tasa|0.100000', 'IVA|Tasa|0.106667'],
                ),
                _traslados_incluidos=False
            )
        ],
        addenda=dvz11.Diverza(
            generales=dvz11.Generales(
                tipo_documento="Factura"
            )
        )
    )
    invoice.sign(signer)
    invoice = invoice.process()
