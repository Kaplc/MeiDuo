import base64
import pickle


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
