"""detallista http://www.sat.gob.mx/detallista"""
from decimal import Decimal
from datetime import datetime, date, time
from collections.abc import Sequence
from ...cfdi import CFDI
from ...xelement import XElement
from ...utils import ScalarMap


class TotalAllowanceCharge(ScalarMap):
    """
    Nodo opcional que especifica el monto total de cargos o descuentos
    
    :param allowance_or_charge_type: Atributo para especificar los cargos o descuentos consolidados
    :param special_services_type: Nodo opcional que especifica el tipo de descuento o cargo. Este atributo sólo se utiliza si el comprador conoce el tipo de descuento o cargo.
    :param amount: Nodo opcional que especifica el monto total de los cargos o descuentos
    """
    
    def __init__(
            self,
            allowance_or_charge_type: str,
            special_services_type: str = None,
            amount: Decimal | int = None,
    ): 
        super().__init__({
            'AllowanceOrChargeType': allowance_or_charge_type,
            'SpecialServicesType': special_services_type,
            'Amount': amount,
        })
        

class TotalAmount(ScalarMap):
    """
    Nodo opcional que especifica el monto total de las líneas de artículos.
    
    :param amount: Nodo requerido que especifica el monto
    """
    
    def __init__(
            self,
            amount: Decimal | int,
    ): 
        super().__init__({
            'Amount': amount,
        })
        

class TradeItemTaxAmount(ScalarMap):
    """
    Nodo opcional que especifica el importe o porcentaje del descuento
    
    :param tax_percentage: Nodo requerido que especifica el porcentaje del impuesto
    :param tax_amount: Nodo requerido que especifica el monto del impuesto
    """
    
    def __init__(
            self,
            tax_percentage: Decimal | int,
            tax_amount: Decimal | int,
    ): 
        super().__init__({
            'TaxPercentage': tax_percentage,
            'TaxAmount': tax_amount,
        })
        

class TradeItemTaxInformation(ScalarMap):
    """
    Nodo opcional que especifica los impuestos por cada línea de artículo
    
    :param tax_type_description: Nodo requerido que especifica el tipo de arancel, impuesto o cuota.
    :param reference_number: Nodo opcional que especifica el numero de identificación del impuesto. Numero asignado al comprador por una jurisdicción de impuesto
    :param trade_item_tax_amount: Nodo opcional que especifica el importe o porcentaje del descuento
    :param tax_category: Nodo opcional que especifica el identificador de impuesto retenido o transferido
    """
    
    def __init__(
            self,
            tax_type_description: str,
            reference_number: str = None,
            trade_item_tax_amount: TradeItemTaxAmount | dict = None,
            tax_category: str = None,
    ): 
        super().__init__({
            'TaxTypeDescription': tax_type_description,
            'ReferenceNumber': reference_number,
            'TradeItemTaxAmount': trade_item_tax_amount,
            'TaxCategory': tax_category,
        })
        

class RatePerUnit(ScalarMap):
    """
    Nodo opcional que especifica la Tarifa por unidad
    
    :param amount_per_unit: Nodo requerido que especifica el importe monetario del cargo o descuento por unidad
    """
    
    def __init__(
            self,
            amount_per_unit: str,
    ): 
        super().__init__({
            'AmountPerUnit': amount_per_unit,
        })
        

class MonetaryAmountOrPercentage(ScalarMap):
    """
    Nodo requerido que especifica la cantidad monetaria o descuento por linea de articulo
    
    :param percentage_per_unit: Nodo requerido que especifica el porcentaje del cargo o descuento
    :param rate_per_unit: Nodo opcional que especifica la Tarifa por unidad
    """
    
    def __init__(
            self,
            percentage_per_unit: str,
            rate_per_unit: RatePerUnit | dict = None,
    ): 
        super().__init__({
            'PercentagePerUnit': percentage_per_unit,
            'RatePerUnit': rate_per_unit,
        })
        

