from django.urls import re_path
from .views import *
app_name = 'carts'
urlpatterns =[
    # 购物车操作
    re_path(r'carts/$', CartsView.as_view(), name='carts'),
    # 全选购物车
    re_path(r'carts/selection/$', CartsSelectAllView.as_view()),
    # 简单购物车
    re_path(r'carts/simple/$', CartsSimpleView.as_view())
]