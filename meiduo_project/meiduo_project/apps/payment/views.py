import os

from alipay import AliPay
from django import http
from django.shortcuts import render
from django.views import View
from orders import models
from utils.response_code import *
from django.conf import settings
import logging

logger = logging.getLogger('django')


class PaymentView(View):
    """订单支付"""

    def get(self, request, order_id):
        """查询要支付的订单"""
        user = request.user
        # order_id = int(order_id)
        # 查询校验参数
        try:
            order = models.OrderInfo.objects.get(order_id=order_id)

        except Exception as e:
            logger.error(e)
            return http.JsonResponse({'code': RETCODE.DBERR, 'errmsg': '参数错误'})
        # app_keys = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'keys/app_private_key.pem')
        # alipay =   os.path.join(os.path.dirname(os.path.abspath(__file__)), 'keys/alipay_public_key.pem')
        # 创建支付宝支付对象
        alipay = AliPay(
            appid=settings.ALIPAY_APPID,
            app_notify_url=None,  # 默认返回url
            app_private_key_string=open(
                os.path.join(os.path.dirname(os.path.abspath(__file__)), 'keys/app_private_key.pem')).read(),
            alipay_public_key_string=open(
                os.path.join(os.path.dirname(os.path.abspath(__file__)), 'keys/alipay_public_key.pem')).read(),
            sign_type='RSA2',
            debug=settings.ALIPAY_DEBUG
        )
        # 生成支付宝链接
        order_string = alipay.api_alipay_trade_page_pay(
            out_trade_no=order_id,  # 订单编号
            total_amount=str(order.total_amount),  # 付款金额
            subject='美哆商城%s' % order_id,
            return_url=settings.ALIPAY_RETURN_URL
        )
        # 响应支付宝登录链接
        alipay_url = settings.ALIPAY_URL + '?' + order_string
        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': 'OK', 'alipay_url': alipay_url})