class AllowanceCharge(ScalarMap):
    """
    Nodo opcional que especifica la información de los cargos o descuentos globales por línea de artículo
    
    :param allowance_charge_type: Atributo para especificar el cargo o descuento
    :param monetary_amount_or_percentage: Nodo requerido que especifica la cantidad monetaria o descuento por linea de articulo
    :param settlement_type: Atributo para especificar la imputación del cargo o descuento
    :param sequence_number: Atributo para especificar la secuencia de cálculo
    :param special_services_type: Nodo opcional que especifica el tipo de descuento o cargo. Este atributo sólo se utiliza si el comprador conoce el tipo de descuento o cargo.
    """
    
    def __init__(
            self,
            allowance_charge_type: str,
            monetary_amount_or_percentage: MonetaryAmountOrPercentage | dict,
            settlement_type: str = None,
            sequence_number: str = None,
            special_services_type: str = None,
    ): 
        super().__init__({
            'AllowanceChargeType': allowance_charge_type,
            'MonetaryAmountOrPercentage': monetary_amount_or_percentage,
            'SettlementType': settlement_type,
            'SequenceNumber': sequence_number,
            'SpecialServicesType': special_services_type,
        })
        

class LotNumber(ScalarMap):
    """
    Nodo requerido que especifica el No. De lote
    
    :param _text: 
    :param production_date: Atributo para especificar la fecha de producción
    """
    
    def __init__(
            self,
            _text: str,
            production_date: date = None,
    ): 
        super().__init__({
            '_text': _text,
            'ProductionDate': production_date,
        })
        

class Transport(ScalarMap):
    """
    Nodo requerido que especifica el pago de transporte de embalaje
    
    :param method_of_payment: Nodo requerido que especifica el metodo de pago
    """
    
    def __init__(
            self,
            method_of_payment: str,
    ): 
        super().__init__({
            'MethodOfPayment': method_of_payment,
        })
        

class Description(ScalarMap):
    """
    Nodo requerido que especifica la descripción del empaquetado
    
    :param _text: 
    :param type: Atributo para especificar el tipo de empaquetado
    """
    
    def __init__(
            self,
            _text: str,
            type: str,
    ): 
        super().__init__({
            '_text': _text,
            'Type': type,
        })
        

class PalletInformation(ScalarMap):
    """
    Nodo opcional que especifica la información de empaquetado
    
    :param pallet_quantity: Nodo requerido que especifica el numero de paquetes
    :param description: Nodo requerido que especifica la descripción del empaquetado
    :param transport: Nodo requerido que especifica el pago de transporte de embalaje
    """
    
    def __init__(
            self,
            pallet_quantity: str,
            description: Description | dict,
            transport: Transport | dict,
    ): 
        super().__init__({
            'PalletQuantity': pallet_quantity,
            'Description': description,
            'Transport': transport,
        })
        

class SerialShippingContainerCode(ScalarMap):
    """
    Nodo requerido que especifica la información de Rangos de identificación de productos
    
    :param _text: 
    :param type: Atributo para especificar el codigo del numero de identidad
    """
    
    def __init__(
            self,
            _text: str,
            type: str,
    ): 
        super().__init__({
            '_text': _text,
            'Type': type,
        })
        

class LogisticUnits(ScalarMap):
    """
    Nodo opcional que especifica la información de identificación logística
    
    :param serial_shipping_container_code: Nodo requerido que especifica la información de Rangos de identificación de productos
    """
    
    def __init__(
            self,
            serial_shipping_container_code: SerialShippingContainerCode | dict,
    ): 
        super().__init__({
            'SerialShippingContainerCode': serial_shipping_container_code,
        })
        

class NameAndAddress(ScalarMap):
    """
    Nodo requerido que especifica la etiqueta padre que indica que se empezará a definir el nombre y dirección de la ubicación donde esta la aduana
    
    :param name: Nodo requerido que especifica el nombre de la Aduana
    """
    
    def __init__(
            self,
            name: str,
    ): 
        super().__init__({
            'Name': name,
        })
        

