from rest_framework.decorators import action
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet
from goods.models import SPUSpecification, SPU, Brand, GoodsCategory, GoodsChannel, GoodsChannelGroup
from meiduo_admin.utils import PageNum
from meiduo_admin.serializers import goods_serializer
from rest_framework.views import Response

import logging

logger = logging.getLogger('django')


class ChannelsView(ModelViewSet):
    """
        meiduo_admin/goods/channels
        频道管理
    """
    queryset = GoodsChannel.objects.all().order_by('id')
    serializer_class = goods_serializer.GoodsChannelSerializer
    pagination_class = PageNum
    permission_classes = [IsAdminUser]


class SPUSpecView(ListAPIView):
    """sku管理显示spu规格"""
    permission_classes = [IsAdminUser]
    serializer_class = goods_serializer.PKSPUSpecificationSerializer

    # 因为我们继承的是ListAPIView，在拓展类中是通过get_queryset获取数据，但是我们现在要获取的是规格信息，所以重写get_queryset
    def get_queryset(self):
        # 获取spu_id值
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

    @action(methods=['get'], detail=False)
    def simple(self, request):
        """
            goods/specs/simple/
            SPU规格
        """
        data = SPUSpecification.objects.all().order_by('id')
        ser = goods_serializer.SPUSpecificationSimpleSerializer(data, many=True)

        return Response(ser.data)


class SPUView(ModelViewSet):
    """
        meiduo_admin/goods
        spu管理
    """
    queryset = SPU.objects.all().order_by('id')
    serializer_class = goods_serializer.SPUSerializer
    pagination_class = PageNum
    permission_classes = [IsAdminUser]

    @action(methods=['get'], detail=False)
    def simple(self, request):
        """
            meiduo_admin/goods/simple/
            SPU
        """
        data = SPU.objects.all().order_by('id')
        ser = goods_serializer.SPUSpecificationSimpleSerializer(data, many=True)

        return Response(ser.data)


class BrandsSimpleView(ListAPIView):
    """BrandsSimple展示"""
    queryset = Brand.objects.all().order_by('id')
    serializer_class = goods_serializer.BrandsSimpleSerializer
    permission_classes = [IsAdminUser]


class CategoriesView(ModelViewSet):
    """
        meiduo_admin/goods/channel/categories/
        添加spu展示分类
    """

    serializer_class = goods_serializer.CategoriesSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        if pk is None:
            return GoodsCategory.objects.filter(parent_id=None).order_by('id')
        else:
            return GoodsCategory.objects.filter(parent_id=pk)


class ChannelsGroupView(ModelViewSet):
    """
        meiduo_admin/goods/channel_types/
        频道组
    """
    queryset = GoodsChannelGroup.objects.all().order_by('id')
    serializer_class = goods_serializer.ChannelGroupSerializer
    permission_classes = [IsAdminUser]


class BrandView(ModelViewSet):
    """
        meiduo_admin/goods/brands/
        展示品牌
    """
    queryset = Brand.objects.all().order_by('id')
    serializer_class = goods_serializer.BrandSerializer
    pagination_class = PageNum
    permission_classes = [IsAdminUser]
