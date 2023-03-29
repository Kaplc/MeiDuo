from fdfs_client.client import Fdfs_client
from rest_framework import serializers
from goods.models import SPUSpecification, SKUImage, SKU
from celery_tasks.generate_static.task import detail_page


class SPUSpecificationSerializer(serializers.ModelSerializer):
    """spu序列化器"""
    # 关联查询
    spu = serializers.StringRelatedField()
    spu_id = serializers.IntegerField()

    class Meta:
        model = SPUSpecification
        fields = ('id', 'name', 'spu', 'spu_id')


class SPUSpecificationSimpleSerializer(serializers.ModelSerializer):
    """spu序列化器(simple)"""

    class Meta:
        model = SPUSpecification
        fields = ('id', 'name')


class ImageSerializer(serializers.ModelSerializer):
    """SKU图片序列化器"""

    class Meta:
        model = SKUImage
        fields = ('id', 'sku', 'image')

    def create(self, validated_data):
        """重写序列化器create"""
        image = validated_data['image']
        sku = validated_data['sku']
        # 上传到fdfs
        fdfs = Fdfs_client('meiduo_project/utils/fastdfs/client.conf')
        ret = fdfs.upload_by_buffer(image.read())
        if ret['Status'] == 'Upload successed.':
            image_url = ret['Remote file_id']
            sku_image = SKUImage.objects.create(image=image_url, sku_id=sku.id)
            sku_image.save()
            detail_page(sku.id)
        else:
            raise ValueError('上传失败')

        return sku_image


class ImageSimpleSerializer(serializers.ModelSerializer):
    """SKU信息序列化器(simple)"""

    class Meta:
        model = SKU
        fields = ('id', 'name',)
