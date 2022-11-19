from django.urls import re_path
from .views import *
app_name = 'oauth'

urlpatterns = [
    # 获取QQ登录链接
    re_path(r'qq/login/$', QQAuthURLView.as_view()),
    # QQ登录成功回调
    re_path (r'oauth_callback.html/', QQAuthUserView.as_view()),

]