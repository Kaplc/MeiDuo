from django.urls import re_path
from .views import *

app_name = 'goods'

urlpatterns = [
    # 展示商品列表
    re_path(r'list/(?P<category_id>\d+)/(?P<page_num>\d+)/$', ListView.as_view(), name='list'),
    # 展示热销排行
    re_path(r'hot/(?P<category_id>\d+)/$', HotGoodsView.as_view()),
    # 展示商品详情
    re_path(r'detail/(?P<sku_id>\d+)/$', DetailView.as_view(), name='detail'),
    # 统计商品访问记录
    re_path(r'detail/visit/(?P<category_id>\d+)/$', DetailVisitView.as_view()),
]
