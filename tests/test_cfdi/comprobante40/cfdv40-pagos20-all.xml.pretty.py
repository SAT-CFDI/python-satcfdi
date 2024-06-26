{'Certificado': '0.00',
 'CfdiRelacionados': [{'CfdiRelacionado': ['0ba31311-f675-4e0f-958d-2f3f50f7b88b'],
                       'TipoRelacion': Code('09', 'Factura generada por pagos diferidos')}],
 'Complemento': {'Pagos': {'Pago': [{'CadPago': 'CadPago',
                                     'CertPago': 'deadbeef',
                                     'CtaBeneficiario': '1234567890',
                                     'CtaOrdenante': '3456789012',
                                     'DoctoRelacionado': [{'EquivalenciaDR': Decimal('0.000001'),
                                                           'Folio': '0.00',
                                                           'IdDocumento': 'C1DF8D01-8436-4E7D-BECF-20F31624280D',
                                                           'ImpPagado': Decimal('1.00'),
                                                           'ImpSaldoAnt': Decimal('0.00'),
                                                           'ImpSaldoInsoluto': Decimal('1.00'),
                                                           'ImpuestosDR': {'RetencionesDR': {'003|Exento|0.000001': {'BaseDR': Decimal('2.00'),
                                                                                                                     'ImporteDR': Decimal('1.00'),
                                                                                                                     'ImpuestoDR': Code('003', 'IEPS'),
                                                                                                                     'TasaOCuotaDR': Decimal('0.000001'),
                                                                                                                     'TipoFactorDR': Code('Exento', None)}},
                                                                           'TrasladosDR': {'003|Exento|0.000001': {'BaseDR': Decimal('2.00'),
                                                                                                                   'ImporteDR': Decimal('1.00'),
                                                                                                                   'ImpuestoDR': Code('003', 'IEPS'),
                                                                                                                   'TasaOCuotaDR': Decimal('0.000001'),
                                                                                                                   'TipoFactorDR': Code('Exento', None)}}},
                                                           'MonedaDR': Code('ZWL', 'Zimbabwe Dólar'),
                                                           'NumParcialidad': 109,
                                                           'ObjetoImpDR': Code('03', 'Sí objeto del impuesto y no obligado al desglose'),
                                                           'Serie': '0.00'}],
                                     'FechaPago': datetime.datetime(2021, 12, 3, 12, 59),
                                     'FormaDePagoP': Code('99', 'Por definir'),
                                     'ImpuestosP': {'RetencionesP': {'003': {'ImporteP': Decimal('0.00'),
                                                                             'ImpuestoP': Code('003', 'IEPS')}},
                                                    'TrasladosP': {'003|Exento|0.000000': {'BaseP': Decimal('0.00'),
                                                                                           'ImporteP': Decimal('0.00'),
                                                                                           'ImpuestoP': Code('003', 'IEPS'),
                                                                                           'TasaOCuotaP': Decimal('0.00'),
                                                                                           'TipoFactorP': Code('Exento', None)}}},
                                     'MonedaP': Code('ZWL', 'Zimbabwe Dólar'),
                                     'Monto': Decimal('0.00'),
                                     'NomBancoOrdExt': '0.00',
                                     'NumOperacion': '0.00',
                                     'RfcEmisorCtaBen': 'BAS600902KL9',
                                     'RfcEmisorCtaOrd': 'AAA010101AAA',
                                     'SelloPago': 'base64string',
                                     'TipoCadPago': Code('01', 'SPEI'),
                                     'TipoCambioP': Decimal('10.00')}],
                           'Totales': {'MontoTotalPagos': Decimal('0.00'),
                                       'TotalRetencionesIEPS': Decimal('0.00'),
                                       'TotalRetencionesISR': Decimal('0.00'),
                                       'TotalRetencionesIVA': Decimal('0.00'),
                                       'TotalTrasladosBaseIVA0': Decimal('0.00'),
                                       'TotalTrasladosBaseIVA16': Decimal('0.00'),
                                       'TotalTrasladosBaseIVA8': Decimal('0.00'),
                                       'TotalTrasladosBaseIVAExento': Decimal('0.00'),
                                       'TotalTrasladosImpuestoIVA0': Decimal('0.00'),
                                       'TotalTrasladosImpuestoIVA16': Decimal('0.00'),
                                       'TotalTrasladosImpuestoIVA8': Decimal('0.00')},
                           'Version': '2.0'}},
 'Conceptos': [{'Cantidad': Decimal('1'),
                'ClaveProdServ': Code('84111506', 'Servicios de facturación'),
                'ClaveUnidad': Code('ACT', 'Actividad'),
                'Descripcion': 'Pago',
                'Importe': Decimal('0'),
                'ObjetoImp': Code('01', 'No objeto de impuesto'),
                'ValorUnitario': Decimal('0')}],
 'Emisor': {'Nombre': 'Esta es una demostración',
            'RegimenFiscal': Code('622', 'Actividades Agrícolas, Ganaderas, Silvícolas y Pesqueras'),
            'Rfc': ' AAA010101AAA'},
 'Exportacion': Code('03', 'Temporal'),
 'Fecha': datetime.datetime(2021, 12, 8, 23, 59, 59),
 'FormaPago': Code('02', 'Cheque nominativo'),
 'LugarExpedicion': '99999',
 'Moneda': Code('XXX', 'Los códigos asignados para las transacciones en que intervenga ninguna moneda'),
 'NoCertificado': '30001000000300023708',
 'Receptor': {'DomicilioFiscalReceptor': '99999',
              'Nombre': 'Juanito Bananas De la Sierra',
              'RegimenFiscalReceptor': Code('630', 'Enajenación de acciones en bolsa de valores'),
              'Rfc': 'BASJ600902KL9',
              'UsoCFDI': Code('P01', 'Por definir')},
 'Sello': '0.00',
 'SubTotal': Decimal('0'),
 'TipoDeComprobante': Code('P', 'Pago'),
 'Total': Decimal('0'),
 'Version': '4.0'}