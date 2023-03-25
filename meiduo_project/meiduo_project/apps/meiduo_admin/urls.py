from django.urls import re_path
from .views.admin_login import AdminLogin
from rest_framework_jwt.views import obtain_jwt_token


app_name = 'meiduo_admin'

urlpatterns = [
    # 登录页面
    re_path(r'madmin/$', AdminLogin.as_view()),
    # 使用jwt认证后端
    re_path(r'meiduo_admin/authorizations/$', obtain_jwt_token),
    # ---------------------数据统计------------------- #
    # 用户总数
    re_path(r'meiduo_admin/statistical/total_count/$', obtain_jwt_token),

]