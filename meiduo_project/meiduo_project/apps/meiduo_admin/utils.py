from rest_framework_jwt.utils import jwt_response_payload_handler


def jwt_response_payload_handler(token, user=None, request=None):
    """自定义字段返回"""
    return {
        'token': token,
        'user': user.id,
        'username': user.username
    }
