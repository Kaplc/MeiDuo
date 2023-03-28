from rest_framework.viewsets import ModelViewSet
from goods.models import SPUSpecification, SPU, SKUImage, SKU
from meiduo_admin.utils import PageNum
from meiduo_admin.serializers import goods_serializer
from rest_framework.views import Response


# 增删改查使用视图集
class SpecsView(ModelViewSet):
    """spu规格"""
    queryset = SPUSpecification.objects.all().order_by('id')
    # 指定序列化器
    serializer_class = goods_serializer.SPUSpecificationSerializer
    pagination_class = PageNum

    def simple(self, request):
        """自定义返回方法"""
        data = SPU.objects.all().order_by('id')
        ser = goods_serializer.SPUSpecificationSimpleSerializer(data, many=True)

        return Response(ser.data)


class ImageView(ModelViewSet):
    """商品图片"""
    queryset = SKUImage.objects.all().order_by('sku')
    serializer_class = goods_serializer.ImageSerializer
    pagination_class = PageNum

    def simple(self, request):
        """自定义返回方法"""
        # 返回SKU信息
        data = SKU.objects.all()
        ser = goods_serializer.ImageSimpleSerializer(data, many=True)

        return Response(ser.data)
