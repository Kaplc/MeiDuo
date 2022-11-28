from django.urls import re_path
from .views import *

app_name = 'contents'

urlpatterns = [
    # 首页
    re_path(r'$', IndexView.as_view(), name='index'),
    re_path(r'index.html$', IndexView.as_view()),
    # 展示商品列表页
    re_path(r'list.html/(?P<category_id>\d+)/(?P<page_num>\d+)/$', ListView.as_view())

]
