.. image:: https://img.shields.io/badge/source-SAT--CFDI/python--satcfdi-blue?logo=github&style=flat
    :target: https://github.com/SAT-CFDI/python-satcfdi
    :alt: Source

.. image:: https://readthedocs.org/projects/satcfdi/badge/?version=latest
    :target: https://satcfdi.readthedocs.io/?badge=latest
    :alt: Documentation Status

.. image:: https://github.com/SAT-CFDI/python-satcfdi/actions/workflows/python-3.10.yml/badge.svg
    :target: https://github.com/SAT-CFDI/python-satcfdi/actions/workflows/python-3.10.yml
    :alt: Python 3.10

.. image:: https://github.com/SAT-CFDI/python-satcfdi/actions/workflows/python-3.11.yml/badge.svg
    :target: https://github.com/SAT-CFDI/python-satcfdi/actions/workflows/python-3.11.yml
    :alt: Python 3.11

.. image:: https://github.com/SAT-CFDI/python-satcfdi/actions/workflows/codeql.yml/badge.svg
    :target: https://github.com/SAT-CFDI/python-satcfdi/actions/workflows/codeql.yml
    :alt: CodeQL

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

SAT-CFDI
==========================

The best open-source python library to generate and process SAT's CFDI

Documentation and User Guide available
____________________________________________________________________________________

`SAT-CFDI Read the Docs <https://satcfdi.readthedocs.io/>`_

Supported Features
____________________

* Crear CFDI - Ingreso, Nomina, Pagos, Traslados, Retenciones
* Representación Impresa PDF y HTML
* Facturación con PAC's
* Descarga Masiva
* Validación de CFDI's
* Listado 69b
* Exportar CFDI's a Excel
* Descarga de Constancia de Situación Fiscal
* DIOT - Declaración Informativa de Operaciones con Terceros
* Certifica - Generación de certificados
* PLD (Prevención de Lavado de Dinero)

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


Quick Example
____________________

.. code-block:: python

    from decimal import Decimal
    from satcfdi import Signer
    from satcfdi.create.cfd import cfdi40
    from satcfdi.create import Issuer
    
    # Load signing certificate
    signer = Signer.load(
        certificate=open('csd/xiqb891116qe4_csd.cer', 'rb').read(),
        key=open('csd/xiqb891116qe4_csd.key', 'rb').read(),
        password=open('csd/xiqb891116qe4_csd.txt', 'r').read()
    )
    
    # create an Emisor
    emisor = Issuer(signer=signer, tax_system="606")
    
    # create Comprobante
    invoice = cfdi40.Comprobante(
        emisor=emisor,
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
                valor_unitario=Decimal('1250.30'),
                traslados='IVA|Tasa|0.160000',
                retenciones=['ISR|Tasa|0.100000', 'IVA|Tasa|0.106667'],
                _traslados_incluidos=False
            )
        ]
    ).process()
    
    # XML
    invoice.xml_write("my_invoice.xml")
    
    # HTML
    invoice.html_write("my_invoice.html")
    
    # PDF
    invoice.pdf_write("my_invoice.pdf")
    


Contributing
____________________

We value feedback and contributions from our community.
