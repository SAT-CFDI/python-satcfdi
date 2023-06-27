.. image:: https://img.shields.io/github/commit-activity/m/SAT-CFDI/python-satcfdi
    :target: https://github.com/badges/SAT-CFDI/python-satcfdi
    :alt: Activity

.. image:: https://readthedocs.org/projects/satcfdi/badge?version=latest
    :target: https://satcfdi.readthedocs.io?badge=latest
    :alt: Documentation Status

.. image:: https://github.com/SAT-CFDI/python-satcfdi/actions/workflows/tests.yml/badge.svg
    :target: https://github.com/SAT-CFDI/python-satcfdi/actions/workflows/tests.yml
    :alt: Tests

.. image:: https://github.com/SAT-CFDI/python-satcfdi/actions/workflows/codeql.yml/badge.svg
    :target: https://github.com/SAT-CFDI/python-satcfdi/actions/workflows/codeql.yml
    :alt: CodeQL

.. image:: https://github.com/SAT-CFDI/python-satcfdi/actions/workflows/publish.yml/badge.svg
    :target: https://github.com/SAT-CFDI/python-satcfdi/actions/workflows/publish.yml
    :alt: Publish

.. image:: https://img.shields.io/github/v/release/SAT-CFDI/python-satcfdi.svg?logo=git&style=flat
    :target: https://github.com/SAT-CFDI/python-satcfdi/releases
    :alt: Releases

.. image:: https://pepy.tech/badge/satcfdi/month
    :target: https://pepy.tech/project/satcfdi
    :alt: Downloads

.. image:: https://img.shields.io/pypi/pyversions/satcfdi.svg
    :target: https://pypi.org/project/satcfdi
    :alt: Supported Versions

.. image:: https://img.shields.io/github/contributors/SAT-CFDI/python-satcfdi.svg
    :target: https://github.com/SAT-CFDI/python-satcfdi/graphs/contributors
    :alt: Contributors

.. image:: https://scrutinizer-ci.com/g/SAT-CFDI/python-satcfdi/badges/quality-score.png?b=main
    :target: https://scrutinizer-ci.com/g/SAT-CFDI/python-satcfdi/?branch=main
    :alt: Scrutinizer Code Quality

.. image:: https://scrutinizer-ci.com/g/SAT-CFDI/python-satcfdi/badges/coverage.png?b=main
    :target: https://scrutinizer-ci.com/g/SAT-CFDI/python-satcfdi/code-structure/main/code-coverage/satcfdi/
    :alt: Code Coverage

.. image:: https://img.shields.io/discord/1045508868807073792?logo=discord&style=flat
    :target: https://discord.gg/6WA9QvZcRn
    :alt: Discord

SAT-CFDI
==========================

The best open-source python library to generate and process SAT's CFDI

Documentation and User Guide available
____________________________________________________________________________________

`SAT-CFDI Read the Docs <https://satcfdi.readthedocs.io>`_

Supported Features
____________________

* CFDI 3.2, 3.3, 4.0 - Ingreso, Nomina, Pagos, Traslados y Complementos
* Retenciones 1.0, 2.0
* Contabilidad Electronica 1.3
* Representación Impresa PDF, HTML, JSON
* Facturación con PAC's

  * Comercio Digital
  * Diverza
  * Prodigia
  * SW Sapien
* Descarga Masiva
* Validación de Comprobantes
* Listado 69B
* Exportar Comprobantes a Excel
* Descarga de Constancia de Situación Fiscal
* Portal SAT - Factura Electrónica

  * Validación de RFC, Razón Social
  * LCO - Lista de Contribuyentes Obligados
* DIOT - Declaración Informativa de Operaciones con Terceros
* Certifica - Solicitud de Certificados, Renovación de Fiel
* PLD - Prevención de Lavado de Dinero


Installation
____________________

Install SAT-CFDI from PyPI with:

.. code-block:: sh

    python -m pip install satcfdi

or install from source with:

.. code-block:: sh

    git clone https://github.com/SAT-CFDI/python-satcfdi
    cd python-satcfdi
    python -m pip install .


Load
____________________

.. code-block:: python

    from satcfdi import CFDI
    
    # from file
    invoice = CFDI.from_file('comprobante.xml')
    
    # from string/bytes
    invoice = CFDI.from_string(open('comprobante.xml', 'rb').read())
    
    

Create
____________________

.. code-block:: python

    from decimal import Decimal
    from satcfdi.models import Signer
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
    

Output
____________________

.. code-block:: python

    # XML
    invoice.xml_write("my_invoice.xml")
    
    # JSON
    invoice.json_write("my_invoice.json", pretty_print=True)
    
    # HTML
    invoice.html_write("my_invoice.html")
    
    # PDF
    invoice.pdf_write("my_invoice.pdf")
    


Contributing
____________________

We value feedback and contributions from our community.

