from fdfs_client.client import Fdfs_client
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

    def create(self, request, *args, **kwargs):
        image = request.FILES.get('image')
        sku_id = request.data.get('sku')
        # 上传到fdfs
        fdfs = Fdfs_client('meiduo_project/utils/fastdfs/client.conf')
        ret = fdfs.upload_by_buffer(image.read())
        if ret['Status'] == 'Upload successed.':
            image_url = ret['Remote file_id']
            sku_image = SKUImage.objects.create(image=image_url, sku_id=sku_id)
            sku_image.save()
            return Response({
                "id": sku_image.id,
                "sku": sku_image.sku_id,
                "image": sku_image.image.name
            })
        else:
            return Response(status=500)
