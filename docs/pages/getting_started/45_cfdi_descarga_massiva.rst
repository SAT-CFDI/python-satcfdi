Descarga Masiva
================================================

Descarga CFDIs Emitidos
___________________

.. code-block:: python

    import base64
    from datetime import date
    from satcfdi.models import Signer
    from satcfdi.pacs.sat import SAT, TipoDescargaMasivaTerceros, EstadoSolicitud
    
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
    response = sat_service.recover_comprobante_emited_request(
        fecha_inicial=date(2020, 1, 1),
        fecha_final=date(2020, 12, 1),
        rfc_receptor=sat_service.signer.rfc,
        tipo_solicitud=TipoDescargaMasivaTerceros.CFDI
    )
    
    # Almacenar el id_solicitud en algún lugar
    id_solicitud = response['IdSolicitud']
    
    # Revisar estado de descarga
    response = sat_service.recover_comprobante_status(id_solicitud)
    
    est = response["EstadoSolicitud"]
    if est == EstadoSolicitud.TERMINADA:
        for id_paquete in response['IdsPaquetes']:
            response, paquete = sat_service.recover_comprobante_download(
                id_paquete=id_paquete
            )
            paquete = base64.b64decode(paquete)
            with open(f"{id_paquete}.zip", "wb") as f:
                f.write(paquete)
    else:
        # volver a intentar más tarde
        pass
    

Descarga CFDIs Recibidos
___________________

.. code-block:: python

    import base64
    from datetime import date
    
    from satcfdi.create.catalogos import EstadoComprobante
    from satcfdi.models import Signer
    from satcfdi.pacs.sat import SAT, TipoDescargaMasivaTerceros, EstadoSolicitud
    
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
    response = sat_service.recover_comprobante_received_request(
        fecha_inicial=date(2020, 1, 1),
        fecha_final=date(2020, 12, 1),
        rfc_receptor=sat_service.signer.rfc,
        tipo_solicitud=TipoDescargaMasivaTerceros.CFDI,
        estado_comprobante=EstadoComprobante.VIGENTE,  # Puedes especificar un estado si es necesario
    )
    
    # Almacenar el id_solicitud en algún lugar
    id_solicitud = response['IdSolicitud']
    
    # Revisar estado de descarga
    response = sat_service.recover_comprobante_status(id_solicitud)
    
    est = response["EstadoSolicitud"]
    if est == EstadoSolicitud.TERMINADA:
        for id_paquete in response['IdsPaquetes']:
            response, paquete = sat_service.recover_comprobante_download(
                id_paquete=id_paquete
            )
            paquete = base64.b64decode(paquete)
            with open(f"{id_paquete}.zip", "wb") as f:
                f.write(paquete)
    else:
        # volver a intentar más tarde
        pass
    

Si ya se tiene una solicitud
______________________________

.. code-block:: python

    # Si ya se tiene un id_solicitud
    for paquete_id, data in sat_service.recover_comprobante_iwait(
            id_solicitud='365e2a3d-6f99-4563-856e-28caddc7ad39',
    ):
        with open(f"{paquete_id}.zip", "wb") as f:
            f.write(data)
    

