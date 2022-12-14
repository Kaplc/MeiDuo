from django.shortcuts import render
from django.views import View


class PaymentView(View):
    """订单支付"""

    def get(self, request, order_id):
        """查询要支付的订单"""
        pass
