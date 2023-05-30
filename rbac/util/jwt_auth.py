import jwt
import datetime
from jwt import exceptions
import traceback
import time

# 加的盐
JWT_SALT = "ds()udsjo@jlsdosjf)wjd_#(#)$"


def create_token(info: dict, timeout=2 * 60 * 60):
    """
    用于加密生成token
    :payload dict e.g. {"user_id": "杨远", "age": 31}:
        payload标准信息：（并不完全强制要求全部使用）
        iss    : jwt签发者
        sub  : 主题名称
        aud  : 面向的用户，一般都是通过ip或者域名控制
        exp  : jwt的有效时间（过期时间），这个有效时间必须要大于签发时间，对于交互接口来说，建议是预设5秒
        nbf   : 在什么时候jwt开始生效（在此之前不可用）
        iat    : jwt的签发时间，只能用utc时间
        jti     : 唯一标识，主要用来回避被重复使用攻击
        ————————————————
        版权声明：本文为CSDN博主「H-大叔」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
        原文链接：https://blog.csdn.net/HRG520JN/article/details/123664105
    :return: {"status": False, "data": None, "error": None, "errmsg": None}
    """
    # 声明类型，声明加密算法
    headers = {
        "type": "jwt",
        "alg": "HS256"
    }
    now = datetime.datetime.utcnow()
    # 设置过期时间
    payload = {
        # "iss": "sinocare.django.com",
        # "iat": int(time.time()),
        # "exp": int(time.time()) + datetime.timedelta(seconds=timeout),
        "iat": now,
        "exp": now + datetime.timedelta(seconds=timeout),
        # "aud": "www.gusibi.mobi",
        # "scopes": ['open']
    }
    payload = dict(payload, **info)
    # payload['iat'] = datetime.datetime.utcnow()  # 只能用utc时间
    # payload['exp'] = datetime.datetime.utcnow() + datetime.timedelta(seconds=timeout)
    # payload['crt'] = datetime.datetime.now() + datetime.timedelta(seconds=timeout)
    # result = jwt.encode(payload=payload, key=JWT_SALT, algorithm="HS256", headers=headers).decode("utf-8")
    ret_token = jwt.encode(payload, JWT_SALT, algorithm="HS256", headers=headers)
    if not isinstance(ret_token, str):
        ret_token = str(ret_token, encoding='utf8')
    payload['grant_type'] = "refresh"
    payload['exp'] = now + datetime.timedelta(seconds=60 * 60 * 24)
    refresh_token = jwt.encode(payload, JWT_SALT, algorithm='HS256', headers=headers)
    if not isinstance(refresh_token, str):
        refresh_token = str(refresh_token, encoding='utf8')
    # 返回加密结果
    return {"access_token": ret_token,
            "refresh_token": refresh_token,
            "iat": payload['iat'],
            "exp": payload['exp']}


def parse_payload(token):
    """
    用于解密
    :param token:
    :return: {"status": False, "data": None, "error": None, "errmsg": None}
    """
    ret = {"status": False, "data": None, "error": None, "errmsg": None}
    try:
        # 进行解密
        verified_payload = jwt.decode(token, key=JWT_SALT, algorithms="HS256")
        ret["status"] = True
        ret['data'] = verified_payload
    except exceptions.ExpiredSignatureError:
        ret['error'] = 'token已失效'
        ret['errmsg'] = traceback.format_exc()
    except jwt.DecodeError:
        ret['error'] = 'token认证失败'
        ret['errmsg'] = traceback.format_exc()
    except jwt.InvalidTokenError:
        ret['error'] = '非法的token'
        ret['errmsg'] = traceback.format_exc()
    except Exception as e:
        ret['error'] = f'其他错误：{str(e)}'
        ret['errmsg'] = traceback.format_exc()
    if not ret["status"]:
        print(f"error:{ret['error']}\n{ret['errmsg']}")
    return ret


if __name__ == '__main__':
    print("*" * 100)
    print("create token.")
    token_info = create_token({"user_id": "杨远", "age": 31}, timeout=2)
    print(token_info)
    print("*" * 100)
    result = parse_payload(token_info['access_token'])
    print(result)
    if not (result["status"]):
        print(f"error:\n{result['error']}\nerrmsg:\n{result['errmsg']}")
    print("*" * 100)
    result = parse_payload(token_info['refresh_token'])
    print(result)
    if not (result["status"]):
        print(f"error:\n{result['error']}\nerrmsg:\n{result['errmsg']}")
    print("*" * 100)
    sleep = 3
    print(f"sleep {sleep}s.")
    time.sleep(sleep)
    result = parse_payload(token_info['token'])
    print(result)
    if not (result["status"]):
        print(result["errmsg"])
