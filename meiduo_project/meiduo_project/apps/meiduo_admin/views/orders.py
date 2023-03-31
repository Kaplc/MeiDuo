from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet
from orders.models import OrderInfo
from meiduo_admin.utils import PageNum
from meiduo_admin.serializers import orders_serializer


class OrdersView(ModelViewSet):
    """订单"""
    # queryset = OrderInfo.objects.all().order_by('order_id')
    # 指定序列化器
    serializer_class = orders_serializer.OrdersSerializer
    pagination_class = PageNum
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        keyword = self.request.query_params.get('keyword')
        if keyword is None:
            return OrderInfo.objects.all().order_by('order_id')
        else:
            return OrderInfo.objects.filter(order_id__contains=keyword).order_by('order_id')
