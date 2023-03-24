from django.urls import re_path
from .views.admin_login import AdminLogin

app_name = 'meiduo_admin'

urlpatterns = [
    re_path(r'madmin/$', AdminLogin.as_view()),
]