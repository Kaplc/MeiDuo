from django.urls import re_path
from .views import *
app_name = 'carts'
urlpatterns =[
    # 购物车操作
    re_path(r'carts/$', CartsView.as_view(), name='carts')
]