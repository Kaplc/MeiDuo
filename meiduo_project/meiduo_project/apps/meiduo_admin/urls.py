from django.urls import re_path
from rest_framework_jwt.views import obtain_jwt_token
from .views import statistical

app_name = 'meiduo_admin'

urlpatterns = [
    # 使用jwt认证后端
    re_path(r'meiduo_admin/authorizations/$', obtain_jwt_token),
    # ---------------------数据统计------------------- #
    # 用户总数
    re_path(r'meiduo_admin/statistical/total_count/$', statistical.UserTotalCountView.as_view()),
    # 日注册用户
    re_path(r'meiduo_admin/statistical/day_increment/$', statistical.UserDayCountView.as_view()),




]