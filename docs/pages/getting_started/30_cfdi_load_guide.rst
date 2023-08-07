Load/Export CFDI
================================================

Loading Existing File
______________________

.. code-block:: python

    from satcfdi.cfdi import CFDI
    
    # from file
    invoice = CFDI.from_file('comprobante.xml')
    
    # from string/bytes
    invoice = CFDI.from_string(open('comprobante.xml', 'rb').read())
    
    

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
    html = render.html_str(invoice)
    # save to file
    render.html_write(invoice, "_comprobante_.html")
    # .. or alternative
    with open("_stream_comprobante_.html", 'w', encoding='utf-8') as f:
        invoice.html_write(f)
    
    # PDF
    pdf = render.pdf_bytes(invoice)
    # save to file
    render.pdf_write(invoice, "_comprobante_.pdf")
    # .. or alternative
    with open("_stream_comprobante_.pdf", 'wb') as f:
        render.pdf_write(invoice, f)
    

