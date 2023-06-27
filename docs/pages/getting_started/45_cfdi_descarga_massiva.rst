Descarga Masiva
================================================

Descarga CFDIs
___________________

.. code-block:: python

    from datetime import date
    from satcfdi.models import Signer
    from satcfdi.pacs.sat import SAT, TipoDescargaMasivaTerceros
    
    # Load Fiel
    signer = Signer.load(
        certificate=open('csd/xiqb891116qe4.cer', 'rb').read(),
        key=open('csd/xiqb891116qe4.key', 'rb').read(),
        password=open('csd/xiqb891116qe4.txt', 'r').read()
    )
    
    sat_service = SAT(
        signer=signer
    )
    
    # Facturas Recibidas
    for paquete_id, data in sat_service.recover_comprobante_iwait(
            fecha_inicial=date(2020, 1, 1),
            fecha_final=date(2020, 12, 1),
            rfc_receptor=sat_service.signer.rfc,
            tipo_solicitud=TipoDescargaMasivaTerceros.CFDI
    ):
        with open(f"{paquete_id}.zip", "wb") as f:
            f.write(data)
    


Si ya se tiene una solicitud
______________________________

.. code-block:: python

    # Si ya se tiene un id_solicitud
    for paquete_id, data in sat_service.recover_comprobante_iwait(
            id_solicitud='365e2a3d-6f99-4563-856e-28caddc7ad39',
    ):
        with open(f"{paquete_id}.zip", "wb") as f:
            f.write(data)
    
