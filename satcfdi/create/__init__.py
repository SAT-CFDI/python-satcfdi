from ..models import Signer, Certificate


# class Issuer:
#     """
#     Instancia generica de Emisor para usar en la creacion y sellado de comprobantes
#     """
#
#     def __init__(self, tax_system: str, signer: Signer | Certificate = None, legal_name: str = None, rfc: str = None, certificate_number: str = None):
#         """
#         Issuer to issue and stamp CFDIs
#
#         :param signer: Llave y Certificado del Emisor
#         :param legal_name: Legal Name (Razon Social)
#         :param tax_system: Atributo requerido para incorporar la clave del régimen del contribuyente emisor al que aplicará el efecto fiscal de este comprobante.
#         """
#         self.signer = signer if isinstance(signer, Signer) else None
#         self.certificate = signer
#         self.rfc = rfc or signer.rfc
#         self.legal_name = legal_name or signer.legal_name
#         self.tax_system = tax_system
#         self.certificate_number = certificate_number or (signer.certificate_number if signer else "")
