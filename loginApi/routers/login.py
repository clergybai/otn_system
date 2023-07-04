import uuid
from fastapi import APIRouter, status, HTTPException
from ..services import mac_srv, permissions_srv, user_srv
from common.utils.crypto_helper import RsaGenerator, LEN_RSA_KEY
from .. import schemas
from common.redis import (redis_client, AUTH_DB,
                          USER_TOKEN_HSET, TOKEN_USER_HSET)


router = APIRouter(
    prefix='/Login',
    tags=['Login']
)


@router.post("/key/",
             response_model=schemas.KeyResponse,
             summary="返回 RSA public key")
def get_key(req: schemas.KeyRequest):

    if req.is_test:
        print('hardcode public key for test.')
        hd_public_key = "-----BEGIN PUBLIC KEY-----\nMIGfMA0GCSqGSIb3DQEBAQUAA4GNAD\nCBiQKBgQDXubz77knETNTq9NfvyZbe\nd49NUWKGdScVoBKN/RA0czy/AiuOQU\n3dM5Axyb3VmT0w2vD1PN9/C0IY+DWG\nNapD57nFvf5tPHkaZYHn4pPM8jLSvI\nPg6dwS7MBsU4Behkz6aMbfCdKuEXqD\nqCwddqLsyE8oxQJymBP6SVZ1SoT0gw\nIDAQAB\n-----END PUBLIC KEY-----"
        return schemas.KeyResponse(data=schemas.KeyDataResponse(
            addr=req.addr, public_key=hd_public_key))

    rsa = RsaGenerator(LEN_RSA_KEY)
    private_key = rsa.gen_xml_key_str()
    public_key = rsa.convert_public_key_to_java()
    mac_srv.set_mac_history(req.addr)
    mac_srv.insert_addr_key(addr=req.addr, key=private_key)

    return schemas.KeyResponse(data=schemas.KeyDataResponse(
        addr=req.addr,
        public_key=public_key))


@router.post("/login/",
             response_model=schemas.LoginResponse,
             summary="登陆操作")
def login(req: schemas.LoginRequest):
    # 首先检查user_name,超检查pw_word，缺一不可
    if not req.is_test and not mac_srv.verify_user_identify(
            addr=req.mac_addr, user_name=req.user_name, pw_word=req.pw_word):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    # 获取用户的的各种授权数据
    user_perm = permissions_srv.get_user_perms(user_name=req.user_name)
    print(f"user_perm: {str(user_perm)}")
    auth_obj = permissions_srv.convert_user_perm_to_dict(user_perm)
    token = str(uuid.uuid4())
    # 把 token 存入到auth_db的键值对中去
    user_srv.cache_user_token(username=req.user_name, token=token)
    return schemas.LoginResponse(data=schemas.LoginDataResponse(
        token=token,
        user_name=req.user_name,
        is_authen=auth_obj
    ))


@router.post("/ssid",
             response_model=schemas.LoginResponse,
             summary="ssid登陆操作")
def ssid(req: schemas.LoginRequest):
    user = mac_srv.verify_user_via_ssid(req.user_name)
    if not req.is_test and not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    # 获取用户的的各种授权数据
    user_perm = permissions_srv.get_user_perms(user_name=req.user_name)
    print(f"user_perm: {str(user_perm)}")
    auth_obj = permissions_srv.convert_user_perm_to_dict(user_perm)
    token = str(uuid.uuid4())
    # 把 token 存入到auth_db的键值对中去
    user_srv.cache_user_token(username=req.user_name, token=token)
    return schemas.LoginResponse(data=schemas.LoginDataResponse(
        token=token,
        user_name=req.user_name,
        is_authen=auth_obj
    ))


@router.get("/test")
def test():
    # mac_srv.test(True)
    return mac_srv.test(True)
