import decimal
from users.models import *
from goods.models import *
from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django_redis import get_redis_connection
import logging

logger = logging.getLogger('django')


class OrderCommitView(LoginRequiredMixin, View):
    """订单提交"""

    def post(self, request):
        """保存订单信息, 订单商品信息"""
        # 接收参数

        pass


class OrderSettlementView(LoginRequiredMixin, View):
    """结算订单"""

    def get(self, request):
        """展示结算订单页面"""
        user = request.user

        try:
            # 查询所有地址
            addresses = Address.objects.filter(user=user, is_deleted=False)
            # 查询redis购物车
            conn_redis = get_redis_connection('carts')
            selected_skus = conn_redis.smembers('selected_%s' % user.id)  # 已勾选的商品
            skus = SKU.objects.filter(id__in=selected_skus)  # 已勾选的商品sku
            # 写入count
            total_count = 0
            total_amount = 0
            for sku in skus:
                sku.count = int(conn_redis.hget('carts_%s' % user.id, sku.id).decode())  # 已勾选的商品数量
                # 计算购买小计
                sku.subtotal_amount = sku.price * decimal.Decimal(sku.count)
                # 计算购买总数
                total_count += sku.count
                # 计算购买总金额
                total_amount += sku.subtotal_amount

        except Exception as e:
            logger.error(e)
            return render(request, '404.html')

        # 运费
        freight = decimal.Decimal(10.00)

        # jinja2渲染内容
        context = {
            'addresses': addresses,
            'skus': skus,
            'total_count': total_count,
            'total_amount': total_amount,
            'freight': freight,  # 运费
            'payment_amount': total_amount + freight
        }
        return render(request, 'place_order.html', context)
