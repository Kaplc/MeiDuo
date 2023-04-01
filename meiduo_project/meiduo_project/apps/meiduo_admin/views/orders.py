from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from orders.models import OrderInfo
from meiduo_admin.utils import PageNum
from meiduo_admin.serializers import orders_serializer
import logging

logger = logging.getLogger('django')


class OrdersView(ModelViewSet):
    """
        meiduo_admin/orders
        订单
    """
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

    def status(self, request, pk):
        """
            meiduo_admin/orders/(?P<pk>\d+)/status/
            订单状态
        """
        status = request.data.get('status')
        try:
            order = OrderInfo.objects.get(order_id=pk)
            order.status = status
            order.save()
        except Exception as e:
            logger.error(e)
            return Response(status=500)
        else:
            return Response(status=201)
