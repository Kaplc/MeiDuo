from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet
from goods.models import SKUImage, SKU, GoodsCategory
from meiduo_admin.utils import PageNum
from meiduo_admin.serializers import skus_serializer
from rest_framework.views import Response

import logging

logger = logging.getLogger('django')


class CategoriesView(ModelViewSet):
    """分类"""
    queryset = GoodsCategory.objects.filter(subs__id=None)
    # 指定序列化器
    serializer_class = skus_serializer.CategoriesSerializer
    permission_classes = [IsAdminUser]


class ImageView(ModelViewSet):
    """
        meiduo_admin/skus/images
        商品图片管理
    """

    queryset = SKUImage.objects.all().order_by('sku')
    serializer_class = skus_serializer.ImageSerializer
    pagination_class = PageNum
    permission_classes = [IsAdminUser]

    def simple(self, request):
        """自定义返回方法"""
        # 返回SKU信息
        data = SKU.objects.all()
        ser = skus_serializer.SKUSimpleSerializer(data, many=True)

        return Response(ser.data)


class SKUView(ModelViewSet):
    """
        meiduo_admin/skus
        sku管理
    """
    # 指定序列化器
    serializer_class = skus_serializer.SKUSerializer
    pagination_class = PageNum
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        keyword = self.request.query_params.get('keyword')
        if keyword is None:
            return SKU.objects.all().order_by('id')
        else:
            return SKU.objects.filter(name__contains=keyword).order_by('id')
