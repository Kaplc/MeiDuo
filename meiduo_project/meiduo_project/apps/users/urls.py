from django.urls import re_path
from .views import *

app_name = 'users'

urlpatterns = [
    # 注册
    re_path(r'register.html/$', RegisterView.as_view(), name='register'),
    # 验证用户名
    re_path(r'usernames/(?P<username>[a-zA-Z0-9_-]{5,20})/count/$', UsernameCountView.as_view()),
    # 验证手机号
    re_path(r'mobiles/(?P<mobile>1[3-9]\d{9})/count/$', PhoneCountView.as_view()),
    # 验证用户名, 手机号是否注册
    re_path(r'isReg/(?P<username>.*)/count/$', IsRegister.as_view()),
    # 登录
    re_path(r'login.html/$', LoginView.as_view(), name='login'),
    # 登出
    re_path(r'logout$', LogoutView.as_view(), name='logout'),
    # 用户中心
    re_path(r'user_center_info.html$', UserInfoView.as_view(), name='center_info'),
    # 添加邮箱
    re_path(r'emails/$', EmailView.as_view()),
    # 邮箱激活验证
    re_path(r'emails/verification/$', VerifyEmailView.as_view()),
]
