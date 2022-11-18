from django.contrib.auth.backends import ModelBackend
import re
from .models import User


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
    except Exception:
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
        user = get_user_by_account(username)
        if user is None:
            return None
        else:
            user.check_password(password)
            return user
