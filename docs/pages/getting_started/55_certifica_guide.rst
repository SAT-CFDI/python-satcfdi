Certifica
================================================

Solicitud de Certificado
________________________________

.. code-block:: python

    from satcfdi import Signer
    from satcfdi.certifica import Certifica
    
    # Load Fiel
    fiel = Signer.load(
        certificate=open('csd/xiqb891116qe4.cer', 'rb').read(),
        key=open('csd/xiqb891116qe4.key', 'rb').read(),
        password=open('csd/xiqb891116qe4.txt', 'r').read()
    )
    
    certifica = Certifica(fiel)
    
    certifica.solicitud_certificado(
        sucursal="MiSucursal",
        password="IsTHisSecure!32?",
        dirname=None
    )
