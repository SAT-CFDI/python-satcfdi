Load/Export CFDI
================================================

Loading Existing File
______________________

.. code-block:: python

    from satcfdi import CFDI
    
    # from file
    cfdi = CFDI.from_file('comprobante.xml')
    
    # from string/bytes
    cfdi = CFDI.from_string(open('comprobante.xml', 'rb').read())

Export It
______________________

.. code-block:: python

    # JSON
    json = invoice.json_str()
    # save to file
    invoice.json_write("_comprobante_.json")
    # .. or alternative
    with open("_stream_comprobante_.json", 'w', encoding='utf-8') as f:
        invoice.json_write(f)
    
    # XML
    xml = invoice.xml_bytes()
    # save to file
    invoice.xml_write("_comprobante_.xml")
    # .. or alternative
    with open("_stream_comprobante_.xml", 'wb') as f:
        invoice.xml_write(f)
    
    # HTML
    html = invoice.html_str()
    # save to file
    invoice.html_write("_comprobante_.html")
    # .. or alternative
    with open("_stream_comprobante_.html", 'w', encoding='utf-8') as f:
        invoice.html_write(f)
    
    # PDF
    pdf = invoice.pdf_bytes()
    # save to file
    invoice.pdf_write("_comprobante_.pdf")
    # .. or alternative
    with open("_stream_comprobante_.pdf", 'wb') as f:
        invoice.pdf_write(f)
