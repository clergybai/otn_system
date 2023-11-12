import base64
import requests
import json
import logging
from ..models.mac import Mac
from ..models.user import User
from fastapi import status, HTTPException
from common.config import settings
from common.utils.crypto_helper import get_private_key_from_xml_java_formatted_private_key, \
    RsaGenerator, Md5Generator


logger = logging.getLogger(__name__)


def set_mac_history(addr):
    Mac.set_mac_record_to_history(addr)


def insert_addr_key(addr, key):
    Mac.add_mac(Mac(addr=addr, key=key))


def verify_user_identify(addr, user_name, pw_word):
    mac = Mac.find_mac_by(addr=addr, is_history=0)
    private_key_java_str = mac.key
    # 难道private用于将通过public加密的pw_word还原成
    user = User.find_user_by(user_name=user_name)
    if not user:
        return False
    private_key = get_private_key_from_xml_java_formatted_private_key(private_key_java_str)
    # Decrypt pw_word
    # pw_word 首先是一个base64的string，我们首先需要把这个string 变成byte[]
    salt = RsaGenerator.decrypt(private_key=private_key, ciphertext=pw_word)
    # 拿到一个md5哈希的salt的字符串
    salt_hash_str = Md5Generator.md5(salt)
    # 然后用user_name以及MD5哈希的salt值去查询user表如果可以查到证明登陆成功！
    user_with_salt = User.find_user_by(user_name=user_name, salt=salt_hash_str)
    if not user_with_salt:
        return False
    return True


def verify_user_via_ssid(ssid):
    url = f"{settings.wo_operation_api}?method=findUserBySessionID&sessionID={ssid}"
    try:
        resp = requests.get(url)
        if resp.status_code != status.HTTP_200_OK:
            logger.error("WO_operation response error: " + resp.text)
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="WO operation 请求失败！")
        resp_json = json.loads(resp.text)
        user = User.find_user_by(user_name=resp_json['userName'])
        return user
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=str(e))


