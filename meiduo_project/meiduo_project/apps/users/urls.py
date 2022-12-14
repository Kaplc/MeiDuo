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
    # 展示收货地址页面
    re_path(r'user_center_site.html/$', AddressView.as_view(), name='address'),
    # 添加收货地址
    re_path(r'addresses/create/$', CreatAddressView.as_view(), name='add_addresses'),
    # 修改, 删除收货地址
    re_path(r'addresses/(?P<address_id>\d+)/$', UpdateDestroyAddressView.as_view()),
    # 设置默认地址
    re_path(r'addresses/(?P<address_id>\d+)/default/$', DefaultAddressView.as_view()),
    # 设置地址标题
    re_path(r'addresses/(?P<address_id>\d+)/title/$', UpdateTitleAddressView.as_view()),
    # 修改密码
    re_path(r'user_center_pass.html/$', ChangePasswordView.as_view(), name='modify_password'),
    # 用户浏览记录
    re_path(r'browse_histories/$', UserBrowseHistory.as_view()),
    # 展示用户订单
    re_path(r'orders/info/(?P<page_num>\d+)/$', UserOrderInfoView.as_view(), name='orders'),
]
