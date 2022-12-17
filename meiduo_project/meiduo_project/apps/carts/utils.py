import base64
import pickle
import json
from django_redis import get_redis_connection


def cookie_to_dict(cookie_str):
    """cookie购物车数据转python字典"""
    # 加密str -> b'加密str'
    byte_cookie_str = cookie_str.encode()
    # b'加密str' -> b'dict
    byte_dict = base64.b64decode(byte_cookie_str)
    # b'dict' -> dict
    dict_data = pickle.loads(byte_dict)
    return dict_data


def dict_to_cookie(dict_data):
    """python字典转cookie数据"""
    # dict -> b'dict'
    byte_dict = pickle.dumps(dict_data)
    # b'dict' -> b'加密str'
    byte_cookie_dict = base64.b64encode(byte_dict)
    # b'加密str' -> 加密str
    cookie_dict = byte_cookie_dict.decode()
    return cookie_dict


def merge_cart_cookie_to_redis(request, response):
    """合并购物车"""
    user = request.user
    if request.COOKIES.get('carts'):

        cookie_carts = request.COOKIES.get('carts')

        dict_carts = cookie_to_dict(cookie_carts)

        conn_redis = get_redis_connection('carts')

        for cookie_sku_id in dict_carts:
            count = dict_carts[cookie_sku_id]['count']
            selected = dict_carts[cookie_sku_id]['selected']
            # 覆盖(新增)redis的
            conn_redis.hset('carts_%s' % user.id, cookie_sku_id, count)
            # 添加勾选
            if selected:
                conn_redis.sadd('selected_%s' % user.id, cookie_sku_id)

    # 清空重置购物车为空字典
    response.set_cookie('carts', dict_to_cookie({}))

    return response
