from django.urls import re_path
from .views import *
app_name = 'orders'

urlpatterns = [
    # 订单
    re_path(r'orders/settlement/$', OrderSettlementView.as_view(), name='info'),
    # 保存订单信息
    re_path(r'orders/commit/$', OrderCommitView.as_view(), name='commit'),
    # 订单提交成功
    re_path(r'orders/success/$', OrderSuccessView.as_view())
]