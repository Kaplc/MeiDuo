from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from django.conf import settings
from .constants import ACCESS_TOKEN_EXPIRES
import logging

logger = logging.getLogger('django')


def check_access_token(access_token):
    # access_token = access_token.decode()
    serializer = Serializer(settings.SECRET_KEY, expires_in=ACCESS_TOKEN_EXPIRES)
    try:
        openid = serializer.loads(access_token)
    except Exception as e:
        logger.error(e)
        return None
    else:
        return openid


def generate_access_token(openid):
    """
    加密签名openid
    :param openid: openid
    :return: access_token
    """
    # 创建Serializer对象设置加解密字符串, 过期时间
    serializer = Serializer(settings.SECRET_KEY, expires_in=ACCESS_TOKEN_EXPIRES)
    # 定义加密字典
    data = {
        'openid': openid,

    }
    # 加密签名
    token = serializer.dumps(data)
    token = token.decode()
    return token
