Portal SAT - Factura Electrónica
================================================

Validación
______________________

.. code-block:: python

    from satcfdi.models import Signer
    from satcfdi.portal import SATFacturaElectronica
    
    # Load Fiel
    signer = Signer.load(
        certificate=open('csd/xiqb891116qe4.cer', 'rb').read(),
        key=open('csd/xiqb891116qe4.key', 'rb').read(),
        password=open('csd/xiqb891116qe4.txt', 'r').read()
    )
    
    sat_session = SATFacturaElectronica(signer)
    sat_session.login()
    
    
    # Validación RFC
    res = sat_session.rfc_valid(
        rfc='XIQB891116QE4'
    )
    print(res)
    
    # Validación Razón Social
    res = sat_session.legal_name_valid(
        rfc='XIQB891116QE4',
        legal_name='KIJ, S.A DE C.V.'
    )
    print(res)
    
    # LCO Detalles
    res = sat_session.lco_details(rfc="XIQB891116QE4")
    print(res)
    

