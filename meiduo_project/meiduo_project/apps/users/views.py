import json
import logging
import re
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django import http
from django_redis import get_redis_connection
from celery_tasks.send_email.tasks import send_verify_email
# noinspection PyUnresolvedReferences
from meiduo_project.utils.parameter import SETTING_TIME
# noinspection PyUnresolvedReferences
from meiduo_project.utils.response_code import RETCODE
from .models import User
from .utils import generate_verify_email_url, check_verify_email_token

# Create your views here.
logger = logging.getLogger('django')


class VerifyEmailView(View):
    """验证邮箱激活链接"""

    def get(self, request):
        """实现激活邮箱并写入数据库保存"""
        # 接收参数
        token = request.GET.get('token')
        # 校验参数
        if not token:
            return http.HttpResponseForbidden('缺少激活邮件token')
        # 通过token获取用户对象
        user = check_verify_email_token(token)
        if not user:
            return http.HttpResponseForbidden('邮件激活token过期')
        # 激活标记写入数据库
        try:
            user.email_active = True
            user.save()
        except Exception as e:
            logger.error(e)
            return http.HttpResponseServerError('邮件激活失败')

        return redirect(reverse('users:center_info'))


class EmailView(LoginRequiredMixin, View):
    """添加邮箱"""

    def put(self, request):
        """添加邮箱逻辑"""
        # 接收参数
        json_str = request.body.decode()
        json_dict = json.loads(json_str)
        email = json_dict['email']
        # 校验参数
        if not email:
            return http.HttpResponseForbidden('缺少email参数')
        if not re.match(r'^[a-z0-9][\w\-.]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return http.HttpResponseForbidden('邮箱格式错误')

        # 更新数据库
        try:
            if email == request.user.email:
                return http.JsonResponse({'code': RETCODE.DBERR, 'errmsg': '该邮箱已验证'})
            request.user.email = email  # 请求对象找到user用户对象控制数据库email字段数据
            request.user.email_active = False
            request.user.save()  # 同步到数据库

        except Exception as e:
            logger.error(e)
            return http.JsonResponse({'code': RETCODE.DBERR, 'errmsg': '添加邮箱失败'})

        # 异步发送验证邮件
        verify_url = generate_verify_email_url(request.user)
        send_verify_email.delay(email, verify_url)  # delay()
        # 响应结果
        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': '添加邮箱成功'})


class UserInfoView(LoginRequiredMixin, View):
    """用户中心"""

    def get(self, request):
        """通过个人信息页面"""
        context = {
            'username': request.user.username,
            'mobile': request.user.mobile,
            'email': request.user.email,
            'email_active': request.user.email_active,

        }
        return render(request, 'user_center_info.html', context=context)


class LogoutView(View):
    """用户退出登录"""

    def get(self, request):
        """
        实现退出登录
        :param request: 请求对象
        :return: 重定向到首页
        """
        # 清理session并登出
        logout(request)
        # 重定向到首页
        response = redirect(reverse('contents:index'))
        # 删除cookie的username信息
        response.delete_cookie('username')
        return response


class LoginView(View):
    """用户登录"""

    def get(self, request):
        """
        提供登录页面
        :param request: 请求对象
        :return: 登录页面
        """
        return render(request, 'login.html')

    def post(self, request):
        # 接收参数
        username = request.POST.get('username')
        password = request.POST.get('password')
        remembered = request.POST.get('remembered')
        # 校验参数
        if not (all([username, password])):  # 判断参数完整
            return http.HttpResponseForbidden('参数错误')
        # 校验用户名

        if not re.match(r'^[a-zA-Z0-9]{5,20}$', username):
            return render(request, 'login.html', {'account_errmsg': '用户名或密码错误, 请重试'})
            # return http.HttpResponseForbidden('用户名或密码格式错误')
        # 校验密码
        if not re.match(r'^.{8,20}$', password):
            return render(request, 'login.html', {'account_errmsg': '用户名或密码错误, 请重试'})
            # return http.HttpResponseForbidden('用户名或密码格式错误')
        if not (re.match(r'.*[a-zA-Z]+.*', password) and re.match(r'.*[0-9]+.*', password)):
            return render(request, 'login.html', {'account_errmsg': '用户名或密码错误, 请重试'})
            # return http.HttpResponseForbidden('用户名或密码格式错误')
        # 认证登录用户
        user = authenticate(username=username, password=password)
        if user is None:
            return render(request, 'login.html', {'account_errmsg': '用户名或密码错误, 请重试'})
        # 状态保持
        login(request, user)
        # 响应结果
        # 取出next
        next = request.GET.get('next')
        if next:
            # 有next重定向到next的路径
            response = redirect(next)
        else:
            # 没有next重定向到首页
            response = redirect(reverse('contents:index'))

        # 设置保持时间
        if remembered == 'on':
            # 选择记住登录保存3天
            request.session.set_expiry(None)
            # 注册登录时把用户名写入cookie
            response.set_cookie('username', user.username, max_age=SETTING_TIME.COOKIE_USERNAME_EXPIRES)
        else:
            # 不选择浏览器关闭就退出登录
            request.session.set_expiry(0)
            # 注册登录时把用户名写入cookie, 保存12小时
            response.set_cookie('username', user.username, max_age=3600 * 12)
            pass

        return response


class IsRegister(View):
    """登录时判断是否注册"""

    def get(self, request, username):
        """
        判断手机号用户名是否注册过
        :param username:要验证的用户名或手机号
        :param request: 请求对象
        :return: json
        """
        username_count = User.objects.filter(username=username).count()
        mobile_count = User.objects.filter(mobile=username).count()
        response = {
            "code": RETCODE.OK,
            "errmsg": "OK",
            "username_count": username_count,
            "mobile_count": mobile_count,
        }
        return http.JsonResponse(response)


class UsernameCountView(View):
    """判断用户名是否重复注册"""

    def get(self, request, username):
        """
        :param username: 接收username参数
        :param request: 请求头
        :return: json
        """
        # 获取数据库相同username的数量并返回
        count = User.objects.filter(username=username).count()
        response = {
            "code": "%s" % RETCODE.OK,
            "errmsg": "OK",
            "count": "%s" % count
        }
        return http.JsonResponse(response)


class PhoneCountView(View):
    """判断手机号重复注册"""

    def get(self, request, mobile):
        """
        :param mobile: 检测手机号
        :param request: 请求头
        :return: json
        """
        count = User.objects.filter(mobile=mobile).count()
        response = {
            "code": "%s" % RETCODE.OK,
            "errmsg": "OK",
            "count": "%s" % count,
        }
        return http.JsonResponse(response)


class RegisterView(View):
    """注册"""

    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        """接收表单的post请求"""
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        mobile = request.POST.get('mobile')
        message_code_cli = request.POST.get('sms_code')
        allow = request.POST.get('allow')

        # --校验参数--
        # 判断参数齐全
        if not all([username, password, password2, mobile, allow]):
            return http.HttpResponseForbidden('缺少参数')
        # 判断用户名是否合法前后端一致
        if re.match(r'^[\d]{5,20}$', username):  # 是全数字
            return http.HttpResponseForbidden('用户名格式错误')
        elif not re.match(r'^[a-zA-Z0-9]{5,20}$', username):
            return http.HttpResponseForbidden('用户名格式错误')
        # 判断密码是否是8-20个数字
        if not re.match(r'^.{8,20}$', password):
            return http.HttpResponseForbidden('密码格式错误')
        if not (re.match(r'.*[a-zA-Z]+.*', password) and re.match(r'.*[0-9]+.*', password)):
            return http.HttpResponseForbidden('密码强度不符合')
        # 判断两次密码是否一致
        if not (password == password2):
            return http.HttpResponseForbidden('密码不一致')
        # 判断手机号是否合法
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return http.HttpResponseForbidden('手机号格式错误')
        # 判断手机验证码
        redis_conn = get_redis_connection('verify_code')
        sms_code_server = redis_conn.get('sms_%s' % mobile)
        if sms_code_server is None:
            # 手机验证码过期
            return render(request, 'register.html', {'register_errmsg': '短信验证码错误'})
        sms_code_server = sms_code_server.decode()
        if not (sms_code_server == message_code_cli):
            return render(request, 'register.html', {'register_errmsg': '短信验证码错误'})
        # 判断是否勾选用户协议
        if allow != 'on':
            # return render(request, 'register.html', {'register_errmsg': '注册失败,请重试!'})
            return http.HttpResponseForbidden('用户协议未同意')

        # ----保存注册数据-----
        # 可能写入失败使用try
        try:
            # create_user() 方法中封装了 set_password() 方法加密密码
            user = User.objects.create_user(username=username, password=password, mobile=mobile)
        except Exception as e:
            logger.error(e)
            return render(request, 'register.html', {'register_errmsg': '注册失败,请重试!'})
        # 注册成功自动登入, 实现状态保持
        # login(请求, 存入数据库对象)
        login(request, user)
        # 响应注册结果: 重定向到首页
        response = redirect(reverse('contents:index'))
        # 注册登录时把用户名写入cookie
        response.set_cookie('username', user.username, max_age=3600 * 12)
        return response
