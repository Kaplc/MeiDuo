from django.urls import re_path
from . import views

app_name = 'payment'

urlpatterns = [
    # 查询支付订单
    re_path(r'payment/(?P<order_id>\d+)/$', views.PaymentView.as_view(), name='info')
]
