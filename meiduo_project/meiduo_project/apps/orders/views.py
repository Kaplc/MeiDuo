import decimal
from utils.response_code import *
from django.utils import timezone

from users.models import *
from goods.models import *
from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django_redis import get_redis_connection
from django import http
from users import models
from . import models
import json
import logging

logger = logging.getLogger('django')


class OrderCommitView(LoginRequiredMixin, View):
    """订单提交"""

    def post(self, request):
        """保存订单信息, 订单商品信息"""
        # 接收参数
        user = request.user
        json_str = request.body.decode()
        json_dict = json.loads(json_str)
        address_id = json_dict['address_id']
        pay_method = json_dict['pay_method']
        # 校验参数
        if not all([address_id, pay_method]):
            return http.HttpResponseForbidden('缺少参数')
        # 校验地址
        try:
            address = models.Address.objects.get(id=address_id)
        except Exception as e:
            logger.error(e)
            return http.HttpResponseForbidden('地址错误')
        # 校验支付方式
        if pay_method not in (models.OrderInfo.PAY_METHODS_ENUM['CASH'], models.OrderInfo.PAY_METHODS_ENUM['ALIPAY']):
            return http.HttpResponseForbidden('支付方式错误')
        # 生成订单号(时间+用户id)
        order_id = timezone.localtime().strftime('%Y%m%d%H%M%S') + ('%09d' % user.id)
        # 保存订单信息
        order = models.OrderInfo.objects.create(
            order_id=order_id,
            user=user,
            address=address,
            total_count=0,  # 商品购买总数量
            total_amount=decimal.Decimal(0.00),
            freight=decimal.Decimal(0.00),
            pay_method=pay_method,
            status=models.OrderInfo.ORDER_STATUS_ENUM['UNPAID'] if pay_method == models.OrderInfo.PAY_METHODS_ENUM[
                'ALIPAY'] else models.OrderInfo.ORDER_STATUS_ENUM['UNSEND']
        )
        # 保存订单商品信息
        try:
            # 获取sku
            conn_redis = get_redis_connection('carts')
            selected_skus = conn_redis.smembers('selected_%s' % user.id)  # 已勾选的商品
            skus = SKU.objects.filter(id__in=selected_skus)  # 已勾选的商品sku
            # 写入count
            total_count = 0
            total_amount = 0

            for sku in skus:
                # 获取该商品的购买数量
                sku.count = int(conn_redis.hget('carts_%s' % user.id, sku.id).decode())  # 已勾选的商品数量
                # 判断商品库存
                if sku.count > sku.stock:
                    return http.JsonResponse({'code': RETCODE.STOCKERR, 'errmsg': '库存不足'})
                # 计算该商品购买小计
                sku.subtotal_amount = sku.price * decimal.Decimal(sku.count)
                # 计算订单购买总数
                total_count += sku.count
                # 计算订单购买总金额(不含邮费)
                total_amount += sku.subtotal_amount
                # 修改销量和库存
                sku.spu.sales += sku.count  # 修改spu
                sku.stock -= sku.count
                sku.sales += sku.count
                sku.save()
                sku.spu.save()
                # 写入订单商品信息
                models.OrderGoods.objects.create(
                    order=order,
                    sku=sku,
                    count=sku.count,
                    price=sku.price,
                )

            # 补充订单信息数据
            order.total_count = total_count
            order.freight = decimal.Decimal(10.00)
            order.total_amount = total_amount + order.freight
            order.save()
            # 清除购物车中已结算的商品
            pl = conn_redis.pipeline()
            pl.hdel('carts_%s' % user.id, *selected_skus)
            pl.srem('selected_%s' % user.id, *selected_skus)
            pl.execute()

        except Exception as e:
            logger.error(e)
            return http.HttpResponseServerError('订单商品信息写入失败')

        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': '下单成功', 'order_Id': order_id})


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
