from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet
from goods.models import SPUSpecification, SPU, SKUImage, SKU, GoodsCategory
from meiduo_admin.utils import PageNum
from meiduo_admin.serializers import goods_serializer
from rest_framework.views import Response

import logging

logger = logging.getLogger('django')


class SPUSpecView(ListAPIView):
    """sku管理显示spu规格"""
    serializer_class = goods_serializer.PKSPUSpecificationSerializer

    # 因为我们继承的是ListAPIView，在拓展类中是通过get_queryset获取数据，但是我们现在要获取的是规格信息，所以重写get_queryset
    def get_queryset(self):
        # 获取spuid值
        pk = self.kwargs['pk']
        # 根据spu的id值关联过滤查询出规格信息
        return SPUSpecification.objects.filter(spu_id=self.kwargs['pk'])


class CategoriesView(ModelViewSet):
    """分类"""
    queryset = GoodsCategory.objects.filter(subs__id=None)
    # 指定序列化器
    serializer_class = goods_serializer.CategoriesSerializer
    permission_classes = [IsAdminUser]


class SKUView(ModelViewSet):
    """sku管理"""
    # 指定序列化器
    serializer_class = goods_serializer.SKUSerializer
    pagination_class = PageNum
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        if self.kwargs.get('pk') is None:
            return SKU.objects.all().order_by('id')
        else:
            return SKU.objects.filter(id=self.kwargs.get('pk'))


# 增删改查使用视图集
class SpecsView(ModelViewSet):
    """规格管理"""
    queryset = SPUSpecification.objects.all().order_by('id')
    # 指定序列化器
    serializer_class = goods_serializer.SPUSpecificationSerializer
    pagination_class = PageNum
    permission_classes = [IsAdminUser]

    def simple(self, request):
        """自定义返回方法"""
        data = SPU.objects.all().order_by('id')
        ser = goods_serializer.SPUSpecificationSimpleSerializer(data, many=True)

        return Response(ser.data)


class ImageView(ModelViewSet):
    """商品图片管理"""
    queryset = SKUImage.objects.all().order_by('sku')
    serializer_class = goods_serializer.ImageSerializer
    pagination_class = PageNum
    permission_classes = [IsAdminUser]

    def simple(self, request):
        """自定义返回方法"""
        # 返回SKU信息
        data = SKU.objects.all()
        ser = goods_serializer.ImageToSKUSimpleSerializer(data, many=True)

        return Response(ser.data)
