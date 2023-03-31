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


"""
  {
        "order_id": "20181126102807000000004",
        "user": "zxc000",
        "total_count": 5,
        "total_amount": "52061.00",
        "freight": "10.00",
        "pay_method": 2,
        "status": 1,
        "create_time": "2018-11-26T18:28:07.470959+08:00",
        "skus": [
            {
                "count": 1,
                "price": "6499.00",
                "sku": {
                    "name": "Apple iPhone 8 Plus (A1864) 64GB 金色 移动联通电信4G手机",
                    "default_image_url": "http://image.meiduo.site:8888/group1/M00/00/02/CtM3BVrRZCqAUxp9AAFti6upbx41220032"
                }
            },
            ......
        ]
    }
"""
