from django.urls import re_path
from .views import *

app_name = 'goods'

urlpatterns = [
    # 展示商品列表
    re_path(r'list.html/(?P<category_id>\d+)/(?P<page_num>\d+)/$', ListView.as_view(), name='list'),


]
