from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from django.conf import settings
from .constants import ACCESS_TOKEN_EXPIRES


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
    return token
