from ...utils import ScalarMap
from ...xelement import XElement


class RSAKeyValueType(ScalarMap):
    def __init__(
            self,
            modulus: str,
            exponent: str,
    ):
        """

        :param modulus:
        :param exponent:
        """

        super().__init__({
            'Modulus': modulus,
            'Exponent': exponent,
        })


class DSAKeyValueType(ScalarMap):
    def __init__(
            self,
            p: str,
            q: str,
            y: str,
            seed: str,
            pgen_counter: str,
            g: str = None,
            j: str = None,
    ):
        """

        :param p:
        :param q:
        :param y:
        :param seed:
        :param pgen_counter:
        :param g:
        :param j:
        """

        super().__init__({
            'P': p,
            'Q': q,
            'Y': y,
            'Seed': seed,
            'PgenCounter': pgen_counter,
            'G': g,
            'J': j,
        })


class SignaturePropertyType(ScalarMap):
    def __init__(
            self,
            target: str,
            id: str = None,
    ):
        """

        :param target:
        :param id:
        """

        super().__init__({
            'Target': target,
            'Id': id,
        })


class SignaturePropertiesType(ScalarMap):
    def __init__(
            self,
            signature_property: SignaturePropertyType | dict = None,
            id: str = None,
    ):
        """

        :param signature_property:
        :param id:
        """

        super().__init__({
            'SignatureProperty': signature_property,
            'Id': id,
        })


class ObjectType(ScalarMap):
    def __init__(
            self,
            id: str = None,
            mime_type: str = None,
            encoding: str = None,
    ):
        """

        :param id:
        :param mime_type:
        :param encoding:
        """

        super().__init__({
            'Id': id,
            'MimeType': mime_type,
            'Encoding': encoding,
        })


class SPKIDataType(ScalarMap):
    def __init__(
            self,
            spkisexp: str,
    ):
        """

        :param spkisexp:
        """

        super().__init__({
            'SPKISexp': spkisexp,
        })


class PGPDataType(ScalarMap):
    def __init__(
            self,
            pgpkey_id: str,
            pgpkey_packet: str = None,
    ):
        """

        :param pgpkey_id:
        :param pgpkey_packet:
        """

        super().__init__({
            'PGPKeyID': pgpkey_id,
            'PGPKeyPacket': pgpkey_packet,
        })


class X509IssuerSerialType(ScalarMap):
    def __init__(
            self,
            x509issuer_name: str,
            x509serial_number: int,
    ):
        """

        :param x509issuer_name:
        :param x509serial_number:
        """

        super().__init__({
            'X509IssuerName': x509issuer_name,
            'X509SerialNumber': x509serial_number,
        })


class X509DataType(ScalarMap):
    def __init__(
            self,
            x509issuer_serial: X509IssuerSerialType | dict = None,
            x509ski: str = None,
            x509subject_name: str = None,
            x509certificate: str = None,
            x509crl: str = None,
    ):
        """

        :param x509issuer_serial:
        :param x509ski:
        :param x509subject_name:
        :param x509certificate:
        :param x509crl:
        """

        super().__init__({
            'X509IssuerSerial': x509issuer_serial,
            'X509SKI': x509ski,
            'X509SubjectName': x509subject_name,
            'X509Certificate': x509certificate,
            'X509CRL': x509crl,
        })


class KeyValueType(ScalarMap):
    def __init__(
            self,
            dsakey_value: DSAKeyValueType | dict = None,
            rsakey_value: RSAKeyValueType | dict = None,
    ):
        """

        :param dsakey_value:
        :param rsakey_value:
        """

        super().__init__({
            'DSAKeyValue': dsakey_value,
            'RSAKeyValue': rsakey_value,
        })


class DigestMethodType(ScalarMap):
    def __init__(
            self,
            algorithm: str,
    ):
        """

        :param algorithm:
        """

        super().__init__({
            'Algorithm': algorithm,
        })


class TransformType(ScalarMap):
    def __init__(
            self,
            algorithm: str,
            xpath: str = None,
    ):
        """

        :param algorithm:
        :param xpath:
        """

        super().__init__({
            'Algorithm': algorithm,
            'XPath': xpath,
        })


class TransformsType(ScalarMap):
    def __init__(
            self,
            transform: TransformType | dict = None,
    ):
        """

        :param transform:
        """

        super().__init__({
            'Transform': transform,
        })


class RetrievalMethodType(ScalarMap):
    def __init__(
            self,
            uri: str = None,
            type: str = None,
            transforms: TransformsType | dict = None,
    ):
        """

        :param uri:
        :param type:
        :param transforms:
        """

        super().__init__({
            'URI': uri,
            'Type': type,
            'Transforms': transforms,
        })


class KeyInfoType(ScalarMap):
    def __init__(
            self,
            id: str = None,
            key_name: str = None,
            key_value: KeyValueType | dict = None,
            retrieval_method: RetrievalMethodType | dict = None,
            x509data: X509DataType | dict = None,
            pgpdata: PGPDataType | dict = None,
            spkid_ata: SPKIDataType | dict = None,
            mgmt_data: str = None,
    ):
        """

        :param id:
        :param key_name:
        :param key_value:
        :param retrieval_method:
        :param x509data:
        :param pgpdata:
        :param spkid_ata:
        :param mgmt_data:
        """

        super().__init__({
            'Id': id,
            'KeyName': key_name,
            'KeyValue': key_value,
            'RetrievalMethod': retrieval_method,
            'X509Data': x509data,
            'PGPData': pgpdata,
            'SPKIData': spkid_ata,
            'MgmtData': mgmt_data,
        })


