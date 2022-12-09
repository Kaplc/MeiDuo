from django.urls import re_path
from .views import *
app_name = 'orders'

urlpatterns = [
    # 订单
    re_path(r'orders/settlement/$', OrderSettlementView.as_view(), name='info'),
]