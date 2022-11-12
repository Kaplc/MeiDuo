from django.contrib.auth import login
from django.db import DatabaseError
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse
from django.views import View
from django import http
from meiduo_project.settings.response_code import *
import re

from .models import User


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
            "code": "%s" % RETCODE,
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
            "code": "%s" % RETCODE,
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
        if not re.match(r'^[0-9a-zA-z@._]{8,20}', password):
            return http.HttpResponseForbidden('密码格式错误')
        if not (re.match(r'[a-zA-Z]+', password) and re.match(r'[\d]+', password)):
            return http.HttpResponseForbidden('密码强度不符合')
        # 判断两次密码是否一致
        if not (password == password2):
            return http.HttpResponseForbidden('密码不一致')
        # 判断手机号是否合法
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return http.HttpResponseForbidden('手机号格式错误')
        # 判断是否勾选用户协议
        if allow != 'on':
            return http.HttpResponseForbidden('用户协议未同意')

        # ----保存注册数据-----
        # 可能写入失败使用try
        try:
            # create_user() 方法中封装了 set_password() 方法加密密码
            user = User.objects.create_user(username=username, password=password, mobile=mobile)
        except DatabaseError:
            return render(request, 'register.html', {'register_errmsg': '注册失败,请重试!'})
        # 注册成功自动登入, 实现状态保持
        # login(请求, 存入数据库对象)
        login(request, user)
        # 响应注册结果: 重定向到首页
        return redirect(reverse('contents:index'))
