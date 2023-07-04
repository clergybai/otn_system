import base64
import hashlib
import binascii
import xml.etree.ElementTree as ET
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateNumbers, RSAPublicNumbers


LEN_RSA_KEY = 1024


def get_private_key_from_xml_java_formatted_private_key(private_key_xml):
    tree = ET.fromstring(private_key_xml)
    modulus = base64.b64decode(tree.find('.//Modulus').text)
    exponent = base64.b64decode(tree.find('.//Exponent').text)
    d = base64.b64decode(tree.find('.//D').text)
    p = base64.b64decode(tree.find('.//P').text)
    q = base64.b64decode(tree.find('.//Q').text)
    dp = base64.b64decode(tree.find('.//DP').text)
    dq = base64.b64decode(tree.find('.//DQ').text)
    inverse_q = base64.b64decode(tree.find('.//InverseQ').text)

    numbers = RSAPrivateNumbers(
        p=int.from_bytes(p, 'big'),
        q=int.from_bytes(q, 'big'),
        d=int.from_bytes(d, 'big'),
        dmp1=int.from_bytes(dp, 'big'),
        dmq1=int.from_bytes(dq, 'big'),
        iqmp=int.from_bytes(inverse_q, 'big'),
        public_numbers=RSAPublicNumbers(
            e=int.from_bytes(exponent, 'big'),
            n=int.from_bytes(modulus, 'big')
        )
    )
    private_key = numbers.private_key(backend=default_backend())
    return private_key


def convert_public_key_to_xml(public_key):
    return public_key.decode()