class ReferenceType(ScalarMap):
    def __init__(
            self,
            digest_method: DigestMethodType | dict = None,
            digest_value: str = None,
            id: str = None,
            uri: str = None,
            type: str = None,
            transforms: TransformsType | dict = None,
    ):
        """

        :param digest_method:
        :param digest_value:
        :param id:
        :param uri:
        :param type:
        :param transforms:
        """

        super().__init__({
            'DigestMethod': digest_method,
            'DigestValue': digest_value,
            'Id': id,
            'URI': uri,
            'Type': type,
            'Transforms': transforms,
        })


class ManifestType(ScalarMap):
    def __init__(
            self,
            reference: ReferenceType | dict = None,
            id: str = None,
    ):
        """

        :param reference:
        :param id:
        """

        super().__init__({
            'Reference': reference,
            'Id': id,
        })


class SignatureMethodType(ScalarMap):
    def __init__(
            self,
            algorithm: str,
            hmacoutput_length: int = None,
    ):
        """

        :param algorithm:
        :param hmacoutput_length:
        """

        super().__init__({
            'Algorithm': algorithm,
            'HMACOutputLength': hmacoutput_length,
        })


class CanonicalizationMethodType(ScalarMap):
    def __init__(
            self,
            algorithm: str,
    ):
        """

        :param algorithm:
        """

        super().__init__({
            'Algorithm': algorithm,
        })


class SignedInfoType(ScalarMap):
    def __init__(
            self,
            canonicalization_method: CanonicalizationMethodType | dict = None,
            signature_method: SignatureMethodType | dict = None,
            reference: ReferenceType | dict = None,
            id: str = None,
    ):
        """

        :param canonicalization_method:
        :param signature_method:
        :param reference:
        :param id:
        """

        super().__init__({
            'CanonicalizationMethod': canonicalization_method,
            'SignatureMethod': signature_method,
            'Reference': reference,
            'Id': id,
        })


class SignatureValueType(ScalarMap):
    def __init__(
            self,
            _text: str,
            id: str = None,
    ):
        """

        :param _text:
        :param id:
        """

        super().__init__({
            '_text': _text,
            'Id': id,
        })


class SignatureType(ScalarMap):
    def __init__(
            self,
            signed_info: SignedInfoType | dict = None,
            signature_value: SignatureValueType | dict = None,
            id: str = None,
            key_info: KeyInfoType | dict = None,
            object: ObjectType | dict = None,
    ):
        """

        :param signed_info:
        :param signature_value:
        :param id:
        :param key_info:
        :param object:
        """

        super().__init__({
            'SignedInfo': signed_info,
            'SignatureValue': signature_value,
            'Id': id,
            'KeyInfo': key_info,
            'Object': object,
        })


class RSAKeyValue(RSAKeyValueType, XElement):
    tag = '{http://www.w3.org/2000/09/xmldsig#}RSAKeyValue'


class DSAKeyValue(DSAKeyValueType, XElement):
    tag = '{http://www.w3.org/2000/09/xmldsig#}DSAKeyValue'


class SignatureProperty(SignaturePropertyType, XElement):
    tag = '{http://www.w3.org/2000/09/xmldsig#}SignatureProperty'


class SignatureProperties(SignaturePropertiesType, XElement):
    tag = '{http://www.w3.org/2000/09/xmldsig#}SignatureProperties'


class Manifest(ManifestType, XElement):
    tag = '{http://www.w3.org/2000/09/xmldsig#}Manifest'


class Object(ObjectType, XElement):
    tag = '{http://www.w3.org/2000/09/xmldsig#}Object'


class SPKIData(SPKIDataType, XElement):
    tag = '{http://www.w3.org/2000/09/xmldsig#}SPKIData'


class PGPData(PGPDataType, XElement):
    tag = '{http://www.w3.org/2000/09/xmldsig#}PGPData'


class X509Data(X509DataType, XElement):
    tag = '{http://www.w3.org/2000/09/xmldsig#}X509Data'


class RetrievalMethod(RetrievalMethodType, XElement):
    tag = '{http://www.w3.org/2000/09/xmldsig#}RetrievalMethod'


class KeyValue(KeyValueType, XElement):
    tag = '{http://www.w3.org/2000/09/xmldsig#}KeyValue'


class KeyInfo(KeyInfoType, XElement):
    tag = '{http://www.w3.org/2000/09/xmldsig#}KeyInfo'


class DigestMethod(DigestMethodType, XElement):
    tag = '{http://www.w3.org/2000/09/xmldsig#}DigestMethod'


class Transform(TransformType, XElement):
    tag = '{http://www.w3.org/2000/09/xmldsig#}Transform'


class Transforms(TransformsType, XElement):
    tag = '{http://www.w3.org/2000/09/xmldsig#}Transforms'


class Reference(ReferenceType, XElement):
    tag = '{http://www.w3.org/2000/09/xmldsig#}Reference'


class SignatureMethod(SignatureMethodType, XElement):
    tag = '{http://www.w3.org/2000/09/xmldsig#}SignatureMethod'


class CanonicalizationMethod(CanonicalizationMethodType, XElement):
    tag = '{http://www.w3.org/2000/09/xmldsig#}CanonicalizationMethod'


class SignedInfo(SignedInfoType, XElement):
    tag = '{http://www.w3.org/2000/09/xmldsig#}SignedInfo'


class SignatureValue(SignatureValueType, XElement):
    tag = '{http://www.w3.org/2000/09/xmldsig#}SignatureValue'


class Signature(SignatureType, XElement):
    tag = '{http://www.w3.org/2000/09/xmldsig#}Signature'