class AlternatePartyIdentification(ScalarMap):
    """
    Nodo requerido que especifica la identificación del no. pedimento a nivel detalle
    
    :param _text: 
    :param type: Atributo para especificar el codigo de identificación secundaria
    """
    
    def __init__(
            self,
            _text: str,
            type: str,
    ): 
        super().__init__({
            '_text': _text,
            'Type': type,
        })
        

class Customs(ScalarMap):
    """
    Nodo opcional que especifica la ubicación donde se especifica el identificador de la aduana
    
    :param alternate_party_identification: Nodo requerido que especifica la identificación del no. pedimento a nivel detalle
    :param reference_date: Nodo requerido que especifica la fecha del pedimento YYYYMMDD
    :param name_and_address: Nodo requerido que especifica la etiqueta padre que indica que se empezará a definir el nombre y dirección de la ubicación donde esta la aduana
    :param gln: Nodo opcional que especifica el número global de localización (GLN) de la aduana
    """
    
    def __init__(
            self,
            alternate_party_identification: AlternatePartyIdentification | dict,
            reference_date: date,
            name_and_address: NameAndAddress | dict,
            gln: str = None,
    ): 
        super().__init__({
            'AlternatePartyIdentification': alternate_party_identification,
            'ReferenceDate': reference_date,
            'NameAndAddress': name_and_address,
            'Gln': gln,
        })
        

class ReferenceIdentification(ScalarMap):
    """
    Nodo opcional que especifica la referencia adicional de los productos
    
    :param _text: 
    :param type: Atributo para especificar el tipo de referencia
    """
    
    def __init__(
            self,
            _text: str,
            type: str,
    ): 
        super().__init__({
            '_text': _text,
            'Type': type,
        })
        

class AdditionalInformation(ScalarMap):
    """
    Nodo opcional que especifica la información adicional de referencia en el detalle de productos
    
    :param reference_identification: Nodo opcional que especifica la referencia adicional de los productos
    """
    
    def __init__(
            self,
            reference_identification: ReferenceIdentification | dict = None,
    ): 
        super().__init__({
            'ReferenceIdentification': reference_identification,
        })
        

class NetPrice(ScalarMap):
    """
    Nodo opcional que especifica la declaración del precion neto
    
    :param amount: Nodo requerido que especifica el precio neto de cada artículo
    """
    
    def __init__(
            self,
            amount: Decimal | int,
    ): 
        super().__init__({
            'Amount': amount,
        })
        

class GrossPrice(ScalarMap):
    """
    Nodo opcional que especifica la declaración del precio bruto
    
    :param amount: Nodo requerido que especifica el precio Bruto del artículo sin incluir descuento ni cargos
    """
    
    def __init__(
            self,
            amount: Decimal | int,
    ): 
        super().__init__({
            'Amount': amount,
        })
        

class AditionalQuantity(ScalarMap):
    """
    Nodo opcional que especifica la cantidad que se esta declarando como adicional
    
    :param _text: 
    :param quantity_type: Atributo para especificar el codigo de tipo de cantidad adicional declarada
    """
    
    def __init__(
            self,
            _text: Decimal | int,
            quantity_type: str,
    ): 
        super().__init__({
            '_text': _text,
            'QuantityType': quantity_type,
        })
        

class TradeItemDescriptionInformation(ScalarMap):
    """
    Nodo opcional que especifica el inicio de la descripción del artículo
    
    :param long_text: Nodo requerido que especifica la descripción del artículo solicitado
    :param language: Atributo para especificar el codigo del idioma en que esta la descripción del articulo
    """
    
    def __init__(
            self,
            long_text: str,
            language: str = None,
    ): 
        super().__init__({
            'LongText': long_text,
            'Language': language,
        })
        

class AlternateTradeItemIdentification(ScalarMap):
    """
    Nodo opcional que especifica el numero de identificación adicional para el artículo.
    
    :param _text: 
    :param type: Atributo para especificar el tipo de identificación adicional, en caso de no utilizar condigo GTIN
    """
    
    def __init__(
            self,
            _text: str,
            type: str,
    ): 
        super().__init__({
            '_text': _text,
            'Type': type,
        })
        

