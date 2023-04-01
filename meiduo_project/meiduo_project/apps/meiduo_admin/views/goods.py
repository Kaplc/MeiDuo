from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet
from goods.models import SPUSpecification, SPU, Brand, GoodsCategory
from meiduo_admin.utils import PageNum
from meiduo_admin.serializers import goods_serializer
from rest_framework.views import Response

import logging

logger = logging.getLogger('django')


class SPUSpecView(ListAPIView):
    """sku管理显示spu规格"""
    permission_classes = [IsAdminUser]
    serializer_class = goods_serializer.PKSPUSpecificationSerializer

    # 因为我们继承的是ListAPIView，在拓展类中是通过get_queryset获取数据，但是我们现在要获取的是规格信息，所以重写get_queryset
    def get_queryset(self):
        # 获取spuid值
        pk = self.kwargs['pk']
        # 根据spu的id值关联过滤查询出规格信息
        return SPUSpecification.objects.filter(spu_id=self.kwargs['pk'])


# 增删改查使用视图集
class SpecsView(ModelViewSet):
    """
        goods/specs/
        规格管理
    """
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


class SPUView(ModelViewSet):
    """spu管理"""
    queryset = SPU.objects.all().order_by('id')
    serializer_class = goods_serializer.SPUSerializer
    pagination_class = PageNum
    permission_classes = [IsAdminUser]


class BrandsSimpleView(ListAPIView):
    """BrandsSimple展示"""
    queryset = Brand.objects.all().order_by('id')
    serializer_class = goods_serializer.BrandsSimpleSerializer
    permission_classes = [IsAdminUser]


class CategoriesView(ModelViewSet):
    """
        goods/channel/categories/
        添加spu展示分类
    """

    serializer_class = goods_serializer.CategoriesSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        if pk is None:
            goods = GoodsCategory.objects.all().order_by('id')
            return GoodsCategory.objects.all().order_by('id')
        else:
            goods1 = GoodsCategory.objects.all().order_by('id')
            goods = GoodsCategory.objects.filter(id=pk).order_by('id')
            return GoodsCategory.objects.filter(parent_id=pk)
