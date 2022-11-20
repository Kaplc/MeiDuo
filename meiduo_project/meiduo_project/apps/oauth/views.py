import re

from django import http
from django.contrib.auth import login
from django.shortcuts import render, redirect
from QQLoginTool.QQtool import OAuthQQ
# Create your views here.
from django.views import View
from django.conf import settings
from django_redis import get_redis_connection

from users.models import User
from utils.response_code import RETCODE
from .models import OAuthQQUser
import logging
from utils.parameter import SETTING_TIME
from .utils import generate_access_token, check_access_token

# 创建日志器对象
logger = logging.getLogger('django')


class QQAuthUserView(View):
    """扫码登录的回调处理"""

    def get(self, request):
        """Oauth2.0认证"""

        # 接收Authorization Code
        code = request.GET.get('code')
        if not code:
            return http.HttpResponse('缺少code')
        # 创建工具对象
        oauth = OAuthQQ(client_id=settings.QQ_CLIENT_ID, client_secret=settings.QQ_CLIENT_SECRET,
                        redirect_uri=settings.QQ_REDIRECT_URI)

        try:
            # 使用code获取access_token
            access_token = oauth.get_access_token(code)
            # access_token获取openid
            openid = oauth.get_open_id(access_token)

        except Exception as e:
            logger.error(e)
            return http.HttpResponseServerError('OAuth2.0认证失败')

        # 查询openid是否绑定
        try:
            oauth_user = OAuthQQUser.objects.get(openid=openid)
        except Exception as e:
            # 未查询到用户 -> 未绑定
            logger.error(e)
            # 签名openid
            access_token = generate_access_token(openid)
            # 将加密后的openid发送给用户页面做标记
            context = {
                "access_token_openid": access_token
            }

            return render(request, 'oauth_callback.html', context)

        else:
            # 查询到用户 -> 已绑定
            # 登录
            qq_user = oauth_user.user  # OAuthQQUser找到User表的user对象
            login(request, qq_user)
            # 响应结果
            # 获取next
            next_url = request.GET.get('state')
            response = redirect(next_url)
            # 设置cookie
            response.set_cookie('username', qq_user.username, max_age=SETTING_TIME.COOKIE_USERNAME_EXPIRES)
            return response

    def post(self, request):
        """用户绑定到openid"""
        # 接收参数
        mobile = request.POST.get('mobile')
        password = request.POST.get('password')
        sms_code_cli = request.POST.get('sms_code')
        access_token_openid = request.POST.get('access_token_openid')
        # 校验参数
        if not all([mobile, password, sms_code_cli, access_token_openid]):
            return http.HttpResponseForbidden('缺少参数')
        if not re.match(r'^1[3-9]\d{9}$', mobile):  # 校验手机号格式
            return http.HttpResponseForbidden('手机号格式错误')
        if not re.match(r'^.{8,20}$', password):
            return http.HttpResponseForbidden('密码格式错误')
        if not (re.match(r'.*[a-zA-Z]+.*', password) and re.match(r'.*[0-9]+.*', password)):
            return http.HttpResponseForbidden('密码强度不符合')
        # 校验短信验证码
        redis_conn = get_redis_connection('verify_code')
        sms_code_server = redis_conn.get('sms_%s' % mobile)
        sms_code_server = sms_code_server.decode()
        if sms_code_server is None:
            return render(request, 'oauth_callback.html', {'sms_code_errmsg': '短信验证码过期'})

        if sms_code_server != sms_code_cli:
            return render(request, 'oauth_callback.html', {'sms_code_errmsg': '短信验证码错误'})
        # 判断openid有效性
        openid = check_access_token(access_token_openid)
        if openid is None:
            return render(request, 'oauth_callback.html', {'openid_errmsg': 'QQ登录已过期'})
        # 保存注册数据
        try:
            user = User.objects.get(mobile=mobile)

        except Exception as e:
            # 用户不存在, 创建新用户
            user = User.objects.create_user(username=mobile, password=password, mobile=mobile)

        else:
            # 用户存在, 检查密码是否正确
            if not user.check_password(password):
                return render(request, 'oauth_callback.html', {'account_errmsg': '用户名或密码错误'})
        # 绑定用户openid
        try:
            OAuthQQUser.objects.create(openid=openid['openid'], user=user)
        except Exception as e:
            logger.error(e)
            return render(request, 'oauth_callback.html', {'qq_login_errmsg': 'QQ登录失败'})


        # 状态保持
        login(request, user)
        # 获取next
        next_url = request.GET.get('state')
        response = redirect(next_url)
        # 设置cookie
        response.set_cookie('username', user.username, max_age=3600 * 12)
        # 响应结果
        return response


class QQAuthURLView(View):
    """提供QQ登录页面"""

    def get(self, request):
        """提供扫码页面"""
        # 获取点击原地址next
        next_url = request.GET.get('next')
        # 创建工具OAuthQQ对象(参数为appid, app密钥, 回调地址)
        oauth = OAuthQQ(client_id=settings.QQ_CLIENT_ID, client_secret=settings.QQ_CLIENT_SECRET,
                        redirect_uri=settings.QQ_REDIRECT_URI, state=next_url)

        # 获取扫码链接
        login_url = oauth.get_qq_url()

        return http.JsonResponse({"code": RETCODE.OK, "errmsg": "OK", "login_url": login_url})