class GrossAmount(ScalarMap):
    """
    Nodo opcional que especifica el importe bruto
    
    :param amount: Nodo requerido que especifica el importe bruto de la línea de artículo
    """
    
    def __init__(
            self,
            amount: Decimal | int,
    ): 
        super().__init__({
            'Amount': amount,
        })
        

class NetAmount(ScalarMap):
    """
    Nodo requerido que especifica el importe neto
    
    :param amount: Nodo requerido que especifica el importe neto de la línea de artículo
    """
    
    def __init__(
            self,
            amount: Decimal | int,
    ): 
        super().__init__({
            'Amount': amount,
        })
        

class TotalLineAmount(ScalarMap):
    """
    Nodo requerido que especifica los importes monetarios por línea de articulo
    
    :param net_amount: Nodo requerido que especifica el importe neto
    :param gross_amount: Nodo opcional que especifica el importe bruto
    """
    
    def __init__(
            self,
            net_amount: NetAmount | dict,
            gross_amount: GrossAmount | dict = None,
    ): 
        super().__init__({
            'NetAmount': net_amount,
            'GrossAmount': gross_amount,
        })
        

class InvoicedQuantity(ScalarMap):
    """
    Nodo requerido que especifica la cantidad facturada del producto en la línea de articulo actual
    
    :param _text: 
    :param unit_of_measure: Atributo para especificar la unidad de medida, solo si el articulo es de unidad variable
    """
    
    def __init__(
            self,
            _text: Decimal | int,
            unit_of_measure: str,
    ): 
        super().__init__({
            '_text': _text,
            'UnitOfMeasure': unit_of_measure,
        })
        

class TradeItemIdentification(ScalarMap):
    """
    Nodo requerido que especifica la identificación de cada artículo
    
    :param gtin: Nodo requerido que especifica el código EAN del artículo solicitado
    """
    
    def __init__(
            self,
            gtin: str,
    ): 
        super().__init__({
            'Gtin': gtin,
        })
        

class LineItem(ScalarMap):
    """
    Nodo opcional que especifica la linea de detalle de la factura
    
    :param trade_item_identification: Nodo requerido que especifica la identificación de cada artículo
    :param invoiced_quantity: Nodo requerido que especifica la cantidad facturada del producto en la línea de articulo actual
    :param total_line_amount: Nodo requerido que especifica los importes monetarios por línea de articulo
    :param type: Atributo para especificar el tipo de línea de detalle
    :param number: Atributo para especificar el numero secuencial que se asigna a cada línea de detalle
    :param alternate_trade_item_identification: Nodo opcional que especifica el numero de identificación adicional para el artículo.
    :param trade_item_description_information: Nodo opcional que especifica el inicio de la descripción del artículo
    :param aditional_quantity: Nodo opcional que especifica la cantidad que se esta declarando como adicional
    :param gross_price: Nodo opcional que especifica la declaración del precio bruto
    :param net_price: Nodo opcional que especifica la declaración del precion neto
    :param additional_information: Nodo opcional que especifica la información adicional de referencia en el detalle de productos
    :param customs: Nodo opcional que especifica la ubicación donde se especifica el identificador de la aduana
    :param logistic_units: Nodo opcional que especifica la información de identificación logística
    :param pallet_information: Nodo opcional que especifica la información de empaquetado
    :param extended_attributes: Nodo opcional que especifica la información adicional de lote del producto facturado
    :param allowance_charge: Nodo opcional que especifica la información de los cargos o descuentos globales por línea de artículo
    :param trade_item_tax_information: Nodo opcional que especifica los impuestos por cada línea de artículo
    """
    
    def __init__(
            self,
            trade_item_identification: TradeItemIdentification | dict,
            invoiced_quantity: InvoicedQuantity | dict,
            total_line_amount: TotalLineAmount | dict,
            type: str = None,
            number: int = None,
            alternate_trade_item_identification: AlternateTradeItemIdentification | dict | Sequence[AlternateTradeItemIdentification | dict] = None,
            trade_item_description_information: TradeItemDescriptionInformation | dict = None,
            aditional_quantity: AditionalQuantity | dict | Sequence[AditionalQuantity | dict] = None,
            gross_price: GrossPrice | dict = None,
            net_price: NetPrice | dict = None,
            additional_information: AdditionalInformation | dict = None,
            customs: Customs | dict | Sequence[Customs | dict] = None,
            logistic_units: LogisticUnits | dict = None,
            pallet_information: PalletInformation | dict = None,
            extended_attributes: LotNumber | dict | Sequence[LotNumber | dict] = None,
            allowance_charge: AllowanceCharge | dict | Sequence[AllowanceCharge | dict] = None,
            trade_item_tax_information: TradeItemTaxInformation | dict | Sequence[TradeItemTaxInformation | dict] = None,
    ): 
        super().__init__({
            'TradeItemIdentification': trade_item_identification,
            'InvoicedQuantity': invoiced_quantity,
            'TotalLineAmount': total_line_amount,
            'Type': type,
            'Number': number,
            'AlternateTradeItemIdentification': alternate_trade_item_identification,
            'TradeItemDescriptionInformation': trade_item_description_information,
            'AditionalQuantity': aditional_quantity,
            'GrossPrice': gross_price,
            'NetPrice': net_price,
            'AdditionalInformation': additional_information,
            'Customs': customs,
            'LogisticUnits': logistic_units,
            'PalletInformation': pallet_information,
            'ExtendedAttributes': extended_attributes,
            'AllowanceCharge': allowance_charge,
            'TradeItemTaxInformation': trade_item_tax_information,
        })
        