def test(is_test):
    pwd = "Test_123."
    print(f"要加密数据: {pwd}")
    # 模拟/key请求，产生公钥
    addr = '106ed0b7-b800-a91f-2fb0-b323faae51f7'
    from common.utils.crypto_helper import RsaGenerator, Md5Generator, LEN_RSA_KEY
    from ..services import mac_srv
    rsa = RsaGenerator(LEN_RSA_KEY)
    private_key_str = rsa.gen_xml_key_str()
    public_key_str = rsa.convert_public_key_to_java()

    print(f"公钥: \n{public_key_str}")
    mac_srv.set_mac_history(addr)
    mac_srv.insert_addr_key(addr=addr, key=private_key_str)
    print("私钥写入数据库！")
    if is_test:
        return public_key_str
    # end 模拟/key请求，产生公钥

    # 这里 public_key 就是 PEM格式的公钥
    # 拿到公钥后，我们用这个公钥加密数据
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.asymmetric import padding
    from cryptography.hazmat.primitives import serialization
    # public_key = rsa.get_public_key()
    # 通过pem的公钥字符串变成公钥对象
    public_key = serialization.load_pem_public_key(public_key_str.encode())
    # 用公钥对象加密对象
    encrypted_data = public_key.encrypt(
        pwd.encode('utf-8'),
        # padding.OAEP(
        #     mgf=padding.MGF1(algorithm=hashes.SHA256()),
        #     algorithm=hashes.SHA256(),
        #     label=None
        # )
        padding.PKCS1v15()
    )
    encrypted_data_str = base64.b64encode(encrypted_data).decode('utf-8')
    print("使用公钥后加密的数据:", encrypted_data_str)
    # 至此我们取得了加密后的base64格式的数据。
    # 以下，我们拿到Java格式的private key xml字符串，然后转成private key对象
    print("用数据库中的私钥数据生成私钥！")
    private_key = get_private_key_from_xml_java_formatted_private_key(private_key_str)
    # 用private key decrypt已经加密过的字符串
    decrypt_str = RsaGenerator.decrypt(private_key=private_key, ciphertext=encrypted_data_str)
    print(f"私钥解密后的数据: {decrypt_str}")
    # 把解密的内容变成md5字符串
    decrypt_str_md5 = Md5Generator.md5(decrypt_str)
    print(f"decrypt_str_md5: {decrypt_str_md5}")
    
    test_pwd = 'Gdc123.'
    test_pwd_md5 = Md5Generator.md5(test_pwd)
    print(f"MD5后的解密数据: {test_pwd_md5}")
    
    print(f"{'>'*100}")
    print("从这里开始我们使用从80环境截取的真实数据")
    # 真实的addr
    hd_addr = 'fc59e480-87cd-df9f-c332-d3841370634e'
    # 真实的数据库中与这次login相一致的Java format private key
    hd_private_key_xml_str = '<RSAKeyValue><Modulus>tYaw+vR78CjS7D0/Rca2OqD/wTcy7nNRJCyzGbNP5fPmgFsu8OxJYSMlppQvRBEef7/2hA/oq1ybcov5KIwbKCJnrAAQnDhHYe1UmrZOg7qPNLlcBLudl1nCNf5qws32G8ThG/5atAuDIFLiP26OgfsnjpbXPT0qXjTvF13waa0=</Modulus><Exponent>AQAB</Exponent><P>4w6HuxU+UMndbFH+4hvuRvUXURfCQfbFAxKy8180h3ePyflym7tdnuskF9VGApuweV81zgULuL3wMc4/2gvNiQ==</P><Q>zKpgBxe0ZV4EnDnWCod3MGws7kskuan14hj3dG5DC3ttlgsHYrgMIQ/o3DmkmakjXIKG00jVFV4CtVKne2a2BQ==</Q><DP>4BZvDsyge8s+pLEoBK/cMluhb38rUT7ioW3K/zZu+WOenY969QeuFjGrpXnvZpORT7gPugxwzRtn+z+69M/BQQ==</DP><DQ>dlhufqtuXM8oy02GP0Bl41IqCQDak6F71Omq7WB01Ebi70ghVSwnl1ajx/RtAY2ULQItBC+xR1G9LyxEPE8AIQ==</DQ><InverseQ>KM/mAmPGVwOr7ZBS6V+KnF/EAk7OhyIO1kzE43etohk3YsFFmXyqAVV+phwUHMsKZKqPI8/xoLV+RQIQci5nuw==</InverseQ><D>Y98kFh5W5g3/5fvYiPJIJj+YFtzgx7JobSeurjAqgFDNe8cvL1xBDxGAUILs8l0c05pw7b22/DjqSX5bagSTl3a3Ur7eN8+gtwPPtoo6/F5nswvYlJahb0Ux4sDN76sbDyjc/sBFp2mhB08/pEZCRW66WEbn+RQc8cqP63twkSE=</D></RSAKeyValue>'
    # 真实的/key请求拿到的PEM公钥数据
    hd_public_key_str = '-----BEGIN PUBLIC KEY-----\nMIGfMA0GCSqGSIb3DQEBAQUAA4GNAD\nCBiQKBgQC1hrD69HvwKNLsPT9FxrY6\noP/BNzLuc1EkLLMZs0/l8+aAWy7w7E\nlhIyWmlC9EER5/v/aED+irXJtyi/ko\njBsoImesABCcOEdh7VSatk6Duo80uV\nwEu52XWcI1/mrCzfYbxOEb/lq0C4Mg\nUuI/bo6B+yeOltc9PSpeNO8XXfBprQ\nIDAQAB\n-----END PUBLIC KEY-----'
    # 真实的前端加密后的数据，在/login时带上的数据。
    hd_pw_word = 'EnsE9JJj6eY9SoFmD/YnjbzKHeH95TJgRGJ9GD0LGAx4/G0u4W9a/8TiUQTjFIZYm8OxrRVxaCg8frXjcYRjKoDLyj0I9iq/Qay/n0POhbwScmwXSK+w1rv0gT+fDAHKAw1gAxpm8hogXC7DZJYqSuV1PhMK7BQ383peCMJtxXw='
    hd_user_name = 'admin'
    hd_password = 'test'
    # user表中的salt字段的值
    hd_salt = '0f20560480be0a80c607f0aa0b101a0220a00590ac0cf01b'
    hd_private_key = get_private_key_from_xml_java_formatted_private_key(hd_private_key_xml_str)
    hd_public_key = serialization.load_pem_public_key(hd_public_key_str.encode())
    # 加密用户密码
    hd_encrypted_data = hd_public_key.encrypt(
        hd_password.encode('utf-8'),
        padding.PKCS1v15()
        # padding.OAEP(
        #     mgf=padding.MGF1(algorithm=hashes.SHA256()),
        #     algorithm=hashes.SHA256(),
        #     label=None
        # )
    )
    hd_encrypted_data_str = base64.b64encode(hd_encrypted_data).decode('utf-8')
    # pw_word生成
    print(f"加密后的pw_word: {hd_encrypted_data_str}")
    
    hd_decrypt_pw = RsaGenerator.decrypt(hd_private_key, ciphertext=hd_encrypted_data_str)
    print(f"解密后的pw_word: {hd_decrypt_pw}")
    
    print(f"解密后的数据: {hd_password}")
    ht_test_pwd_md5 = Md5Generator.md5(hd_decrypt_pw)
    print(f"MD5解密后的数据: {ht_test_pwd_md5}")
    
    print(f"{'>'*100}")
    print("使用真实的加密数据进行测试")
    hd_decrypt_pw_word = RsaGenerator.decrypt(hd_private_key, ciphertext=hd_pw_word)
    print(f"解密后的 hd_pw_word: {hd_decrypt_pw_word}")
    hd_pw_word_md5 = Md5Generator.md5(hd_decrypt_pw_word)
    print(f"MD5解密后的数据: \t{hd_pw_word_md5}")
    
    print(f"salt: \t\t\t{hd_salt}")
