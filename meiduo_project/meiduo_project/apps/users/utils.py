from django.conf import settings
from django.contrib.auth.backends import ModelBackend
import re
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from .contents import VERIFY_EMAIL_TOKEN_EXPIRES
from .models import User
import logging

logger = logging.getLogger('django')


def check_verify_email_token(token):
    """通过token获取激活对象"""
    serializer = Serializer(settings.SECRET_KEY, expires_in=VERIFY_EMAIL_TOKEN_EXPIRES)
    # token可能过期
    try:
        data = serializer.loads(token)
    except Exception as e:
        logger.error(e)
        return None
    else:
        email = data['email']
        user_id = data['user_id']

        try:
            user = User.objects.get(email=email, id=user_id)
        except Exception as e:
            logger.error(e)
            return None
        else:
            return user


def generate_verify_email_url(user):
    """
    生成邮箱链接
    :param user: 当前登录用户对象
    :return: verify_url
    """
    serializer = Serializer(settings.SECRET_KEY, expires_in=VERIFY_EMAIL_TOKEN_EXPIRES)
    data = {
        'user_id': user.id,
        'email': user.email
    }
    token = serializer.dumps(data).decode()
    # 拼接激活链接
    verify_url = settings.EMAIL_VERIFY_URL + '?token=' + token
    return verify_url


def get_user_by_account(account):
    """
    根据account查询用户
    :return:
    """
    try:  # 进行查询要try
        if re.match(r'^1[3-9]\d{9}$', account):
            # 手机号登录(以手机号查询用户)
            user = User.objects.get(mobile=account)
        else:
            user = User.objects.get(username=account)
    except Exception as e:
        logger.error(e)
        return None
    else:
        return user


class UsernameMobileAuthBacken(ModelBackend):
    """自定义用户后端"""

    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        重写认证方法: 实现多账号登录
        :param request: 请求对象
        :param username: 用户名
        :param password: 密码
        :param kwargs: 其他参数
        :return:
        """
        if request is None:
            # 查询用户名和身份
            try:
                user = User.objects.get(username=username, is_staff=True)
            except Exception as e:
                logger.error(e)
                user = None

            if user and user.check_password(password):
                return user
            else:
                return None

        else:
            user = get_user_by_account(username)
            if user and user.check_password(password):
                return user
            else:
                return None