class Rate(ScalarMap):
    """
    Nodo opcional que especifica la tarifa
    
    :param base: Atributo para especificar la base del porcentaje que se aplicara
    :param percentage: Nodo opcional que especifica el porcentaje de descuento que se está aplicando según se ha indicado en el campo anterior a toda la factura
    """
    
    def __init__(
            self,
            base: str,
            percentage: Decimal | int,
    ): 
        super().__init__({
            'Base': base,
            'Percentage': percentage,
        })
        

class ShipmentDetail(ScalarMap):
    """
    Nodo opcional que especifica la información pertinente para el embarque de la mercancía.
    
    """
    
    def __init__(
            self,
    ): 
        super().__init__({
        })
        

class DiscountPayment(ScalarMap):
    """
    Nodo opcional que especifica los descuentos por pago
    
    :param discount_type: Atributo para especificar el calificador de porcentajes
    :param percentage: Nodo requerido que especifica el valor de los porcentajes que serán descontados o cargados si la factura no se paga dentro del término. El porcentaje será en base al valor de la factura
    """
    
    def __init__(
            self,
            discount_type: str,
            percentage: str,
    ): 
        super().__init__({
            'DiscountType': discount_type,
            'Percentage': percentage,
        })
        

class TimePeriodDue(ScalarMap):
    """
    Nodo requerido que especifica el tiempo de pago
    
    :param time_period: Atributo para especificar el tipo de periodo
    :param value: Nodo requerido que especifica el numero de periodos
    """
    
    def __init__(
            self,
            time_period: str,
            value: str,
    ): 
        super().__init__({
            'TimePeriod': time_period,
            'Value': value,
        })
        

class PaymentTimePeriod(ScalarMap):
    """
    Nodo opcional que especifica el periodo de pago de la factura
    
    :param time_period_due: Nodo requerido que especifica el tiempo de pago
    """
    
    def __init__(
            self,
            time_period_due: TimePeriodDue | dict,
    ): 
        super().__init__({
            'TimePeriodDue': time_period_due,
        })
        

class NetPayment(ScalarMap):
    """
    Nodo opcional que especifica las condiciones de pago
    
    :param net_payment_terms_type: Atributo para especificar las condiciones de pago
    :param payment_time_period: Nodo opcional que especifica el periodo de pago de la factura
    """
    
    def __init__(
            self,
            net_payment_terms_type: str,
            payment_time_period: PaymentTimePeriod | dict = None,
    ): 
        super().__init__({
            'NetPaymentTermsType': net_payment_terms_type,
            'PaymentTimePeriod': payment_time_period,
        })
        

