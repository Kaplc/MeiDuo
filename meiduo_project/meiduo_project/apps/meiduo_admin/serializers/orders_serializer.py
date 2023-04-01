from rest_framework import serializers
from goods.models import SKU
from orders.models import OrderInfo, OrderGoods


class SKUSerializer(serializers.ModelSerializer):
    """sku"""

    class Meta:
        model = SKU
        fields = ('name', 'default_image_url')


class OrderGoodsSerializer(serializers.ModelSerializer):
    """OrderGoods"""
    sku = SKUSerializer()

    class Meta:
        model = OrderGoods
        fields = ('count', 'price', 'sku')


class OrdersSerializer(serializers.ModelSerializer):
    """订单serializer"""
    user = serializers.StringRelatedField()
    skus = OrderGoodsSerializer(many=True)

    class Meta:
        model = OrderInfo
        fields = ('order_id', 'user', 'total_count', 'total_amount', 'freight',
                  'pay_method', 'status', 'create_time', 'skus')

