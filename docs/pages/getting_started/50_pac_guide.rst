Integration with PAC's
================================================

Pick your PAC

.. code-block:: python

    from satcfdi.pacs import Environment, PAC
    
    # Use your preferred PAC to stamp your Comprobante
    pac = PAC(environment=Environment.TEST)  # dummy
    
    # from satcfdi.pacs.diverza import Diverza
    # pac = Diverza(rfc="ABC",id="12345",token="$123456&", environment=Environment.TEST)
    
    # from satcfdi.pacs.prodigia import Prodigia
    # pac = Prodigia(user="1234", password="pass", contrato="1234", environment=Environment.TEST)
    
    # from satcfdi.pacs.comerciodigital import ComercioDigital
    # pac = ComercioDigital(user="1234", password="pass", environment=Environment.TEST)
    
    # from satcfdi.pacs.swsapien import SWSapien
    # pac = SWSapien(token="$1234%", environment=Environment.TEST)
    

Stamp
______________________

.. code-block:: python

    from satcfdi.pacs import Accept
    
    doc = pac.stamp(invoice, accept=Accept.XML_PDF)
    
    with open('_stamped_.xml', 'wb') as f:
        f.write(doc.xml)
    

Recover Comprobantes
______________________

.. code-block:: python

    import datetime
    from satcfdi import Signer
    from satcfdi.pacs.sat import SAT, TipoDescargaMasivaTerceros
    
    # Load fiel
    signer = Signer.load(
        certificate=open('csd/xiqb891116qe4.cer', 'rb').read(),
        key=open('csd/xiqb891116qe4.key', 'rb').read(),
        password=open('csd/xiqb891116qe4.txt', 'r').read()
    )
    
    sat = SAT(
        signer=signer
    )
    
    fecha_final = datetime.date.today()
    fecha_inicial = fecha_final - datetime.timedelta(days=10)
    
    # Recover Comprobantes
    for paquete_id, p in sat.recover_comprobante_iwait(
        # id_solicitud="",
        fecha_inicial=fecha_inicial,
        fecha_final=fecha_final,
        rfc_receptor=sat.signer.rfc,
        tipo_solicitud=TipoDescargaMasivaTerceros.CFDI
    ):
        with open(f"{paquete_id}.zip", "wb") as f:
            f.write(p)
    
    

Status Comprobante
______________________

.. code-block:: python

    from satcfdi import CFDI
    from satcfdi.pacs.sat import SAT
    
    sat = SAT()
    res = sat.status(
        cfdi=CFDI.from_file('comprobante.xml')
    )
    
    print(res)
    

Listado 69B
______________________

.. code-block:: python

    from satcfdi.pacs import TaxpayerStatus
    from satcfdi.pacs.sat import SAT
    
    sat_service = SAT()
    res = sat_service.list_69b('AAL081211JP0')
    assert res == TaxpayerStatus.DEFINITIVO
    