class PaymentTerms(ScalarMap):
    """
    Nodo opcional que especifica los términos de pago de la factura
    
    :param payment_terms_event: Atributo para especificar la referencia del tiempo de pago
    :param payment_terms_relation_time: Atributo para especificar el termino de relación del tiempo de pago
    :param net_payment: Nodo opcional que especifica las condiciones de pago
    :param discount_payment: Nodo opcional que especifica los descuentos por pago
    """
    
    def __init__(
            self,
            payment_terms_event: str = None,
            payment_terms_relation_time: str = None,
            net_payment: NetPayment | dict = None,
            discount_payment: DiscountPayment | dict = None,
    ): 
        super().__init__({
            'PaymentTermsEvent': payment_terms_event,
            'PaymentTermsRelationTime': payment_terms_relation_time,
            'NetPayment': net_payment,
            'DiscountPayment': discount_payment,
        })
        

class Currency(ScalarMap):
    """
    Nodo opcional que especifica el tipo de divisa utilizada, para efectos de comprobantes fiscales digitales emitidos UNICAMENTE se podrá utilizar como divisa la moneda nacional (MXN), sin embargo dentro del complemento se podrá detallar en otra de forma informativa. Lo detallado en esta etiqueta deberá coincidir con lo declarado en las etiquetas del SAT considerando el tipo de cambio.
    
    :param currency_isocode: Atributo para especificar el codigo de la moneda utilizada para detallar la relación de facturas.Todas las cantidades posteriores seran expresadas en la divisa detallada en esta etiqueta
    :param currency_function: Nodo requerido que especifica la función de divisa
    :param rate_of_change: Nodo opcional que especifical la tasa de cambio que se aplica a las monedas. La regla general para calcular la tasa de cambio es la siguiente: Divisa de Referencia multiplicada por la Tasa = Divisa Objetivo
    """
    
    def __init__(
            self,
            currency_isocode: str,
            currency_function: str | Sequence[str],
            rate_of_change: Decimal | int = None,
    ): 
        super().__init__({
            'CurrencyISOCode': currency_isocode,
            'CurrencyFunction': currency_function,
            'RateOfChange': rate_of_change,
        })
        

class InvoiceCreator(ScalarMap):
    """
    Nodo opcional que especifica la ubicación donde se especifica el identificador del emisor de la factura si es distinto del identificador del proveedor.
    
    :param gln: Nodo opcional que especifica el número global de localización (GLN)de la ubicación del emisor de la factura
    :param alternate_party_identification: Nodo opcional que especifica la identificación secundaria del emisor de la factura
    :param name_and_address:
    """
    
    def __init__(
            self,
            gln: str = None,
            alternate_party_identification: AlternatePartyIdentification | dict = None,
            name_and_address: NameAndAddress | dict = None,
    ): 
        super().__init__({
            'Gln': gln,
            'AlternatePartyIdentification': alternate_party_identification,
            'NameAndAddress': name_and_address,
        })
        

class ShipTo(ScalarMap):
    """
    Nodo opcional que especifica la ubicación donde debe realizarse la entrega de la mercancía.
    
    :param gln: Nodo opcional que especifica el número global de localización (GLN) de la ubicación a entregar la mercancía
    :param name_and_address: Nodo opcional que especifica el nombre y dirección de la ubicación donde debe realizarse la entrega de mercancía
    """
    
    def __init__(
            self,
            gln: str = None,
            name_and_address: NameAndAddress | dict = None,
    ): 
        super().__init__({
            'Gln': gln,
            'NameAndAddress': name_and_address,
        })
        

class Seller(ScalarMap):
    """
    Nodo opcional que especifica información del vendedor
    
    :param gln: Nodo requerido que especifica el número global de localización (GLN) del vendedor.
    :param alternate_party_identification: Nodo requerido que especifica el código para identificar qué tipo de identificación secundaria se le asignó al proveedor
    """
    
    def __init__(
            self,
            gln: str,
            alternate_party_identification: AlternatePartyIdentification | dict,
    ): 
        super().__init__({
            'Gln': gln,
            'AlternatePartyIdentification': alternate_party_identification,
        })
        