def convert_public_key_to_java(public_key):
    rsa_public_key = serialization.load_pem_public_key(public_key, backend=default_backend())
    modulus = int.from_bytes(rsa_public_key.public_numbers().n.to_bytes((rsa_public_key.key_size + 7) // 8, 'big'), 'big')
    exponent = rsa_public_key.public_numbers().e
    java_public_key = "-----BEGIN PUBLIC KEY-----\n"
    java_public_key += modulus.to_bytes((rsa_public_key.key_size + 7) // 8, 'big').hex() + "\n"  # Modulus in hexadecimal format
    java_public_key += exponent.to_bytes(4, 'big').hex() + "\n"  # Exponent in 4-byte big-endian format
    java_public_key += "-----END PUBLIC KEY-----"
    return java_public_key


def component_to_b64str(component):
    component_bytes = component.to_bytes((component.bit_length() + 7) // 8, 'big')
    return base64.b64encode(component_bytes).decode('utf-8')


class RsaGenerator(object):

    def __init__(self, key_len):
        self.private_key_raw = None
        self.public_key_raw = None
        self.private_key, self.public_key = self.__gen_pri_pub_keys_obj_pair(key_len)
        self.comp_dict = self.__gen_key_components()

    def __gen_pri_pub_keys_obj_pair(self, key_len):
        self.private_key_raw = rsa.generate_private_key(
            public_exponent=65537,
            key_size=key_len,
            backend=default_backend())
        self.public_key_raw = self.private_key_raw.public_key()
        return (
            self.private_key_raw.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            ),
            self.public_key_raw.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
        )

    def __gen_key_components(self):
        private_key_obj = serialization.load_pem_private_key(self.private_key, password=None)
        public_key_obj = serialization.load_pem_public_key(self.public_key)
        private_numbers = private_key_obj.private_numbers()
        public_numbers = public_key_obj.public_numbers()
        # 获取 P、Q、DP、DQ、InverseQ 和 D 的值
        p = private_numbers.p
        q = private_numbers.q
        dp = private_numbers.dmp1
        dq = private_numbers.dmq1
        inverse_q = private_numbers.iqmp
        d = private_numbers.d
        # 获取 Exponent 和 Modulus 的值
        e = public_numbers.e
        n = public_numbers.n
        return {
            "p": p,
            "q": q,
            "dp": dp,
            "dq": dq,
            "inverse_q": inverse_q,
            "d": d,
            "e": e,
            "n": n
        }

    def get_private_key(self):
        return self.private_key_raw
    
    def get_public_key(self):
        return self.public_key_raw

    def gen_xml_key_str(self, is_private_key=True):
        root = ET.Element("RSAKeyValue")
        # Modulus
        modulus_elem = ET.SubElement(root, "Modulus")
        modulus_elem.text = component_to_b64str(self.comp_dict['n'])
        # Exponent
        exponent_elem = ET.SubElement(root, "Exponent")
        exponent_elem.text = component_to_b64str(self.comp_dict['e'])

        if not is_private_key:
            return ET.tostring(root, encoding="unicode")

        # P
        p_elem = ET.SubElement(root, "P")
        p_elem.text = component_to_b64str(self.comp_dict['p'])
        # Q
        q_elem = ET.SubElement(root, "Q")
        q_elem.text = component_to_b64str(self.comp_dict['q'])
        # DP
        dp_elem = ET.SubElement(root, "DP")
        dp_elem.text = component_to_b64str(self.comp_dict['dp'])
        # DQ
        dq_elem = ET.SubElement(root, "DQ")
        dq_elem.text = component_to_b64str(self.comp_dict['dq'])
        # InverseQ
        inverse_q_elem = ET.SubElement(root, "InverseQ")
        inverse_q_elem.text = component_to_b64str(self.comp_dict['inverse_q'])
        # D
        d_elem = ET.SubElement(root, "D")
        d_elem.text = component_to_b64str(self.comp_dict['d'])
        xml_string = ET.tostring(root, encoding="unicode")
        return xml_string

    def convert_public_key_to_java(self):
        """用户产生PEM格式的public key然后输出给cookie用

        Returns:
            _type_: str
        """
        # pem_public_key = self.public_key_raw.public_bytes(
        #     encoding=serialization.Encoding.PEM,
        #     format=serialization.PublicFormat.SubjectPublicKeyInfo
        # )
        # return pem_public_key.decode('utf-8')
        pem_public_key = self.public_key_raw.public_bytes(
            encoding=serialization.Encoding.DER,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        base64_public_key = base64.b64encode(pem_public_key).decode('utf-8')
        return self.combine_to_java_format(base64_public_key)

    def combine_to_java_format(self, base64_public_key: str):
        if not base64_public_key:
            return ""
        key = "-----BEGIN PUBLIC KEY-----\n"
        cnt = 0
        len_each_line = 30
        yu = len(base64_public_key) - cnt
        while yu > 0:
            length = min(yu, len_each_line)
            key += base64_public_key[cnt:cnt + length] + "\n"
            cnt += len_each_line
            yu = len(base64_public_key) - cnt
        key += "-----END PUBLIC KEY-----"
        return key
        
    
    
    @classmethod
    def gen_xml_jave_formatted(cls, private_key):
        public_key = private_key.public_key()
        private_obj = private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            )
        public_obj = public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
        private_bytes = serialization.load_pem_private_key(private_obj, password=None)
        public_bytes = serialization.load_pem_public_key(public_obj)
        private_numbers = private_bytes.private_numbers()
        public_numbers = public_bytes.public_numbers()
        p = private_numbers.p
        q = private_numbers.q
        dp = private_numbers.dmp1
        dq = private_numbers.dmq1
        inverse_q = private_numbers.iqmp
        d = private_numbers.d
        # 获取 Exponent 和 Modulus 的值
        e = public_numbers.e
        n = public_numbers.n
        
        root = ET.Element("RSAKeyValue")
        # Modulus
        modulus_elem = ET.SubElement(root, "Modulus")
        modulus_elem.text = component_to_b64str(n)
        # Exponent
        exponent_elem = ET.SubElement(root, "Exponent")
        exponent_elem.text = component_to_b64str(e)
        public_key_xml = ET.tostring(root, encoding="unicode")

        # P
        p_elem = ET.SubElement(root, "P")
        p_elem.text = component_to_b64str(p)
        # Q
        q_elem = ET.SubElement(root, "Q")
        q_elem.text = component_to_b64str(q)
        # DP
        dp_elem = ET.SubElement(root, "DP")
        dp_elem.text = component_to_b64str(dp)
        # DQ
        dq_elem = ET.SubElement(root, "DQ")
        dq_elem.text = component_to_b64str(dq)
        # InverseQ
        inverse_q_elem = ET.SubElement(root, "InverseQ")
        inverse_q_elem.text = component_to_b64str(inverse_q)
        # D
        d_elem = ET.SubElement(root, "D")
        d_elem.text = component_to_b64str(d)
        private_key_xml = ET.tostring(root, encoding="unicode")
        return (private_key_xml, public_key_xml)

    @classmethod
    def decrypt(cls, private_key, ciphertext):
        ciphertext_byte = base64.b64decode(ciphertext)
        # return private_key.decrypt(
        #     ciphertext_byte,
        #     padding.OAEP(
        #         mgf=padding.MGF1(algorithm=hashes.SHA256()),
        #         algorithm=hashes.SHA256(),
        #         label=None
        #     )
        # ).decode('utf-8')
        return private_key.decrypt(
            ciphertext_byte,
            padding.PKCS1v15()
        ).decode('utf-8')
    
    @classmethod
    def encrypt_to_b64_str(cls, public_key, content):
        encrypted_data = public_key.encrypt(
            content.encode('utf-8'),
            padding.PKCS1v15()
        )
        return base64.b64encode(encrypted_data).decode('utf-8')

    @classmethod
    def decrypt_test(cls, private_key, ciphertext):
        ciphertext_byte = base64.b64decode(ciphertext)
        return private_key.decrypt(
            ciphertext_byte,
            padding.PKCS1v15()
        ).decode('utf-8')


class Md5Generator(object):
    @classmethod
    def md5(cls, message):
        md5_hash = hashlib.md5(message.encode('utf-8'))
        return '0' + binascii.hexlify(md5_hash.digest(), sep='0').decode('utf-8')


if __name__ == "__main__":
    rsa_gen = RsaGenerator(LEN_RSA_KEY)
    xml_private_str = rsa_gen.gen_xml_key_str()
    xml_public_str = rsa_gen.gen_xml_key_str(False)
    public_key_str = rsa_gen.convert_public_key_to_java()
    print(f"private key xml: {xml_private_str}")
    print(f"public key xml: {xml_public_str}")
    print(f"public key: \r\n{public_key_str}")

    pri_key = get_private_key_from_xml_java_formatted_private_key(xml_private_str)
    regen_private_xml_str, regen_public_xml_str = RsaGenerator.gen_xml_jave_formatted(pri_key)
    
    if xml_private_str != regen_private_xml_str:
        print("not equal")
        
    if xml_public_str != regen_public_xml_str:
        print("not equal")
    print("done")
