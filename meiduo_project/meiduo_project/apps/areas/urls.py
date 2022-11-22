from django.urls import re_path
from .views import *
app_name = 'areas'


urlpatterns = [
    # 查询省市区
    re_path(r'areas/', Areas.as_view())
]