class DeliveryNote(ScalarMap):
    """
    Nodo opcional donde se especifica información de recepción de mercancia.Información emitida por el comprador cuando recibe la mercancía que es facturada
    
    :param reference_identification: Nodo requerido que especifica el numero de folio. Número emitido por el comprador cuando recibe la mercancía que es facturada
    :param reference_date: Nodo opcional que especifica la fecha en que fue asignado el no. de folio de recibo
    """
    
    def __init__(
            self,
            reference_identification: str | Sequence[str],
            reference_date: date = None,
    ): 
        super().__init__({
            'ReferenceIdentification': reference_identification,
            'ReferenceDate': reference_date,
        })
        

class SpecialInstruction(ScalarMap):
    """
    Nodo opcional que especifica que tipo de instrucciones comerciales son enviadas
    
    :param code: Atributo para especificar el codigo del tipo de instrucciones comerciales que son enviadas
    :param text: Nodo requerido que especifica información de texto que aplica a todo el mensaje de la factura. La información estará en función al código del tema de texto
    """
    
    def __init__(
            self,
            code: str,
            text: str | Sequence[str],
    ): 
        super().__init__({
            'Code': code,
            'Text': text,
        })
        

class PersonOrDepartmentName(ScalarMap):
    """
    Etiqueta que especifica el contacto de compras
    
    :param text: Contacto de Nodo requerido que especifica el contacto de compras
    """
    
    def __init__(
            self,
            text: str,
    ): 
        super().__init__({
            'Text': text,
        })
        

class ContactInformation(ScalarMap):
    """
    Nodo requerido que especifica información del contacto de compras
    
    :param person_or_department_name: Etiqueta que especifica el contacto de compras
    """
    
    def __init__(
            self,
            person_or_department_name: PersonOrDepartmentName | dict,
    ): 
        super().__init__({
            'PersonOrDepartmentName': person_or_department_name,
        })
        

class Buyer(ScalarMap):
    """
    Nodo requerido que especifica información del comprador
    
    :param gln: Nodo requerido que especifica el número global de localización (GLN) del comprador.
    :param contact_information: Nodo requerido que especifica información del contacto de compras
    """
    
    def __init__(
            self,
            gln: str,
            contact_information: ContactInformation | dict = None,
    ): 
        super().__init__({
            'Gln': gln,
            'ContactInformation': contact_information,
        })
        

class OrderIdentification(ScalarMap):
    """
    Nodo requerido que especifica información sobre la orden de compra a la que hace referencia la factura
    
    :param reference_identification: Nodo requerido que especifica el número de orden de compra (comprador) a la que hace referencia la factura
    :param reference_date: Nodo opcional que especifica la fecha de la orden de compra(comprador) a la que hace referencia la factura
    """
    
    def __init__(
            self,
            reference_identification: ReferenceIdentification | dict | Sequence[ReferenceIdentification | dict],
            reference_date: date = None,
    ): 
        super().__init__({
            'ReferenceIdentification': reference_identification,
            'ReferenceDate': reference_date,
        })
        

class RequestForPaymentIdentification(ScalarMap):
    """
    Nodo requerido que especifica la transacción a utilizar
    
    :param entity_type: Nodo requerido que especifica el tipo de transacción
    """
    
    def __init__(
            self,
            entity_type: str,
    ): 
        super().__init__({
            'EntityType': entity_type,
        })
        

