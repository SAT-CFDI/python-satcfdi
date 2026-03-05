Constancia de Situación Fiscal
================================================

Descarga de Constancia
____________________________________

.. code-block:: python

    from satcfdi import csf
    
    res = csf.retrieve("AAA010101AAA", id_cif="012345678")


Descarga de Constancia PDF
____________________________________

.. code-block:: python

    from satcfdi.models import Signer
    from satcfdi.portal import SATPortalConstancia

    # Load Fiel
    signer = Signer.load(
        certificate=open('csd/xiqb891116qe4.cer', 'rb').read(),
        key=open('csd/xiqb891116qe4.key', 'rb').read(),
        password=open('csd/xiqb891116qe4.txt', 'r').read()
    )

    sp = SATPortalConstancia(signer)

    res = sp.generar_constancia()
    with open('constancia.pdf', 'wb') as f:
        f.write(res)