class Detallista(CFDI):
    """
    Complemento requerido para la emision y recepcion de comprobantes fiscales digitales en el sector Retail
    
    :param document_status: Función del mensaje
    :param request_for_payment_identification: Nodo requerido que especifica la transacción a utilizar
    :param order_identification: Nodo requerido que especifica información sobre la orden de compra a la que hace referencia la factura
    :param additional_information: Nodo requerido que especifica las referencias adicionales a nivel global de la factura
    :param buyer: Nodo requerido que especifica información del comprador
    :param type: Tipo de transacción bajo estandar del sector detallista
    :param content_version: Versión del estandar XML utilizado para la elaboración de la guia del sector detallista
    :param special_instruction: Nodo opcional que especifica que tipo de instrucciones comerciales son enviadas
    :param delivery_note: Nodo opcional donde se especifica información de recepción de mercancia.Información emitida por el comprador cuando recibe la mercancía que es facturada
    :param seller: Nodo opcional que especifica información del vendedor
    :param ship_to: Nodo opcional que especifica la ubicación donde debe realizarse la entrega de la mercancía.
    :param invoice_creator: Nodo opcional que especifica la ubicación donde se especifica el identificador del emisor de la factura si es distinto del identificador del proveedor.
    :param customs: Nodo opcional que especifica la ubicación de la aduana
    :param currency: Nodo opcional que especifica el tipo de divisa utilizada, para efectos de comprobantes fiscales digitales emitidos UNICAMENTE se podrá utilizar como divisa la moneda nacional (MXN), sin embargo dentro del complemento se podrá detallar en otra de forma informativa. Lo detallado en esta etiqueta deberá coincidir con lo declarado en las etiquetas del SAT considerando el tipo de cambio.
    :param payment_terms: Nodo opcional que especifica los términos de pago de la factura
    :param shipment_detail: Nodo opcional que especifica la información pertinente para el embarque de la mercancía.
    :param allowance_charge: Nodo opcional que especifica la información de los cargos o descuentos globales mercantiles por factura
    :param line_item: Nodo opcional que especifica la linea de detalle de la factura
    :param total_amount: Nodo opcional que especifica el monto total de las líneas de artículos.
    :param total_allowance_charge: Nodo opcional que especifica el monto total de cargos o descuentos
    """
    
    tag = '{http://www.sat.gob.mx/detallista}detallista'
    document_structure_version = 'AMC8.1'
    
    def __init__(
            self,
            document_status: str,
            request_for_payment_identification: RequestForPaymentIdentification | dict,
            order_identification: OrderIdentification | dict,
            additional_information: ReferenceIdentification | dict | Sequence[ReferenceIdentification | dict],
            buyer: Buyer | dict,
            type: str = None,
            content_version: str = None,
            special_instruction: SpecialInstruction | dict | Sequence[SpecialInstruction | dict] = None,
            delivery_note: DeliveryNote | dict = None,
            seller: Seller | dict = None,
            ship_to: ShipTo | dict = None,
            invoice_creator: InvoiceCreator | dict = None,
            customs: str | Sequence[str] = None,
            currency: Currency | dict | Sequence[Currency | dict] = None,
            payment_terms: PaymentTerms | dict = None,
            shipment_detail: ShipmentDetail | dict = None,
            allowance_charge: AllowanceCharge | dict | Sequence[AllowanceCharge | dict] = None,
            line_item: LineItem | dict | Sequence[LineItem | dict] = None,
            total_amount: TotalAmount | dict = None,
            total_allowance_charge: TotalAllowanceCharge | dict | Sequence[TotalAllowanceCharge | dict] = None,
    ): 
        super().__init__({
            'DocumentStructureVersion': self.document_structure_version,
            'DocumentStatus': document_status,
            'RequestForPaymentIdentification': request_for_payment_identification,
            'OrderIdentification': order_identification,
            'AdditionalInformation': additional_information,
            'Buyer': buyer,
            'Type': type,
            'ContentVersion': content_version,
            'SpecialInstruction': special_instruction,
            'DeliveryNote': delivery_note,
            'Seller': seller,
            'ShipTo': ship_to,
            'InvoiceCreator': invoice_creator,
            'Customs': customs,
            'Currency': currency,
            'PaymentTerms': payment_terms,
            'ShipmentDetail': shipment_detail,
            'AllowanceCharge': allowance_charge,
            'LineItem': line_item,
            'TotalAmount': total_amount,
            'TotalAllowanceCharge': total_allowance_charge,
        })
        

